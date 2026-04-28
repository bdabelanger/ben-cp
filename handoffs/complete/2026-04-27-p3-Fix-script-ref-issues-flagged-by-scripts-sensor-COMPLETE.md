---
title: "Fix script reference issues flagged by scripts sensor"
type: handoff
priority: P3
status: ✅ COMPLETE
date: 2026-04-27
assigned_to: Code
---

# Fix Script Reference Issues Flagged by Scripts Sensor

## Context

The new `scripts` dream sensor (`skills/dream/sensors/scripts.py`) found 5 real issues
on its first run. All are stale or incorrect script references left behind by prior
restructuring (flatten of `skills/pipelines/` and the `asana` skill scaffold).

## Findings

```
[status] skills/status/run.py
  → References "full_run.py" — file does not exist at skills/status/full_run.py
  → Was renamed to skills/status/scripts/run.py during the flatten

[status] skills/status/scripts/run.py
  → References "skills/asana/run.py" as a string path
  → Resolves incorrectly relative to skills/status/scripts/ instead of REPO_ROOT
  → Should be an absolute path built from REPO_ROOT

[asana] skills/asana/run.py
  → References "01_fetch_projects.py", "02_fetch_tasks.py", "03_normalize.py"
  → These scripts live in skills/asana/scripts/ not skills/asana/
  → run.py is calling them without the scripts/ prefix
```

## Logic

### Fix 1 — skills/status/run.py

Find the reference to `full_run.py` and update it to point to `scripts/run.py`:

```python
# Before
subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "full_run.py")], ...)
# After
subprocess.run(["python3", os.path.join(SCRIPTS_DIR, "run.py")], ...)
```

### Fix 2 — skills/status/scripts/run.py

Find the string `"skills/asana/run.py"` and replace with an absolute path built from REPO_ROOT:

```python
# Before (approximate)
asana_run = "skills/asana/run.py"
# After
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
asana_run = os.path.join(REPO_ROOT, "skills", "asana", "run.py")
```

### Fix 3 — skills/asana/run.py

Check how `01_fetch_projects.py`, `02_fetch_tasks.py`, `03_normalize.py` are referenced.
Update each to resolve via the `scripts/` subdirectory:

```python
# Before
os.path.join(SCRIPT_DIR, "01_fetch_projects.py")
# After
os.path.join(SCRIPT_DIR, "scripts", "01_fetch_projects.py")
```

## Execution Steps

- [ ] 1. Read `skills/status/run.py` — find and fix the `full_run.py` reference
- [ ] 2. Read `skills/status/scripts/run.py` — find and fix the `skills/asana/run.py` string reference
- [ ] 3. Read `skills/asana/run.py` — fix the 3 script references to include `scripts/` prefix
- [ ] 4. Run `python3 skills/dream/sensors/scripts.py` — confirm 0 findings
- [ ] 5. Add changelog entry to `skills/changelog.md`

## Verification

`python3 skills/dream/sensors/scripts.py` reports 0 findings.
