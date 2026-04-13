# Bug Triage Report: CBP-2573
**Issue Title:** Duplicate Service interactions when adding multiple services on a note (intermittently)
**Project Context:** CBP-2924 (Notes - Bulk Service Notes)
**Status:** Sub-task / Bug under CBP-2924
**Date:** 2026-04-12

## Findings
- **Intermittency**: The bug is flagged as intermittent, suggesting a race condition or state synchronization issue during the "bulk" creation phase of service notes.
- **Scope**: Exclusive to the addition of *multiple* services on a single note. This likely points to the loop logic or the API batch processing in the frontend or backend related to CBP-2924 development.
- **Project Affiliation**: Strongly tied to CBP-2924. It is not an independent regression but a maturing bug within the active development of the Bulk Service Notes feature.

## Recommended Actions
1. **Developer Triage**: Assigned developer for CBP-2924 should inspect the `service_interaction` payload generation.
2. **Reproduction**: Attempt to trigger the bug by adding 5+ services rapidly to a note in the dev/QA environment.
3. **Tracking**: Maintain as a sub-task of CBP-2924; do not split into a separate initiative as it blocks the primary GA criteria for that project.

## Verification
- Search of vault `jira_issues.json` confirms parentage and status.
- No direct source code for the service creation logic found in this vault repository (appears to be an external dependency or sibling project).
