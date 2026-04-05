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
    ROVO_FILE = get_path_from_manifest("3_rovo_context")
    JIRA_DATA = get_path_from_manifest("4_jira_harvest")
    OUTPUT = get_path_from_manifest("5_report_generation")

    try:
        with open(ASANA_FILE, 'r') as f:
            asana_data = [d for d in json.load(f) if "_metadata" not in d]
        with open(ROVO_FILE, 'r') as f:
            rovo_data = json.load(f)
        with open(JIRA_DATA, 'r') as f:
            jira_data = [d for d in json.load(f) if "_metadata" not in d]

        report = [f"### Platform Weekly Status Report\n", f"_Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n"]

        total_projects = len(asana_data)
        total_rovo_insights = 0
        total_blockers = 0
        total_jira_issues = len(jira_data)

        for project in asana_data:
            name = project.get('name', 'Unknown Project')
            permalink = project.get('permalink_url', '#')
            
            report.append(f"**Project Header:** {name}")
            report.append(f"**Asana Permalink:** [View Project]({permalink})")
            report.append(f"**Overall Status:** {get_progress_bar(50)} (On Track)\n")
            
            # --- ROVO CONTEXT INJECTION ---
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

            # Group Jira issues by status
            statuses = {}
            for issue in jira_data:
                # Only include issues related to this project (simplification for dummy run)
                # SAFE: get status name or fallback to "N/A"
                status_name = issue.get('fields', {}).get('status', {}).get('name', 'N/A')
                if status_name not in statuses:
                    statuses[status_name] = []
                statuses[status_name].append(issue)

            for status, issues in statuses.items():
                report.append(f"#### **{status}** ({get_progress_bar(70)})")
                for isue in issues:
                    key = isue.get('key', 'Unknown')
                    # SAFE: get summary, assignee, priority
                    fields = isue.get('fields', {})
                    summary = fields.get('summary', 'No summary provided')
                    assignee = fields.get('assignee', {}).get('displayName', 'Unassigned')
                    priority = fields.get('priority', {}).get('name', 'P3')
                    report.append(f"* **{key}**: {summary}")
                    report.append(f"    * Assignee: {assignee} | Priority: {priority}")
                report.append("")

        # Save the report
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        with open(OUTPUT, 'w') as f:
            f.write("\n".join(report))
        
        # --- STDOUT REPORT CONTRACT ---
        print("--- REPORT START ---")
        print("\n".join(report))
        print("--- REPORT END ---")
        
        print(f"✅ 5_report_generation Complete: {OUTPUT}")

    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Started step_4_report_generator.py")
    generate_report()
