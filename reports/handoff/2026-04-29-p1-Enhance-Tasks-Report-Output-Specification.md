---
title: "Enhance Tasks Report Output Specification"
priority: P1
assigned_to: Cowork
status: READY
date: 2026-04-29
---
# Implementation Plan: Enhance Tasks Report Output Specification

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** Cowork
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: 🔲 READY — pick up 2026-04-29

---

**Goal:** Modify the 'tasks' report generation pipeline (Skill: `tasks`) to provide a more actionable output for human review and agent consumption.

**Required Changes:**
1.  **Content Inclusion:** The report must include the actual task content/description for each listed item, not just the title.
2.  **Cross-System Linking:** For every Asana task, the report must list all associated Jira issues (and vice versa).
3.  **Sorting Logic:** All tasks must be sorted first by **Due Date**, and secondarily by **Priority** (P1 > P2 > P3...).
4.  **Presentation Layer Rule:** The default output of the report should *only* surface prioritized titles and links, suppressing full content unless explicitly requested by a human user.
5.  **Utility vs. Actionable Data:** Task counts are useful for high-level dashboards but should not be the primary focus of the actionable task list.

This change requires modification to the `tasks/SKILL.md` or associated pipeline scripts within the repository structure. Please coordinate with Code Agent for implementation.
## Execution Steps

- [🔲] **Pipeline Refactor**: Update `skills/tasks/run.py` to include task descriptions and cross-system links.
- [🔲] **Sorting & Filtering**: Implement sorting by due date and priority; add `--verbose` flag.
- [🔲] **Documentation**: Update `skills/tasks/SKILL.md` to reflect the new output specification.
- [🔲] **Verification**: Generate the report and confirm output format.


---

## Scoping Notes (Cowork, 2026-04-29)

### Current State of `skills/tasks/run.py`

The script fetches Asana tasks and Jira issues, writes raw snapshots to `reports/tasks/data/raw/`, and generates `reports/tasks/report.md`.

**What's already fetched but not surfaced:**
- `notes` field on Asana tasks ✅ already in `opt_fields`
- `description` field on Jira issues ✅ already in `fields` param

**What's missing:**
- Notes/description not rendered in `build_report()`
- No cross-system Asana ↔ Jira linking logic
- Sort is `modified_at` (Asana default) — not due date or priority
- No presentation layer toggle (verbose vs. titles-only)

### Required Changes → Code Locations

| # | Change | Where |
|---|---|---|
| 1 | Surface task content in report | `build_report()` — add notes under each task entry |
| 2 | Cross-system linking | New helper function — parse Asana `notes` for `CBP-XXXX` keys; check Jira `description` for Asana URLs |
| 3 | Sort by due date → priority | `build_report()` — sort tasks before rendering |
| 4 | Default titles+links only; `--verbose` for full content | Add `argparse` flag; gate notes rendering on flag |

### Key Notes for Code Agent
- Jira `description` is ADF (Atlassian Document Format JSON) — needs an ADF-to-plaintext helper before rendering
- Asana has no native `priority` field in the standard API — check `intelligence/product/projects/asana_field_definitions.md` for the custom field GID
- Priority sort order: P1 > P2 > P3 > P4 > no priority

### Files to Modify
- `skills/tasks/run.py` — primary
- `skills/tasks/SKILL.md` — update output spec description
