#!/usr/bin/env python3
import json
import os
import re
import subprocess
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CHANGELOG_PATH = os.path.join(ROOT_DIR, "changelog.md")

def get_git_status():
    try:
        res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=ROOT_DIR)
        lines = res.stdout.strip().split("\n")
        return [l.strip() for l in lines if l.strip()]
    except:
        return []

def main():
    if not os.path.exists(CHANGELOG_PATH):
        print(json.dumps({"status": "error", "summary": "Root changelog missing."}))
        return

    with open(CHANGELOG_PATH, "r") as f:
        content = f.read()
    
    unreleased_match = re.search(r"## \[Unreleased\](.*?)(?=\n## \[|\Z)", content, re.DOTALL)
    unreleased_count = 0
    if unreleased_match:
        entries = re.findall(r"\n## ", unreleased_match.group(1))
        unreleased_count = len(entries)
    
    version_match = re.search(r"## \[(\d+)\.(\d+)\.(\d+)\]", content)
    current_version = version_match.group(1) + "." + version_match.group(2) + "." + version_match.group(3) if version_match else "0.0.0"

    git_changes = get_git_status()
    git_msg = f"Git reports {len(git_changes)} uncommitted file(s)." if git_changes else "Git workspace is clean."

    envelope = {
        "skill": "orchestration/changelog",
        "preferred_agent": "Changelog Auditor (Yukon Cornelius)",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "ok",
        "summary": f"Changelog Audit: v{current_version}. {unreleased_count} [Unreleased] entries. {git_msg}",
        "findings": [
            f"Latest published version: {current_version}",
            f"Active session count in queue: {unreleased_count}",
            f"Pending technical changes: {len(git_changes)}"
        ],
        "flags": []
    }
    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
