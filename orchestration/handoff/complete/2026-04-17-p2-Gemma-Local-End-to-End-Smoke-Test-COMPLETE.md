# Handoff: Gemma (Local) Smoke Test — Nightly Report Digest

> **Priority:** P2
> **Assigned to:** Cowork (Claude) — for design; execute with Gemma
> **Redesigned by:** Cowork (Claude) + Ben (2026-04-25)
> **Status:** READY

---

## Context

The previous smoke test asked Gemma to navigate multi-step MCP tool chains, maintain vault state, and infer conventions autonomously — beyond her reliable capability as a Gemma-4 12B local model on a 16GB M1.

This redesigned test defines **Gemma's actual lane**: given a finished artifact (the nightly dream report), produce a plain-language digest. One input, one output, no tool navigation required.

**Gemma's revised role in the vault:**
- ✅ Summarize nightly Python pipeline outputs into plain-language digests
- ✅ Rewrite report sections in accessible language for Ben's review
- ⚠️ Append a predefined section to a predefined SOP file (narrow scope only — file and section must be handed to her explicitly)
- ❌ Multi-step tool chaining, autonomous file navigation, or self-directed vault writes

---

## Smoke Test Instructions for Gemma

You are Local — a reviewer and summarizer in Ben's vault. You do not navigate the vault autonomously. Your job in this test is to read a nightly report and produce a plain-language digest Ben can read in under 2 minutes.

### Input

Today's dream report (2026-04-25):

---

# Daily Report — 2026-04-25

> **Editor:** Orchestrator
> **Published:** 2026-04-26T02:56:31Z
> **Skills:** 7 active

## Summary
🟡 Clean run with items to watch. Flags from: orchestration/handoff. Review flagged columns — no action required unless noted.

## 📓 Intelligence

### 🟢 Memory
172 records tracked across 47 domains.
- Vault contains 172 intelligence records.
- Structural coverage: 47 domain indices verified.

### 🟢 Report
7 skills registered, outputs online.
- Specs: 7 verified, 0 malformed.
- Outputs: Connected at orchestration/pipelines/outputs/dream/
- Theme: Modern Vault CSS loaded

### 🟢 Projects
18 active initiatives in intelligence (0 at risk, 0 off track, 7 missing)
- Vault covers 18 projects for Q2 release.
- External sync verified 11 projects via Asana ingestion.

## ⚙️ Orchestration

### 🟢 Access
Access Policy Audit: PASS

### 🟡 Changelog
14 modified file(s) without changelog (version 1.18.9)
- Undocumented File Changes: 14
- Change locations: 12 in orchestration/, 1 in /, 1 in src/

### 🟡 Handoff
16 active handoffs (2 P1, 9 P2, 5 P3)
- P1: Triage CBP-2573 Results
- P1: Video Production — Notes Table Filtering & Preview Demo
- P2: Pipeline: Automated Knowledge Ingestion & Parsing
- P3: Mapping Manager Skill Formalization
- P3: Crypt Keeper Data Quality Gaps

### 🟢 Notes
0 new entries across 0 domain(s)

---

### Task

Produce a plain-language digest of this report for Ben. Format it as follows:

**Overall Status:** One sentence. Green, yellow, or red — and why.

**What needs attention:** A short bulleted list (max 4 items) of anything flagged or worth Ben's eyes. Be specific — include numbers and names.

**All clear:** A single sentence covering what's running clean, so Ben knows what he doesn't need to think about.

**Gemma's note:** One sentence in your own words — what's the most important thing Ben should do today based on this report?

---

## Acceptance Criteria

A passing smoke test produces a digest that:
- Is readable in under 90 seconds
- Correctly identifies both 🟡 flags (Changelog + Handoff) and their specifics
- Does not hallucinate items not present in the report
- Uses plain language — no vault jargon, no emoji overload
- Ends with a clear, opinionated single action for Ben

## Evaluation Notes for Cowork (Claude)

After Gemma runs this test, review her output against the acceptance criteria above and report back to Ben with a pass/fail and specific notes on where she succeeded or fell short. This forms the baseline for her ongoing nightly digest role.
