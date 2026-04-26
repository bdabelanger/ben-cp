import json
import subprocess
import os
from collections import defaultdict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILLS_DIR = os.path.join(ROOT_DIR, "intelligence/core/skills")

def generate_sync_entry():
    # Run the changelog report to get the raw list
    report_cmd = ["python3", os.path.join(ROOT_DIR, "tools/orchestration/changelog/report.py")]
    result = subprocess.run(report_cmd, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
    except:
        print("Failed to parse report output.")
        return

    snowed_in = [f.replace("Snowed In: ", "").replace(" modified in Git but undocumented in latest log.", "") 
                 for f in data.get("flags", []) if f.startswith("Snowed In:")]

    if not snowed_in:
        print("No Snowed In files found.")
        return

    # Group by base directory
    grouped = defaultdict(list)
    for f in snowed_in:
        parts = f.split("/")
        if len(parts) > 1:
            group = parts[0]
            if group == "intelligence" and len(parts) > 3 and parts[1] == "core" and parts[2] == "skills":
                group = f"intelligence/core/skills/{parts[3]}"
            grouped[group].append(f)
        else:
            grouped["root"].append(f)

    # Generate Markdown
    md = f"## [1.18.2] — Milestone: Vault-wide Structural Alignment ({data['run_at'][:10]})\n\n"
    md += "> **Sync Operation:** Finalizing the Documentation Triad normalization by bulk-logging path-drift from the last 72 hours.\n\n"
    md += "Changes:\n"
    
    for group in sorted(grouped.keys()):
        md += f"- **{group}**:\n"
        for f in sorted(grouped[group]):
            md += f"  - `{f}`\n"
        md += "\n"

    print(md)

if __name__ == "__main__":
    generate_sync_entry()
