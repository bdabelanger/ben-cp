# reports/tasks/data

Live task data synced from Asana and Jira. Contents change with every sync run — do not edit manually.

## Layout

```
manifest.json       Pipeline state tracker (step completion, file paths, last run date)
raw/                Synced task files (one .md per task, plus asana.md and jira.md indexes)
processed/          Normalized/transformed task data ready for downstream use
archive/            Previous sync snapshots (e.g. q2-shareout/)
```

## Owned by

`skills/tasks/` — all writes happen via the tasks sync pipeline. Do not edit directly.
