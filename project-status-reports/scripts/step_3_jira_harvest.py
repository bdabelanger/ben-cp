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
    OUTPUT = get_path_from_manifest("4_jira_harvest")

    # Status Category Overrides from official logic
    OVERRIDES = {
        "Blocked - Needs Review": "To Do",
        "Blocked - Third-Party": "To Do",
        "QA Revise": "In Progress"
    }

    # 1. Load active Asana projects
    with open(ASANA_ACTIVE, 'r') as f:
        active_projects = json.load(f)
    
    valid_keys = set()
    for p in active_projects:
        # Extract Epic Key from various potential Asana fields
        link = p.get('jira_link') or ""
        if "CBP-" in link:
            valid_keys.add(link.split('/')[-1])
        for cf in p.get('custom_fields', []):
            if cf.get('gid') == "1208818005809198": # Official JIRA Link GID
                val = cf.get('text_value') or cf.get('display_value') or ""
                if "CBP-" in val:
                    valid_keys.add(val.split('/')[-1])

    # 2. Filter and Map Jira issues
    with open(JIRA_RAW, 'r') as f:
        all_issues = json.load(f)
        
    if not all_issues:
        print("❌ Error: Jira issues fetch returned empty results. The agent step failed to retrieve data.")
        import sys
        sys.exit(1)
        
    
    # Pass 1: Deduplicate and exclude QAFE
    filtered = []
    for i in all_issues:
        fields = i.get('fields', {})
        
        # Exclude QAFE issue types
        if fields.get('issuetype', {}).get('name') == "QAFE":
            continue
            
        # Determine effective status category for reporting
        status_name = fields.get('status', {}).get('name')
        native_category = fields.get('status', {}).get('statusCategory', {}).get('name')
        
        # Apply Overrides
        effective = OVERRIDES.get(status_name) or native_category
        i['effective_category'] = effective
        
        # Check hierarchy (Epic -> Standard -> Sub-task)
        parent_key = fields.get('parent', {}).get('key')
        if i['key'] in valid_keys or parent_key in valid_keys:
            filtered.append(i)
        else:
            # Check for second-level hierarchy (Sub-task of a child of an Epic)
            # This is handled by recursively checking in full_run or here
            filtered.append(i) # For now we keep all and let platform_report bucket them

    # Final filter: Only return items that belong to the active project set
    final_harvest = [i for i in filtered if i['key'] in valid_keys or i.get('fields', {}).get('parent', {}).get('key') in valid_keys]

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    import datetime
    final_harvest.insert(0, {"_metadata": {"generated_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
    with open(OUTPUT, 'w') as f:
        json.dump(final_harvest, f, indent=2)
    
    print(f"✅ 3_jira_harvest Complete: {len(final_harvest)} issues harvested.")


if __name__ == "__main__":
    import datetime
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Started step_3_jira_harvest.py")
    harvest()
