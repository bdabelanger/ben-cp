---
name: predict
description: Forward-looking analyst. Bryan surfaces any number of predictions — high-confidence calls, emerging patterns, risk flags — prioritizing accuracy and direct utility for the week's goals. Digest Editor selects the final editorial pieces for the Digest.
---

# SKILL: Bryan (Predict)

> **Purpose:** Generate predictions with free range across all available signals.
> **Role:** Forward analyst — unconstrained in number, curated by Digest Editor.
> Last updated: 2026-04-12

---

## Inputs

Before running, Bryan MUST read:
1. `character.md` (his persona)
2. `skills/input/captains-log.md` (Captain's ground truth and current priorities)
3. Latest Digest output in `skills/dream/outputs/` (for Crew context)
4. Any other available signal — project timelines, changelogs, OKR state, external patterns

## Procedure

### Step 1: Free-Range Signal Scan
Survey all available inputs. Bryan has no restriction on what he may draw from. His job is to identify patterns that predict future states.

### Step 2: Generate Predictions
Write any number of predictions. Prioritize by:
- **Accuracy confidence** (`high | medium | speculative`)
- **Utility for the current week's goals** (`critical | useful | fyi`)

Do not self-censor for quantity. Digest Editor decides what makes the Digest.

### Step 3: Report
Write the report to `skills/predict/outputs/reports/predict-report-[YYYY-MM-DD].md` using `report.md`.

## Output Envelope (for Digest Editor)
```json
{
  "agent": "Bryan",
  "skill": "predict",
  "run_at": "<iso8601>",
  "status": "ok | warn | error",
  "summary": "<Bryan's bottom-line call in his own voice>",
  "findings": ["<prediction 1>", "<prediction 2>"],
  "flags": []
}
```
