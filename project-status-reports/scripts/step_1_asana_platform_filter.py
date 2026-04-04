import json
import os

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

def get_path_from_manifest(step_id):
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    repo_root = data['config']['repo_root']
    relative_path = next(s['file'] for s in data['steps'] if s['id'] == step_id)
    return os.path.join(repo_root, relative_path)

def filter_platform_projects(input_path, output_path):
    PLATFORM_TEAM_GID = "1208820967756799"
    TEAM_FIELD_GID = "1208820967756795"
    
    print(f"Reading from: {input_path}")
    
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        filtered = []
        for p in data:
            if 'custom_fields' in p:
                # Check custom fields for Platform Team GID
                team_field = next((f for f in p.get('custom_fields', []) if f['gid'] == TEAM_FIELD_GID), None)
                if team_field and team_field.get('enum_value', {}).get('gid') == PLATFORM_TEAM_GID:
                    # Keep if not complete
                    if p.get('current_status_update', {}).get('status_type') != "complete":
                        filtered.append(p)
            else:
                # Handle flat dummy data
                if p.get('status') != "complete":
                    filtered.append(p)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(filtered, f, indent=2)
            
        print(f"✅ 1_asana_ingest Complete: {output_path}")
    except FileNotFoundError:
        print(f"❌ Error: Could not find input file at {input_path}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")

# --- THE EXECUTION BLOCK (The "Hands") ---
if __name__ == "__main__":
    with open(MANIFEST_PATH, 'r') as f:
        manifest_data = json.load(f)
    repo_root = manifest_data['config']['repo_root']
    
    INPUT_FILE = os.path.join(repo_root, "inputs/raw/asana_all_projects.json")
    OUTPUT_FILE = get_path_from_manifest("1_asana_ingest")
    
    filter_platform_projects(INPUT_FILE, OUTPUT_FILE)
