import os
import sys
import json
from datetime import datetime
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print(f"❌ Error running {script_name}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    run_script("01_fetch_projects.py")
    run_script("02_fetch_tasks.py")
    run_script("03_normalize.py")
    print("\n✅ Asana pipeline completed successfully.")
