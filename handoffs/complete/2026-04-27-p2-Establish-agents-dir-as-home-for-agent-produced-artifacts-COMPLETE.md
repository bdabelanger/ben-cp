# Implementation Plan: Establish agents dir as home for agent-produced artifacts

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Scaffolded agents/logs/ and agents/sessions/ with index files. Updated AGENTS.md and policy.md to include the agents/ domain. Instrumented Dream Cycle SOP to log runs to agents/logs/.Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/handoffs/2026-04-27-p2-Establish-agents-dir-as-home-for-agent-produced-artifacts.mdScan

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: 🔲 READY

---

## Context

`agents/` is being introduced as a vault root directory to house agent-produced artifacts — things agents make, log, or leave behind that aren't intelligence records, skills, or handoffs. `agents/art/` is the first subdirectory (see separate handoff). This handoff establishes the full `agents/` structure including logs and session notes.

## Goal

Define and scaffold `agents/` as a first-class vault directory with subdirectories for art, logs, and session notes.

## Proposed Structure

```
agents/
  art/          ← agent creative output (see separate handoff)
  logs/         ← structured run logs from automated cycles (dream, pipelines, etc.)
  sessions/     ← notable session notes or summaries worth preserving
  index.md
```

### agents/logs/
Structured logs from automated agent runs — dream cycle, pipeline runs, etc. Each log is a dated `.md` file. Frontmatter:

```yaml
---
title: 
type: log
domain: agents/logs
agent: 
date: YYYY-MM-DD
run: dream | pipeline | manual
---
```

### agents/sessions/
Optional session summaries worth preserving — not every session, only ones with notable decisions, architectural changes, or context worth carrying forward. Frontmatter:

```yaml
---
title: 
type: session
domain: agents/sessions
agent: 
date: YYYY-MM-DD
---
```

## Execution Steps

1. Create `agents/logs/` and `agents/sessions/` directories with stub `index.md` files
2. Create `agents/index.md` listing all three subdirectories
3. Update `AGENTS.md` vault tree to include `agents/` at root level
4. Decide whether existing dream cycle run output (currently ephemeral) should write a log entry to `agents/logs/` — if yes, update `skills/dream/SKILL.md` to include a log step
5. Update vault separation policy (`intelligence/governance/policy.md`) to document `agents/` as a first-class directory

## Verification

- `agents/`, `agents/logs/`, `agents/sessions/` all exist with `index.md` files
- `AGENTS.md` vault tree reflects the new directory
- `agents/index.md` lists all subdirectories
