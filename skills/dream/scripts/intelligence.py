#!/usr/bin/env python3
"""intelligence.py — Monitor intelligence record integrity.
Wraps the existing intelligence scan pipeline as a sensor.
"""
import os, json, subprocess
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')
SCAN_SCRIPT = os.path.join(REPO_ROOT, 'skills', 'intelligence', 'run.py')

def run():
    print(f"  🔍 running intelligence scan...")
    try:
        proc = subprocess.run(
            ['python3', SCAN_SCRIPT, '--scan'],
            capture_output=True, text=True, timeout=60, cwd=REPO_ROOT
        )
        stdout = proc.stdout
        stderr = proc.stderr
        
        # Parse findings count from stdout: "⚠️ Found N orphaned source file(s):"
        orphans = []
        found_m = re.search(r'Found (\d+) orphaned', stdout)
        count = int(found_m.group(1)) if found_m else 0
        
        if count > 0:
            # Extract orphan paths from lines starting with "  - "
            for line in stdout.splitlines():
                if line.strip().startswith('- '):
                    orphans.append(line.strip('- ').strip())
    except Exception as e:
        stdout = ""
        stderr = str(e)
        count = 0
        orphans = []

    report = {
        "sensor": "intelligence",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "orphaned_sources": count
        },
        "orphans": orphans,
        "stdout": stdout,
        "stderr": stderr
    }
    
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'intelligence_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ intelligence → {out}")
    return report

if __name__ == '__main__':
    import re # Needed for the regex
    run()
