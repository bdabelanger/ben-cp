import json
import os
import sys
import re

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

# GIDs from the Official Specification
TEAM_FIELD_GID = "1208820967756795"
PLATFORM_TEAM_GID = "1208820967756799"
MILESTONE_GIDS = {
    "qa_start": "1211631943113717",
    "uat_start": "1210467277124544",
    "beta_start": "1208818118032458",
    "ga_date": "1210909549820601",  # Falling back to GA Month by default
    "ga_target": "1208818124273418"
}

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    repo_root = data['config']['repo_root']
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(repo_root, relative_path)

def extract_gid_from_url(url):
    match = re.search(r'/0/(\d+)', url)
    return match.group(1) if match else None

def filter_platform_projects(input_path, output_path, target_gid=None):
    print(f"Reading from: {input_path}")
    
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        filtered = []
        for p in data:
            # Single project mode: match GID
            if target_gid and p['gid'] != target_gid:
                continue

            # Batch mode: Extract fields
            custom_fields = p.get('custom_fields', [])
            
            # 📡 Robust field extraction (Full detail or Flat detail)
            jira_link = p.get('jira_link')
            stage = p.get('stage')
            
            # If nested detail exists, it takes precedence
            team_field = next((f for f in custom_fields if f['gid'] == TEAM_FIELD_GID), None)
            is_platform = (team_field and team_field.get('enum_value', {}).get('gid') == PLATFORM_TEAM_GID)
            
            if is_platform or not custom_fields:
                # Exclude completed projects
                if p.get('current_status_update', {}).get('status_type') == "complete" or p.get('status') == "complete":
                    continue
                
                # Extract milestones
                milestones = p.get('milestones', {})
                for key, gid in MILESTONE_GIDS.items():
                    field = next((f for f in custom_fields if f['gid'] == gid), None)
                    if field:
                        milestones[key] = field.get('date_value', {}).get('date') or field.get('enum_value', {}).get('name')
                
                p['milestones'] = milestones
                # Ensure jira_link is present for the harvester
                if not jira_link:
                    link_field = next((f for f in custom_fields if f['gid'] == "1208818005809198"), None)
                    jira_link = link_field.get('text_value') or link_field.get('display_value') if link_field else "N/A"
                
                p['jira_link'] = jira_link
                filtered.append(p)

        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        import datetime
        filtered.insert(0, {"_metadata": {"generated_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
        with open(output_path, 'w') as f:
            json.dump(filtered, f, indent=2)
            
        print(f"✅ 1_asana_ingest Complete: {len(filtered)} projects filtered.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import datetime
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Started step_1_asana_ingest.py")
    with open(MANIFEST_PATH, 'r') as f:
        manifest_data = json.load(f)
    repo_root = manifest_data['config']['repo_root']
    INPUT_FILE = os.path.join(repo_root, "inputs/raw/asana_all_projects.json")
    OUTPUT_FILE = get_path_from_manifest("1_asana_ingest")
    
    # Check for Single-project mode (URL in sys.argv)
    target_gid = None
    if len(sys.argv) > 1 and "asana.com" in sys.argv[1]:
        target_gid = extract_gid_from_url(sys.argv[1])
        print(f"🎯 Single-project mode detected for GID: {target_gid}")

    filter_platform_projects(INPUT_FILE, OUTPUT_FILE, target_gid)

