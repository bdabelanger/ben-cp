#!/usr/bin/env python3
"""
releasinator/scripts/run.py — Release Readiness Report

Ports the "Home" tab logic from cbp-pivotal-tracker-doc-generator.
Supports Platform (CBP) and Data (DATA) projects, defaulting to both.

Usage:
    python3 run.py --release "2026-5-1"
    python3 run.py --release "2026-5-1" --project CBP
    python3 run.py --release "2026-5-1" --project DATA
    python3 run.py --release "2026-5-1" --jql "assignee = bisoye"

Output: reports/releasinator/report.md
"""
import os, sys, re, time, argparse
from datetime import datetime

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("❌ 'requests' not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT    = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
REPORT_DIR    = os.path.join(VAULT_ROOT, "reports", "releasinator")
REPORT_PATH   = os.path.join(REPORT_DIR, "report.md")
ENV_PATH      = os.path.join(VAULT_ROOT, ".env")

JIRA_BASE     = "https://casecommons.atlassian.net/rest/api/3"
JIRA_DEV_BASE = "https://casecommons.atlassian.net/rest/dev-status/latest"
GITHUB_BASE   = "https://api.github.com"
GITHUB_ORG    = "Casecommons"

# Project config: key → (version prefix, label)
PROJECTS = {
    "CBP":  {"prefix": "Platform-", "label": "Platform"},
    "DATA": {"prefix": "Data-",     "label": "Data"},
}

BE_MIGRATION_TYPES = {"BE Migration", "Backend Migration"}

# Shared libraries that have PRs but don't need a qa→master bump
SHARED_LIB_REPOS = {
    "cbp-core-components",
    "cbp-core-java",
    "cbp-core-typescript",
    "cbp-iforms-core",
    "cbp-undercase-lib",
}

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

def load_env():
    if not os.path.exists(ENV_PATH):
        print(f"❌ .env not found at {ENV_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

def jira_auth():
    return HTTPBasicAuth(os.environ["ATLASSIAN_USER_EMAIL"], os.environ["ATLASSIAN_API_TOKEN"])

def github_auth():
    return HTTPBasicAuth(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_API_TOKEN"])

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def call_with_retry(fn, depth=0):
    try:
        return fn()
    except Exception as e:
        if depth > 7:
            raise
        delay = (2 ** depth) * 5
        print(f"  ⏳ retry {depth+1}/8 in {delay}s ({e})", file=sys.stderr)
        time.sleep(delay)
        return call_with_retry(fn, depth + 1)

# ---------------------------------------------------------------------------
# Jira
# ---------------------------------------------------------------------------

_ff_field_id_cache = None

def get_feature_flags_field_id():
    global _ff_field_id_cache
    if _ff_field_id_cache is not None:
        return _ff_field_id_cache
    resp = requests.get(
        f"{JIRA_BASE}/field/search",
        params={"type": "custom", "query": "Feature flags", "maxResults": 1},
        auth=jira_auth(), headers={"Accept": "application/json"}, timeout=30
    )
    resp.raise_for_status()
    values = resp.json().get("values", [])
    _ff_field_id_cache = values[0]["id"] if values else None
    return _ff_field_id_cache

def resolve_version_name(project_key, release_name):
    """Try bare name first, then prefix variant."""
    prefix = PROJECTS[project_key]["prefix"]
    candidates = [release_name]
    if not release_name.startswith(prefix):
        candidates.append(f"{prefix}{release_name}")
    return candidates

def get_jira_issues(project_key, release_name, extra_jql="", ff_field=None):
    fields = ["summary", "status", "assignee", "issuetype"]
    if ff_field:
        fields.append(ff_field)

    for name in resolve_version_name(project_key, release_name):
        jql = f'project={project_key} AND fixVersion="{name}"'
        if extra_jql.strip():
            jql = f'{extra_jql.strip()} AND {jql}'
        resp = requests.get(
            f"{JIRA_BASE}/search/jql",
            params={"jql": jql, "maxResults": 100, "fields": ",".join(fields)},
            auth=jira_auth(), headers={"Accept": "application/json"}, timeout=30
        )
        resp.raise_for_status()
        issues = resp.json().get("issues", [])
        if issues:
            if name != release_name:
                print(f"  [{project_key}] matched as '{name}'")
            return issues

    return []

def get_jira_issues_by_keys(keys, ff_field=None):
    if not keys:
        return []
    jql = f'key in ({",".join(keys)})'
    fields = ["summary", "status", "assignee", "issuetype"]
    if ff_field:
        fields.append(ff_field)
    resp = requests.get(
        f"{JIRA_BASE}/search/jql",
        params={"jql": jql, "maxResults": 100, "fields": ",".join(fields)},
        auth=jira_auth(), headers={"Accept": "application/json"}, timeout=30
    )
    resp.raise_for_status()
    return resp.json().get("issues", [])

def get_prs_for_issue_via_jira(issue):
    resp = requests.get(
        f"{JIRA_DEV_BASE}/issue/detail",
        params={"issueId": issue["id"], "applicationType": "github", "dataType": "pullrequest"},
        auth=jira_auth(),
        headers={"Accept": "application/json"},
        timeout=30
    )
    resp.raise_for_status()
    detail = resp.json().get("detail", [])
    return detail[0].get("pullRequests", []) if detail else []

# ---------------------------------------------------------------------------
# GitHub
# ---------------------------------------------------------------------------

def search_github_prs(query):
    def _do():
        resp = requests.get(
            f"{GITHUB_BASE}/search/issues",
            params={"q": query, "per_page": 50},
            auth=github_auth(), headers={"Accept": "application/vnd.github+json"}, timeout=30
        )
        resp.raise_for_status()
        return resp.json().get("items", [])
    return call_with_retry(_do)

def get_qa_to_master_prs():
    return search_github_prs(f"is:pr is:open user:{GITHUB_ORG} head:qa base:master")

def repo_url_from_pr_url(html_url):
    idx = html_url.find("/pull")
    return html_url[:idx] if idx != -1 else html_url

def get_in_flight_jira_keys(repo_url, project_key):
    """Compare master...qa to find Jira keys riding out in this release."""
    repo_path = repo_url.replace("https://github.com/", "")
    resp = requests.get(
        f"{GITHUB_BASE}/repos/{repo_path}/compare/master...qa",
        auth=github_auth(),
        headers={"Accept": "application/vnd.github+json"},
        timeout=30
    )
    if resp.status_code == 404:
        return set()
    resp.raise_for_status()
    keys = set()
    pattern = re.compile(rf'{project_key}-\d+')
    for commit in resp.json().get("commits", []):
        msg = commit.get("commit", {}).get("message", "")
        keys.update(pattern.findall(msg))
    return keys

# ---------------------------------------------------------------------------
# PR normalisation
# ---------------------------------------------------------------------------

def normalise_pr(pr, source):
    """Return a uniform dict regardless of whether pr came from Jira or GitHub."""
    if source == "jira":
        url = pr.get("url", "")
        return {
            "html_url": url,
            "title":    pr.get("title", ""),
            "number":   url.split("/")[-1],
            "branch":   pr.get("source", {}).get("branch", {}).get("name", ""),
            "repo_url": pr.get("repositoryUrl", ""),
        }
    # github
    html_url = pr.get("html_url", "")
    return {
        "html_url": html_url,
        "title":    pr.get("title", ""),
        "number":   pr.get("number", ""),
        "branch":   pr.get("head", {}).get("ref", ""),
        "repo_url": repo_url_from_pr_url(html_url),
    }

def is_in_flight(pr):
    """Raw dev-status PR is still moving toward master."""
    dest   = pr.get("destination", {}).get("branch", {}).get("name", "")
    status = pr.get("status", "")
    return status == "OPEN" or (status == "MERGED" and dest != "master")

def is_merged_to_master(pr):
    """Raw dev-status PR has already landed on master."""
    dest   = pr.get("destination", {}).get("branch", {}).get("name", "")
    status = pr.get("status", "")
    return status == "MERGED" and dest == "master"

# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------

def extract_feature_flags(issues, ff_field):
    if not ff_field:
        return []
    flags = set()
    for issue in issues:
        val = issue.get("fields", {}).get(ff_field)
        if isinstance(val, list):
            flags.update(v for v in val if v)
        elif isinstance(val, str) and val:
            flags.add(val)
    return sorted(flags)

# ---------------------------------------------------------------------------
# Per-project pipeline
# ---------------------------------------------------------------------------

def _collect_prs(issues, label_prefix):
    """
    Fetch dev-status PRs for each issue, normalise, and classify repos.
    Returns (issues_with_prs, all_release_repos, already_merged_repos).
    """
    items = []
    all_release_repos    = set()
    already_merged_repos = set()

    for issue in issues:
        key = issue["key"]
        print(f"    PRs for {label_prefix}{key}...")
        raw_prs  = get_prs_for_issue_via_jira(issue)
        norm_prs = []
        for raw_pr in raw_prs:
            norm_pr   = normalise_pr(raw_pr, "jira")
            repo_name = norm_pr["repo_url"].split("/")[-1]
            if repo_name not in SHARED_LIB_REPOS:
                if is_in_flight(raw_pr):
                    all_release_repos.add(norm_pr["repo_url"])
                elif is_merged_to_master(raw_pr):
                    already_merged_repos.add(norm_pr["repo_url"])
            norm_prs.append(norm_pr)
        items.append({"issue": issue, "prs": norm_prs})

    return items, all_release_repos, already_merged_repos

def run_project_pipeline(project_key, release_name, extra_jql, qa_master_items):
    label = PROJECTS[project_key]["label"]
    print(f"\n  [{label}]")

    ff_field   = get_feature_flags_field_id()
    raw_issues = get_jira_issues(project_key, release_name, extra_jql, ff_field)
    print(f"  Found {len(raw_issues)} issues")

    if not raw_issues:
        return None

    migrations  = [
        i for i in raw_issues
        if (i.get("fields", {}).get("issuetype") or {}).get("name") in BE_MIGRATION_TYPES
    ]
    main_issues = [i for i in raw_issues if i not in migrations]

    found_keys = {i["key"] for i in raw_issues}

    issues_with_prs,  repos_main,  merged_main  = _collect_prs(main_issues, "")
    migration_items,  repos_migr,  merged_migr  = _collect_prs(migrations,  "migration ")

    all_release_repos    = repos_main | repos_migr
    already_merged_repos = merged_main | merged_migr

    # Repos to bump: in-flight repos that have an open qa→master PR
    qa_master_repos = {
        repo_url_from_pr_url(item.get("html_url", ""))
        for item in qa_master_items
    }
    repos_to_bump = all_release_repos & qa_master_repos

    # Leak detection: compare master...qa per repo, extract keys not in this release
    leaked_keys      = set()
    leaked_pr_sources = {}
    for repo in all_release_repos:
        keys = get_in_flight_jira_keys(repo, project_key)
        for key in keys:
            if key not in found_keys:
                leaked_keys.add(key)
                leaked_pr_sources.setdefault(key, []).append(repo)

    print(f"  {len(leaked_keys)} potential leaks")
    leaked_details_list = get_jira_issues_by_keys(list(leaked_keys), ff_field) if leaked_keys else []
    leaked_details      = {i["key"]: i for i in leaked_details_list}

    all_leak_repos = set()
    leak_items     = []
    for key in leaked_keys:
        issue_obj = leaked_details.get(key)
        if issue_obj:
            raw_prs = get_prs_for_issue_via_jira(issue_obj)
            prs     = [normalise_pr(pr, "jira") for pr in raw_prs]
        else:
            prs = []
        for pr in prs:
            all_leak_repos.add(pr["repo_url"])
        leak_items.append({
            "key":         key,
            "details":     leaked_details.get(key),
            "prs":         prs,
            "found_in_prs": leaked_pr_sources.get(key, []),
        })

    return {
        "project_key":         project_key,
        "label":               label,
        "ff_field":            ff_field,
        "issues_with_prs":     issues_with_prs,
        "migration_items":     migration_items,
        "all_release_repos":   all_release_repos,
        "already_merged_repos": already_merged_repos,
        "repos_to_bump":       repos_to_bump,
        "leak_items":          leak_items,
        "leak_repos":          all_leak_repos - all_release_repos,
        "flags_on":            extract_feature_flags(main_issues, ff_field),
        "flags_leave":         extract_feature_flags(leaked_details_list, ff_field),
    }

# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def issue_link(key):
    return f"[{key}](https://casecommons.atlassian.net/browse/{key})"

def pr_link(pr):
    repo_name = repo_url_from_pr_url(pr.get("html_url", "")).split("/")[-1]
    number    = pr.get("number", "")
    return f"[{repo_name} #{number}]({pr.get('html_url', '')})"

def render_repo_list(repos):
    lines = []
    for repo in sorted(repos):
        name = repo.split("/")[-1]
        lines.append(f"- [{name}]({repo})")
    return "\n".join(lines)

def render_issues_table(issues_with_prs):
    lines = ["| Key | Summary | Status | Assignee | PRs |", "|---|---|---|---|---|"]
    for item in sorted(issues_with_prs, key=lambda x: x["issue"]["key"]):
        issue    = item["issue"]
        f        = issue.get("fields", {})
        key      = issue["key"]
        summary  = f.get("summary", "")[:60]
        status   = f.get("status", {}).get("name", "")
        assignee = (f.get("assignee") or {}).get("displayName", "—")
        prs_str  = ", ".join(pr_link(pr) for pr in item["prs"]) or "—"
        lines.append(f"| {issue_link(key)} | {summary} | {status} | {assignee} | {prs_str} |")
    return "\n".join(lines)

def render_leaks_table(leak_items):
    lines = ["| Key | Summary | Status | Assignee | Found in Repo |", "|---|---|---|---|---|"]
    for item in sorted(leak_items, key=lambda x: x["key"]):
        key      = item["key"]
        details  = item.get("details") or {}
        f        = details.get("fields", {})
        summary  = f.get("summary", "")[:60]
        status   = f.get("status", {}).get("name", "")
        assignee = (f.get("assignee") or {}).get("displayName", "—")
        found_in = ", ".join(
            f"[{u.split('/')[-1]}]({u})"
            for u in item.get("found_in_prs", [])
        ) or "—"
        lines.append(f"| {issue_link(key)} | {summary} | {status} | {assignee} | {found_in} |")
    return "\n".join(lines)

def render_migrations_table(issues):
    lines = ["| Key | Summary | Status | Assignee |", "|---|---|---|---|"]
    for issue in sorted(issues, key=lambda x: x["key"]):
        f        = issue.get("fields", {})
        key      = issue["key"]
        summary  = f.get("summary", "")[:60]
        status   = f.get("status", {}).get("name", "")
        assignee = (f.get("assignee") or {}).get("displayName", "—")
        lines.append(f"| {issue_link(key)} | {summary} | {status} | {assignee} |")
    return "\n".join(lines)

def write_report(release_name, results):
    os.makedirs(REPORT_DIR, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"---",
        f"title: Release Readiness — {release_name}",
        f"generated: {now}",
        f"release: {release_name}",
        f"---",
        f"",
        f"# 🚀 Release Readiness — {release_name}",
        f"",
    ]

    # --- All repos (per project) ---
    for r in results:
        all_repos = r["all_release_repos"]
        if all_repos:
            lines += [f"## 🗂️ All Repositories — {r['label']} ({len(all_repos)})", ""]
            lines.append(render_repo_list(all_repos))
            lines.append("")

    # --- Already merged to master ---
    all_merged_repos = set().union(*(r["already_merged_repos"] for r in results))
    if all_merged_repos:
        lines += [f"## ✅ Already Merged to Master ({len(all_merged_repos)})", ""]
        lines.append("These repos had release PRs that are fully landed — no action needed.")
        lines.append("")
        lines.append(render_repo_list(all_merged_repos))
        lines.append("")

    # --- Repos to bump ---
    all_bump_repos = set().union(*(r["repos_to_bump"] for r in results))
    if all_bump_repos:
        lines += [f"## 📦 Repositories to Bump — qa → master ({len(all_bump_repos)})", ""]
        lines.append(render_repo_list(all_bump_repos))
        lines.append("")

    # --- Issues per project ---
    for r in results:
        all_items      = r["issues_with_prs"] + r["migration_items"]
        migration_keys = {i["issue"]["key"] for i in r["migration_items"]}
        main_items     = [i for i in all_items if i["issue"]["key"] not in migration_keys]
        if main_items:
            lines += [
                f"## 📋 Release Issues — {r['label']} ({len(main_items)})",
                "",
                render_issues_table(main_items),
                "",
            ]

    # --- Leaks (per project) ---
    for r in results:
        if r["leak_items"]:
            lines += [
                f"## ⚠️ Potential Leaks — {r['label']} ({len(r['leak_items'])})",
                "",
                render_leaks_table(r["leak_items"]),
                "",
            ]

    # --- Additional repos for leaks ---
    all_leak_only_repos = set().union(*(r["leak_repos"] for r in results))
    if all_leak_only_repos:
        lines += ["## 📦 Additional Repos Needed for Leaks", ""]
        lines.append(render_repo_list(all_leak_only_repos))
        lines.append("")

    # --- Feature flags ---
    all_flags_on    = sorted(set().union(*(r["flags_on"]    for r in results)))
    all_flags_leave = sorted(set().union(*(r["flags_leave"] for r in results)))

    if all_flags_on:
        lines += ["## 🚩 Feature Flags — ENABLE for this release", ""]
        for flag in all_flags_on:
            lines.append(f"- `{flag}`")
        lines.append("")

    if all_flags_leave:
        lines += ["## 🚩 Feature Flags — DO NOT ENABLE (from leaked issues)", ""]
        for flag in all_flags_leave:
            lines.append(f"- `{flag}`")
        lines.append("")

    # --- BE Migrations ---
    for r in results:
        if r["migration_items"]:
            migration_issues = [i["issue"] for i in r["migration_items"]]
            lines += [
                f"## 🗃️ BE Migrations — {r['label']} ({len(migration_issues)})",
                "",
                render_migrations_table(migration_issues),
                "",
            ]

    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(lines))

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Release readiness report")
    parser.add_argument("--release",  required=True, help='Release name, e.g. "2026-5-1"')
    parser.add_argument("--project",  nargs="+", choices=["CBP", "DATA"],
                        default=["CBP", "DATA"],
                        help="Projects to include (default: CBP DATA)")
    parser.add_argument("--jql",      default="", help="Additional JQL filter")
    args = parser.parse_args()

    load_env()

    project_str = " + ".join(args.project)
    print(f"🚀 Releasinator — {args.release} ({project_str})")

    print("\n  Fetching open qa→master PRs...")
    qa_master_items = get_qa_to_master_prs()
    print(f"  Found {len(qa_master_items)} open qa→master PRs")

    results = []
    for project_key in args.project:
        result = run_project_pipeline(project_key, args.release, args.jql, qa_master_items)
        if result:
            results.append(result)

    if not results:
        print(f"\n❌ No issues found for release '{args.release}' in any project.")
        print("   Check the release name matches a Jira fix version (e.g. '2026-5-1' → 'Platform-2026-5-1')")
        sys.exit(1)

    print("\n  Writing report...")
    write_report(args.release, results)

    total_issues = sum(len(r["issues_with_prs"]) for r in results)
    total_bump   = len(set().union(*(r["repos_to_bump"] for r in results)))
    total_leaks  = sum(len(r["leak_items"]) for r in results)
    total_repos  = len(set().union(*(r["all_release_repos"] for r in results)))

    print(f"\n✅ Releasinator complete for {args.release}")
    print(f"   {total_repos} repos touched · {total_issues} issues · {total_bump} repos to bump · {total_leaks} leaks")
    print(f"   Report: {REPORT_PATH}")

if __name__ == "__main__":
    main()
