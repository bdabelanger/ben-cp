#!/usr/bin/env python3
"""scripts.py — Validate script health across all skills.

Checks that:
1. Every skill directory that has a run.py can be parsed (no syntax errors)
2. Every script referenced inside a run.py or SKILL.md actually exists on disk
3. No skill run.py is a stub (detected by placeholder strings)
"""
import os, json, re, ast
from datetime import datetime

VAULT_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SKILLS_DIR   = os.path.join(VAULT_ROOT, 'skills')
OUTPUTS_DIR  = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'complete', 'archive', 'archived'}

# Strings that indicate a script is a stub with no real implementation
STUB_SIGNALS = [
    'placeholder',
    'pass  #',
    '# TODO',
    'print("✅',   # bare success print with no logic above it
    'Reconstructed',
]

# Pattern to find script filenames referenced in strings (e.g. "02_parse.py", "scripts/run.py")
# Only match clean paths: optional path prefix + filename, no spaces, no template vars, no special chars
SCRIPT_REF_PATTERN = re.compile(r'["\']([a-zA-Z0-9_\-/]+\.py)["\']')


def collect_skill_dirs():
    """Return all first-level skill directories."""
    dirs = []
    try:
        for entry in os.scandir(SKILLS_DIR):
            if entry.is_dir() and not entry.name.startswith('.') and entry.name not in SKIP_DIRS:
                dirs.append(entry.path)
    except OSError:
        pass
    return dirs


def check_syntax(filepath):
    """Return None if syntax OK, error string if not."""
    try:
        with open(filepath, errors='replace') as f:
            source = f.read()
        ast.parse(source)
        return None
    except SyntaxError as e:
        return f"SyntaxError line {e.lineno}: {e.msg}"
    except OSError as e:
        return str(e)


def is_stub(filepath):
    """Return True if the script looks like a placeholder stub."""
    try:
        with open(filepath, errors='replace') as f:
            source = f.read()
    except OSError:
        return False
    # A stub has very few non-empty, non-comment lines of actual logic
    logic_lines = [
        l for l in source.splitlines()
        if l.strip() and not l.strip().startswith('#')
        and not l.strip().startswith('"""')
        and not l.strip().startswith("'''")
    ]
    if len(logic_lines) < 8:
        return True
    for signal in STUB_SIGNALS:
        if signal.lower() in source.lower():
            return True
    return False


def find_referenced_scripts(filepath, base_dir):
    """Find .py filenames referenced as string literals and check they exist."""
    missing = []
    try:
        with open(filepath, errors='replace') as f:
            source = f.read()
    except OSError:
        return missing
    for m in SCRIPT_REF_PATTERN.finditer(source):
        ref = m.group(1)
        # Skip self-references and sensor names
        if ref == os.path.basename(filepath):
            continue
        # Resolve relative to the script's directory, base_dir, or base_dir/scripts/
        candidate = os.path.join(os.path.dirname(filepath), ref)
        if not os.path.exists(candidate):
            candidate2 = os.path.join(base_dir, ref)
            if not os.path.exists(candidate2):
                candidate3 = os.path.join(base_dir, 'scripts', ref)
                if not os.path.exists(candidate3):
                    missing.append({
                        "ref": ref,
                        "resolved": os.path.relpath(candidate, VAULT_ROOT),
                    })
    return missing


def run():
    findings = []
    skills_checked = 0

    for skill_dir in collect_skill_dirs():
        skill_name = os.path.basename(skill_dir)
        run_py = os.path.join(skill_dir, 'run.py')

        if not os.path.exists(run_py):
            continue

        skills_checked += 1
        rel = os.path.relpath(run_py, VAULT_ROOT)

        # 1. Syntax check
        err = check_syntax(run_py)
        if err:
            findings.append({
                "skill": skill_name,
                "file": rel,
                "issue": "syntax_error",
                "detail": err,
                "severity": "ERROR",
            })

        # 2. Stub detection
        if is_stub(run_py):
            findings.append({
                "skill": skill_name,
                "file": rel,
                "issue": "stub",
                "detail": "run.py appears to be a placeholder with no real implementation",
                "severity": "WARN",
            })

        # 3. Referenced scripts that don't exist
        missing = find_referenced_scripts(run_py, skill_dir)
        for m in missing:
            findings.append({
                "skill": skill_name,
                "file": rel,
                "issue": "missing_script_ref",
                "detail": f"References {m['ref']} but {m['resolved']} not found",
                "severity": "WARN",
            })

        # Also check scripts/ subdirectory if present
        scripts_dir = os.path.join(skill_dir, 'scripts')
        if os.path.isdir(scripts_dir):
            for entry in os.scandir(scripts_dir):
                if not entry.name.endswith('.py') or entry.name.startswith('_'):
                    continue
                srel = os.path.relpath(entry.path, VAULT_ROOT)
                serr = check_syntax(entry.path)
                if serr:
                    findings.append({
                        "skill": skill_name,
                        "file": srel,
                        "issue": "syntax_error",
                        "detail": serr,
                        "severity": "ERROR",
                    })
                missing = find_referenced_scripts(entry.path, skill_dir)
                for m in missing:
                    findings.append({
                        "skill": skill_name,
                        "file": srel,
                        "issue": "missing_script_ref",
                        "detail": f"References {m['ref']} but {m['resolved']} not found",
                        "severity": "WARN",
                    })

    errors = sum(1 for f in findings if f["severity"] == "ERROR")
    warnings = sum(1 for f in findings if f["severity"] == "WARN")

    report = {
        "sensor": "scripts",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "skills_checked": skills_checked,
            "total_findings": len(findings),
            "errors": errors,
            "warnings": warnings,
        },
        "findings": findings,
    }

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'scripts_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ scripts → {out}")
    return report


if __name__ == '__main__':
    report = run()
    findings = report["findings"]
    if findings:
        print(f"\n{'ERROR' if report['summary']['errors'] else '⚠️ '} {len(findings)} finding(s):")
        for f in findings:
            icon = "🔴" if f["severity"] == "ERROR" else "🟡"
            print(f"  {icon} [{f['skill']}] {f['file']} — {f['issue']}: {f['detail']}")
    else:
        print("✅ All scripts healthy.")
