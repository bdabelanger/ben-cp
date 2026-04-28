---
title: 'Claude Code Implementation Plan: Handoff Editability Rule'
type: handoff
domain: handoffs/complete
---


# Claude Code Implementation Plan: Handoff Editability Rule

> **Prepared by:** Claude (Cowork) (2026-04-10)
> **Repo root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1 — Corrects a rule ambiguity that blocks iterative handoff development.
> **v1.0**
> **STATUS**: ✅ COMPLETE

---

## Problem

Handoffs cannot currently be edited after creation. This is the wrong constraint — handoffs are living implementation plans, not historical records. The append-only / never-edit discipline belongs to `changelog.md` files only.

The confusion likely arose from changelog rules being applied too broadly across all repo documents.

---

## Correct Model

| File type | Edit rule | Rationale |
| :--- | :--- | :--- |
| `changelog.md` | Append-only — never edit past entries | Historical record; errors corrected in next entry |
| `handoff/*.md` (open) | **Fully editable** | Living plan — must be iterable as requirements evolve |
| `handoff/complete/*.md` | Never edit | Completed handoffs are historical record |

---

## Tasks for Claude Code

### 1. Update `skills/handoff/index.md`

Add an explicit section clarifying editability:

```
## Editability Rules

- **Open handoffs** (`handoff/*.md`) — fully editable. Iterate freely as plans evolve.
- **Completed handoffs** (`handoff/complete/*.md`) — never edit. Historical record only.
- **Changelogs** — append-only always. This rule does NOT extend to handoffs.
```

### 2. Update `AGENTS.md` — Handoff Check section

After step 4 ("If human user confirms, execute using the handoff protocol"), add:

```
> **Note:** Open handoffs are living documents — they may be edited and iterated before execution. Only completed handoffs (in `handoff/complete/`) are immutable.
```

### 3. Changelog + Completion

- Write changelog entry (subdirectory `skills/handoff/`, then root)
- Move this handoff to `handoff/complete/`

---

## Constraints

- Do not touch any files in `handoff/complete/` — those remain immutable
- This change does not affect changelog discipline anywhere in the repo