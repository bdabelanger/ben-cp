---
title: Intelligence — Ingestion & Parsing Pipeline
type: skill
domain: skills/intelligence
---

# Intelligence — Ingestion & Parsing Pipeline

> **Agent:** Local (for parsing/refining), Code (for running scripts)
> **Output:** New records in `intelligence/` subdirectories.

---

## Purpose

Semi-automated pipeline to keep the domain knowledge base fresh. It handles harvesting data from external sources and parsing them into structured repo-native markdown records.

## Pipeline Stages

| Stage | Command | Agent | What it does |
|---|---|---|---|
| **01: Harvest** | `python3 run.py --harvest` | Code | Walks intelligence records, refreshes stale sources from APIs/Files. |
| **02: Parse** | `python3 run.py <file_path>` | Local | Applies LLM synthesis to extract structured intelligence from source files. |
| **03: Verify** | `python3 run.py --scan` | Code | Scans for "orphans" (source files missing matching records). |

## How to run

All commands should be run from `skills/intelligence/`:

```bash
# General status
python3 run.py

# Run orphan scan
python3 run.py --scan

# Refresh all sources
python3 run.py --harvest
```

## Token Economy Rules

This skill performs automatic remediation after each run:
1. Prunes old source archives (retention = 3).
2. Purges raw JSON artifacts from `reports/asana/raw` and `reports/status/data/raw` to save context tokens.
