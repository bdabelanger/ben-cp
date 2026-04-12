# Audit Procedure: Handoff

> **Owner:** Relay Runner (Baton)

## Requirements
- [ ] Continuity: Every session must starting with a handoff check and end with a handoff update/creation.
- [ ] Traceability: All handoff files must follow the kebab-case naming convention.
- [ ] Closure: Completed work must be explicitly noted in the FINAL call to the handoff tool.

## Operating Procedures

### 1. Ingestion Protocol (Start)
1. List open handoffs using `mcp_ben-cp_list_handoffs`.
2. Select the highest priority or most recent relevant file.
3. Read the content to establish the execution boundary.

### 2. Transition Protocol (End)
1. **Status Mapping:** Identify ✅ Complete, 🟡 Partial, and ⚠️ Needs Review items.
2. **Next Steps:** List the immediate next three commands or files for the following agent.
3. **Baton Pass:** Write the new handoff file or mark the current one as complete using the `ben-cp` MCP.

### 3. Verification
Verify that the `assigned_to` field matches the intended model or "anyone" if generic.
