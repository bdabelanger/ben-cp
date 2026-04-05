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
        # New Linear ID naming logic
        if step['id'] == "1_asana_ingest":
            step['file'] = f"inputs/processed/asana_active_{run_id}.json"
        elif step['id'] == "2_jira_fetch":
            step['file'] = f"inputs/raw/jira_issues.json"
        elif step['id'] == "3_rovo_context":
            step['file'] = f"inputs/processed/rovo_insights_{run_id}.json"
        elif step['id'] == "4_jira_harvest":
            step['file'] = f"inputs/processed/jira_issues_{run_id}.json"
        elif step['id'] == "5_report_generation":
             step['file'] = f"outputs/Platform_Status_{run_id}.md"
            
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