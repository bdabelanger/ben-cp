# Implementation Plan: Update Stale Release Dates on Notes Datagrid Jira Issues

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Cowork (Sonnet 4.6)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

Several in-progress issues in CBP-2736 (Notes - Notes Datagrid) still carry a release date of `2026-4-2`, which is three weeks past. The project is at GA stage as of today (2026-04-27) and these stale dates are causing noise in readiness reporting.

Affected issues (all currently in QA or merged to QA):
- [CBP-3183](https://casecommons.atlassian.net/browse/CBP-3183) — Notes - Lagging Case Details page when page size = 50 · Release: 2026-4-2
- [CBP-3105](https://casecommons.atlassian.net/browse/CBP-3105) — Notes - Migrate Start/End dates from service interactions to service notes · Release: 2026-4-2
- [CBP-3254](https://casecommons.atlassian.net/browse/CBP-3254) — FE - write the note start/end date on the old service note module · Release: 2026-4-2
- [CBP-3111](https://casecommons.atlassian.net/browse/CBP-3111) — Service Note - Note type switch confirmation dialog (Notes - Bulk Service Notes) · Release: 2026-4-2 / 2026-5-1
- [CBP-3112](https://casecommons.atlassian.net/browse/CBP-3112) — FE - Service Note - Trash icon tooltip (Notes - Bulk Service Notes) · Release: 2026-4-2
- [CBP-2831](https://casecommons.atlassian.net/browse/CBP-2831) — Issue with End Date Validation in Service Notes · Release: 2026-4-2

## Goal

Update the fix version / release field on each issue to the next appropriate release (`2026-5-1` is the likely target for most) so readiness reporting reflects reality.

## Execution Steps

1. For each issue above, check current status and which release they're realistically targeting based on where they are in the workflow (QA, merged to QA, product review, etc.)
2. Update the fix version field to `2026-5-1` unless the issue is already resolved/released, in which case leave it or set to `2026-4-2` as appropriate.
3. For CBP-3111 which already shows dual release dates, confirm the correct single target and update accordingly.
4. Add a comment on each updated issue noting the date was updated during triage (brief — one line).

## Verification

- [ ] No open in-progress issues in Notes Datagrid or Bulk Service Notes carry a release date of `2026-4-2`
- [ ] All updated issues have a valid future release date set
