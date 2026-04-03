import json
import os
from datetime import datetime

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    repo_root = data['config']['repo_root']
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(repo_root, relative_path)

def get_progress_bar(percent):
    filled = int(percent / 10)
    return "▓" * filled + "░" * (10 - filled)

def generate_report():
    today = datetime.now().strftime("%B %d, %Y")
    
    # Resolve step-specific file dependencies dynamically
    ASANA_FILE = get_path_from_manifest("1_asana_ingest")
    JIRA_FILE = get_path_from_manifest("2_jira_harvest")
    OUTPUT_PATH = get_path_from_manifest("3_report_generation")

    try:
        with open(ASANA_FILE, 'r') as f:
            asana_data = json.load(f)
        with open(JIRA_FILE, 'r') as f:
            jira_data = json.load(f)

        report = [f"### Platform Weekly Status Report ({today})\n"]

        for project in asana_data:
            name = project.get('name', 'Unknown Project')
            permalink = project.get('permalink_url', '#')
            # Custom logic for status bar (defaulting to 50% for dummy data)
            report.append(f"**Project Header:** {name}")
            report.append(f"**Asana Permalink:** [View Project]({permalink})")
            report.append(f"**Overall Status:** {get_progress_bar(50)} (On Track)\n")
            report.append("---\n### ⚙️ Jira Issue Breakdown\n")

            # Group Jira issues by status
            statuses = {}
            for issue in jira_data:
                # Only include issues related to this project (simplification for dummy run)
                status_name = issue['fields']['status']['name']
                if status_name not in statuses:
                    statuses[status_name] = []
                statuses[status_name].append(issue)

            for status, issues in statuses.items():
                report.append(f"#### **{status}** ({get_progress_bar(70)})")
                for isue in issues:
                    key = isue['key']
                    summary = isue['fields']['summary']
                    assignee = isue['fields'].get('assignee', {}).get('displayName', 'Unassigned')
                    priority = isue['fields'].get('priority', {}).get('name', 'P3')
                    report.append(f"* **{key}**: {summary}")
                    report.append(f"    * Assignee: {assignee} | Priority: {priority}")
                report.append("")

        # Save the report
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, 'w') as f:
            f.write("\n".join(report))
        
        print(f"✅ 3_report_generation Complete: {OUTPUT_PATH}")

    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")

if __name__ == "__main__":
    generate_report()