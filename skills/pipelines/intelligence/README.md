---
title: Intelligence Ingestion Pipeline
type: intelligence
domain: skills/pipelines/intelligence
---

# Intelligence Ingestion Pipeline

> **Domain:** Intelligence Lifecycle
> **Purpose:** Automate the transition from raw source material (Confluence, PDF, TXT) to structured vault intelligence records.

## Pipeline Architecture

1.  **Harvester (`harvest.py`)**: Fetches data from external sources (Confluence) or identifies new local files in `source/` directories.
2.  **Parser (`parse.py`)**: Uses LLM-based synthesis to extract structured metadata and narratives based on `schemas/source-to-intelligence-prompt.md`.
3.  **Generator**: Produces initial `.md` records in the target domain, tagged as `Status: 🟡 Draft`.

## Directory Structure
- `harvest.py`: Harvester logic.
- `parse.py`: LLM synthesis logic.
- `scan_orphans.py`: Utility to find raw source files without matching MD records.
- `schemas/`: Prompt templates and metadata definitions.

## Usage
*Coming Soon*
