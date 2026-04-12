# Skill: Handoff

> **Description:** Management of the asynchronous agent relay system to ensure perfect continuity across session gaps.
> **Preferred Agent:** Relay Runner (Baton)
> **Cadence:** Start and End of every session

## Connections
- **Input:** Unresolved blockers, in-progress implementation plans, and terminal session state.
- **Output:** Structured handoff files in the central `orchestration/handoff/` directory.

## Tool Utility
- **mcp_ben-cp_write_handoff**: Primary tool for creating the persistent context for the next agent.
- **mcp_ben-cp_list_handoffs**: Used to scan for the most recent queue of active work.

## Workflow Summary
1. **Intake (Session Start):** Reading the active handoff to immediately assume the predecessor's mental state.
2. **Maintenance:** Updating the active handoff if significant pivots occur mid-session.
3. **Transition (Session End):** Collapsing the work into a sharp, staccato baton pass for the next runner.

## Constraints
- **Zero Ambiguity:** Handoffs must provide exact file paths and status boundaries.
- **Relay Focus:** Frame all context around what the *next* agent needs to execute immediately.
- **Brevity:** Staccato declarations only; no conversational fluff.
