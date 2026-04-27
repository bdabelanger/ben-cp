---
Status: active
Priority: P3
Date: 2026-04-26
Owner: Ben
---
# Skill: Predict

> **Description:** Forward-looking analyst surfacing high-confidence predictions, emerging patterns, and risk flags across all vault signals.
> **Preferred Agent:** Intelligence (Predict)
> **Cadence:** Daily / Ad-hoc

## Connections
- **Input:** Latest Dream Cycle digests, and all vault manifests.
- **Output:** `skills/intelligence/analysis/predict/outputs/reports/`, feeds into Dream Cycle (Strategic Outlook).

## Tool Utility
- **grep_search**: Used to identify patterns across historical session logs.
- **filesystem**: Used to survey architectural changes and velocity.

## Workflow Summary
1. **Discovery:** Free-range signal scan across all available vault manifests.
2. **Analysis:** Calculation of confidence levels and utility scores for logical next steps.
3. **Communication:** Producing grounded, pragmatic forecasts for the Strategic Outlook.

## Constraints
- Accuracy confidence must be explicitly rated (High, Medium, Speculative).
- Never over-indexes on outlier events; focuses on structural outcomes.
- No self-censorship on quantity; utility curation is delegated to the Dream orchestrator.
