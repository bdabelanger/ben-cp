# inputs/status-reports

Live run data for the Platform Weekly Status Report pipeline. Contents change with every run — do not edit manually.

## Layout

```
manifest.json       Pipeline state tracker (step completion, file paths, last run ID)
raw/                Raw API responses
  asana_all_projects.json   Full Asana Product team project list (step 0 output)
  jira/                     Per-epic Jira child issues ({CBP-XXXX}.json, {CBP-XXXX}_epic.json)
processed/          Filtered/transformed data ready for report generation
  asana_active.json         Platform team projects filtered from raw Asana data (step 1 output)
  jira_issues.json          Harvested and deduplicated Jira issues (step 3/4 output)
archive/            Previous run data archived by update_manifest.py reset
```

## Owned by

`tools/status-reports/scripts/` — all writes happen via pipeline scripts. Do not edit directly.
