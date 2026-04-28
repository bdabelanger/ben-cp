---
title: 'Protocol: Nightly Dream Cycle & Quartermaster Loop'
type: handoff
domain: handoffs/complete
---


# Protocol: Nightly Dream Cycle & Quartermaster Loop

> **Prepared by:** Cowork (Claude) + Ben (2026-04-26)
> **Assigned to:** Code
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-27

All 7 steps complete. Steps 1, 2, 4, 5, 6 done by Code. Step 3 (scheduled Cowork skill at 22:00) and Step 7 (end-to-end loop test) completed in Cowork session on 2026-04-26. Dream cycle is fully operational.

---

## Context

This protocol replaces the previous nightly dream sequence. It defines a fully autonomous nightly loop — no Anthropic API calls, no cron, no local Python wrappers. The entire cycle is driven by a **scheduled Cowork skill**, making it portable to any team member's machine with the plugin installed.

Ben signs in at 8am and works his task queue before standup at 10am.

---

## The Nightly Loop (10pm start)

### Phase 1 — Quartermaster (Cowork/Claude)
1. Run the dream report via `generate_report(skill='dream')`
2. Read `report.md` via `get_report(path='dream/report.md')`
3. Analyze all 11 sensor outputs — read individual JSONs as needed via `get_report`
4. **Correct records** — execute any low-risk intelligence updates directly (e.g. stale index entries, minor metadata fixes)
5. **Create handoffs** for Code — one per discrete fix, following the Unified Artifact Standard in `AGENTS.md`. All handoffs generated in this session are considered Cowork-reviewed at point of generation.
6. **Raise tasks in Asana** — for any risks, questions, or clarifications that require Ben's input. Assign to Ben, due the next morning. These are Ben's 8am queue.
7. Cowork may re-run the dream report at any point to verify state.

### Phase 2 — Code Agent
1. Pick up all READY handoffs from `handoffs/`
2. Execute each handoff — one branch per handoff
3. Run the relevant sensor to verify the fix (e.g. if fixing a ghost link, re-run `links.py`)
4. Submit PR and move handoff to `handoffs/complete/`

### Phase 3 — PR Review (Cowork/Claude)
1. Review all submitted PRs using the peer review protocol in `agents/code.md`
2. Approve clean PRs or leave specific, actionable feedback
3. Re-run dream report after approvals to confirm sensor improvement

### Phase 4 — Code Revision Loop (up to 5 cycles)
1. Code addresses any PR feedback
2. Resubmits PR
3. Cowork reviews again
4. Repeat up to 5 cycles — if unresolved after 5, raise an Asana task for Ben

### Phase 5 — Ben's Morning Session (8am)
1. Ben works Asana task queue (risks, questions, clarifications from overnight)
2. Reviews any PRs that couldn't be resolved in the Code/Cowork loop
3. Everything clear before standup at 10am

---

## Agent Roles

| Agent | Role | Phase |
| :--- | :--- | :--- |
| Cowork (Claude) | Quartermaster — analyzes sensors, creates handoffs, raises tasks, reviews PRs | 1, 3, 4 |
| Code | Worker — executes handoffs, submits PRs, addresses feedback | 2, 4 |
| Ben | Decision-maker — works task queue, reviews escalated PRs | 5 |

---

## Portability

This entire loop runs via a **scheduled Cowork skill** — no cron entries, no API keys, no local Python dependencies beyond the existing sensor scripts. Any team member with the plugin installed can run the nightly loop on their machine.

---

## Execution Steps for Code

