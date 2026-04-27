---
title: Implementation Plan Investigate Agents Sensor - False positives on bold markdown
  text
type: handoff
domain: handoffs/complete
---

# Implementation Plan: Investigate Agents Sensor - False positives on bold markdown text

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-27

Completed investigation and fix alongside the P3 handoff. 0 unknown agents reported.Scan

---

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-26

---

## Context

The agents sensor found 38 issues across multiple files, but the vast majority are false positives — the sensor is matching bold markdown text (`**Bryan**`, `**Peer Team**`, `**Pragmatic Analyst**`, `**Synthesis Lead**`) as unknown agent references.

Examples of false positives:
- `skills/intelligence/analysis/predict/report.md` — `** Pragmatic Analyst`, `** Bryan`
- `skills/intelligence/analysis/synthesize/report.md` — `** Synthesis Lead`, `** Robert`
- `skills/styles/report.md` — `** Peer Team`
- `changelog.md` — fragments of inline code or text, not agent names

Genuine unknowns appear only in `changelog.md` — references to old agent/handoff filenames like `python-wrappers.md`, `permission-and-behavior-refinement-COMPLETE.md` which are legacy names predating current conventions.

## Goal

Fix the sensor's false-positive rate so it reports meaningful unknown agent refs only.

## Logic

Fix the sensor's false-positive rate so it reports meaningful unknown agent refs only.

## Execution Steps

1. [ ] Review the sensor's agent-matching regex/logic in `src/` — identify what pattern triggers `unknown_agent`
2. [ ] Tightened the pattern to exclude bold markdown fragments (starting with `**`), inline code fragments, and partial sentence matches
3. [ ] Re-run the sensor and assess whether any true unknown agents remain
4. [ ] The genuine `changelog.md` unknowns are historical — leave as-is

## Verification

- Re-run `generate_report(skill='dream')` and confirm agents sensor improves from red to yellow or green
- Issue count should drop from 38 to under 5
