#!/usr/bin/env python3
import json
import os
import re
import subprocess
from collections import defaultdict
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CHANGELOG_PATH = os.path.join(ROOT_DIR, "changelog.md")
SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
VAULT_CSS = os.path.join(SKILLS_DIR, "styles", "vault.css")
DETAILED_REPORT_DIR = os.path.join(ROOT_DIR, "orchestration", "pipelines", "outputs", "dream", "reports")

def load_css():
    if os.path.exists(VAULT_CSS):
        with open(VAULT_CSS, "r") as f:
            return f.read()
    return "body { font-family: sans-serif; padding: 2rem; background: #0f172a; color: #f8fafc; }"

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
    uncommitted = len(git_changes)

    if unreleased_count == 0 and uncommitted > 0:
        summary = f"Version {current_version} is active, but you have {uncommitted} modified file(s) that need to be documented."
    elif unreleased_count > 0:
        summary = f"Currently drafting {unreleased_count} unreleased update(s) for the next version. Git shows {uncommitted} modified files."
    else:
        summary = f"Version {current_version} is cleanly published with no outstanding changes."

    group_counts = defaultdict(int)
    for line in git_changes:
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            filepath = parts[1]
            path_parts = filepath.split('/')
            group = path_parts[0] + "/" if len(path_parts) > 1 else "/"
            group_counts[group] += 1

    findings = [
        f"Current Version: v{current_version}",
        f"Unreleased Updates Logged: {unreleased_count}",
        f"Undocumented File Changes: {uncommitted}"
    ]

    if group_counts:
        breakdown = ", ".join([f"{count} in {path}" for path, count in sorted(group_counts.items(), key=lambda x: x[1], reverse=True)])
        findings.append(f"Change locations: {breakdown}")
        
        # Generate detailed report
        os.makedirs(DETAILED_REPORT_DIR, exist_ok=True)
        css = load_css()
        
        # Markdown version
        md_path = os.path.join(DETAILED_REPORT_DIR, "orchestration-changelog.md")
        with open(md_path, "w") as mf:
            mf.write(f"# Detailed Changelog Status — {datetime.now().strftime('%Y-%m-%d')}\n\n")
            mf.write(f"## Undocumented Files\n\n")
            for line in git_changes:
                mf.write(f"- `{line}`\n")
                
        # HTML version
        html_path = os.path.join(DETAILED_REPORT_DIR, "orchestration-changelog.html")
        with open(html_path, "w") as hf:
            hf.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>{css}</style>
</head>
<body class="gazette-body">
<div class="container">
<h1>Detailed Changelog Status — {datetime.now().strftime('%Y-%m-%d')}</h1>
<div class="lede">
    <p><strong>Total Modifications:</strong> {uncommitted} files waiting to be documented.</p>
</div>
''')
            # Group by directories for the UI
            grouped_files = defaultdict(list)
            for line in git_changes:
                parts = line.strip().split(maxsplit=1)
                filepath = parts[1] if len(parts) == 2 else line
                path_parts = filepath.split('/')
                group = path_parts[0] + "/" if len(path_parts) > 1 else "/"
                grouped_files[group].append(line)
                
            for group_name in sorted(grouped_files.keys()):
                files = grouped_files[group_name]
                hf.write(f'<div class="column" style="border-left-color:#f59e0b; margin-bottom: 2rem;">\n')
                hf.write(f'  <h3>📁 {group_name} ({len(files)})</h3>\n')
                hf.write(f'  <pre style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 4px; overflow-x: auto;">\n')
                for f in files:
                    hf.write(f"{f}\n")
                hf.write(f'  </pre>\n')
                hf.write(f'</div>\n')

            hf.write('<footer class="vault-footer">End of Detailed Report</footer>\n')
            hf.write("</div>\n</body></html>")

        findings.append("Full Report: [View Details](reports/orchestration-changelog.md)")

    envelope = {
        "skill": "orchestration/changelog",
        "preferred_agent": "Changelog Auditor (Yukon Cornelius)",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "warn" if (uncommitted > 0 and unreleased_count == 0) else "ok",
        "summary": summary,
        "findings": findings,
        "flags": []
    }
    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
