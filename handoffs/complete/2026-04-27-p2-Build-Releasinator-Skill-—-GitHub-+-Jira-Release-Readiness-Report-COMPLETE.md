# Implementation Plan: Build Releasinator Skill — GitHub + Jira Release Readiness Report

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

The Releasinator skill has been successfully built, allowing for automated release readiness reporting by correlating Jira issues with GitHub PR statuses. The skill is now functional and integrated into the repo's skill set.

---

# Build Releasinator Skill — GitHub + Jira Release Readiness Report

> **Prepared by:** Cowork (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

---

## Context

Ben's team runs a release readiness check before every CBP release to identify which GitHub repositories need to be bumped from `dev` → `master`. This is currently done via a legacy Electron app (`cbp-pivotal-tracker-doc-generator`) on Ben's machine. The goal is to retire that app and replace its core "Home / Casebook Platform Release Planner" tab logic with a native Cowork skill — invoked with a simple prompt, outputting a clean `report.md` that follows the same conventions as the existing status report.

The skill should be installable as a `.skill` file (ZIP archive containing `SKILL.md` and a `scripts/` subdirectory).

---

## Source App Location

```
/Users/benbelanger/GitHub/cbp-pivotal-tracker-doc-generator
```

Relevant files only (Migranator and Pivotal tabs are deprecated — ignore them):

| File | Purpose |
|---|---|
| `src/ui/pages/Home/Home.tsx` | Main component — full orchestration logic |
| `src/github/index.ts` | GitHub API client (search PRs, retry logic) |
| `src/github/models.ts` | GitHub response types |
| `src/jira/index.ts` | Jira API client (projects, releases, issues, fields) |
| `src/jira/model.ts` | Jira response types |
| `src/consts.ts` | `GITHUB_CASEBOOK_ORGANIZATION = 'Casecommons'` |

---

## Credentials

Both GitHub and Jira credentials are in `.env` at the repo root. Read them from there — do not hardcode.

```
GITHUB_USERNAME
GITHUB_TOKEN
JIRA_EMAIL
JIRA_API_TOKEN
```

**Jira base URL:** `https://casecommons.atlassian.net/rest/api/3/`
**GitHub base URL:** `https://api.github.com/`
**GitHub org:** `Casecommons`
**Jira project key:** `CBP`

---

## What the Skill Does — Full Logic

### Input
Ben invokes the skill with a release version name, e.g.:
> "Run the releasinator for release 2026-5-1"

Or optionally with an additional JQL filter:
> "Run the releasinator for 2026-5-1, only include issues assigned to Bisoye"

### Step 1: Fetch Jira Issues for the Release

**Approach:** There are two valid options — let Code decide based on what's already cached:

- **Option A (preferred if daily Jira sync is fresh):** Read from existing cached Jira data in `reports/status/data/` and filter by `fixVersion = {releaseName}`.
- **Option B (always correct):** Run a dedicated Jira query: `GET /rest/api/3/search?jql=project=CBP AND fixVersion="{releaseName}"&maxResults=100&fields=summary,status,assignee,issuetype,customfield_XXXXX`

Either way, also fetch the custom field ID for "Feature flags" per project (query `GET /rest/api/3/field` and filter by name — do this once and cache it).

Separate out **BE Migration** issues (issue type name = `BE Migration` or `Backend Migration`) into their own list.

### Step 2: Find GitHub PRs for Each Issue

For each Jira issue key (e.g. `CBP-3075`):

```
GET https://api.github.com/search/issues
  ?q=is:pr+user:Casecommons+head:{CBP-KEY}
GET https://api.github.com/search/issues
  ?q=is:pr+user:Casecommons+{CBP-KEY}
```

- Match results by regex against branch name or PR title
- Fetch full PR details via the PR URL in the search result
- Extract the repository URL from each PR → build the **release repo list** (deduplicated)
- **Retry logic:** Exponential backoff — `2^depth * 5000ms`, up to 8 retries. GitHub search API rate-limits aggressively; this is essential.

### Step 3: Find Open qa→master PRs in Release Repos

```
GET https://api.github.com/search/issues
  ?q=is:pr+is:open+user:Casecommons+head:qa+base:master
```

Filter results to only repos in the release repo list from Step 2. These are the **repos that need to be bumped**.

### Step 4: Detect Leaked Issues

From all `qa→master` PR bodies:
1. Extract all Jira keys via regex: `Casecommons/(?:[A-Z]*)-(?:[0-9]*)` or simpler `CBP-\d+`
2. Filter out keys already in the main release issue list
3. Remaining keys = **leaked issues** — riding along in the release but not assigned to it

For each leaked issue key: fetch full Jira details (summary, status, assignee, feature flags field).

Build a secondary **leaked repo list**: repos from leaked issues' PRs that are NOT already in the main release repo list.

### Step 5: Extract Feature Flags

From main release issues and leaked issues: extract the value of the "Feature flags" custom field (if populated). Keep these two lists separate — flags from main issues should be turned ON; flags from leaked issues should be left alone.

---

## Output Format

Write to `reports/releasinator/report.md`. Follow the same conventions as `reports/status/report.md` — frontmatter, emoji section headers, markdown tables, issue links.

```markdown
---
title: Release Readiness — {releaseName}
generated: {ISO date}
release: {releaseName}
---

# 🚀 Release Readiness — {releaseName}

## 📦 Repositories to Bump (dev → master)
One repo per line with GitHub link. These have open qa→master PRs tied to release issues.

- [casebook-api](https://github.com/Casecommons/casebook-api)
- ...

## 📋 Release Issues ({count})
| Key | Summary | Status | Assignee | PRs |
|---|---|---|---|---|
| [CBP-XXXX](https://casecommons.atlassian.net/browse/CBP-XXXX) | Summary | In QA | Bisoye | [PR #42](https://github.com/...) |

## ⚠️ Potential Leaks ({count})
Issues found in qa→master PR bodies that are NOT in this release.

| Key | Summary | Status | Assignee | Found in PR |
|---|---|---|---|---|
| [CBP-XXXX](...) | Summary | In development | Tuan | [casebook-api #99](...) |

## 📦 Additional Repos Needed for Leaks
Repos from leaked issues not already in the main bump list.

- [casebook-frontend](https://github.com/Casecommons/casebook-frontend)

## 🚩 Feature Flags — ENABLE for this release
Flags from main release issues. Turn these ON.

- `some_feature_flag_name`

## 🚩 Feature Flags — DO NOT ENABLE (from leaked issues)
Flags from leaked issues. Leave these alone.

- `another_flag_name`

## 🗃️ BE Migrations
| Key | Summary | Status | Assignee |
|---|---|---|---|
| [CBP-XXXX](...) | Summary | In QA | Tuan |
```

---

## SKILL.md Instructions to Agent

The `SKILL.md` should instruct the agent to:

1. Read `.env` from `/Users/benbelanger/GitHub/cbp-pivotal-tracker-doc-generator/.env` for credentials
2. Run the releasinator script (see below) with the release name as argument
3. Write output to `reports/releasinator/report.md` in the repo
4. Confirm with: `✅ Releasinator complete for {releaseName} — {N} repos to bump, {M} leaks found`
5. Offer to open the report

---

## Implementation Notes for Code

**Language:** TypeScript/Node preferred (matches the source app). Alternatively Python if simpler for the shell-script pattern used by other skills in the repo.

**Script location:** `skills/releasinator/scripts/run.ts` (or `.py`)

**Script interface:**
```bash
node skills/releasinator/scripts/run.js --release "2026-5-1" [--jql "assignee = bisoye"]
# writes to reports/releasinator/report.md
# exits 0 on success, 1 on error
```

**Rate limiting:** The GitHub search API has a 10 req/min rate limit for authenticated requests. The source app uses exponential backoff — replicate this. Consider batching issue → PR lookups with a small sleep between calls.

**Jira sync decision:** Check if `reports/status/data/` contains fresh data (< 24h old) for the target `fixVersion`. If yes, use it and skip the Jira API call. If not, run a targeted JQL query. This keeps the skill fast on release day when status report has just run.

**Repo deduplication:** A single release may have many issues pointing to the same repo (e.g. `casebook-api`). Deduplicate before writing the repo list.

**Empty sections:** If no leaks, no feature flags, or no BE migrations are found, omit those sections from the report rather than showing empty tables.

---

## Verification Checklist

- [ ] Script reads credentials from `.env` without hardcoding
- [ ] Release issues are correctly filtered by `fixVersion`
- [ ] GitHub PR search finds PRs by Jira key in branch name AND PR title
- [ ] Retry logic handles GitHub rate limiting (test with a release that has 20+ issues)
- [ ] Leaked issue detection correctly excludes keys already in the release
- [ ] Feature flags are split: main release vs. leaked
- [ ] BE Migrations appear in their own section
- [ ] Report renders cleanly in markdown with working links
- [ ] `reports/releasinator/report.md` is written to the repo (not the outputs scratch dir)
- [ ] Skill invocation phrase works: "Run the releasinator for 2026-5-1"
