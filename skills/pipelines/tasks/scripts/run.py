#!/usr/bin/env python3
"""
harvest_tasks.py — Unified Task Harvester
Writes tasks/asana.md and tasks/jira.md as daily snapshots.
Run daily. Wipes and rebuilds both files each run.
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
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
TASKS_DIR = os.path.join(VAULT_ROOT, "tasks")

ASANA_WORKSPACE_GID = "1123317448830974"

def load_dotenv():
    env_path = os.path.join(VAULT_ROOT, ".env")
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
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# Asana — My Tasks", f"", f"_Last synced: {today} · {len(tasks)} tasks_", ""]

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
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# Jira — My Issues", f"", f"_Last synced: {today} · {len(issues)} issues_", ""]

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
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] harvest_tasks.py")
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

    os.makedirs(TASKS_DIR, exist_ok=True)

    print("📥 Fetching Asana tasks...")
    asana_tasks = fetch_asana_tasks(asana_token)
    asana_tasks = [t for t in asana_tasks if t.get("name", "").strip()]
    print(f"   {len(asana_tasks)} tasks found")
    with open(os.path.join(TASKS_DIR, "asana.md"), "w") as f:
        f.write(build_asana_md(asana_tasks))
    print(f"   ✅ tasks/asana.md written")

    print("📥 Fetching Jira issues...")
    jira_issues = fetch_jira_issues(atlassian_email, atlassian_token)
    print(f"   {len(jira_issues)} issues found")
    with open(os.path.join(TASKS_DIR, "jira.md"), "w") as f:
        f.write(build_jira_md(jira_issues))
    print(f"   ✅ tasks/jira.md written")

    print(f"\n✅ harvest_tasks complete")

if __name__ == "__main__":
    main()
