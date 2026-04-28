---
title: 'Implementation Plan: Fix Agent Sensor False Positives - Bold Markdown in Report
  Files'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Fix Agent Sensor False Positives - Bold Markdown in Report Files

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-27

Resolved false positives by updating the agents sensor to strip bold markdown formatting and semantically correcting report templates to use 'Persona:' instead of 'Agent:'. verified 0 issues.Scan

---

## Fix Agent Sensor False Positives - Bold Markdown in Report Files

## Context

The agents sensor flagged 5 issues across 3 files, all with `invalid_agent_format`. The sensor expects the pattern `Name (Model)` but is matching bold markdown text (`**`) in report files that describe agent personas — not actual agent declarations:

- `skills/intelligence/analysis/predict/report.md`: flagged `** Pragmatic Analyst (Bryan)` and `** Bryan (Predict)`
- `skills/intelligence/analysis/synthesize/report.md`: flagged `** Synthesis Lead (Robert)` and `** Robert (Synthesis)`
- `skills/styles/report.md`: flagged `** Peer Team (Joint Operating Environment)`

These appear to be narrative/descriptive content in report template files where `**text**` markdown bold formatting happens to match the `Name (Model)` detection pattern when the sensor strips the `**` prefix.

## Logic

Resolve the 5 false positives so the agents sensor reports 0 issues. Either fix the sensor's detection logic or restructure the flagged content in the report files.

## Execution Steps

1. [ ] Open the three flagged files and review the context around each flagged line. Determine whether:
   - The lines are truly descriptive prose that should not match the agent format sensor, OR
   - The lines are intended as agent declarations that need the format corrected

2. [ ] If descriptive prose: Update the agents sensor regex/parser to exclude lines beginning with `**` (bold markdown) from the `Name (Model)` check. The sensor should only flag actual agent declaration fields, not narrative text.

3. [ ] If agent declarations with wrong format: Update the content in the three files to use the correct `Name (Model)` format without the `**` prefix.

4. [ ] Re-run `generate_report(skill='dream')` and confirm the agents sensor shows 0 issues.

## Verification Checklist

- [ ] `get_report('dream/agents.json')` shows 0 issues
- [ ] Legitimate agent format violations (non-bold lines with wrong format) are still caught by the sensor
- [ ] Report template files in `skills/intelligence/analysis/` render correctly in markdown
