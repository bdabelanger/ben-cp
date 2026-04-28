#!/usr/bin/env python3
"""
tasks/run.py — Unified Task Harvester + Report Generator

1. Fetches tasks from Asana and issues from Jira
2. Writes raw snapshots to reports/tasks/data/raw/
3. Generates reports/tasks/report.md — a structured daily digest

Run daily. Wipes and rebuilds raw files each run.
"""
import os
import sys
import re
try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("❌ Error: 'requests' library not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)
from datetime import datetime, date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RAW_DIR = os.path.join(REPO_ROOT, "reports", "tasks", "data", "raw")
REPORT_PATH = os.path.join(REPO_ROOT, "reports", "tasks", "report.md")

ASANA_WORKSPACE_GID = "1123317448830974"

def load_dotenv():
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

# ---------------------------------------------------------------------------
# Asana
# ---------------------------------------------------------------------------

def fetch_asana_tasks(token):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    url = (
        f"https://app.asana.com/api/1.0/tasks"
        f"?assignee=me"
        f"&workspace={ASANA_WORKSPACE_GID}"
        f"&completed_since=now"
        f"&opt_fields=name,due_on,notes,permalink_url,projects.name"
    )
    tasks = []
    while url:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            print(f"❌ Asana API error {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
            return []
        body = resp.json()
        tasks.extend(body.get("data", []))
        nxt = body.get("next_page")
        url = nxt.get("uri") if nxt else None
    return tasks

def build_asana_md(tasks):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = ["# Asana — My Tasks", "", f"_Last synced: {today} · {len(tasks)} tasks_", ""]

    by_project = {}
    for t in tasks:
        projects = t.get("projects") or []
        project = projects[0]["name"] if projects else "No Project"
        by_project.setdefault(project, []).append(t)

    for project, items in sorted(by_project.items()):
        lines.append(f"## {project}")
        for t in items:
            title = t.get("name", "").strip()
            if not title:
                continue
            gid = t.get("gid", "")
            url = t.get("permalink_url", f"https://app.asana.com/0/{gid}")
            due = t.get("due_on")
            due_str = f" · due {due}" if due else ""
            lines.append(f"- [{title}]({url}){due_str}")
        lines.append("")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Jira
# ---------------------------------------------------------------------------

def fetch_jira_issues(email, token):
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    base = "https://casecommons.atlassian.net"
    jql = 'assignee = currentUser() AND resolution = Unresolved AND status not in ("Won\'t do", "Cancelled", "Done") ORDER BY priority ASC, updated DESC'
    issues = []
    start = 0
    while True:
        params = {
            "jql": jql,
            "fields": "summary,status,priority,project,duedate,description",
            "maxResults": 100,
            "startAt": start,
        }
        resp = requests.get(f"{base}/rest/api/3/search/jql", auth=auth, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"❌ Jira API error {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
            return []
        body = resp.json()
        batch = body.get("issues", [])
        issues.extend(batch)
        start += len(batch)
        if start >= body.get("total", 0) or not batch:
            break
    return issues

def build_jira_md(issues):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = ["# Jira — My Issues", "", f"_Last synced: {today} · {len(issues)} issues_", ""]

    by_project = {}
    for issue in issues:
        fields = issue.get("fields", {})
        project = (fields.get("project") or {}).get("name", "—")
        by_project.setdefault(project, []).append(issue)

    for project, items in sorted(by_project.items()):
        lines.append(f"## {project}")
        for issue in items:
            key = issue.get("key", "")
            fields = issue.get("fields", {})
            title = fields.get("summary", key)
            url = f"https://casecommons.atlassian.net/browse/{key}"
            priority = (fields.get("priority") or {}).get("name", "")
            status = (fields.get("status") or {}).get("name", "")
            due = fields.get("duedate")
            meta = " · ".join(filter(None, [priority, status, f"due {due}" if due else None]))
            meta_str = f" _({meta})_" if meta else ""
            lines.append(f"- [{key} — {title}]({url}){meta_str}")
        lines.append("")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def build_report(asana_tasks, jira_issues):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    today_date = date.today()
    lines = [
        f"# Task Report — {today}",
        "",
        f"_Last synced: {today} · {len(asana_tasks)} Asana tasks · {len(jira_issues)} Jira issues_",
        "",
    ]

    # --- Asana Scorecard ---
    lines += ["## Asana Scorecard", ""]

    by_project = {}
    for t in asana_tasks:
        projects = t.get("projects") or []
        project = projects[0]["name"] if projects else "No Project"
        by_project.setdefault(project, []).append(t)

    # Bucket table
    lines.append("| Bucket | Count |")
    lines.append("|---|---|")
    for project, items in sorted(by_project.items()):
        lines.append(f"| {project} | {len(items)} |")
    lines.append("")

    # Overdue
    overdue = []
    due_today = []
    for t in asana_tasks:
        due = t.get("due_on")
        if not due:
            continue
        try:
            due_date = date.fromisoformat(due)
        except ValueError:
            continue
        title = t.get("name", "").strip()
        url = t.get("permalink_url", "")
        entry = f"- [{title}]({url}) · due {due}"
        if due_date < today_date:
            overdue.append(entry)
        elif due_date == today_date:
            due_today.append(entry)

    if overdue:
        lines += ["### Overdue", ""]
        lines += overdue
        lines.append("")

    if due_today:
        lines += [f"### Due Today ({today})", ""]
        lines += due_today
        lines.append("")

    lines.append("---")
    lines.append("")

    # --- Jira Scorecard ---
    lines += ["## Jira Scorecard", ""]

    status_counts = {}
    active = []
    blocked = []

    for issue in jira_issues:
        fields = issue.get("fields", {})
        status = (fields.get("status") or {}).get("name", "Unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

        key = issue.get("key", "")
        title = fields.get("summary", key)
        url = f"https://casecommons.atlassian.net/browse/{key}"
        priority = (fields.get("priority") or {}).get("name", "")
        meta = f"_{priority}_" if priority else ""
        entry = f"- [{key} — {title}]({url}) {meta}"

        if "block" in status.lower() or "needs review" in status.lower():
            blocked.append(entry)
        elif status.lower() in ("in development", "in qa", "in uat", "qa revise", "product review", "beta"):
            active.append(entry)

    lines.append("| Status | Count |")
    lines.append("|---|---|")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {status} | {count} |")
    lines.append("")

    if active:
        lines += ["### Active (in flight)", ""]
        lines += active
        lines.append("")

    if blocked:
        lines += ["### Blocked", ""]
        lines += blocked
        lines.append("")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] tasks/run.py")
    load_dotenv()

    asana_token = os.environ.get("ASANA_API_TOKEN")
    atlassian_email = os.environ.get("ATLASSIAN_USER_EMAIL")
    atlassian_token = os.environ.get("ATLASSIAN_API_TOKEN")

    if not asana_token:
        print("❌ Missing ASANA_API_TOKEN", file=sys.stderr)
        sys.exit(1)
    if not atlassian_email or not atlassian_token:
        print("❌ Missing ATLASSIAN_USER_EMAIL or ATLASSIAN_API_TOKEN", file=sys.stderr)
        sys.exit(1)

    os.makedirs(RAW_DIR, exist_ok=True)

    print("📥 Fetching Asana tasks...")
    asana_tasks = fetch_asana_tasks(asana_token)
    asana_tasks = [t for t in asana_tasks if t.get("name", "").strip()]
    print(f"   {len(asana_tasks)} tasks found")
    with open(os.path.join(RAW_DIR, "asana.md"), "w") as f:
        f.write(build_asana_md(asana_tasks))
    print(f"   ✅ reports/tasks/data/raw/asana.md written")

    print("📥 Fetching Jira issues...")
    jira_issues = fetch_jira_issues(atlassian_email, atlassian_token)
    print(f"   {len(jira_issues)} issues found")
    with open(os.path.join(RAW_DIR, "jira.md"), "w") as f:
        f.write(build_jira_md(jira_issues))
    print(f"   ✅ reports/tasks/data/raw/jira.md written")

    print("📝 Generating report...")
    report = build_report(asana_tasks, jira_issues)
    with open(REPORT_PATH, "w") as f:
        f.write(report)
    print(f"   ✅ reports/tasks/report.md written")

    print(f"\n✅ tasks/run.py complete")

if __name__ == "__main__":
    main()
