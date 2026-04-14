# Claude Code Implementation Plan: Fix AGENTS.md and skills/index.md

> **Prepared by:** Claude (Cowork) via knowledge skill run (2026-04-12)
> **Assigned to:** Claude Code
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1 — agent navigation broken
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-12.md`
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-12**

Synchronized AGENTS.md and the skills index with the post-cleanup vault structure, ensuring agents are no longer misrouted to defunct paths.

**Changelog:** (see root changelog.md)


---

## Context
The knowledge skill run on 2026-04-12 identified that `AGENTS.md` and `skills/index.md` are both outdated following today's session changes. Agents reading these files will be misrouted — wrong artifact names, defunct skill paths, and stale role references. These are P1 because they affect agent navigation on every session start.

---

## Execution Order

1. **Update `AGENTS.md` Session Pattern** — fix `notes.md` reference
2. **Update `AGENTS.md` vault structure diagram** — reflect current `skills/` layout
3. **Update `AGENTS.md` "Who Are You?" table** — fix Roz dispatch entry
4. **Rewrite `skills/index.md`** — reflect current directory structure
5. Write changelog and mark complete

---

## Task 1: Update AGENTS.md Session Pattern (step 3)

In `AGENTS.md`, find the Session Pattern block. Step 3 currently reads:
> "If writes are intended, create/update `quartermaster.md` in the target `skills/` subdirectory using the template at `skills/pmm/quartermaster_template.md`."

Update to:
> "If writes are intended, create/update `notes.md` in the target `skills/` subdirectory using the template at `skills/pmm/report.md`."

Also update step 6 cleanup line from "Delete the `quartermaster.md` file" to "Delete the `notes.md` file."

---

## Task 2: Update AGENTS.md Vault Structure Diagram

The diagram currently shows:
```
├── skills/
    ├── crypt-keeper/
    ├── lumberjack/
    ├── roz/
    └── robert/
```

Update to reflect actual current structure:
```
├── skills/
    ├── access/        ← permission & access auditing
    ├── casebook/
    ├── changelog/     ← changelog auditing
    ├── dream/         ← nightly Digest orchestration
    ├── handoff/
    ├── input/
    ├── knowledge/     ← vault quality watchdog
    ├── okr-reporting/
    ├── pmm/           ← session planning (Strategic PM convention)
    ├── predict/
    ├── project-status-reports/
    ├── rovo/
    ├── skill-builder/
    └── synthesis/
```

Also update file placement table — `Vault Auditor watchdog` entry points to `skills/knowledge/`, and `Roz audit reports` entry points to `skills/access/outputs/reports/`. Confirm these are already correct and update any remaining `crypt-keeper/` or `lumberjack/` path references.

---

## Task 3: Update AGENTS.md "Who Are You?" Table

Current entry:
```
| Roz | agents/roz.md | Permission & Access Auditor — nightly "Violation!" and "Oops!" reports |
```

Update to:
```
| Access Auditor | skills/access/SKILL.md | Permission & Access Auditor — nightly violation and oops reports |
```

---

## Task 4: Rewrite skills/index.md

Current `skills/index.md` (last updated 2026-04-08) lists defunct directories and is missing most current skills. Rewrite to:

```markdown
# Skills Index

> Master index for all skills in this vault.
> Last updated: 2026-04-12

---

## 📂 Skills

| Directory | Purpose |
| :--- | :--- |
| `access/` | Permission & access auditing — nightly violation and oops reports |
| `casebook/` | Casebook reference docs, Reveal BI, Admin MCP, Subscriptions MCP |
| `changelog/` | Changelog auditing — accuracy, completeness, git cross-reference checks |
| `dream/` | Nightly Digest orchestration — runs all skill agents and compiles output |
| `handoff/` | Cross-agent handoff protocol and file format |
| `input/` | Session input capture and captain's log |
| `knowledge/` | Weekly vault quality watchdog — 8 checks, flags only |
| `okr-reporting/` | Platform OKR measurement runbooks and KR SOPs |
| `pmm/` | Session planning (Strategic PM convention) — ephemeral notes.md artifacts |
| `predict/` | Forward-looking analysis skill (in development) |
| `project-status-reports/` | Platform Weekly Status Report pipeline and runbook |
| `rovo/` | Rovo issue management SOP |
| `skill-builder/` | Reusable standards — emoji keys, status mappings |
| `synthesis/` | Cross-skill synthesis and diff checking |
```

---

## Task 5: Changelog + Completion

Write changelog entries (subdirectory first at `skills/knowledge/changelog.md`, then root `changelog.md`), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Read `AGENTS.md` fully before editing — use targeted edits, not full rewrites where possible.
- Do not rename or move `agents/roz.md` in this task — that is handled in the P2 handoff.
- Character names are not used in skill references outside of `character.md` files.
