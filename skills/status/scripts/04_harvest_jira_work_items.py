import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
MANIFEST_PATH = os.path.join(VAULT_ROOT, "reports/status/data/manifest.json")
REPO_ROOT = VAULT_ROOT

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(REPO_ROOT, relative_path)

def harvest():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] harvest_jira_work_items.py")
    ASANA_ACTIVE = get_path_from_manifest("1_asana_ingest")
    JIRA_RAW_DIR = os.path.join(VAULT_ROOT, "reports/status/data/raw/jira")
    OUTPUT = get_path_from_manifest("4_jira_harvest")

    OVERRIDES = {
        "Blocked - Needs Review": "To Do",
        "Blocked - Third-Party": "To Do",
        "QA Revise": "In Progress"
    }

    # Load active Asana projects
    with open(ASANA_ACTIVE, 'r') as f:
        active_projects = [p for p in json.load(f) if '_metadata' not in p]

    valid_keys = set()
    for p in active_projects:
        link = p.get('jira_link') or ""
        if "CBP-" in link:
            valid_keys.add(link.split('/')[-1])
        for cf in p.get('custom_fields', []):
            if cf.get('gid') == "1208818005809198":
                val = cf.get('text_value') or cf.get('display_value') or ""
                if "CBP-" in val:
                    valid_keys.add(val.split('/')[-1])

    # Load all per-epic raw Jira files from inputs/raw/jira/
    all_issues = []
    if os.path.isdir(JIRA_RAW_DIR):
        for fname in sorted(os.listdir(JIRA_RAW_DIR)):
            if fname.endswith('.json'):
                fpath = os.path.join(JIRA_RAW_DIR, fname)
                with open(fpath, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_issues.extend(data)
    else:
        print(f"❌ Jira raw directory not found: {JIRA_RAW_DIR}")
        import sys
        sys.exit(1)

    if not all_issues:
        print("❌ Error: No Jira issues found in raw directory.")
        import sys
        sys.exit(1)

    print(f"  Loaded {len(all_issues)} raw issues from {JIRA_RAW_DIR}")

    # Deduplicate by key (overlapping results across epic files)
    seen = {}
    for i in all_issues:
        seen[i['key']] = i
    all_issues = list(seen.values())

    # Apply overrides, exclude QAFE, filter to active epics
    filtered = []
    for i in all_issues:
        fields = i.get('fields', {})

        if fields.get('issuetype', {}).get('name') == "QAFE":
            continue

        status_name = fields.get('status', {}).get('name')
        native_category = fields.get('status', {}).get('statusCategory', {}).get('name')
        i['effective_category'] = OVERRIDES.get(status_name) or native_category
        
        i['jira_status'] = status_name
        versions = fields.get('fixVersions', [])
        eff_rel_date = None
        for v in versions:
            rd = v.get('releaseDate')
            if rd:
                if eff_rel_date is None or rd > eff_rel_date:
                    eff_rel_date = rd
        i['effective_release_date'] = eff_rel_date

        parent_key = fields.get('parent', {}).get('key')
        if i['key'] in valid_keys or parent_key in valid_keys:
            filtered.append(i)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        json.dump(filtered, f, indent=2)

    print(f"✅ step_3_jira_harvest Complete: {len(filtered)} issues harvested.")


if __name__ == "__main__":
    harvest()
