---
title: 'Implementation Plan: agent-python-wrappers'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: agent-python-wrappers

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **v1.2**
> **STATUS**: ✅ COMPLETE

---

## Context
Digest Editor (`run.py`) provides the orchestration for the Digest, but currently our Meta-Agents exist primarily as human-readable Markdown procedures.

## Task
We must build basic, autonomous `.py` wrappers for our core skills so Digest Editor can invoke them reliably without LLM intervention every night. Each skill is independently runnable by any LLM — but each declares a **preferred agent** for its daily report so Digest Editor can route intelligently.

Character names belong exclusively in `character.md` files. All code, routing logic, and skill references use the generic skill name only.

## The Claude Perspective
> **Injected by:** Claude (Cowork) (2026-04-12)

**On `report_spec.json`:**
Each skill directory should ship a `report_spec.json` alongside `run.py`. This is the contract Digest Editor reads to build its nightly run order dynamically — no hardcoded names. Minimum fields:

```json
{
  "skill": "changelog",
  "preferred_agent": "gemma",
  "cadence": "daily",
  "output_schema": "gazette-envelope-v1"
}
```

**On structured output — shared envelope schema:**
All `run.py` outputs should conform to a shared envelope so Digest Editor has a consistent contract:

```json
{
  "agent": "<agent name>",
  "skill": "<skill name>",
  "run_at": "<iso8601 timestamp>",
  "status": "ok | warn | error",
  "summary": "<character-voiced summary string>",
  "findings": [...],
  "flags": [...]
}
```

The `summary` field is where character voice lives — Digest Editor injects that into the Digest. Everything else is structured data Digest Editor can reason over programmatically. Keeping voice confined to `summary` prevents character bleed into machine-readable fields.

**On character voice in headless Python:**
These scripts won't have an LLM reading `character.md` at runtime. Character voice in `summary` should either be: (a) hardcoded tone conventions baked into string templates, or (b) a lightweight LLM call with `character.md` injected as system prompt just for summary generation. Decide upfront — option (b) is more faithful but adds latency.

**On error handling:**
Each `run.py` must never crash silently. If a check fails, output a valid envelope with `"status": "error"` and populated `flags`. Digest Editor needs to distinguish "skill ran, found nothing" from "skill failed to run."

### Execution
1. Define shared `report_spec.json` schema (see kucera-orchestrator-scaffold handoff for full context).
2. Create `skills/changelog/run.py` — preferred agent: Gemma. Automates Check 9 and missing log detection.
3. Create `skills/knowledge/run.py` — preferred agent: Antigravity. Vault health execution.
4. Create `report_spec.json` in each skill directory declaring preferred agent, cadence, and output schema.
5. Ensure all scripts output the shared envelope schema with character voice confined to `summary`.
6. Define tone approach for `summary` generation (hardcoded templates vs. LLM-assisted).
