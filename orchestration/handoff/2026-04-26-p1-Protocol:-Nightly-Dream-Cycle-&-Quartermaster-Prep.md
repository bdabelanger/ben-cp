# Implementation Plan: Protocol: Nightly Dream Cycle & Quartermaster Prep

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: 🔲 READY — pick up 2026-04-26

---

# Protocol: Nightly Dream Cycle & Quartermaster Prep

> **Prepared by:** Cowork (Claude) + Ben (2026-04-25)
> **Assigned to:** Code
> **Priority:** P1
> **STATUS: 🔲 READY**

---

## Context

This protocol defines the automated handover between the local Python Audit Suite (Dream), Claude Code (Initial Triage), and Claude (Quartermastering). It replaces the previous nightly dream sequence in ben-cp.

**Migration note:** Existing dream scripts (currently at `orchestration/utilities/intelligence/report.py`) and any cron entries referencing them must be removed as part of adoption. The new entry point is `orchestration/utilities/dream.py`.

---

## The Nightly Sequence

### Phase 1 — 02:00 AM: The Dream
Local cron triggers `python3 orchestration/utilities/dream.py`.
- Executes all 11 sensors
- Generates 11 JSON reports in `orchestration/pipelines/outputs/`

### Phase 2 — 02:15 AM: Initial Triage (Watchman)
Local cron triggers `python3 orchestration/utilities/triage.py`.
- Calls the Anthropic API (claude-haiku or sonnet) with all 11 JSONs
- Synthesizes results into a single `TRIAGE_REPORT.md` using the schema defined below
- Goal: use a lightweight Claude model to condense ~1MB of JSON into a ~2KB summary at low cost
- **Failure handling:** If the API call fails or returns malformed output, write a sentinel file `TRIAGE_FAILED.flag` to `orchestration/pipelines/outputs/`. Claude reads this at 08:00 and falls back to raw JSON in that directory.

### Phase 3 — 08:00 AM: Quartermastering (Claude)
Human initiates Claude session.
- Claude reads `TRIAGE_REPORT.md` (or falls back to raw outputs if sentinel is present)
- Claude, acting as Cowork-level Quartermaster, generates handoff files in `orchestration/handoff/`. All handoffs generated in this session are considered Cowork-reviewed at point of generation.
- Claude writes `DISPATCH_SUMMARY.md` to `orchestration/` as a human-facing prioritization artifact summarizing the day's tasks. Code does not consume this file directly.

---

## Agent Roles

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| Code/Claude (Watchman) | High-volume data ingestion | Calls Anthropic API, condenses raw sensor output into structured triage report. Identifies what is broken. |
| Claude (Quartermaster) | Architect | Reads triage output, reasons about fixes, writes reviewed handoffs ready for Code execution. |
| Code Agent | Worker | Executes handoffs, submits PRs. |

---

## PR and Approval Loop

The Code Agent is authorized to self-manage the fix loop without waiting for human approval between steps:

1. Create a branch for each handoff
2. Perform the fix
3. Run the relevant individual sensor (e.g., `links.py`) to verify the fix
4. Submit the PR and move the handoff to `orchestration/handoff/complete/` per the standard handoff SOP in `AGENTS.md`
5. Cowork (Claude) reviews all PRs in bulk at the start of the human session, using the peer review protocol defined in `code.md`

---

## `TRIAGE_REPORT.md` Schema

The triage API call must produce `TRIAGE_REPORT.md` in the following fixed structure to ensure reliable parsing at 08:00:

```markdown
# Triage Report — YYYY-MM-DD

## Summary
<2–3 sentence overview of overnight findings>

## Sensor Results
| Sensor | Status | Failures | Notes |
|--------|--------|----------|-------|
| links.py | PASS/FAIL | N | ... |
...

## Failures Detail
### <sensor-name>
- **Affected files:** ...
- **Severity:** P1 / P2 / P3
- **Recommended action type:** Fix / Review / Ignore

## Recommended Handoff Count
N handoffs expected from Quartermaster session.
```

---

## Execution Steps for Code

- [ ] **Step 1: Scaffold `dream.py`** — Create `orchestration/utilities/dream.py` as the new unified entry point. It should discover and execute all sensors under `orchestration/utilities/sensors/` (or equivalent), writing one JSON output per sensor to `orchestration/pipelines/outputs/`.
- [ ] **Step 2: Scaffold `triage.py`** — Create `orchestration/utilities/triage.py`. It should read all JSON files from `orchestration/pipelines/outputs/`, call the Anthropic API (haiku preferred for cost), and write `TRIAGE_REPORT.md` using the schema above. On API failure, write `TRIAGE_FAILED.flag` instead.
- [ ] **Step 3: Wire cron** — Add two cron entries: `dream.py` at 02:00 AM and `triage.py` at 02:15 AM. Document the cron setup in `orchestration/utilities/README.md`.
- [ ] **Step 4: Retire old dream scripts** — Remove or archive `orchestration/utilities/intelligence/report.py` and the nested `report/report.py`. Update `generate_report` MCP tool path accordingly (coordinate with `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md`).
- [ ] **Step 5: Add `get_report` MCP tool** — Expose `TRIAGE_REPORT.md` and `DISPATCH_SUMMARY.md` via the ben-cp MCP server so Claude (Quartermaster) can read them without filesystem fallback. Coordinate with `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md`.
- [ ] **Step 6: Verify end-to-end** — Run `dream.py` manually, confirm 11 JSON outputs. Run `triage.py` manually, confirm `TRIAGE_REPORT.md` is produced and matches schema. Confirm sentinel behavior on simulated API failure.

---

## Dependencies

- `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md` — MCP tool fixes should be implemented in coordination with Step 5 above
- Anthropic API key must be available in the local cron environment

## Acceptance Criteria

- `dream.py` runs at 02:00 AM and produces 11 JSON files in `orchestration/pipelines/outputs/`
- `triage.py` runs at 02:15 AM and produces a valid `TRIAGE_REPORT.md` matching the schema
- On API failure, `TRIAGE_FAILED.flag` is written and Claude falls back to raw JSON correctly
- Claude (Quartermaster) can read `TRIAGE_REPORT.md` via ben-cp MCP tool — no filesystem workaround needed
- Old dream scripts removed, cron updated, `generate_report` tool path corrected
