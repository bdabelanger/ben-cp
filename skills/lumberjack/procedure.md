# Lumberjack Procedure

> **PURPOSE:** Audit changelogs for accuracy and completeness.
> Run after significant sessions or handoff executions.
> Flag only — never edit changelogs directly during this run.

---

## Inputs

Before running, collect:
1. Root `changelog.md` — full read
2. All `skills/*/changelog.md` files touched this session
3. `handoff/complete/` — list of recently completed handoffs
4. **Git log** — the authoritative record of what actually changed:
   ```
   git log --oneline --since="7 days ago"
   git diff HEAD~N --name-only   # files actually touched
   git show --stat HEAD          # last commit detail
   ```
   Use `git log` and `git diff` to build the ground truth before reading any changelog.
   Changelogs are validated against git — not the other way around.

---

## Check 1 — Missing Entries

**Question:** Was work done this session that has no changelog entry?

Steps:
1. Run `git log --oneline --since="[session date]"` and `git diff HEAD~N --name-only` to get the ground-truth file list
2. Cross-reference against changelog entries for that date
3. Flag any `skills/` subdirectory with modified files but no changelog entry
4. Flag any session (date with commits) with no root changelog entry
5. Flag any committed file whose change isn't described anywhere in the changelog

**Flag format:**
```
Missing: [skill/] — [description of work done with no entry]
```

---

## Check 2 — Phantom Entries

**Question:** Do entries describe things that no longer exist or never existed?

Steps:
1. For each path, tool name, or directory referenced in a recent changelog entry:
   - Check if the file/dir exists
   - Check if the tool name matches what's in the code
2. Flag mismatches

Common phantoms:
- Directories created per the entry but not on disk
- Tool names that were later renamed or removed
- `reports/archive/` or other dirs listed as created but absent

**Flag format:**
```
Phantom: [entry version] — "[quoted claim]" — [what's actually true]
```

---

## Check 3 — Stale Next Tasks

**Question:** Do any changelog entries have Next Tasks that were already completed in a later entry?

Steps:
1. Read Next Tasks in each entry
2. Check if a later entry covers that work
3. Flag — stale Next Tasks mislead agents loading context

**Flag format:**
```
Stale Next Task: [entry version] — "[task text]" — completed in [later version]
```

---

## Check 4 — Inaccurate Counts or Names

**Question:** Are numbers, tool names, or paths stated accurately?

Steps:
1. For entries that list counts ("3 new tools", "9 files", "4 unexposed functions"):
   - Verify the count against the actual files/code
2. For entries referencing old names (pre-rename):
   - Note whether the entry is historical (accurate at time of writing) or actively misleading
3. Flag inaccuracies that could confuse agents

**Flag format:**
```
Inaccurate: [entry version] — "[wrong claim]" — actual: [correct value]
```

---

## Check 5 — Subdirectory ↔ Root Alignment

**Question:** Does every subdirectory changelog entry have a root pointer, and vice versa?

Steps:
1. For each `## [X.Y.Z]` root entry with a `**Detail logs:**` section:
   - Confirm each listed subdirectory changelog exists and has an entry for that date
2. For each subdirectory changelog entry:
   - Confirm a root entry references it

**Flag format:**
```
Alignment gap: root [X.Y.Z] points to skills/[name]/changelog.md but no entry exists there for [date]
Alignment gap: skills/[name]/changelog.md has [date] entry with no root pointer
```

---

## Check 6 — Handoff Cross-Reference

**Question:** Do completed handoffs have changelog entries, and do changelog entries reference their handoff?

Steps:
1. List all files in `handoff/complete/`
2. For each: check if any root changelog entry has `**Handoff:** handoff/complete/[filename]`
3. For root entries that should reference a handoff (session was handoff-driven): check the field is present
4. Also check: do files in `handoff/complete/` follow the naming convention (ending in `-COMPLETE.md`)?

**Flag format:**
```
Missing handoff ref: root [X.Y.Z] was handoff-driven but has no Handoff field
Unlogged handoff: handoff/complete/[filename] — no root changelog entry references it
Bad naming: handoff/complete/[filename] — missing -COMPLETE suffix
```

---

## Check 7 — Version Sequence

**Question:** Are root changelog versions sequential with no gaps or duplicates?

Steps:
1. Extract all `## [X.Y.Z]` versions from root `changelog.md`
2. Verify:
   - No duplicate version numbers
   - No version skipped (e.g., 1.2.0 → 1.4.0 with no 1.3.0)
   - Bump type matches what happened (patch for routine, minor for structural, major for rearchitecture)

**Flag format:**
```
Version gap: [X.Y.Z] skipped between [A.B.C] and [D.E.F]
Duplicate version: [X.Y.Z] appears twice
Wrong bump: [X.Y.Z] — [description suggests minor/major but bumped as patch]
```

---

## Output

Write a report to `skills/lumberjack/reports/lumberjack-report-YYYY-MM-DD.md` using the template:

```markdown
# Lumberjack Report — YYYY-MM-DD

> **Run by:** [Agent]
> **Scope:** [which changelogs were audited]

## Summary
| Check | Result |
| :--- | :--- |
| 1 — Missing entries | ✅ Clean / ⚠️ N flags |
...

## Flags
[One section per flag, with suggested fix]

## Suggested Actions
[Handoff recommendations if fixes are needed]
```

---

## Rules

- **Flag only** — do not edit changelogs during this run
- **Historical entries are not wrong** — a 1.1.0 entry that references `wrap-up/` was accurate at the time; flag only if it's actively misleading agents
- **Write a handoff for fixes** — don't fix inline; Ben reviews first
