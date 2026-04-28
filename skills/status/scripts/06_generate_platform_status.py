import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
MANIFEST_PATH = os.path.join(REPO_ROOT, "reports/status/data/manifest.json")
REPO_ROOT = REPO_ROOT

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(REPO_ROOT, relative_path)

def get_progress_bar(percent):
    filled = int(percent / 10)
    return "▓" * filled + "░" * (10 - filled)

def generate_report():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] step_4_report_generator.py")
    today = datetime.now().strftime("%B %d, %Y")

    ASANA_FILE = get_path_from_manifest("1_asana_ingest")
    ROVO_FILE  = get_path_from_manifest("3_rovo_context")
    JIRA_DATA  = get_path_from_manifest("4_jira_harvest")
    OUTPUT     = get_path_from_manifest("5_report_generation")

    try:
        with open(ASANA_FILE, 'r') as f:
            asana_data = [d for d in json.load(f) if "_metadata" not in d]
        with open(ROVO_FILE, 'r') as f:
            rovo_data = json.load(f)
        with open(JIRA_DATA, 'r') as f:
            jira_data = [d for d in json.load(f) if "_metadata" not in d]

        report = [
            f"### Platform Weekly Status Report ({today})\n",
            f"_Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n"
        ]

        total_rovo_insights = 0
        total_blockers = 0

        for project in asana_data:
            name = project.get('name', 'Unknown Project')
            permalink = project.get('permalink_url', '#')

            report.append(f"**Project Header:** {name}")
            report.append(f"**Asana Permalink:** [View Project]({permalink})")
            report.append(f"**Overall Status:** {get_progress_bar(50)} (On Track)\n")

            insight = rovo_data.get(name, {})
            if insight:
                total_rovo_insights += 1
                blocker = insight.get('blockers_mention', 'N/A')
                if blocker and blocker.lower() != 'n/a':
                    total_blockers += 1

                report.append("#### 🧠 Rovo Decisions & Context")
                report.append(f"* **Sentiment**: {insight.get('sentiment', 'N/A')}")
                report.append(f"* **Insight**: {insight.get('summary', 'No summary available.')}")
                report.append(f"* **Blockers**: {blocker}\n")

            report.append("---\n### ⚙️ Jira Issue Breakdown\n")

            statuses = {}
            for issue in jira_data:
                status_name = issue.get('fields', {}).get('status', {}).get('name', 'N/A')
                statuses.setdefault(status_name, []).append(issue)

            for status, issues in statuses.items():
                report.append(f"#### **{status}** ({get_progress_bar(70)})")
                for issue in issues:
                    key = issue.get('key', 'Unknown')
                    fields = issue.get('fields', {})
                    summary = fields.get('summary', 'No summary provided')
                    assignee = (fields.get('assignee') or {}).get('displayName', 'Unassigned')
                    priority = (fields.get('priority') or {}).get('name', 'P3')
                    report.append(f"* **{key}**: {summary}")
                    report.append(f"    * Assignee: {assignee} | Priority: {priority}")
                report.append("")

        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        with open(OUTPUT, 'w') as f:
            f.write("\n".join(report))

        print("--- REPORT START ---")
        print("\n".join(report))
        print("--- REPORT END ---")
        print(f"✅ step_4_report_generator Complete: {OUTPUT}")

    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")

if __name__ == "__main__":
    generate_report()
