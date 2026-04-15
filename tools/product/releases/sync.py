#!/usr/bin/env python3
import os
import json
import glob
import re
from datetime import datetime

# Standard Vault Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PROJECTS_BASE_DIR = os.path.join(REPO_ROOT, "intelligence/product/roadmap/projects")
RELEASE_DIR = os.path.join(REPO_ROOT, "intelligence/product/releases")

def normalize_date(date_str):
    """Convert various date formats to YYYY-MM-DD."""
    date_str = date_str.split('T')[0].strip() # Handle ISO strings
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str # Return as is if no match

def parse_project_file(filepath):
    """Extract metadata from a project intelligence markdown file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception:
        return None

    metadata = {}
    
    name_match = re.search(r"^# (.*)", content)
    if name_match:
        metadata['name'] = name_match.group(1)

    jira_match = re.search(r"- \*\*Jira Link:\*\* (.*)", content)
    if jira_match:
        metadata['jira_link'] = jira_match.group(1)

    dates = []
    # 1. Check GA field
    ga_match = re.search(r"- \*\*GA:\*\* (.*)", content)
    if ga_match and ga_match.group(1).lower() != 'null':
        dates.append(normalize_date(ga_match.group(1)))

    # 2. Check Release Date(s) field
    release_dates_match = re.search(r"- \*\*Release Date\(s\):\*\* (.*)", content)
    if release_dates_match and release_dates_match.group(1).lower() != 'null':
        for d in release_dates_match.group(1).split(','):
            dates.append(normalize_date(d))
    
    metadata['release_dates'] = list(set(dates)) # dedupe
    return metadata

def sync():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Product Release Sync (Coordination)")
    
    if not os.path.exists(PROJECTS_BASE_DIR):
        print(f"❌ Projects directory not found: {PROJECTS_BASE_DIR}")
        return

    os.makedirs(RELEASE_DIR, exist_ok=True)
    
    project_files = glob.glob(os.path.join(PROJECTS_BASE_DIR, "**/*.md"), recursive=True)
    project_files = [f for f in project_files if os.path.basename(f) != "index.md"]
    print(f"  Scanning {len(project_files)} project records...")

    releases = {} # mapping date -> list of projects

    for fpath in project_files:
        meta = parse_project_file(fpath)
        if not meta: continue
        dates = meta.get('release_dates', [])
        for d in dates:
            if d not in releases:
                releases[d] = []
            # Store relative path from intelligence/product/roadmap/projects
            rel_path = os.path.relpath(fpath, PROJECTS_BASE_DIR)
            releases[d].append({
                'name': meta.get('name'),
                'rel_path': rel_path,
                'jira': meta.get('jira_link')
            })

    print(f"  Found {len(releases)} unique release dates.")

    # Sort dates and generate/update release intelligence
    for date, projects in sorted(releases.items()):
        # Create a safe filename (already normalized to YYYY-MM-DD by parse_project_file)
        filepath = os.path.join(RELEASE_DIR, f"{date}-release.md")
        
        content = f"# Release: {date}\n\n"
        content += f"- **Target Date:** {date}\n"
        content += "- **Status:** Synced\n"
        content += "- **Theme:** Coordination Snapshot\n\n"
        
        content += "## Linked Projects\n"
        for p in projects:
            content += f"- [**{p['name']}**](../roadmap/projects/{p['rel_path']})\n"
        
        content += "\n## Scope Status (Jira Alignment)\n"
        content += "*Note: Jira Fix Version extraction requires ATLASSIAN_API_TOKEN. Currently mapped via Project Metadata.*\n"
        
        content += "\n## Alignment Risks\n"
        content += "- [ ] **Schedule Slip**: Project target matches release date?\n"
        content += "- [ ] **Orphaned Scope**: Are there non-mapped epics in this release?\n"

        # Overwrite or update
        with open(filepath, 'w') as out:
            out.write(content)
        print(f"  ✅ Written: {os.path.basename(filepath)}")

    # Update Index.md
    index_path = os.path.join(RELEASE_DIR, "index.md")
    index_content = "# Product Release Index\n\n"
    index_content += "> **Domain:** Execution Coordination\n"
    index_content += "> **Purpose:** Tracking Jira Fix Versions against tactical project status and strategic OKRs.\n"
    index_content += f"> **Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    index_content += "## Upcoming Releases\n\n"
    index_content += "| Release | Date | Status | Health |\n"
    index_content += "| :--- | :--- | :--- | :--- |\n"
    
    # Sort by date for the index table
    for date, projects in sorted(releases.items()):
        index_content += f"| [{date}]({date}-release.md) | {date} | Synced | 🟢 Healthy |\n"

    index_content += "\n## Alignment Governance\n"
    index_content += "- **Red (Off-Track):** Project stage is behind Release readiness.\n"
    index_content += "- **Yellow (Risk):** Mismatched Jira epics or orphaned scope.\n"
    index_content += "- **Green (Aligned):** Project and Jira tickets match.\n"
    index_content += "\n## Navigation\n"
    index_content += "- [**Product Roadmap Root**](../roadmap/index.md)\n"
    index_content += "- [**Tactical Projects**](../roadmap/projects/index.md)\n"

    with open(index_path, 'w') as out:
        out.write(index_content)
    print(f"  ✅ Updated: index.md")

if __name__ == "__main__":
    sync()
