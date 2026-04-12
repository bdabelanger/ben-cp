# SKILL: Memory Learn

> **Role:** Information Intake and Encoding
> **Entry point:** `skills/memory/learn/SKILL.md`
> **Status:** Procedural (v1.0)

---

## Purpose
Standardized procedure for an agent to capture a significant structural finding or pattern and move it from ephemeral scratchpads into the persistent **Memory Store**.

## Procedure

1. **Scan Source**: Read `dream/outputs/gazette-[DATE].md` and `collaboration/notes.md`.
2. **identify Candidates**:
    - New mapping rules (e.g., a new status emoji or metric threshold).
    - Strategic pivots in human user's notes.
    - Repeated structural failures flagged by the Watchdog.
3. **Format Knowledge**: convert the finding into a structured [Knowledge Item (KI)](/Users/benbelanger/GitHub/ben-cp/skills/knowledge/outputs/reports/) or update a file in `mapping/`.
4. **Sign & Ledger**: Record the addition in `memory/changelog.md`.

---

## Tool Interface (Future)
When wired to Python, this will use `memory_learn(content, tags)` to auto-archive findings.
