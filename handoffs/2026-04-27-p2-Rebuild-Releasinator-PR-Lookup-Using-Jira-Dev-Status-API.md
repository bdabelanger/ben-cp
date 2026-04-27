# Implementation Plan: Rebuild Releasinator PR Lookup Using Jira Dev-Status API

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

The Releasinator skill (`skills/releasinator/scripts/run.py`) currently finds GitHub PRs for each Jira issue by hitting the GitHub Search API twice per issue (once by branch name, once by title). With 20–30 issues per release across CBP + DATA, this generates 40–60+ search calls, which consistently triggers GitHub's secondary rate limit (403 Forbidden) and forces exponential backoff — turning a 30-second run into a multi-minute slog.

Jira already has this data. GitHub is synced to Jira via the development integration, and the dev-status API returns linked PRs directly from Jira's cache — no GitHub rate limits, no retries, no waiting.

The `qa→master` PR search (one call to detect repos needing a bump) can stay on GitHub — it's a single call, not per-issue.

---

## Goal

Replace the per-issue GitHub Search API calls with the **Jira dev-status API**, keeping only the single `qa→master` GitHub search.

Expected result: a full CBP + DATA release run in under 30 seconds with no rate limiting.

---

## Jira Dev-Status API

```
GET https://casecommons.atlassian.net/rest/dev-status/latest/issue/detail
  ?issueId={numeric_issue_id}
  &applicationType=github
  &dataType=pullrequest
```

- Auth: same `ATLASSIAN_USER_EMAIL` + `ATLASSIAN_API_TOKEN` Basic auth as the rest of the Jira calls
- `issueId` is the **numeric ID** from `issue["id"]` (already returned by the Jira search query)
- Returns: `detail[0].pullRequests[]` — each with `url`, `name` (title), `status` (OPEN/MERGED/DECLINED), `source.branch.name`, `destination.branch.name`, `repositoryUrl`

### Response shape (relevant fields):
```json
{
  "detail": [{
    "pullRequests": [{
      "id": "CBP-123",
      "title": "CBP-3138 Add delete endpoint",
      "status": "MERGED",
      "url": "https://github.com/Casecommons/casebook-api/pull/42",
      "source": { "branch": { "name": "CBP-3138-add-delete-endpoint" } },
      "destination": { "branch": { "name": "dev" } },
      "repositoryUrl": "https://github.com/Casecommons/casebook-api"
    }]
  }]
}
```

---

## Execution Steps

### 1. Add a new function `get_prs_for_issue_via_jira(issue)`

```python
def get_prs_for_issue_via_jira(issue):
    issue_id = issue["id"]  # numeric, e.g. "10234"
    resp = requests.get(
        "https://casecommons.atlassian.net/rest/dev-status/latest/issue/detail",
        params={"issueId": issue_id, "applicationType": "github", "dataType": "pullrequest"},
        auth=jira_auth(),
        headers={"Accept": "application/json"},
        timeout=30
    )
    resp.raise_for_status()
    detail = resp.json().get("detail", [])
    return detail[0].get("pullRequests", []) if detail else []
```

### 2. Adapt the PR data shape

The dev-status response uses slightly different field names than the GitHub API. Update the downstream helpers to handle both or normalise on ingest:

| GitHub field | Dev-status equivalent |
|---|---|
| `pr["html_url"]` | `pr["url"]` |
| `pr["title"]` | `pr["title"]` |
| `pr["number"]` | extract from `pr["url"].split("/")[-1]` |
| `pr["head"]["label"]` | `pr["source"]["branch"]["name"]` |

Introduce a `normalise_pr(pr, source)` helper that takes either format and returns a dict with `html_url`, `title`, `number`, `branch`, `repo_url`.

### 3. Replace `get_prs_for_issue()` calls in `run_project_pipeline()`

Swap out:
```python
prs = get_prs_for_issue(key)
```
for:
```python
prs = get_prs_for_issue_via_jira(issue)
prs = [normalise_pr(pr, "jira") for pr in prs]
```

### 4. Repo URL extraction

Dev-status provides `repositoryUrl` directly on each PR — no need to parse it from `html_url`. Update `repo_url_from_pr_url()` or use `repositoryUrl` directly in the pipeline.

### 5. Rebuild leak detection using GitHub compare API (per repo)

The current `get_qa_to_master_prs()` approach extracts Jira keys from open `qa→master` PR *bodies* — fragile, since it depends on humans including keys in the description. Replace it with GitHub's **compare API**, which gives the exact set of commits riding out in this release per repo, and extracts Jira keys reliably from branch names.

**New approach — one call per release repo:**

