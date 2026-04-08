# ben-cp

Personal repo for Ben — two main components live here:

---

## MCP Server (Skill Vault)

A local [Model Context Protocol](https://modelcontextprotocol.io) server that exposes SOPs and skill templates to Claude Code.

**Entry point:** `src/ben-cp.ts`

**Tools exposed:**
| Tool | Description |
|---|---|
| `get_skill` | Read a SOP or skill template by path relative to `/skills` |
| `list_vault` | List all files available in the SOP vault |

**Run locally:**
```
npm start
```

**SOPs live in:** `skills/` — organized by tool/workflow (e.g. `skills/project-status-reports/`)

---

## Platform Weekly Status Report Pipeline

Automated pipeline that generates an HTML status report for the Platform engineering team by pulling live data from Asana and Jira.

**Quick start (from repo root):**
```bash
# Full fresh run — wipes Jira cache, re-fetches everything
python3 project-status-reports/scripts/full_run.py --force

# Re-render only — Jira data already fresh, skip re-fetching
python3 project-status-reports/scripts/full_run.py
```

**Pipeline steps:**

| Step | Script | What it does |
|---|---|---|
| 0 | `step_0_asana_refresh.py` | Fetches all active Product team projects from Asana API |
| 1 | `step_1_asana_ingest.py` | Filters to Platform team, extracts stage/status/milestones/Jira links |
| 2 | `step_2_atlassian_fetch.py` | Fetches child issues + epic estimates per CBP key from Jira |
| 3 | `step_3_jira_harvest.py` | Harvests and normalizes Jira issue data |
| 4 | `platform_report.py` | Synthesizes Asana + Jira into a markdown report |
| — | `render_html.py` | Converts markdown report to a self-contained HTML file |

**Output:** `project-status-reports/outputs/Platform_Status_<date>.html`

**Required environment variables** (`.env` at repo root):
```
ASANA_API_TOKEN=...
ATLASSIAN_USER_EMAIL=...
ATLASSIAN_API_TOKEN=...
```

Full SOP: [`skills/project-status-reports/index.md`](skills/project-status-reports/index.md)
