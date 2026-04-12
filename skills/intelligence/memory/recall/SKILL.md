# SKILL: Memory Recall

> **Role:** Standardized Retrieval and Context Injection
> **Entry point:** `skills/memory/recall/SKILL.md`
> **Status:** Procedural (v1.0)

---

## Purpose
Standardized procedure for an agent to retrieve relevant context before starting a new complex session.

## Procedure

1. **Define Scope**: Identify keywords or domain paths related to the current task.
2. **Query the Store**:
    - Scan `mapping/` for relevant logic.
    - Scan `watchdog/outputs/reports/` for recent structural health issues in that domain.
    - Scan `collaboration/notes.md` for specific recent instructions from Ben.
3. **Synthesize Findings**: Produce a brief "Context Brief" (3-5 bullet points) for the active agent's `notes.md`.
4. **Inject**: Write the Context Brief to the session's ephemeral `notes.md`.

---

## Tool Interface (Future)
When wired to Python, this will use `memory_recall(tokens)` to surface matches.