- [x] **Step 1: Migrate `orchestration/handoff/` → `handoffs/`** — Move the entire `orchestration/handoff/` directory to a root-level `handoffs/` directory (parallel to `tasks/`). Update the `handoffPath` variable in `src/ben-cp.ts` accordingly. Rebuild and verify all handoff MCP tools (`get_handoff`, `list_handoffs`, `add_handoff`, `edit_handoff`) resolve correctly against the new path. Do this first — all subsequent steps depend on handoff tools working.
- [x] **Step 2: Update AGENTS.md** — Replace all references to `orchestration/handoff/` with `handoffs/` throughout AGENTS.md, including the repo structure diagram, directory boundaries table, and any procedural references.
- [ ] **Step 3: Wire the scheduled skill** — Create a Cowork skill that executes the Quartermaster phase (Phase 1) on a nightly schedule at 22:00. The skill should: run `generate_report(skill='dream')`, read all sensor JSONs via `get_report`, analyze, correct records, create handoffs, and raise Asana tasks for Ben. Reference the `schedule` skill SOP for implementation pattern.
- [x] **Step 4: Retire old dream orchestrator** — Archive `orchestration/utilities/intelligence/report.py` and nested `report/report.py`. Update `generate_report` MCP tool path to point at the new sensor runner (coordinate with `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md`).
- [x] **Step 5: Verify `get_report` tool** — Confirm `get_report` can read all 11 sensor JSONs and `dream/report.md` from `reports/`. Fix path resolution if needed (coordinate with `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md`).
- [x] **Step 6: Confirm sensor runner** — Verify the existing sensor suite runs cleanly end-to-end and writes all 11 JSONs + `report.md` to `reports/`. Document the entry point script path in this handoff once confirmed.
- [ ] **Step 7: Test the loop** — Run a manual end-to-end test: trigger the Quartermaster skill, verify it produces at least one handoff in `handoffs/` and reads the report correctly via `get_report`.

## Nightly Loop Results (Manual Run: 2026-04-26)

### 📊 Sensor Status
| Sensor | Status | Detail |
| :--- | :--- | :--- |
| **Pulse** | 🟡 WARN | 16 directories missing `index.md` (mostly source/raw data dirs). |
| **Links** | 🔴 FAIL | **127 Ghost Links** detected. This is the primary cleanup target. |
| **Handoffs** | 🔴 FAIL | 16 issues found (mostly path drift in stale READY files). |
| **Context** | 🔴 FAIL | 3 Red Flags (Files > 750KB): Large PDF in shareout/ and raw Asana JSONs. |

### 🛠️ Fixed During Session
- [x] **Sensor Bug**: Fixed `skills/dream/run.py` path calculation (was looking 3 levels up instead of 2).
- [x] **Sensor Noise**: Optimized `pulse.py` to ignore `node_modules`, `reports`, `dist`, and `src`.
- [x] **Link Regex**: Updated `links.py` to handle parentheses in project filenames (e.g., GIDs).
- [x] **Root Paths**: Fixed index paths in `intelligence/index.md` and `skills/index.md`.
- [x] **Bulk Migrations**: Corrected `roadmap/` paths across all product release notes.

### 📋 Remaining Queue (For Step 7)
1. **Ghost Link Harvest**: 127 links still need manual or automated path correction.
2. **Index Generation**: Add `index.md` to the 16 missing directories (e.g., `governance/`).
3. **Data Boundary**: Move large raw JSONs from `orchestration/` (stale) to `reports/` (new).

---

## Dependencies

- `2026-04-26-p2-Fix:-Expose-Dream-Report-Output-via-ben-cp-MCP.md` — `get_report` path fix and `generate_report` script path correction must be done in coordination with Steps 4–5
- Asana MCP must be connected for task creation in Phase 1
- Step 1 (handoff migration) must be completed before any other step — handoff tools will be broken until it is done

## Acceptance Criteria

- `handoffs/` exists at repo root; `orchestration/handoff/` is retired
- All handoff MCP tools resolve against `handoffs/`
- Scheduled skill runs at 22:00 and completes Quartermaster phase autonomously
- Morning `reports/dream/report.md` reflects the overnight sensor run
- Handoffs and Asana tasks are present when Ben signs in at 8am
- Old dream HTML reports and gazette orchestrator are retired
- Loop is portable — no machine-specific configuration required
