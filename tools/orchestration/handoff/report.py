#!/usr/bin/env python3
import json
import os
import glob
import re
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HANDOFF_DIR = os.path.join(REPO_ROOT, "orchestration/handoff")

def main():
    active_files = glob.glob(os.path.join(HANDOFF_DIR, "*.md"))
    
    p_counts = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    active_summaries = []
    
    for f in sorted(active_files):
        name = os.path.basename(f)
        # Try to extract P-level from filename
        p_match = re.search(r"-p([1-4])-", name, re.I)
        p_level = f"P{p_match.group(1).upper()}" if p_match else "P2" # Default to P2
        if p_level in p_counts:
            p_counts[p_level] += 1
        
        display_name = name.replace(".md", "").split("-", 3)[-1].replace("-", " ").title()
        active_summaries.append(f"{p_level}: {display_name}")

    total_active = len(active_files)
    p_str = ", ".join([f"{p_counts[k]} {k}" for k in ["P1", "P2", "P3", "P4"] if p_counts[k] > 0])
    
    summary = f"Handoff Queue: {total_active} active ({p_str})." if total_active > 0 else "Handoff Queue: Clean (0 active)."

    envelope = {
        "skill": "orchestration/handoff",
        "preferred_agent": "Handoff",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "ok" if p_counts["P1"] == 0 else "warn",
        "summary": summary,
        "findings": active_summaries[:5], # Show top 5
        "flags": []
    }
    
    if p_counts["P1"] > 0:
        envelope["flags"].append(f"BLOCKER: {p_counts['P1']} P1 handoff(s) require immediate attention.")

    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
