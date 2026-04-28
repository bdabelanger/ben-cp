# reports/asana/data

Shared Asana data cache. Fetched once per run; downstream pipelines (status, intelligence) read from here rather than making redundant API calls.

## Layout

```
manifest.json       Pipeline state tracker (step completion, file paths, last run date)
raw/                Raw API responses
  all_projects.json     Full Asana project list
  all_tasks.json        Tasks assigned to Ben
processed/          Filtered views derived from raw cache
  platform_projects.json    Platform team projects
  intelligence_queue.json   Projects with prd_link, launch_plan_link, or Jira epic key
archive/            Previous run snapshots
```

## Owned by

`skills/asana/` — all writes happen via the Asana pipeline. Do not edit directly.
