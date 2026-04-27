---
title: Implementation Plan Implement Jira Fix Version Alignment Audit
type: handoff
domain: handoffs/complete
---

# Implementation Plan: Implement Jira Fix Version Alignment Audit

> **Prepared by:** Code (Gemini) (2026-04-14); Refined by Cowork (2026-04-15)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2 — Major pipeline enhancement (additive, not critical path)
> **STATUS**: ✅ COMPLETE

Implemented the Jira Fix Version Alignment Audit with 4-bucket logic (Aligned, Stalled, Lagging, Unmapped) in the project reporting pipeline. Mapped visual indicators to emoji-key standards and ensured all symbols are left-aligned for consistency. Successfully ran the pipeline generating the expected alignment tables inside project summaries and formatting the issue list exactly as required.

---

> **Strategic Note for the "Code" Agent:**
> In `step_1_asana_ingest.py`, the `ga_target` is already being extracted into the milestones dictionary. Focus energy on `step_3_jira_harvest.py` (adding `status.name` alongside `effective_release_date`) and the 4-bucket categorization logic in `step_4_report_generator.py`. Bullet-proof `None/NA` handling — reporting failures are unacceptable.

---

## Goal

Enhance the `product/projects` pipeline to surface **Release Alignment** intelligence: whether work that Asana promises for a GA date is actually scheduled *and moving* in Jira.

Fix Version answers "is this committed to a release?" — but Jira `status.name` answers "is the work actually progressing?" Together they produce the complete signal.

## Context

We currently consolidate Epics and Projects but lack Release Intelligence. The gap: a story can be assigned to a Fix Version that aligns with the Asana GA target while sitting at **To Do** with no velocity behind it. Sprint visibility helps week-to-week, but Fix Version + Status is the real tell for whether the GA commitment is credible.

> **Why `status.name` over `statusCategory.name`:** statusCategory collapses the entire active workflow into a single "In Progress" bucket — covering everything from raw development through UAT Approved. The actual Jira status name (e.g., "To Do", "In Progress", "In QA", "UAT Approved", "Done") is required to distinguish meaningful health signals. A story at "UAT Approved" days before release is in a fundamentally different state from one at "To Do" with the same Fix Version.

## 🚀 Strategic PM Perspective

- **The Real Commitment Gap**: The question isn't just "is this scheduled after the GA date?" — it's "is this scheduled *correctly* AND is anyone actually working on it?" Fix Version + Status closes both gaps simultaneously.
- **The Stalled Story Problem**: The highest-value new signal is a story with an on-time Fix Version but a stagnant status ("To Do", "Backlog"). These are invisible to sprint-based views and represent commitments with no engine behind them.
- **Unmapped = Invisible Work**: Stories with no Fix Version remain the highest-risk category because they represent work with no release commitment at all.
- **Technical Robustness**: `None/NA` handling in `step_4` is non-negotiable. Flag gracefully as "Unmapped" — never break the report build.
- **Future Tuning**: Flag all drift strictly for now. A configurable "Grace Period" (e.g., <3 days) can be added in a future iteration.

## Required Changes

### 1. `step_2_atlassian_fetch.py`
- **Field Expansion**: Ensure the JQL search explicitly requests `fixVersions` and `status` in the `fields` parameter.
- **Release Metadata**: Verify the Atlassian API response for `fixVersions` includes `releaseDate`. If not, implement a secondary fetch to `rest/api/3/version/{id}` to cache version metadata per version ID.

### 2. `step_3_jira_harvest.py`
- **Effective Release Date**: Process the `fixVersions` array per issue. Extract the **latest** `releaseDate` across all assigned versions and store as `effective_release_date` (format: `YYYY-MM-DD`).
  - Rationale for latest date: conservative pick — if a story spans versions, we assume it ships with the latest scheduled one.
- **Status Capture**: Extract `fields.status.name` for each issue and store as `jira_status` (raw string — do not normalize or map to a category).
- Store both fields as top-level keys in the harvested JSON per issue.

### 3. `step_4_report_generator.py`
- **Date Comparison Logic**: For each project in `asana_data`, retrieve `ga_target` from the `milestones` object.
- **4-Bucket Story Categorization** (evaluate in this order):

  | Bucket | Condition | HTML Meaning / Emoji (`styles/emoji-key.md`) |
  | :--- | :--- | :--- |
  | **Unmapped** | No `fixVersions` or no `releaseDate` | `👀 Not Set` (Data Quality risk) |
  | **Lagging** | `effective_release_date` > `ga_target` | `🛑 Off Track` (Date drift — scheduled after GA) |
  | **Stalled** | `effective_release_date` <= `ga_target` AND `jira_status` in `["To Do", "Backlog", "Open"]` | `⚠️ At Risk` (On-time Fix Version but no velocity) |
  | **Aligned** | `effective_release_date` <= `ga_target` AND `jira_status` not in stalled set | `🎯 On Track` (Committed and moving) |

  > **Stalled status set**: `["To Do", "Backlog", "Open"]` — Code should confirm these match the actual Jira workflow status names in use. If the project uses non-standard statuses, surface them in the report rather than silently miscategorizing.

- **Reporting Elements**: 
  - **Audit Summary Table**: Add a "Release Alignment Audit" table to each project section, showing counts for On Track, At Risk, Off Track, and Unmapped stories.
  - **Issue-Level Display**: For each issue listed in the report, display its release information below the description (e.g., `Release: [Version Name]`). 
    - If Unmapped, display `Release: not set 👀`. 
    - If Stalled (At Risk), show a `⚠️` warning sign next to it. 
    - If Lagging (Off Track), show a `🛑` symbol.
  - **Project Status Escalation**: Evaluate the overall health of the project based on these buckets. If a significant percentage of issues are `⚠️ At Risk` or `🛑 Off Track`, the report should strongly signal that the **project itself** is At Risk or Off Track.

### 4. `asana_push_corrections.py` (Optional / Future P3)
- **Risk Flagging**: Define a custom field GID (e.g., "Jira Sync Risk").
- **Logic**: If a project hits thresholds for `🛑 Off Track` or `⚠️ At Risk` issues, automatically update the Asana project status.
- **Hold**: Threshold values are provisional. Define with human user before implementing.

## Success Criteria
1. The Weekly Status Report includes a "Release Alignment Audit" table for every active project.
2. Stories without a Fix Version are flagged as **Unmapped**.
3. Stories with an on-time Fix Version but stagnant Jira status are flagged as **Stalled**.
4. `status.name` is stored raw — no normalization — so the report reflects actual Jira workflow state.
5. The pipeline handles multiple Fix Versions per story by selecting the latest release date.
6. `None/NA` in any date or status field never crashes the report build.
