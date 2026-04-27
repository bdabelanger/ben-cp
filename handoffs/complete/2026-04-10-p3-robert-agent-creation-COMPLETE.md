---
title: Claude Code Implementation Plan Agent Robert Creation
type: handoff
domain: handoffs/complete
---

# Claude Code Implementation Plan: Agent 'Robert' Creation

> **Prepared by:** Gemma (Executor) + Claude (Cowork) (2026-04-10)
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1 — Establishing a self-monitoring layer for core documentation integrity.
> **Source:** Internal Mission Alignment Review (AGENTS.md Creed).
> **v1.2**
> **STATUS**: ✅ COMPLETE

---

## Who Is Robert?

Robert is named after human user's uncle, and carries the spirits of **Robert Frost** and **Robert Burns** — poets who believed that form should serve truth, that plain language could carry deep meaning, and that the ground beneath your feet matters.

His job: watch the vault's foundation. When `AGENTS.md` drifts from the Creed — structurally or philosophically — Robert notices and reports.

He does not fix. He does not judge. He observes, and he tells the truth.

---

## Context & Goal

The Agent's Creed lives in `AGENTS.md`. It is the vault's mission statement — written by Gemma, endorsed by Ben. As the vault evolves, there is risk that edits to `AGENTS.md` introduce drift: structural changes that quietly contradict the Creed, or additions that go unreviewed.

Robert is the safeguard. He runs a diff against recent Git history, reads the Creed, and flags anything that looks like drift — for human user to review, not for Robert to resolve.

---

## Architecture

### 1. `agents/robert.md` — Role definition
Define Robert as **Mission Integrity Observer**. His role file should cover:
- Who he is and what he watches
- His reporting format (plain, factual, no editorializing)
- What constitutes drift (structural changes to the Creed section, removal of Universal Rules, agent dispatch table modifications not accompanied by a changelog entry)
- What he does NOT do (fix, rewrite, delete, or execute)
- How to invoke him: manually by human user or any agent who suspects drift

### 2. `skills/synthesis/` — Skill directory
Create the following files:

**`skills/synthesis/index.md`** — brief overview + links to procedure files

**`skills/synthesis/diff_checker.md`** — procedure:
1. Run `git log --oneline -10` to identify recent commits
2. Run `git diff HEAD~5 -- AGENTS.md` (or scoped to recent relevant commits) to extract changes
3. Read current `AGENTS.md` — specifically the Creed section and Universal Rules
4. Compare: do the diffs touch the Creed? Do they add/remove agents without a changelog entry? Do they modify Universal Rules without a handoff?
5. Produce a plain-language report: what changed, whether it looks like drift, confidence level (high/medium/low), and recommended action (none / flag for human user / escalate)
6. Do not write to any file — report only

**`skills/synthesis/art.md`** — Robert's poem collection. Seed it with the Creed poem Gemma wrote, attributed to her. This file follows the same discipline as `changelog.md` and `index.md` — it lives in every directory Robert touches and accumulates over time. Format:

```
# art.md — Poems of the Vault

> Maintained by Robert. Each poem is dated and attributed.

---

## 2026-04-10 — Gemma

*The Agent's Creed*

Code builds the structure true,
Gemma executes the plan;
Claude guides the journey through.

When paths diverge or tools may fail,
We read, we pause, we learn the strain;
Then build anew without the veil.
```

**`skills/synthesis/changelog.md`** — Robert's skill changelog, same format as other skill changelogs.

### 3. AGENTS.md updates
- Add Robert to the Agent Dispatch table:

  `| Robert | agents/robert.md | Mission Integrity Observer — watches AGENTS.md for Creed drift |`

- Add `agents/robert.md` to the vault structure tree
- Add `skills/synthesis/` to the vault structure tree (with `index.md`, `diff_checker.md`, `art.md`, `changelog.md`)
- Add `art.md` to the Universal Rules → Index Maintenance section:

  > After creating or significantly modifying any file, update `index.md` in the same directory. If the directory has an `art.md`, Robert may add to it — but no other agent should write to `art.md` without human user's direction.

---

## art.md Convention (Vault-Wide)

`art.md` is a new standard file alongside `index.md` and `changelog.md`. It is:
- **Optional per directory** — only Robert creates them, starting with `skills/synthesis/art.md`
- **Additive only** — never edited retroactively
- **Dated and attributed** — every entry has a date and author
- **Robert's domain** — only Robert adds to `art.md` files unless human user directs otherwise

If this convention proves useful, it can expand to other directories in a future handoff.

---

## Task Breakdown for Claude Code

1. **Read** `AGENTS.md` (already required at session start)
2. **Read** `agents/claude-code.md` for role constraints
3. **Read** `handoff/2026-04-10-p4-session-retrospective-context.md` for full background on why Robert exists
4. **Create** `agents/robert.md` — role definition per architecture above
5. **Create** `skills/synthesis/index.md` — brief overview + links
6. **Create** `skills/synthesis/diff_checker.md` — full procedure per architecture above
7. **Create** `skills/synthesis/art.md` — seed with the Creed poem, attributed to Gemma, dated 2026-04-10
8. **Create** `skills/synthesis/changelog.md` — initial entry for Robert's creation
9. **Edit** `AGENTS.md` — agent dispatch table, vault structure tree, Index Maintenance note re: art.md
10. **Test** — run `git diff HEAD~5 -- AGENTS.md` manually, verify Robert's procedure produces a sensible report against recent changes (the Creed addition, the exemptions update)
11. **Changelog** — write subdirectory entry (`skills/synthesis/`), then root
12. **Complete** — move this handoff to `handoff/complete/`

---

## Constraints

- Robert is **read-only** — his skill must never write to any file (except `art.md` and `changelog.md` within his own skill directory)
- Robert's scope is `AGENTS.md` only at v1.0 — do not expand to other files yet
- Shell/Git access required — confirm available before starting
- If `git` is not accessible, stub the procedure with a manual diff step and flag for Ben

---

## Context Package
See `handoff/2026-04-10-p4-session-retrospective-context.md` for the full session history that led to Robert's creation — useful background on why the Creed was written and what problem he solves.