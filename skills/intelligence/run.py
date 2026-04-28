#!/usr/bin/env python3
"""
Intelligence Ingestion Pipeline — Orchestrator

This is a semi-automated pipeline. Steps 01 (harvest) and 02 (parse) require
agent involvement because they use LLM synthesis to produce structured repo records.
Step 03 (scan_orphans) is fully automated and can be run standalone.

Usage:
    python3 run.py               # Print pipeline status and instructions
    python3 run.py --scan        # Run orphan scan only (step 03)
    python3 run.py --harvest     # Run harvest step (step 01)
    python3 run.py --harvest --force  # Force-refresh all sources (step 01)
    python3 run.py <file_path>   # Run parse step for a specific source file (step 02)
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))


def print_status():
    print("--- Intelligence Ingestion Pipeline ---")
    print()
    print("Stage 01: harvest     [AUTOMATED]")
    print("  → Walk intelligence records, refresh stale sources by system")
    print("  → Script: python3 skills/intelligence/scripts/01_harvest.py")
    print()
    print("Stage 02: parse       [AGENT-ASSISTED]")
    print("  → Apply LLM synthesis to extract structured repo intelligence records")
    print("  → Script: python3 skills/intelligence/scripts/02_parse.py <file_path>")
    print()
    print("Stage 03: scan_orphans [AUTOMATED]")
    print("  → Verify all source files have matching .md records; list any gaps")
    print("  → Script: python3 skills/intelligence/scripts/03_scan_orphans.py")
    print("         or: python3 skills/intelligence/run.py --scan")
    print()
    print("Schema: skills/intelligence/schemas/source-to-intelligence-prompt.md")


def prune_archive(archive_dir, keep=3):
    """Maintain rolling retention of snapshots."""
    if not os.path.isdir(archive_dir):
        return
    files = [os.path.join(archive_dir, f) for f in os.listdir(archive_dir) if os.path.isfile(os.path.join(archive_dir, f))]
    files.sort(key=os.path.getmtime, reverse=True)
    for f in files[keep:]:
        print(f"🗑️  Pruning old archive: {f}")
        os.remove(f)

def main():
    args = sys.argv[1:]

    if not args:
        print_status()
        return

    if args[0] == "--scan":
        subprocess.run(["python3", os.path.join(SCRIPT_DIR, "03_scan_orphans.py")], check=True)
    elif args[0] == "--harvest":
        cmd = ["python3", os.path.join(SCRIPT_DIR, "01_harvest.py")]
        if "--force" in args:
            cmd.append("--force")
        subprocess.run(cmd, check=True)
    else:
        # Treat first arg as file path → run parse step
        file_path = args[0]
        subprocess.run(["python3", os.path.join(SCRIPT_DIR, "02_parse.py"), file_path], check=True)

    # Token Economy Remediation
    print("\n📉 Performing Token Economy Remediation...")
    
    # 1. Prune Known Archives
    archives = [
        os.path.join(REPO_ROOT, "../../intelligence/product/shareout/q2/source/archive")
    ]
    for arch in archives:
        prune_archive(arch)
    
    # 2. Purge Raw Data from reports/
    raw_dirs = [
        os.path.join(REPO_ROOT, "../../reports/asana/raw"),
        os.path.join(REPO_ROOT, "../../reports/status/data/raw")
    ]
    for rd in raw_dirs:
        if os.path.isdir(rd):
            for f in os.listdir(rd):
                if f.endswith(".json"):
                    print(f"🔥 Purging raw artifact: {f}")
                    os.remove(os.path.join(rd, f))

if __name__ == "__main__":
    main()
