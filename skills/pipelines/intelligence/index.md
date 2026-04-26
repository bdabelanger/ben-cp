# intelligence pipeline

Ingests raw source material (Confluence docs, PDFs, text files) and produces structured **vault intelligence records** — markdown files tagged, summarized, and indexed so agents can retrieve and reason over them.

## What it produces

- `intelligence/{domain}/{topic}.md` — structured intelligence records with title, summary, key capabilities, strategic alignment, metrics, and open questions
- Each record is tagged `Status: 🟡 Draft` on creation and promoted through review
- `intelligence/*/source/` — raw source files (Confluence HTML, PDFs) that records were derived from

## Pipeline stages

| # | Script | Mode | What it does |
|---|--------|------|--------------|
| 01 | `01_harvest.py` | Automated | Walk intelligence records, refresh stale sources by system |
| 02 | `02_parse.py` | Agent-assisted | **Parse** — prints instructions for the agent to read a source file and apply the extraction schema, then call `add_intelligence` to create the vault record |
| 03 | `03_scan_orphans.py` | Automated | **Scan** — walks all `intelligence/*/source/` directories and reports any source files that don't have a matching `.md` record in the parent directory |

**Utilities:**
- `run.py` — prints pipeline status and routes to individual stages; `--scan` runs orphan check; `<file_path>` runs parse for that file
- `schemas/source-to-intelligence-prompt.md` — LLM extraction prompt defining the 7-field output schema for intelligence records

## Pipeline stages in detail

### Stage 01 — Harvest (automated)
`01_harvest.py` walks intelligence records, reads `sources` frontmatter, and refreshes stale data (>7 days) by system (Confluence, Asana, Jira). Uses the shared Asana cache.

### Stage 02 — Parse (agent-assisted)
`02_parse.py <file_path>` prints a structured prompt instructing the agent to:
1. Read the source file
2. Apply the extraction schema (`schemas/source-to-intelligence-prompt.md`)
3. Call `add_intelligence` to write the resulting record
4. Run `03_scan_orphans.py` to confirm completion

### Stage 03 — Scan Orphans (automated)
`03_scan_orphans.py` walks every `intelligence/*/source/` directory, checks each file against the parent directory's `.md` files (exact + loose name matching), and prints a list of any unmatched source files. Clean output = `✅ No orphaned source files found.`

## How to run

```bash
# From vault root (ben-cp/)

# Print pipeline status
python3 skills/pipelines/intelligence/scripts/run.py

# Run orphan scan
python3 skills/pipelines/intelligence/scripts/run.py --scan

# Parse a specific source file (agent-assisted)
python3 skills/pipelines/intelligence/scripts/run.py intelligence/product/source/my-doc.pdf
```

## Intelligence record format

Records follow the schema defined in `schemas/source-to-intelligence-prompt.md`:

```markdown
# [Title]

- **Source:** [Filename/URL]
- **Status:** 🟡 Draft
- **Date Ingested:** [YYYY-MM-DD]

## Overview
[2-3 sentence summary]

## Key Capabilities
- [Capability 1]

## Tactical Metadata
- **Strategic Theme:** [Theme]
- **Target Date:** [Date]
- **Customer Quote:** "[Quote]"

## Analysis & Open Questions
- [Question 1]
```

## Accessing via ben-cp

```
list_reports              → shows all available reports including ingestion scan output
get_report(intelligence)  → returns latest orphan scan results with pipeline context
```
