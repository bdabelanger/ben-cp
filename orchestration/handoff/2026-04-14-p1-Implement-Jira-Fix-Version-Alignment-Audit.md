# Implementation Plan: Implement Jira Fix Version Alignment Audit

> **Prepared by:** Code (Gemini) (2026-04-14)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS: 🔲 READY — pick up 2026-04-14**

---

> **Strategic Note for the "Code" Agent:**
> In `step_1_asana_ingest.py`, the `ga_target` is already being extracted into the milestones dictionary. Claude should focus its energy on the date parsing comparison in `step_4_report_generator.py`, ensuring it handles None or N/A values gracefully to avoid breaking the report build.

---
project: Infrastructure / Pipelines
status: READY
version: 2026.04.14
tags: [python, jira, asana, alignment-audit]
agent_sync: Gemini-Native
---
# Handoff: Implement Jira Fix Version Alignment Audit

## Goal
Enhance the `product/projects` pipeline to identify "Lagging" stories where the assigned Jira Fix Version release date is later than the Asana project's GA target date.

## Context
We currently consolidate Epics and Projects but lack "Release Intelligence." We need to know if 20% of stories are scheduled for a release *after* the GA date committed in Asana.

## 🚀 Strategic PM Perspective
*   **Closing the Commitment Gap**: This audit moves the vault from "vibe-based" tracking to a hard data comparison between Asana promises (GA Target) and Jira reality (Fix versions).
*   **Risk Signal Prioritization**: Distinguishing between **Lagging** (missed dates) and **Unmapped** (missing commitments) is critical. "Unmapped" stories are the highest risk because they represent invisible work.
*   **Technical Robustness**: The agent must ensure `None/NA` handling in `step_4` is bulletproof. Reporting failures due to missing Jira dates are unacceptable; the Auditor must simply flag them as "Unmapped" and keep moving.
*   **Future Tuning**: Strictly flag all drift for now. In a future iteration, we may introduce a "Grace Period" config for minor alignment drift (e.g., <3 days).

## Required Changes

### 1. `step_2_atlassian_fetch.py`
- **Field Expansion**: Ensure the JQL search explicitly requests `fixVersions` in the `fields` parameter.
- **Release Metadata**: Verify the Atlassian API response for `fixVersions` includes the `releaseDate`. If not, implement a secondary fetch to `rest/api/3/version/{id}` to cache version metadata.

### 2. `step_3_jira_harvest.py`
- **Standardization**: Process the `fixVersions` array for each issue. 
- **Effective Release Date**: Extract the latest `releaseDate` from the assigned versions and store it as a top-level `effective_release_date` string (format: `YYYY-MM-DD`) in the harvested JSON.

### 3. `step_4_report_generator.py`
- **Date Comparison Logic**: For each project in `asana_data`, retrieve the `ga_target` from the `milestones` object.
- **Story Categorization**:
    - **Aligned**: `effective_release_date` <= `ga_target`.
    - **Lagging**: `effective_release_date` > `ga_target`.
    - **Unmapped**: No `fixVersions` or no `releaseDate` found.
- **Reporting**: Add a "Release Alignment Audit" table to each project section in the status report, showing counts for Aligned, Lagging, and Unmapped stories.

### 4. `asana_push_corrections.py` (Optional / P2)
- **Risk Flagging**: Define a new custom field GID (e.g., "Jira Sync Risk").
- **Logic**: If a project has >10% "Lagging" stories, update this field to "At Risk" during the push phase.

## Success Criteria
1. The Weekly Status Report includes a "Release Alignment Audit" summary for every active project.
2. Stories without a Fix Version are explicitly flagged as "Unmapped" risk.
3. The pipeline correctly handles cases where a story has multiple Fix Versions by selecting the latest date.
