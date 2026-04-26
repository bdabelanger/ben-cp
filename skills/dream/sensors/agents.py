#!/usr/bin/env python3
"""agents.py — Monitor role compliance and tone across vault files."""
import os, json, re
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'archived', 'complete'}

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
    r'(Prepared by|Agent)\s*[:\-]\s*Code.*?(architecture|vault structure|SOP design|new skill)',
    re.IGNORECASE | re.DOTALL
)

def collect_md_files():
    files = []
    for root, dirs, fs in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in fs:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))
    return files

def audit_file(path):
    rel = os.path.relpath(path, VAULT_ROOT)
    issues = []
    try:
        with open(path, errors='replace') as f:
            content = f.read()
    except OSError:
        return issues

    # AI assistant phrases
    for pattern in AI_PHRASES:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({"file": rel, "issue": "ai_assistant_phrase", "pattern": pattern})

    # Code making architecture decisions
    if CODE_ARCH_PATTERN.search(content):
        issues.append({"file": rel, "issue": "code_agent_architecture_decision"})

    # Unknown agent in Prepared by
    prepared = re.findall(r'(?:Prepared by|Agent)\s*[:\-]\s*([^\n\(]+)', content, re.IGNORECASE)
    known_agents = {'code', 'cowork', 'local', 'human', 'ben', 'gemini', 'claude',
                    'antigravity', 'vault auditor', 'dispatch'}
    for author in prepared:
        name = author.strip().split('(')[0].strip().lower()
        if name and not any(k in name for k in known_agents):
            issues.append({"file": rel, "issue": "unknown_agent", "value": author.strip()})

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
