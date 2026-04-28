# Implementation Plan: Add Full Timestamp to Report Headers in All Pipelines

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

status/run.py line 81 and tasks/run.py lines 67, 122, 153 updated from '%Y-%m-%d' to '%Y-%m-%d %H:%M'. dream/run.py confirmed exempt — time already shown via time_str. All acceptance criteria met.

---

## Context

All report pipelines currently write date-only headers (e.g. `2026-04-27`). When multiple runs happen in a day it's impossible to tell which report is current without checking file metadata. Full timestamps should be recorded so agents and users can immediately see when a report was last run.

Affected files:
- `skills/status/run.py` — line 81 uses `strftime('%Y-%m-%d')`
- `skills/tasks/run.py` — lines 67, 122, 153 use `strftime('%Y-%m-%d')`

Note: `skills/dream/run.py` may also be affected — check and fix if so.

---

## Execution Steps

### Step 1 — Edit `skills/status/run.py`

**Old:**
```python
rf.write(f"# Detailed Project Status — {datetime.now().strftime('%Y-%m-%d')}\n\n")
```

**New:**
```python
rf.write(f"# Detailed Project Status — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
```

### Step 2 — Edit `skills/tasks/run.py`

Three occurrences of `datetime.now().strftime("%Y-%m-%d")` used in report headers. Replace all three with `datetime.now().strftime("%Y-%m-%d %H:%M")`:

- Line ~67: `_Last synced:` line in Asana section
- Line ~122: `_Last synced:` line in Jira section  
- Line ~153: `# Task Report —` title line

### Step 3 — Check `skills/dream/run.py`

Search for `strftime` usage in dream pipeline. Apply the same `%Y-%m-%d %H:%M` format to any report header or "last synced" lines.

### Step 4 — Verify
Run a quick sanity check:
```bash
grep -n "strftime" skills/status/run.py skills/tasks/run.py skills/dream/run.py
```
Confirm all header/title timestamps include time component.

### Step 5 — Changelog
Root `changelog.md` entry only (Handoff Exemption applies).

---

## Acceptance Criteria

- [ ] `status` report header includes time e.g. `2026-04-28 14:32`
- [ ] `tasks` report header and last synced lines include time
- [ ] `dream` pipeline checked and updated if applicable
- [ ] No `strftime('%Y-%m-%d')` remaining in report header/title lines across all three pipelines
- [ ] Root changelog entry written
