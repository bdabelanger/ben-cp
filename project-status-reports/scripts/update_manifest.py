import json
import sys
import os
import shutil
from datetime import datetime

MANIFEST_PATH = "/Users/benbelanger/GitHub/ben-cp/project-status-reports/manifest.json"

def load_manifest():
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)

def save_manifest(data):
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def reset_manifest():
    data = load_manifest()
    root = data['config']['repo_root']
    run_id = datetime.now().strftime("%Y_%m_%d")
    
    # 1. Hybrid Archive: Move existing processed files to archive
    proc_dir = os.path.join(root, data['config']['processed_dir'])
    arch_dir = os.path.join(root, data['config']['archive_dir'])
    os.makedirs(arch_dir, exist_ok=True)

    if os.path.exists(proc_dir):
        for filename in os.listdir(proc_dir):
            if filename.endswith(('.json', '.md')):
                src = os.path.join(proc_dir, filename)
                dst = os.path.join(arch_dir, f"archived_{run_id}_{filename}")
                shutil.move(src, dst)
                print(f"📦 Archived: {filename} -> {dst}")

    # 2. Update Manifest State
    data['last_run'] = run_id
    for step in data['steps']:
        step['status'] = "pending"
        # Extract base name without existing dates to rebuild path
        if step['id'] == "3_report_generation":
            step['file'] = f"outputs/Platform_Status_{run_id}.md"
        else:
            # Logic to keep the prefix but update the date suffix
            # Applying a minor correction to user's logic to match the explicit asana_active/jira_issues format
            if step['id'] == '1_asana_ingest':
                base_name = 'asana_active'
            elif step['id'] == '2_jira_harvest':
                base_name = 'jira_issues'
            else:
                base_name = step['id'].replace('1_', 'asana_').replace('2_', 'jira_')
                
            step['file'] = f"{data['config']['processed_dir']}/{base_name}_{run_id}.json"
            
    save_manifest(data)
    print(f"🔄 Manifest Reset for RUN_ID: {run_id}")

def update_status(step_id, new_status):
    data = load_manifest()
    for step in data['steps']:
        if step['id'] == step_id:
            step['status'] = new_status
    save_manifest(data)
    print(f"✅ Status Updated: {step_id} -> {new_status}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 update_manifest.py [reset | step_id status]")
        sys.exit(1)
        
    action = sys.argv[1]
    if action == "reset":
        reset_manifest()
    else:
        update_status(action, sys.argv[2])