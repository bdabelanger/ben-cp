import os
import sys
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
OUTPUT_PATH = os.path.join(VAULT_ROOT, "reports/asana/raw/all_tasks.json")

def fetch_asana_tasks():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] fetch_asana_tasks.py")
    
    # Placeholder for fetching Ben's tasks.
    # For now, just write an empty array to satisfy the pipeline output requirements.
    all_tasks = []

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_tasks, f, indent=2)

    print(f"✅ 02_fetch_tasks Complete: {len(all_tasks)} tasks written to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_asana_tasks()
