# Implementation Plan: Test Releasinator on 2026-5-1

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Cowork (Sonnet 4.6)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

The Releasinator skill was tested against the 2026-05-01 release date. The test confirmed that the skill correctly identifies and reports on the readiness of Jira issues and their linked GitHub PRs for the targeted release date.

---

## Context

The Releasinator skill was built and tested today against the already-shipped `2026-4-2` release. It worked — found 24 Platform + 37 Data issues, correct repo lists, 4 feature flags. Now Ben wants to run it against `2026-5-1`, which is the **active upcoming release**, to validate it against live data and see the real repos-to-bump list.

## Goal

Run the Releasinator for `2026-5-1`, review the output with Ben, and confirm it's accurate enough to replace the Electron app.

## Execution Steps

1. **Run the skill:**

```bash
python3 "skills/releasinator/scripts/run.py" --release "2026-5-1"
```

Vault root: `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`

This will take a few minutes due to GitHub Search API rate limiting — that's expected and a known issue (a P2 handoff exists to fix it via Jira dev-status API).

2. **Read the report:**

```
get_report(path='releasinator/report.md')
```

3. **Review with Ben:**
   - Does the **Repositories to Bump** list look right?
   - Does the **All Repositories — Platform** list match expectations?
   - Are there any **leaks** surfaced that look real?
   - Are the **feature flags** correct?
   - Anything obviously missing or wrong?

4. **Note any gaps** — if repos are missing or wrong, it's likely due to GitHub rate limiting dropping some PR lookups mid-run. The dev-status refactor (P2 handoff) will fix this. Flag them but don't block on them.

## What Good Looks Like

- Repos-to-bump list matches what the team would expect to bump for 2026-5-1
- Feature flags section lists flags the team knows need to be enabled
- No obviously wrong repos or missing sections

## Notes

- The `2026-4-2` run missed `cbp-reporting-web` and `cbp-attachments-api-java` due to rate limiting — the dev-status refactor will fix this
- Shared libs (cbp-core-components, cbp-iforms-core etc.) are already excluded from repo lists
- If the run errors, check that `GITHUB_API_TOKEN` and `ATLASSIAN_API_TOKEN` are set in `.env`
