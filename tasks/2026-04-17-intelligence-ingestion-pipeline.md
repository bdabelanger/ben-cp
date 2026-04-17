# Intelligence Ingestion Pipeline Development

- **priority:** P2
- **status:** 🟢 Pipeline Operational (Alpha)
- **methodology:** Link-Driven Discovery via Asana/Jira

# Task: Intelligence Ingestion Pipeline Development

## Priority: P2
## Status: 🟢 Pipeline Operational (Alpha)
## Assignee: Code

## Goals
1. [x] Scaffold pipeline directory.
2. [x] Implement orphan scanner (`scan_orphans.py`).
3. [x] Manual verification of parsing logic (Q2 Shareout).
4. [x] Implement automated parser instruction script (`parse.py`).
5. [ ] **Link-Driven Harvester**: Build `harvest_links.py` to:
    - Scan Asana projects for Confluence/PRD links.
    - Fetch linked documents via Atlassian API.
    - Stage them in `source/` directories for the parser.

## Progress
- **2026-04-17**: Scanned vault and found orphans. Successfully parsed `Q2 2026 Product Shareout.txt` and `asana-custom-fields.md`.
- **2026-04-17**: **Pivot to Link-Driven Strategy**: User recommended using Asana custom fields as the discovery mechanism for Confluence PRDs and Launch Plans.
- **Next**: Implement `harvest_links.py` using Asana project data as the seed.
