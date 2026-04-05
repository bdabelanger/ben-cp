import os
import sys
import json
import subprocess
from datetime import datetime
from platform_report import PlatformStatusReport

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

def get_path_from_manifest(data, step_id):
    repo_root = data['config']['repo_root']
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(repo_root, relative_path)

def build_jql_from_asana(asana_path):
    """Extract epic keys from Asana output and return a ready-to-run JQL string."""
    with open(asana_path, 'r') as f:
        projects = json.load(f)
    keys = []
    for p in projects:
        link = p.get('jira_link') or ''
        if 'CBP-' in link:
            keys.append(link.split('/')[-1].strip())
        for cf in p.get('custom_fields', []):
            if cf.get('gid') == '1208818005809198':
                val = cf.get('text_value') or cf.get('display_value') or ''
                if 'CBP-' in val:
                    keys.append(val.split('/')[-1].strip())
    return list(dict.fromkeys(keys))  # dedupe, preserve order

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 📡 Mode Detection (Asana URL / Batch)
    target_arg = sys.argv[1] if len(sys.argv) > 1 else None

    # Resolve all paths from manifest (dynamic — date-safe)
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    base_dir = manifest['config']['repo_root']
    ASANA_RAW = os.path.join(base_dir, "inputs/raw/asana_all_projects.json")
    ASANA_FILTERED = get_path_from_manifest(manifest, "1_asana_ingest")
    JIRA_HARVESTED = get_path_from_manifest(manifest, "4_jira_harvest")
    OUTPUT_PATH = get_path_from_manifest(manifest, "5_report_generation")

    if not os.path.exists(ASANA_RAW):
        print(f"❌ Error: Raw Asana data missing at {ASANA_RAW}")
        sys.exit(1)

    print("🚀 Triggering Pipeline Components...")

    # Step 1: Execute Asana Filter (Pass GID/URL if present)
    cmd = ["python3", os.path.join(script_dir, "step_1_asana_ingest.py")]
    if target_arg:
        cmd.append(target_arg)
    subprocess.run(cmd)

    # Step 2 (Agent-side): Jira fetch via searchJiraIssuesUsingJql
    if not os.path.exists(JIRA_HARVESTED):
        print(f"\n❌ PIPELINE PAUSED: Jira harvest data missing at {JIRA_HARVESTED}")
        print("=" * 60)
        print("🤖 AGENT ACTION REQUIRED — Step 2: Jira Fetch")
        print("=" * 60)
        print("Call tool: searchJiraIssuesUsingJql (Atlassian MCP)")
        print("Do NOT use: searchAtlassian, fetchAtlassian, or any other tool.\n")

        if os.path.exists(ASANA_FILTERED):
            epic_keys = build_jql_from_asana(ASANA_FILTERED)
            if epic_keys:
                key_list = ', '.join(epic_keys)
                print(f"Epic keys found: {key_list}\n")
                print("JQL to use:")
                print(f'  project = CBP AND issuetype != QAFE AND (issuekey in ({key_list}) OR "Epic Link" in ({key_list}) OR parent in ({key_list})) ORDER BY updated DESC')
                print(f"\nFields to request: summary, status, assignee, priority, issuetype, parent, timeoriginalestimate, timespent, fixVersions, created, updated")
                print(f"Max results: 100 (paginate if total > 100)")
            else:
                print("⚠️  No epic keys found in Asana output. Check that jira_link fields are populated.")
        else:
            print(f"⚠️  Asana output not found at {ASANA_FILTERED}. Run step_1_asana_ingest.py first.")

        print("=" * 60)
        print(f"After fetching, save the issues array to:")
        print(f"  {os.path.join(base_dir, 'inputs/raw/jira_issues.json')}")
        print(f"Then run: python3 {os.path.join(script_dir, 'step_3_jira_harvest.py')}")
        print(f"Then run: python3 {os.path.join(script_dir, 'step_4_report_generator.py')}")
        print("=" * 60)
        sys.exit(1)

    # 📊 FINAL SYNTHESIS
    print("📊 Synthesizing Platform Weekly Status...")

    reporter = PlatformStatusReport(ASANA_FILTERED, JIRA_HARVESTED)
    report_md = reporter.render()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(report_md)

    print(f"✅ Report generated: {OUTPUT_PATH}")
    print(f"\n--- PREVIEW ---\n")
    print(report_md)

if __name__ == "__main__":
    import datetime
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Started full_run.py")
    main()

