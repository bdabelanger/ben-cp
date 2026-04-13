#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence/product/projects")
DATA_FILE = os.path.join(REPO_ROOT, "inputs/status-reports/processed/asana_active.json")
DETAILED_REPORT_DIR = os.path.join(REPO_ROOT, "outputs/dream/reports")
DETAILED_REPORT_URL = "reports/product-projects.md"
VAULT_CSS = os.path.join(SKILLS_DIR, "styles", "vault.css")

ACTIVE_STAGES = {"Development", "In QA", "In UAT", "Beta", "GA"}

def load_css():
    if os.path.exists(VAULT_CSS):
        with open(VAULT_CSS, "r") as f:
            return f.read()
    return "body { font-family: sans-serif; padding: 2rem; background: #0f172a; color: #f8fafc; }"

def main():
    # 1. Summary of intelligence records
    q2_files = glob.glob(os.path.join(INTEL_DIR, "q2/*.md"))
    total_intel = len(q2_files)
    
    # 2. Summary of live data from Asana
    live_active = 0
    at_risk = 0
    off_track = 0
    active_list = []
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Filter specifically by active stages
            active_list = [p for p in data if p.get("stage") in ACTIVE_STAGES]
            live_active = len(active_list)
            for p in active_list:
                status = (p.get("status") or p.get("last_status_type") or "").lower()
                if "risk" in status:
                    at_risk += 1
                elif "off" in status:
                    off_track += 1

    summary = f"Project Health: Tracking {total_intel} Q2 initiatives in intelligence."
    if live_active:
        summary += f" Live harvest shows {live_active} active projects ({at_risk} at risk, {off_track} off track)."

    flags = [f"CRITICAL: {off_track} project(s) reported as OFF TRACK in Asana."] if off_track > 0 else []
    if at_risk > 0:
        flags.append(f"WARNING: {at_risk} project(s) reported as AT RISK.")

    # 3. Generate Detailed Pages (MD and HTML)
    os.makedirs(DETAILED_REPORT_DIR, exist_ok=True)
    
    # Markdown Version
    with open(os.path.join(DETAILED_REPORT_DIR, "product-projects.md"), "w") as rf:
        rf.write(f"# Detailed Project Status — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        rf.write(f"## Active Scorecard\n")
        rf.write(f"- **Intelligence Records**: {total_intel} (Q2 initiatives)\n")
        rf.write(f"- **Asana Live Active**: {live_active}\n")
        rf.write(f"- **Risk Level**: {'WARN' if (at_risk or off_track) else 'OK'}\n\n")
        rf.write(f"## Active Projects\n")
        if active_list:
            sorted_list = sorted(active_list, key=lambda x: (x.get("status") or "on_track") != "on_track", reverse=True)
            for p in sorted_list:
                p_status = (p.get("status") or p.get("last_status_type") or "").lower()
                emoji = "🔴" if "off" in p_status else ("🟡" if "risk" in p_status else "🟢")
                rf.write(f"### {emoji} {p.get('name')} ({p.get('stage')})\n")
                status_text = p.get('current_status_update', {}).get('text', 'No status update.')
                rf.write(f"{status_text}\n\n")

    # Themed HTML Version
    css = load_css()
    with open(os.path.join(DETAILED_REPORT_DIR, "product-projects.html"), "w") as hf:
        hf.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>{css}</style>
</head>
<body class="gazette-body">
<div class="container">
<h1>Detailed Project Status — {datetime.now().strftime('%Y-%m-%d')}</h1>
<div class="lede">
    <p><strong>Intelligence Coverage:</strong> {total_intel} / <strong>Live Harvest:</strong> {live_active}</p>
</div>
""")
        if active_list:
            sorted_list = sorted(active_list, key=lambda x: (x.get("status") or "on_track") != "on_track", reverse=True)
            for p in sorted_list:
                p_status = (p.get("status") or p.get("last_status_type") or "").lower()
                emoji = "🔴" if "off" in p_status else ("🟡" if "risk" in p_status else "🟢")
                sev = "error" if "off" in p_status else ("warn" if "risk" in p_status else "ok")
                status_text = p.get('current_status_update', {}).get('text', 'No status update.').replace("\n", "<br>")
                hf.write(f'  <div class="column" style="border-left-color:{"#ef4444" if sev=="error" else ("#f59e0b" if sev=="warn" else "#22c55e")}; margin-bottom: 2rem;">\n')
                hf.write(f'    <h3>{emoji} {p.get("name")} ({p.get("stage")})</h3>\n')
                hf.write(f'    <p>{status_text}</p>\n')
                hf.write(f'  </div>\n')
        hf.write('  <footer class="vault-footer">End of Detailed Report</footer>\n')
        hf.write("</div>\n</body></html>")

    envelope = {
        "skill": "product/projects",
        "preferred_agent": "Strategic PM",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "ok" if (at_risk == 0 and off_track == 0) else "warn",
        "summary": summary,
        "findings": [
            f"Vault covers {total_intel} projects for Q2 release.",
            f"External sync verified {live_active} projects via Asana ingestion.",
            f"Full Report: [View Details]({DETAILED_REPORT_URL})"
        ],
        "flags": flags
    }

    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
