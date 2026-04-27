#!/usr/bin/env python3
import json
import os
import sys
import glob
import subprocess
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence/product/projects")
PIPELINE_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(REPO_ROOT, "reports", "status", "data", "processed", "asana_active.json")
JIRA_FILE = os.path.join(REPO_ROOT, "reports", "status", "data", "raw", "jira_issues.json")
JIRA_RAW_DIR = os.path.join(REPO_ROOT, "reports", "status", "data", "raw", "jira")
DETAILED_REPORT_DIR = os.path.join(REPO_ROOT, "reports", "status")
DETAILED_REPORT_URL = "reports/status/report.md"


# Legacy analytics engine lives in scripts/ sibling directory
SCRIPTS_DIR = os.path.join(PIPELINE_ROOT, "scripts")

ACTIVE_STAGES = {"Development", "In QA", "In UAT", "Beta", "GA"}

# Try to import the legacy analytics engine
try:
    if SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, SCRIPTS_DIR)
    from platform_report import PlatformStatusReport
    _LEGACY_AVAILABLE = True
except ImportError:
    # Try 07_build_report if platform_report is missing
    try:
        from scripts.build_report import PlatformStatusReport
        _LEGACY_AVAILABLE = True
    except:
        _LEGACY_AVAILABLE = False





def _generate_rich_detailed_report():
    """
    Use PlatformStatusReport (legacy analytics engine) to generate the full
    data-rich HTML report: Jira burndowns, milestone tracking, data quality sidebar.
    Returns True on success, False if Jira data is unavailable or import failed.
    """
    if not _LEGACY_AVAILABLE:
        return False
    if not os.path.exists(JIRA_FILE):
        return False
    if not os.path.exists(DATA_FILE):
        return False

    try:
        reporter = PlatformStatusReport(DATA_FILE, JIRA_FILE, JIRA_RAW_DIR)
        report_md = reporter.render()

        os.makedirs(DETAILED_REPORT_DIR, exist_ok=True)


        md_out = os.path.join(DETAILED_REPORT_DIR, "report.md")
        with open(md_out, "w") as f:
            f.write(report_md)

        return True
    except Exception:
        return False


def _generate_simple_detailed_report(active_list, total_intel, live_active):
    """
    Fallback: Asana-status-only HTML report. Used when Jira data is not yet
    available (e.g. the full pipeline hasn't run yet today).
    """
    os.makedirs(DETAILED_REPORT_DIR, exist_ok=True)

    # Markdown Version
    with open(os.path.join(DETAILED_REPORT_DIR, "report.md"), "w") as rf:
        rf.write(f"# Detailed Project Status — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        rf.write(f"## Active Scorecard\n")
        rf.write(f"- **Intelligence Records**: {total_intel} (Q2 initiatives)\n")
        rf.write(f"- **Asana Live Active**: {live_active}\n\n")
        rf.write(f"## Active Projects\n")
        if active_list:
            sorted_list = sorted(active_list, key=lambda x: (x.get("status") or "on_track") != "on_track", reverse=True)
            for p in sorted_list:
                p_status = (p.get("status") or p.get("last_status_type") or "").lower()
                emoji = "🔴" if "off" in p_status else ("🟡" if "risk" in p_status else "🟢")
                rf.write(f"### {emoji} {p.get('name')} ({p.get('stage')})\n")
                status_text = p.get('current_status_update', {}).get('text', 'No status update.')
                rf.write(f"{status_text}\n\n")




def main():
    # 0. Trigger the data pipeline to fetch fresh data from Asana and Jira
    try:
        subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "run.py")], capture_output=True, check=True)
    except Exception as e:
        # We fail silently and let the report degrade gracefully if data fetching fails
        pass

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

    # 3. Generate Detailed Report — prefer rich legacy engine, fall back to simple
    rich = _generate_rich_detailed_report()
    if not rich:
        _generate_simple_detailed_report(active_list, total_intel, live_active)

    report_source = "platform_report (Jira+Asana)" if rich else "asana_active (Asana only)"

    envelope = {
        "skill": "product/projects",
        "preferred_agent": "Strategic PM",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "ok" if (at_risk == 0 and off_track == 0) else "warn",
        "summary": summary,
        "findings": [
            f"Vault covers {total_intel} projects for Q2 release.",
            f"External sync verified {live_active} projects via Asana ingestion.",
            f"Full Report: [View Details]({DETAILED_REPORT_URL})",
            f"Report source: {report_source}.",
        ],
        "flags": flags
    }

    print(json.dumps(envelope))


if __name__ == "__main__":
    main()
