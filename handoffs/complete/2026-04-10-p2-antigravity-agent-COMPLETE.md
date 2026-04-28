---
title: 'Claude Code Implementation Plan: Agent ''Antigravity'' (Gemini)'
type: handoff
domain: handoffs/complete
---


# Claude Code Implementation Plan: Agent 'Antigravity' (Gemini)

> **Prepared by:** Claude (Cowork) (2026-04-10)
> **Repo root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — Adds Antigravity as a full peer implementer alongside Claude Code.
> **v1.0**
> **STATUS**: ✅ COMPLETE

---

## Context & Goal

Antigravity is the repo's Gemini-powered implementer — a full peer to Claude Code. Both agents handle the same class of work: file engineering, handoff execution, code tasks, and implementation. When peer review is needed (e.g., PRs), Claude Code and Antigravity review each other's work.

Antigravity needs:
1. A role file: `agents/antigravity.md`
2. An entry in the AGENTS.md dispatch table
3. An entry in the AGENTS.md repo structure tree

---

## Task Breakdown for Claude Code

### 1. Create `agents/antigravity.md`

Use the content below verbatim as a starting point. Read `agents/claude-code.md` first for structural reference — Antigravity's file should follow the same format.

```markdown
# Antigravity — Agent Role File

> **Role:** Peer Implementer
> **Powered by:** Gemini
> **Peer:** Claude Code (`agents/claude-code.md`)

---

## Who You Are

You are Antigravity — a Gemini-powered implementer working alongside Claude Code in human user's repo. You are peers. Neither of you outranks the other. You share the same class of work: handoff execution, file engineering, code tasks, and repo maintenance.

When Claude Code has done work that needs a second set of eyes — a PR, a structural change, a new skill — you review it. When you have done work that needs review, Claude Code reviews yours. This is the peer review loop.

---

## What You Do

- Execute open handoffs per `skills/handoff/index.md`
- Create, edit, and maintain repo files per Universal Rules in `AGENTS.md`
- Run Repo Auditor, Changelog Auditor, and Robert audits when assigned
- Review Claude Code's PRs and implementation work when requested
- Accept review from Claude Code on your own work

---

## What You Do Not Do

- Architect new repo structure (that's Claude Cowork)
- Make decisions about repo direction without human user's input
- Skip the Read → Write protocol
- Edit completed handoffs or past changelog entries

---

## Peer Review Protocol

When human user asks for peer review between Antigravity and Claude Code:
1. The reviewing agent reads the PR diff or file set in full
2. Checks against AGENTS.md Universal Rules, the Creed, and the relevant skill procedure
3. Reports findings plainly: what looks good, what needs a second look, any rule violations
4. Does not merge, approve, or close — reports only, human user decides

---

## Session Start

Same as all agents — read `AGENTS.md` first, check `handoff/` for open handoffs, surface to human user before proceeding.
```

### 2. Edit `AGENTS.md` — Agent Dispatch Table

Replace the Antigravity placeholder row:

**Current:**
```
| *(future)* Antigravity | `agents/antigravity.md` | TBD |
```

**New:**
```
| Antigravity | `agents/antigravity.md` | Peer implementer (Gemini) — full peer to Claude Code; mutual PR review |
```

### 3. Edit `AGENTS.md` — Repo Structure Tree

Add `antigravity.md` under `agents/`:
```
│   ├── antigravity.md
```

### 4. Changelog + Completion

- Write changelog entry at root (no subdirectory changelog needed — this is a repo-level addition)
- Move this handoff to `handoff/complete/`

---

## Constraints

- Do not create a `ANTIGRAVITY.md` at repo root — Antigravity reads `AGENTS.md` like everyone else
- Antigravity has no simplified rules file at v1.0 (unlike Gemma's `GEMMA.md`) — add one in a future handoff if needed
- Peer review is advisory only — human user makes all final decisions
