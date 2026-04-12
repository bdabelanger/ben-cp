# Audit Procedure: Access Domain

> **Owner:** Roz (Access Auditor)

## Requirements
- [ ] No credential patterns (keys, tokens) in session logs.
- [ ] Check `outputs/access/` for report consistency.
- [ ] Flag any multi-agent session where a PII-scrub was not verified.
- [ ] **Supply Chain Audit:** Scan `node_modules/` for extraneous packages (not in `package.json`).
- [ ] **Resource Audit:** Flag any file >1MB that is not a database.

## Operating Procedure

### Pre-Flight
1. Read `AGENTS.md` — confirm role definitions and authorized directory boundaries.
2. Read latest changelog skill report in `skills/orchestration/changelog/outputs/reports/` — specifically Check 9.
3. Read root `changelog.md` and relevant skill changelogs for the audit period.

### Step 1 — Synthesis
For each flag in Check 9, cross-reference against changelog entries and git log. For each violation ask:
- What was the agent doing in that directory? Did they create, modify, or delete files, or just read?
- Was there an approved plan and task list before writes occurred?
- explicitly flag overly broad tool permission grants (e.g. `Bash(*)`) or orphaned project entries referencing deleted repos.

### Step 2 — Separation Policy Scan (ALWAYS RUN)
1. Read `skills/shared/separation-policy.md` § Known Migration Debt.
2. Walk `skills/` and flag any violation of the four-layer architecture (scripts, data, or logs in skill subdirectories) that is not already tracked in the debt list.
3. Scan for stale `notes.md` files in `skills/` subdirectories.

### Step 3 — Deletion & Overwrite Watch (ALWAYS RUN)
Scan all agent outputs, skill instructions, and handoffs for any language advocating:
- Deleting files (other than ephemeral `notes.md` cleanup).
- Overwriting existing files with `write_file` where `edit_file` was appropriate.
- Force-pushing or destructive git operations.
**Flag every instance as a P1 violation.**

### Step 4 — Supply Chain & Resource Audit
1. **Extraneous Module Check**: Flag any directory in `node_modules/` top-level that is not a dependency or devDependency in `package.json`.
2. **Resource Bloat Check**: Flag any file >1MB that is not a `.json` database or `.sqlite` file.
