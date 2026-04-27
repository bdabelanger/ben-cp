import json
import sys
import os
import shutil
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# skills/pipelines/status/scripts/ -> ben-cp/
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../.."))
MANIFEST_PATH = os.path.join(VAULT_ROOT, "reports/status/data/manifest.json")
REPO_ROOT = VAULT_ROOT

def load_manifest():
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)

def save_manifest(data):
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def reset_manifest():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] update_manifest.py reset")
    data = load_manifest()
    run_id = datetime.now().strftime("%Y_%m_%d")

    # Archive existing processed files
    proc_dir = os.path.join(REPO_ROOT, data['config']['processed_dir'])
    arch_dir = os.path.join(REPO_ROOT, data['config']['archive_dir'])
    os.makedirs(arch_dir, exist_ok=True)

    d = datetime.now()
    date_str = f"{d.strftime('%b')}-{d.day}-{d.year}"  # e.g. Apr-7-2026

    for dir_to_archive in [proc_dir]:
        if os.path.exists(dir_to_archive):
            for filename in os.listdir(dir_to_archive):
                if filename.endswith(('.json', '.md')):
                    src = os.path.join(dir_to_archive, filename)
                    dst = os.path.join(arch_dir, f"archived_{run_id}_{filename}")
                    shutil.move(src, dst)
                    print(f"📦 Archived: {filename} -> {dst}")
                    
    # Enforce 7-Day Retention Policy on JSON Archives
    def cleanup_old_archives(directory, days=7):
        if not os.path.exists(directory): return
        now = datetime.now().timestamp()
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root_dir, file)
                    if now - os.path.getmtime(filepath) > days * 86400:
                        os.remove(filepath)
                        print(f"🗑️ Purged old archive: {filepath}")

    cleanup_old_archives(arch_dir)
    cleanup_old_archives(os.path.join(REPO_ROOT, "reports/status/data/raw"))

    data['last_run'] = run_id
    for step in data['steps']:
        step['status'] = "pending"
        if step['id'] == "1_asana_ingest":
            step['file'] = "reports/status/data/processed/asana_active.json"
        elif step['id'] == "2_atlassian_fetch":
            step['file'] = "reports/status/data/raw/jira"
        elif step['id'] == "3_rovo_context":
            step['file'] = "reports/status/data/processed/rovo_insights.json"
        elif step['id'] == "4_jira_harvest":
            step['file'] = "reports/status/data/processed/jira_issues.json"
        elif step['id'] == "5_report_generation":
            step['file'] = "reports/status/report.md"

    save_manifest(data)
    print(f"🔄 Manifest Reset for RUN_ID: {run_id}")

def update_status(step_id, new_status):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] update_manifest.py update_status")
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
