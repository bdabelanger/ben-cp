# Claude Code Implementation Plan: Fix skill-builder Subdirectory index.md Files

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Source:** Vault Auditor report `reports/knowledge-report-2026-04-08.md` flags 3.1, 3.2, 3.3
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-09**

`skills/skill-builder/mappings/index.md` and `skills/skill-builder/styles/index.md` created as proper directory TOCs. `skills/skill-builder/rules/` confirmed empty and removed via `rmdir` (no git-tracked files, so `git rm -r` had nothing to remove; `rmdir` completed cleanly).

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

Three subdirectories under `skills/skill-builder/` are missing `index.md` files:
- `mappings/` — contains `status_mapping.md`, no index
- `styles/` — contains `emoji_key.md`, no index
- `rules/` — empty directory, no index

Decision needed on `rules/`: either seed with a stub index or remove entirely.
Human user's preference: **remove if empty, don't create empty structure**.

---

## Execution Order

1. **Task 1** — Audit all three subdirectories
2. **Task 2** — Create `mappings/index.md`
3. **Task 3** — Create `styles/index.md`
4. **Task 4** — Handle `rules/` directory
5. **Task 5** — Final audit and completion report

---

## Task 1: Audit

1. `list_directory` on `skills/skill-builder/mappings/`
2. `list_directory` on `skills/skill-builder/styles/`
3. `list_directory` on `skills/skill-builder/rules/`

Confirm file counts before proceeding. Report if anything unexpected is found.

---

## Task 2: Create mappings/index.md

**Check first:** confirm `skills/skill-builder/mappings/index.md` does not exist.

```markdown
# Skill Builder: Mappings

> Reusable business logic and transformation rules for skill outputs.
> Last updated: [YYYY-MM-DD]

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `status_mapping.md` | Status string → Green/Yellow/Red mapping logic |
```

---

## Task 3: Create styles/index.md

**Check first:** confirm `skills/skill-builder/styles/index.md` does not exist.

```markdown
# Skill Builder: Styles

> Visual presentation standards — emoji keys, progress bars, formatting.
> Last updated: [YYYY-MM-DD]

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `emoji_key.md` | Standard emoji usage across all skill outputs |
```

---

## Task 4: Handle rules/ Directory

`list_directory` on `skills/skill-builder/rules/`.

- **If empty:** remove it with `git rm -r skills/skill-builder/rules/`
- **If it has files:** create a `rules/index.md` TOC listing those files and report to Ben

---

## Task 5: Final Audit and Completion Report

1. Read `skills/skill-builder/mappings/index.md` — confirm present
2. Read `skills/skill-builder/styles/index.md` — confirm present
3. Confirm `rules/` disposition (removed or indexed)
4. Write changelog entry using `write_changelog_entry`

```
## Completion Report

**Files created:**
- skills/skill-builder/mappings/index.md
- skills/skill-builder/styles/index.md

**Files deleted (if empty):**
- skills/skill-builder/rules/ (empty directory)

**Flags for Ben:** [anything unexpected]
```
