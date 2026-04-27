#!/usr/bin/env python3
"""
Intelligence Ingestion Pipeline — Orchestrator

This is a semi-automated pipeline. Steps 01 (harvest) and 02 (parse) require
agent involvement because they use LLM synthesis to produce structured vault records.
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))


def print_status():
    print("--- Intelligence Ingestion Pipeline ---")
    print()
    print("Stage 01: harvest     [AUTOMATED]")
    print("  → Walk intelligence records, refresh stale sources by system")
    print("  → Script: python3 skills/intelligence/01_harvest.py")
    print()
    print("Stage 02: parse       [AGENT-ASSISTED]")
    print("  → Apply LLM synthesis to extract structured vault intelligence records")
    print("  → Script: python3 skills/intelligence/02_parse.py <file_path>")
    print()
    print("Stage 03: scan_orphans [AUTOMATED]")
    print("  → Verify all source files have matching .md records; list any gaps")
    print("  → Script: python3 skills/intelligence/03_scan_orphans.py")
    print("         or: python3 skills/intelligence/run.py --scan")
    print()
    print("Schema: skills/intelligence/schemas/source-to-intelligence-prompt.md")


def main():
    args = sys.argv[1:]

    if not args:
        print_status()
        return

    if args[0] == "--scan":
        subprocess.run(["python3", os.path.join(SCRIPT_DIR, "03_scan_orphans.py")], check=True)
        return

    if args[0] == "--harvest":
        cmd = ["python3", os.path.join(SCRIPT_DIR, "01_harvest.py")]
        if "--force" in args:
            cmd.append("--force")
        subprocess.run(cmd, check=True)
        return

    # Treat first arg as file path → run parse step
    file_path = args[0]
    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "02_parse.py"), file_path], check=True)


if __name__ == "__main__":
    main()
