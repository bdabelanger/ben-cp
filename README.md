# ben-cp (v2.1.1)

Personal repo for Ben — the central nervous system for vault automation and agentic coordination.

---

## 🛠 MCP Server (ben-cp)

A purpose-built [Model Context Protocol](https://modelcontextprotocol.io) server that provides structured access to the vault's intelligence and orchestration layers.

**Entry point:** `src/ben-cp.ts`  
**Build path:** `dist/ben-cp.js`

### Core Tools Exposed:

| Domain | Tool | Purpose |
| :--- | :--- | :--- |
| **Governance** | `get_agent_info` | Retrieve `AGENTS.md` and role definitions. |
| **Handoffs** | `get_handoff` / `list_handoffs` | Manage cross-agent implementation plans. |
| **Intelligence** | `get_intelligence` / `list_intelligence` | Read/write to the long-term knowledge base. |
| **Tasks** | `get_task` / `list_tasks` | Manage active deliverables and drafting. |
| **Skills** | `get_skill` / `list_skills` | Retrieve SOPs and procedural logic. |
| **Reports** | `get_report` / `list_reports` | Access nightly pipeline outputs (Dream cycle). |
| **Vault** | `add_changelog` / `get_changelog` | Maintain the audit trail of all vault changes. |

### ⚠️ Google Drive Sync Warning
The vault is hosted on Google Drive. Agents and scripts should **NEVER** use raw filesystem reads (e.g., `read_text_file` with absolute paths) for recently generated pipeline outputs in `orchestration/pipelines/outputs/`. 

**Requirement:** Always use the `get_report` tool. It runs on the host and guarantees access to the latest data, bypassing Google Drive's local sync latency.

---

## 🌙 Dream Cycle (Nightly Reporting)

The vault features an automated synthesis pipeline that runs nightly to coordinate project data from Asana and Jira.

**Runner:** `orchestration/utilities/intelligence/report.py`  
**Outputs:** `orchestration/pipelines/outputs/dream/`

### Quick Start:
```bash
# Generate a fresh nightly report
python3 orchestration/utilities/intelligence/report.py
```

---

## 🏗 Directory Structure

| Layer | Lives in | Contents |
| :--- | :--- | :--- |
| **Intelligence** | `intelligence/` | Domain knowledge, strategic core, and source documents. |
| **Orchestration** | `orchestration/` | Active work (handoffs, tasks) and pipeline logic. |
| **Skills** | `intelligence/core/skills/` | Procedural SOPs and agent instructions. |
| **Agents** | `agents/` | Specific role documentation for Cowork, Local, and Code. |

---

## Development

```bash
npm install     # Install dependencies
npm run build   # Rebuild the MCP server
npm start       # Run the server via tsx (dev)
```
