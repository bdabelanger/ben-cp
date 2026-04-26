# Handoff: Gemma (Local) Smoke Test — Results & Tool Fix

> **Prepared by:** Cowork (Claude) + Ben (2026-04-25)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-26

Processed Gemma's smoke test results. Updated Local agent role documentation with get_report routing and Rule 8 (metrics framing). Updated the smoke test template to use get_report instead of embedded content.

---

## Context

Gemma ran the redesigned smoke test on 2026-04-25. The test asked her to read the nightly dream report (embedded in the handoff) and produce a plain-language digest. Results were evaluated by Cowork (Claude) against defined acceptance criteria.

---

## Smoke Test Results

**Overall: PASS**

| Criterion | Result | Notes |
| :--- | :--- | :--- |
| Readable in under 90 seconds | ✅ Pass | Clean, well-structured, no fluff |
| Both 🟡 flags identified with specifics | ✅ Pass | Changelog (14 files, locations named) and Handoff (16 active, both P1s named) |
| No hallucinated items | ✅ Pass | Everything maps directly to the report |
| Plain language, no vault jargon | ✅ Pass | "Memory Growth" framing was a nice touch |
| Clear opinionated action for Ben | ✅ Pass | Correctly prioritized P1 handoffs as potential blockers |

**Minor issue:** Gemma placed the 🟢 "Memory Growth" metric (172 records / 47 domains) inside "What needs attention" — it's a clean stat, not a flag. Small framing error, not a failure. Worth noting in her role documentation.

---

## Tool Issue Identified (Action Required for Code)

Gemma attempted several MCP tool calls to locate the dream report externally before falling back to the embedded content in the handoff. Specific calls attempted:

- `get_intelligence` with a path approximating the dream report output — failed with `ENOENT`
- `get_handoff` and `get_task` calls looking for the report — not the right tools

**Root cause:** There is no ben-cp MCP tool that can read files from `reports/`. Gemma (and Cowork) are forced to either embed report content manually or fall back to raw filesystem reads.

This is the same issue documented in `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md`. The two handoffs are related — this one adds Gemma's failed tool call pattern as a concrete reproduction case.

**Impact on production use:** In her nightly digest role, Gemma will burn unnecessary tokens attempting MCP calls that will always fail before falling back to embedded content. This needs to be fixed before she runs nightly.

---

## Requested Action for Code

1. **Implement `get_report` tool** (or equivalent) per `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md` — expose `reports/dream/daily-report.md` via a purpose-built ben-cp MCP tool
2. **Update `agents/local.md`** — add `get_report` to Local's tool routing table so Gemma knows to call it first for pipeline outputs
3. **Update the smoke test template** — once the tool exists, revise the smoke test instructions to replace the embedded report block with a `get_report(scope='dream')` call as Step 0
4. **Minor doc fix** — note in Local's role file that 🟢 clean metrics should not appear in the "What needs attention" digest section

## Acceptance Criteria

- `get_report(scope='dream')` returns `daily-report.md` content successfully
- Gemma can run the smoke test without any failed MCP calls before reaching the digest task
- `agents/local.md` reflects the updated tool routing
