#!/usr/bin/env python3
import json
import os
import glob
import re
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
TODAY_STR = datetime.now().strftime("%Y-%m-%d")

def find_notes_files():
    """Find all notes.md files in the repository."""
    return glob.glob(os.path.join(REPO_ROOT, "**", "notes.md"), recursive=True)

def parse_today_notes(file_path):
    """Parse a notes.md file for entries from today using multiple formats."""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r") as f:
        content = f.read()

    titles = []
    
    # Format A: ### [YYYY-MM-DD] Title
    # Capture everything after the date on the same line
    header_matches = re.findall(rf'### \[{re.escape(TODAY_STR)}\](.*?)(?:\n|$)', content)
    for m in header_matches:
        t = m.strip()
        if t: titles.append(t)

    # Format B: > **Date:** YYYY-MM-DD entries
    # Often followed by a title or status in subsequent lines
    # We'll look for the entry block containing today's date
    if f"> **Date:** {TODAY_STR}" in content:
        # Just grab a snippet of the line or the status as a "title"
        status_matches = re.findall(rf'> \*\*Date:\*\* {re.escape(TODAY_STR)}.*? \*\*Status:\*\* (.*?)(?:\n|$)', content, re.DOTALL)
        if status_matches:
            titles.append(f"Status update: {status_matches[0].strip()}")
        else:
            titles.append("Standardized data update")

    return list(set(titles)) # Deduplicate

def main():
    note_files = find_notes_files()
    activity = {} # domain: [titles]
    
    for nf in note_files:
        # Get domain name from path
        rel = os.path.relpath(nf, REPO_ROOT)
        parts = rel.split(os.sep)
        # Map legacy skills/ to intelligence/core/skills/ for domain clarity
        if len(parts) >= 4 and parts[0] == "intelligence" and parts[1] == "core" and parts[2] == "skills":
            domain = "/".join(parts[3:-1])
        elif len(parts) >= 3 and parts[0] == "skills":
            domain = "/".join(parts[1:-1])
        else:
            domain = os.path.dirname(rel)

        titles = parse_today_notes(nf)
        if titles:
            activity[domain] = titles

    total_entries = sum(len(t) for t in activity.values())
    active_domains = len(activity)

    summary = f"{total_entries} new entries across {active_domains} domain(s)"
    
    findings = []
    if activity:
        # Sort domains for consistent output
        for domain in sorted(activity.keys()):
            domain_titles = activity[domain]
            findings.append(f"{domain}: {'; '.join(domain_titles)}")
    else:
        findings.append("No note activity recorded in the vault today.")

    envelope = {
        "skill": "orchestration/notes",
        "preferred_agent": "Notes Auditor (Sea Shanty)",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "ok",
        "summary": summary,
        "findings": findings,
        "flags": []
    }

    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
