---
name: human-input
description: Captures raw ground truth, ad-hoc decisions, and context from human user and all agents. Any agent may write to any notes.md — entries must be signed with agent name and timestamp.
---

# SKILL: Communication & Notes

> **Purpose:** The single shared intelligence layer across the agents. The user and all agents write here. All agents read here.
> Last updated: 2026-04-12

---

## The Notes System

Every active skill in the vault has a `notes.md` file. These are open, persistent, collaborative scratchpads. There is no hierarchy between human user's entries and agent entries — all entries are equal crew contributions, signed and dated.

**The primary channel:** `skills/orchestration/notes/notes.md` is the vault-wide broadcast. Agents MUST read it before any planning, OKR, or status work.

---

## Write Rules (Universal — applies to ALL `notes.md` files)

1. **Sign every entry:**
   ```
   [Your Name — YYYY-MM-DD HH:MM]
   Your entry here.
   ```
2. **Append only** — never edit or delete another agent's or human user's entries.
3. **Own your followups** — if your note implies an action, you're responsible unless explicitly handed off.
4. **Any agent may write to any skill's `notes.md`** — not just their own domain.

---

## Read Rules

- Before any planning, OKR, or status work: read `skills/orchestration/notes/notes.md`
- Before executing work in a specific skill: read that skill's `notes.md` if one exists
- human user's entries carry ground truth — they supersede inferred context from memory or past sessions

---

## Edit Rules

- You may **only edit your own entries** (entries signed with your name)
- Corrections to your own entries should be appended as `[Correction — YYYY-MM-DD]` inline, not silently overwritten

---

## Skill-Level `notes.md` Map

Each active agent skill has a stub `notes.md` created on 2026-04-12. They are empty until the agents writes in them.

| Communication (primary) | `skills/orchestration/notes/notes.md` |
| Handoff | `skills/orchestration/handoff/notes.md` |
| Access | `skills/orchestration/access/notes.md` |
| Changelog | `skills/orchestration/changelog/notes.md` |
| Reporting | `skills/intelligence/report/notes.md` |
| Memory | `skills/intelligence/memory/notes.md` |
| Analysis/Predict | `skills/intelligence/analysis/predict/notes.md` |
| Analysis/Synthesize | `skills/intelligence/analysis/synthesize/notes.md` |
| Product | `skills/product/notes.md` |
