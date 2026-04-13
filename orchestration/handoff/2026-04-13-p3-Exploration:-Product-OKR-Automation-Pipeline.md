# Exploration: Product OKR Automation Pipeline

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P3
> **STATUS: 🔲 READY — pick up when P1/P2 queue is clear**

---

## Goal

Reduce the manual overhead of updating Q2 OKRs by deriving factual progress automatically from existing project pipelines — while keeping strategic context (the "why") human-authored.

## The Hybrid Model

| Layer | Source | Who owns it |
|-------|--------|-------------|
| **Facts** — % complete, milestone dates, ticket counts | Jira epics, Asana projects | Automated |
| **Context** — confidence score, narrative, risk flags | Intelligence files | Agent/Ben |

The pipeline populates the Facts layer on a schedule. Ben (or an agent) reviews and updates the Context layer when it matters.

---

## Proposed Architecture

- **Pipeline Home:** `orchestration/pipelines/product/okrs/`
- **Project Linker Schema** (in `schemas/okr-project-map.json`): maps each KR to one or more Asana project GIDs and/or Jira epic keys
- **Progress Scraper** (`pipeline/scrape_progress.py`): reads the map, pulls current status from each source, writes a "Facts" block into the corresponding OKR intelligence file
- **OKR intelligence files** (`intelligence/product/roadmap/okrs/q2/*.md`): updated in-place with a `## Auto-Progress (last updated: DATE)` section

---

## Concrete First Steps

1. **Audit Q2 KRs for quantifiability**: Read all files in `intelligence/product/roadmap/okrs/q2/`. For each KR, note whether progress can be derived from a Jira filter or Asana project — or whether it's purely qualitative. Produce a simple table: `KR name | Quantifiable? | Source`.
2. **Draft `schemas/okr-project-map.json`**: A JSON file mapping each quantifiable KR to its Asana GID(s) and/or Jira JQL filter. Start with the 3–4 KRs that are most clearly measurable (e.g., Notes Datagrid, Client Portal).
3. **Write a minimal scraper**: `pipeline/scrape_progress.py` that reads the map, calls Asana/Jira, and prints a human-readable progress summary for each KR. No file writes yet — just validate the data is correct.
4. **Wire up the write step**: Once the scraper output looks right, add the logic to patch the `## Auto-Progress` section into each OKR file.
5. **Schedule it**: Register as a scheduled task to run weekly (Monday morning is ideal — fresh data before status reports).

## Open Questions for Ben

- Should auto-progress updates be committed to git automatically, or staged for review first?
- Are there KRs where the "right" metric isn't obvious from Jira/Asana? (e.g., qualitative outcomes like customer satisfaction) — flag these so we don't try to automate what can't be automated.
