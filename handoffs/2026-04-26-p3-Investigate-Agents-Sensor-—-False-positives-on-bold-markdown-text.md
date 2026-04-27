# Implementation Plan: Investigate Agents Sensor — False positives on bold markdown text

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-26

---

## Context

The agents sensor found 38 issues across multiple files, but on inspection the vast majority appear to be false positives — the sensor is matching bold markdown text (`**Bryan**`, `**Peer Team**`, `**Pragmatic Analyst**`, `**Synthesis Lead**`) as unknown agent references.

Examples of apparent false positives:
- `skills/intelligence/analysis/predict/report.md` — `unknown_agent` value: `** Pragmatic Analyst` and `** Bryan`
- `skills/intelligence/analysis/synthesize/report.md` — `unknown_agent` value: `** Synthesis Lead` and `** Robert`
- `skills/styles/report.md` — `unknown_agent` value: `** Peer Team`
- `changelog.md` — multiple `unknown_agent` values that are fragments of inline code or text, not agent names

The genuine unknowns appear to be in `changelog.md` — references to old agent/handoff filenames like `python-wrappers.md`, `permission-and-behavior-refinement-COMPLETE.md`, `creation-COMPLETE.md` which are legacy handoff names that predate the current naming conventions.

## Goal

Fix the sensor's false-positive rate so it reports meaningful unknown agent refs, not bold markdown fragments.

## Execution Steps

1. Review the sensor's agent-matching regex/logic in `src/` — identify what pattern triggers `unknown_agent`
2. Tighten the pattern to exclude: bold markdown fragments (starting with `**`), inline code backtick fragments, and partial sentences caught mid-match
3. After fix, re-run the sensor and assess whether any true unknown agents remain
4. For the genuine `changelog.md` unknowns (old handoff filename references) — these are historical and can likely be left as-is or updated to point to current equivalents

## Verification

- Re-run `generate_report(skill='dream')` and confirm agents sensor improves from red to yellow or green
- Issue count should drop from 38 to under 5 (genuine unknowns only)
