# Enforce 7-Day Retention Policy on Jira and Asana JSON Archives

## Context

The context sensor is flagging accumulating JSON archive files under `reports/projects/data/`:

**Raw Asana dumps (red flags, >750KB):**
- `reports/projects/data/raw/asana.json` — 1.4MB
- `reports/projects/data/raw/asana_all_projects.json` — 1.0MB

**Archived Jira snapshots (yellow flags, 500-650KB each):**
- `reports/projects/data/archive/archived_2026_04_05_jira_issues.json`
- `reports/projects/data/archive/archived_2026_04_06_jira_issues.json`
- `reports/projects/data/archive/archived_2026_04_09_jira_issues.json`
- `reports/projects/data/archive/archived_2026_04_10_jira_issues.json`
- `reports/projects/data/archive/archived_2026_04_11_jira_issues.json`
- `reports/projects/data/archive/archived_2026_04_16_jira_issues.json`
- `reports/projects/data/processed/jira_issues.json` — 537KB

Ben's decision: these JSON archives are not necessary to keep long-term. **Maximum 7-day rolling retention.** Anything older should be automatically purged by the pipeline.

## Logic

Implement a 7-day TTL (Time-To-Live) for JSON archive files in `skills/orchestration/pipelines/inputs/`. Files older than 7 days should be automatically purged during each pipeline run to prevent storage bloat.

1. Create `intelligence/governance/retention_policy.md` — document the 7-day TTL for JSON archive files.
2. Implement the policy in the pipeline (auto-purge on each run).
3. Do a one-time cleanup of existing archives older than 7 days.

## Execution Steps

1. [ ] Create `intelligence/governance/retention_policy.md` — document the 7-day TTL for JSON archive files.
2. [ ] Locate the JSON archival logic in the Asana/Jira pipelines.
3. [ ] Add a `cleanup_old_archives(days=7)` function that runs at the end of each harvest.
4. [ ] Run the cleanup once manually to purge files older than 7 days from the input folders.
5. [ ] Re-run `generate_report(skill='dream')` and confirm the pulse report reflects reduced file counts if applicable.

## Verification Checklist

- [ ] `intelligence/governance/retention_policy.md` exists and covers JSON archive retention
- [ ] Archive files older than 7 days are deleted (one-time cleanup done)
- [ ] Pipeline auto-purges archives older than 7 days on each run going forward
- [ ] `get_report('dream/context.json')` shows no yellow/red flags for JSON archive files
- [ ] Governance doc is referenced from the pipeline script or a comment
