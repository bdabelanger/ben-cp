---
name: memory
description: Vault memory store and intelligence domain. Overseen by the Vault Auditor. Handles long-term mappings, active learning (learn), and standardized retrieval (recall).
---

# SKILL: Memory Store

> **Role:** Custodian of Intelligence and Structural Truth
> **Agent:** Vault Auditor (Senior Archivist)
> **Entry point:** `skills/memory/index.md`
> Last updated: 2026-04-12

---

## Operations

| Operation | Trigger | Outcome |
| :--- | :--- | :--- |
| `learn` | Post-session / Daily Digest | Updated KIs or mapping logic |
| `recall` | Pre-session / Planning | Injected context from past records |
| `watchdog` | Weekly (Monday 9am) | Structural hygiene audit report |

---

## Callable Procedures (Protocols)

### 1. The Learn Protocol (`memory/learn/`)
Invoked to encode new structural state or significant findings into the memory store.
- Input: Session notes, Digest report, or raw data findings.
- Step: Update `mapping/` files or create a permanent `KI` in the knowledge skill.

### 2. The Recall Protocol (`memory/recall/`)
Invoked to find relevant context for a new task.
- Input: Current task summary or keywords.
- Process: Search `memory/`, `dream/outputs/`, and `collaboration/notes.md`.
- Output: Synthesized context report for the agent's scratchpad.

---

## Mapping Ownership

The `mapping/` directory is the **Source of Truth** for all health logic and structural interpretation. Agents MUST NOT define inline mappings; reference the central store here.
