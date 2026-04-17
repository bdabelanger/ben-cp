# Skill: Agent-Python Wrappers

- **agent:** Antigravity
- **priority:** P1
- **type:** skill

# Skill: Agent-Python Wrappers

> **Standard for script-to-agent communication.**
> Last updated: 2026-04-17

## 1. The Intelligence Envelope (JSON)

Every executable skill in the vault MUST output a JSON object to `stdout` upon successful completion. This envelope is the primary data source for the **Dream Cycle (The Gazette)**.

```json
{
  "skill": "domain/sub-domain",
  "preferred_agent": "Agent Personality Name",
  "run_at": "ISO-8601 Timestamp",
  "status": "ok | warn | error",
  "summary": "Single paragraph high-level summary for the lede.",
  "findings": [
    "Key observation 1",
    "Key observation 2 with [Markdown Link](file:///path/to/report.html)"
  ],
  "flags": [
    "CRITICAL: Description of blocker or risk"
  ]
}
```

## 2. Invocation Logic

The **Dream Orchestrator** expects to find an `executable` path in `report_spec.json`.

1. **Discovery**: Orchestrator finds `report_spec.json`.
2. **Execution**: Orchestrator runs `python3 [executable_path]`.
3. **Capture**: Orchestrator captures the LAST line of `stdout` as the JSON envelope.
4. **Assembly**: Data is injected into the Daily Gazette.

## 3. Best Practices

- **Silent Scripts**: Log operational data to `stderr`. Reserve `stdout` for the final JSON envelope.
- **Graceful Degradation**: If a data source (Asana, Jira) is missing, return `status: warn` with a summary explaining the missing coverage.
- **Relative Pathing**: Use `REPO_ROOT` calculated via 4-level parent jumps (`../../../../`) from the tool depth.

