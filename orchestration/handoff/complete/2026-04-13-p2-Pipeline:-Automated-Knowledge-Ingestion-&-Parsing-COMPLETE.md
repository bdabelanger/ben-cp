# Concept: Automated Knowledge Ingestion & Parsing Pipeline

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-26

Pipeline was already substantially built. Fixed two off-by-one REPO_ROOT path bugs (4 levels up vs 5) in step_5_intelligence_ingest.py and confluence_v2.py that caused silent failures on every run. Also fixed stale module import (fetch_confluence_v2 → confluence_v2) and added sys.exit(1) on fetch failure for proper error surfacing. All 12 projects with Confluence links now fetch PRDs and Launch Plans successfully.

---

## Goal

Automate the extraction of structured intelligence records from raw source materials (PDFs, TXT, meeting notes, Confluence pages) staged in `source/` subdirectories — reducing the manual parsing load on Gemma and ensuring PRDs and specs flow into the vault consistently.

## Context

There is currently a backlog of raw source materials in directories like `intelligence/product/tasks/q2-shareout/source/`. Agents are manually parsing these one at a time. Confluence PRDs are a particular gap — they are authoritative sources of truth that aren't yet flowing into the vault automatically.

## Proposed Architecture

- **Pipeline Home:** `orchestration/pipelines/intelligence/ingestion/`
- **Harvester**: Pulls directly from Confluence (PRDs, Technical Specs) and stages them in the appropriate `source/` directory
- **Scanner**: Identifies files in any `source/` directory that do not have a corresponding `.md` record in the parent directory — these are "orphaned" source files
- **Parser**: Ingestion script (with LLM synthesis) that extracts key themes, metrics, and narratives from each orphaned source
- **Generator**: Creates the initial `.md` record, tagged with `Status: 🟡 Draft` and `Source: Auto-Ingested`
- **Review step**: Agent or Ben promotes the draft via `edit_intelligence` — no auto-promotion to `✅ Complete`

---

## Concrete First Steps

1. **Scaffold the pipeline directory**: Create `orchestration/pipelines/intelligence/ingestion/` with a `README.md` describing the architecture and a `schemas/source-to-intelligence-prompt.md` with the extraction prompt template (what fields to pull: title, summary, key metrics, open questions, status).
2. **Build the scanner**: Write `pipeline/scan_orphans.py` that walks all `source/` directories in `intelligence/` and lists files with no matching `.md` sibling. Run it now — establish a baseline count of how many orphaned source files currently exist.
3. **Test the parser on Q2 Shareout materials**: The `intelligence/product/tasks/q2-shareout/source/` directory is a known backlog. Use the extraction prompt template to manually parse one file and produce a draft `.md` — validate the format before automating it.
4. **Research Confluence export options**: Check whether the Confluence MCP (`mcp__369ca651__getConfluencePage`) returns usable markdown, or whether additional parsing is needed. Test on one known PRD page.
5. **Wire up the harvester**: Once the Confluence output format is understood, write `pipeline/harvest_confluence.py` that fetches pages from the Projects space and stages them in the appropriate `source/` directory.

## Open Questions for Ben

- Which Confluence spaces/page trees should the harvester target? (Projects space is the obvious start — any others?)
- Should auto-ingested drafts go into a single holding area (`intelligence/intake/`) before being routed to the right domain, or directly into their target domain marked as draft?
