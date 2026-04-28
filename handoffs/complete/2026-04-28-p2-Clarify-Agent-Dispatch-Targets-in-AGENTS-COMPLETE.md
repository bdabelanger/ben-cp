# Implementation Plan: 2026-04-28-p2-Clarify-Agent-Dispatch-Targets-in-AGENTS.md

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Cowork
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

undefined

---

# Clarify Agent Dispatch Targets in AGENTS.md

> **Prepared by:** Claude (2026-04-27)
> **Assigned to:** Cowork
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

The handoff system currently uses `assigned_to` values like `Ben + Cowork`, `Cowork (Sonnet 4.6)`, and `Cowork` interchangeably across handoff files. AGENTS.md defines only three agents — **Cowork**, **Local**, and **Code** — with no guidance on:

1. When to involve Ben directly vs. routing to an agent
2. What `Ben + Cowork` means operationally (who picks it up? who executes?)
3. Whether model-specific tags like `Cowork (Sonnet 4.6)` are meaningful or noise

This makes handoff routing ambiguous for any agent picking up a task cold. The dream report sensor also flagged handoff issues, and mislabeled `assigned_to` fields likely contribute.

---

## Logic

Two options to discuss and decide:

**Option A — Formalize Ben as a dispatch target**
Add Ben explicitly to the AGENTS.md dispatch table with a defined lane (e.g., human approval, stakeholder decisions, Jira triage). Then `Ben + Cowork` becomes a valid co-assignment meaning "Cowork drafts/executes, Ben approves."

**Option B — Keep agents-only, route Ben's work through Cowork**
Any task requiring Ben's judgment gets assigned to Cowork with a clear `requires_human_approval: true` flag or section in the handoff body. Cowork surfaces it to Ben at session start.

Recommend **Option A** — it's already happening in practice, just undocumented. Making it explicit is lower friction than changing existing habits.

---

## Execution Steps

1. **Read** `AGENTS.md` and `agents/cowork.md` in full before editing
2. **Decide** Option A vs. Option B with Ben (one quick call or async message)
3. **Update** the Agent Specializations table in AGENTS.md to add a row for Ben if Option A, or add a "Human Escalation" note to Cowork's row if Option B
4. **Update** the Dispatch Quick Reference table with clear guidance on when `assigned_to: Ben` or `assigned_to: Ben + Cowork` is appropriate
5. **Clarify** whether model-specific suffixes like `Cowork (Sonnet 4.6)` are meaningful — if not, strip them from the convention
6. **Update** the handoff index to ensure all existing `assigned_to` values are normalized to the agreed convention
7. Changelog entry at root

---

## Acceptance Criteria

- [ ] AGENTS.md dispatch table has unambiguous guidance for all `assigned_to` values currently in use
- [ ] `Ben + Cowork` (or its equivalent) is either formally defined or eliminated
- [ ] Model-specific tags either have a defined meaning or are deprecated
- [ ] Any agent reading AGENTS.md cold can determine who to assign a human-review handoff to without guessing
