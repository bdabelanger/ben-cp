---
title: Releasinator — Release Readiness Report
type: skill
domain: skills/releasinator
---

# Releasinator — Release Readiness Report

> **Trigger:** Ben says "Run the releasinator for [release name]" or "Release readiness for [release]"
> **Agent:** Code (Claude)
> **Output:** `reports/releasinator/report.md`

---

## What it does

Replaces the legacy `cbp-pivotal-tracker-doc-generator` Electron app. For a given CBP release:

1. Fetches all Jira issues assigned to that fix version
2. Discovers all involved repositories from these issues
3. Compares `master...develop` for each repo to identify everything "in flight"
4. Identifies repos that need a bump (`develop` ahead of `master`)
5. Deep scans PRs merged into `develop` since the last production push for "leaked" Jira keys
6. Filters leaks to exclude issues already in the release or marked as "Done" in Jira
7. Extracts feature flags and BE Migrations
8. Writes `reports/releasinator/report.md`

---

## Invocation

Run the script with the release name as an argument:

```bash
python3 "skills/releasinator/scripts/run.py" --release "2026-5-1"
```

With an optional JQL filter:

```bash
python3 "skills/releasinator/scripts/run.py" --release "2026-5-1" --jql "assignee = bisoye"
```

All paths are relative to the repo root:
`/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`

---

## Credentials

The script reads from the repo root `.env`:
`/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/.env`

- `GITHUB_USERNAME`
- `GITHUB_TOKEN`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

Do not hardcode or echo these values.

---

## After running

Confirm to Ben:

```
✅ Releasinator complete for {releaseName} — {N} repos to bump, {M} leaks found
   Report: reports/releasinator/report.md
```

Then offer to open the report. If Ben wants to view it, read and display `reports/releasinator/report.md`.

---

## Troubleshooting

- **Rate limit errors from GitHub:** The script has built-in exponential backoff (up to 8 retries). If it still fails, wait a few minutes and re-run.
- **`requests` not installed:** Run `pip3 install requests` then retry.
- **`.env` not found:** Confirm the Electron app repo is at `/Users/benbelanger/GitHub/cbp-pivotal-tracker-doc-generator`.
- **No issues found:** Verify the release name exactly matches the Jira fix version name (e.g. `2026-5-1` not `2026.5.1`).
