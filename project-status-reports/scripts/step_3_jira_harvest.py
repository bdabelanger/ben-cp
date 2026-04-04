import json
import os

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    repo_root = data['config']['repo_root']
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(repo_root, relative_path)

def harvest():
    # Helper to resolve raw absolute input dir
    with open(MANIFEST_PATH, 'r') as f:
        manifest_data = json.load(f)
    repo_root = manifest_data['config']['repo_root']
    
    # Resolve step-specific file dependencies dynamically
    ASANA_ACTIVE = get_path_from_manifest("1_asana_ingest")
    JIRA_RAW = os.path.join(repo_root, "inputs/raw/jira_issues.json")
    OUTPUT = get_path_from_manifest("3_jira_harvest")

    # 1. Load active Asana projects to get Jira keys
    with open(ASANA_ACTIVE, 'r') as f:
        active_projects = json.load(f)
    
    # Extract keys (e.g., "CBP-2736") from the Jira Link custom field
    valid_keys = []
    for p in active_projects:
        if 'jira_link' in p and p['jira_link'] != "N/A":
            valid_keys.append(p['jira_link'])
        for cf in p.get('custom_fields', []):
            if cf.get('name') == "JIRA Link" and cf.get('display_value'):
                # Extract key from URL
                valid_keys.append(cf['display_value'].split('/')[-1])

    # 2. Filter raw Jira issues
    with open(JIRA_RAW, 'r') as f:
        all_issues = json.load(f)
    
    # Keep issues where the parent key matches our active projects
    filtered = [i for i in all_issues if i.get('fields', {}).get('parent', {}).get('key') in valid_keys]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        json.dump(filtered, f, indent=2)
    
    print(f"✅ 3_jira_harvest Complete: {OUTPUT}")

if __name__ == "__main__":
    harvest()
