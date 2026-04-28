---
title: ben-cp (v2.1.1)
type: task
domain: .
---

# ben-cp (v2.1.1)

Personal repo for Ben — the central nervous system for automation and agentic coordination.

---

## ⚙️ Setup

Install Python dependencies:
```bash
pip3 install -r requirements.txt --break-system-packages
```

---

## 🛠 MCP Server (ben-cp)

A purpose-built [Model Context Protocol](https://modelcontextprotocol.io) server that provides structured access to the intelligence and orchestration layers.

**Entry point:** `src/ben-cp.ts`  
**Build path:** `dist/ben-cp.js`

### Core Tools Exposed:

| Domain | Tool | Purpose |
| :--- | :--- | :--- |
| **Governance** | `get_agent` | Retrieve `AGENTS.md` and role definitions. |
| **Handoffs** | `get_handoff` / `list_handoffs` | Manage cross-agent implementation plans. |
| **Intelligence** | `get_intelligence` / `list_intelligence` | Read/write to the long-term knowledge base. |
| **Tasks** | `search_tasks` / `add_task` | Search report data and stage new deliverables. |
| **Skills** | `get_skill` / `list_skills` | Retrieve SOPs and procedural logic. |
| **Reports** | `get_report` / `list_reports` | Access nightly pipeline outputs (Dream cycle). |
| **Changelogs** | `add_changelog` / `get_changelog` | Maintain the audit trail of all changes. |

### ⚠️ Google Drive Sync Warning
The repo is hosted on Google Drive. Agents and scripts should **NEVER** use raw filesystem reads (e.g., `read_text_file` with absolute paths) for recently generated pipeline outputs in `skills/pipelines/outputs/`. 

**Requirement:** Always use the `get_report` tool. It runs on the host and guarantees access to the latest data, bypassing Google Drive's local sync latency.

---

## 🌙 Dream Cycle (Nightly Reporting)

The repo features an automated synthesis pipeline that runs nightly to coordinate project data from Asana and Jira.

**Runner:** `skills/dream/run.py`  
**Outputs:** `reports/dream/`

### Quick Start:
```bash
# Generate a fresh nightly report
python3 skills/dream/run.py
```

---

## 🏗 Directory Structure

| Layer | Lives in | Contents |
| :--- | :--- | :--- |
| **Intelligence** | `intelligence/` | Domain knowledge, strategic core, and source documents. |
| **Orchestration** | `handoffs/` | Active work (handoffs, tasks) and implementation plans. |
| **Skills** | `skills/` | Procedural SOPs and agent instructions. |
| **Agents** | `agents/` | Specific role documentation for Cowork, Local, and Code. |

---

## Development

```bash
npm install     # Install dependencies
npm run build   # Rebuild the MCP server
npm start       # Run the server via tsx (dev)
```
