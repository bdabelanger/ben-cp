#!/usr/bin/env python3
"""agents.py — Monitor role compliance and tone across repo files."""
import os, json, re
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'archived', 'complete', 'reports'}

# Phrases that suggest generic AI assistant bleed-through
AI_PHRASES = [
    r'as an ai (model|assistant|language model)',
    r'happy to help',
    r"i('m| am) just an ai",
    r'i cannot (actually|truly)',
    r'as a large language model',
    r'i don\'t have (personal|real|actual) (experience|feelings|opinions)',
]

# Code agent should not be the author of architecture/design decisions
CODE_ARCH_PATTERN = re.compile(
    r'^\s*[\*_\-]*\b(Prepared by|Agent)\b[\*_\-]*\s*[:\-]\s*Code.*?(architecture|repo structure|SOP design|new skill)',
    re.IGNORECASE | re.MULTILINE | re.DOTALL
)

def strip_code_blocks(content):
    return re.sub(r'```.*?```', '', content, flags=re.DOTALL)

def collect_md_files():
    files = []
    for root, dirs, fs in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in fs:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))
    return files

def audit_file(path):
    rel = os.path.relpath(path, REPO_ROOT)
    issues = []
    try:
        with open(path, errors='replace') as f:
            content = strip_code_blocks(f.read())
    except OSError:
        return issues

    # AI assistant phrases
    for pattern in AI_PHRASES:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({"file": rel, "issue": "ai_assistant_phrase", "pattern": pattern})

    # Code making architecture decisions
    if CODE_ARCH_PATTERN.search(content):
        issues.append({"file": rel, "issue": "code_agent_architecture_decision"})

    # Skip AGENTS.md as it defines the standard
    # Skip index.md files to avoid template/registry false positives
    if rel == 'AGENTS.md' or rel.endswith('index.md'):
        return issues

    # Unknown agent in Prepared by / Agent lines
    # Requirement: Exactly one of [Code, Cowork, Local] followed by (Model Name)
    prepared = re.findall(r'^\s*[\*_\-]*\b(Prepared by|Agent)\b[\*_\-]*\s*[:]\s*([^\n]+)', content, re.IGNORECASE | re.MULTILINE)
    known_agents = {'code', 'cowork', 'local'}
    
    for author_key, author_val in prepared:
        val = author_val.strip().strip('*').strip()
        # Check for Name (Model) format
        match = re.match(r'^([\w\s]+)\s*\(([^)]+)\)', val)
        if not match:
            issues.append({
                "file": rel, 
                "issue": "invalid_agent_format", 
                "value": author_val.strip(),
                "expected": "Name (Model)"
            })
            continue
            
        name = match.group(1).strip().lower()
        if name not in known_agents:
            issues.append({
                "file": rel, 
                "issue": "unknown_agent", 
                "value": name,
                "allowed": sorted(list(known_agents))
            })

    return issues

def run():
    all_issues = []
    files = collect_md_files()
    for path in files:
        all_issues.extend(audit_file(path))

    report = {
        "sensor": "agents",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": len(files),
            "issues_found": len(all_issues),
        },
        "issues": all_issues,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'agents_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ agents → {out}")
    return report

if __name__ == '__main__':
    run()