```python
def get_in_flight_jira_keys(repo_url, project_key):
    """
    Compare master...qa on this repo to find all commits going out in the release.
    Extract Jira keys from commit messages and branch names.
    """
    repo_path = repo_url.replace("https://github.com/", "")  # e.g. Casecommons/casebook-api
    resp = requests.get(
        f"{GITHUB_BASE}/repos/{repo_path}/compare/master...qa",
        auth=github_auth(),
        headers={"Accept": "application/vnd.github+json"},
        timeout=30
    )
    if resp.status_code == 404:
        return set()  # repo may not have a qa branch
    resp.raise_for_status()

    keys = set()
    pattern = re.compile(rf'{project_key}-\d+')
    for commit in resp.json().get("commits", []):
        msg = commit.get("commit", {}).get("message", "")
        keys.update(pattern.findall(msg))
    return keys
```

Call this for each repo in `all_release_repos`, union all keys, subtract the release's `found_keys` → leaked keys.

**Why this is better than the PR body approach:**
- Branch names (`CBP-3138-feature-name`) are machine-generated and reliable
- Commit messages consistently include the Jira key
- Uses the regular GitHub REST API (5000 req/hr) — not the Search API (10 req/min)
- N calls = number of repos (~10-20), not number of issues (40+)

**Keep `get_qa_to_master_prs()` for the "Repos to Bump" section only** — it still correctly identifies which repos have an open `qa→master` PR. Remove its role in leak detection.

### 6. Filter out PRs already merged to master

When building `all_release_repos`, only include a repo if the associated PR is still "in flight" — i.e. not already landed on `master`. A PR that's already merged to `master` means that repo's work is done and it should not appear in the repo list.

Filter condition (using dev-status field `destination.branch.name`):

```python
def is_in_flight(pr):
    dest = pr.get("destination", {}).get("branch", {}).get("name", "")
    status = pr.get("status", "")
    return status == "OPEN" or (status == "MERGED" and dest != "master")

def is_merged_to_master(pr):
    dest = pr.get("destination", {}).get("branch", {}).get("name", "")
    status = pr.get("status", "")
    return status == "MERGED" and dest == "master"
```

When building `all_release_repos`, only add repos where `is_in_flight(pr)` is True.

**Do not silently drop already-merged repos** — instead, track them separately and render a new report section:

```markdown
## ✅ Already Merged to Master ({count})
These repos had release PRs that are fully landed — no action needed.

- [casebook-api](https://github.com/Casecommons/casebook-api)
```

This gives a complete picture at a glance: repos still needing a bump vs. repos already done. Particularly useful for cross-cutting fixes (e.g. an accessibility change that touched 8 repos but shipped in a prior cycle) that are attached to a ticket still open in the release.

### 7. Add shared-library exclusion list

The current GitHub-based run surfaced repos that have legitimate PRs but don't need a `qa→master` bump — shared libraries that are consumed by the release but not directly released. Add a constant to filter these from the **"All Repositories"** and **"Repos to Bump"** sections:

```python
SHARED_LIB_REPOS = {
    "cbp-core-components",
    "cbp-core-java",
    "cbp-core-typescript",
    "cbp-iforms-core",
    "cbp-undercase-lib",
}
```

Apply this filter when building `all_release_repos` — exclude repos whose name (last path segment) is in `SHARED_LIB_REPOS`. These repos still appear in the PR column of the issues table (for reference), just not in the repo list sections.

Ben confirmed the following are the correct releasable repos for a CBP+DATA release (use as ground truth for the verification step):

**FE:** cbp-admin-web, cbp-cases-web, cbp-home-web, cbp-intake-web, cbp-providers-web, cbp-reporting-web
**GraphQL:** cbp-admin-api-graphql, cbp-cases-api-graphql, cbp-global-api-graphql, cbp-home-api-graphql, cbp-intake-api-graphql, cbp-internal-api-graphql, cbp-portal-api-graphql, cbp-reporting-api-graphql, cbp-services-api-graphql
**Java:** cbp-attachments-api-java, cbp-providers-api-java, cbp-tasks-api-java
**Data:** cbp-datagroup-emr, cbp-datagroup-scheduled, cbp-mcp-server-node

### 7. Remove dead code

Once the switch is made, remove `get_prs_for_issue()`, `get_pr_details()`, and `search_github_prs()` if they are no longer called. Keep `get_qa_to_master_prs()`.

---

## Verification Checklist

- [ ] Script runs for `2026-5-1` (CBP + DATA) in under 60 seconds with no retries
- [ ] PR links in the report resolve correctly to GitHub URLs
- [ ] Repo list matches what the old GitHub-based version produced for a known release
- [ ] Feature flags still extracted correctly (those come from Jira fields, unaffected)
- [ ] `qa→master` bump detection still works (identifies repos with open qa→master PRs)
- [ ] Leak detection uses `master...qa` compare per repo — not PR body regex
- [ ] Leaked issues show up correctly for a release with known leaks (test with a release that has in-flight work)
- [ ] "Already Merged to Master" section appears and correctly excludes those repos from the bump list
- [ ] Shared library repos (cbp-core-components etc.) excluded from repo list sections
- [ ] No `get_prs_for_issue` / `search_github_prs` calls remain
