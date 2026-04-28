# Implementation Plan: Add asana as first dream pipeline and fix pipeline order and naming

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

Dream pipeline currently: `tasks → releasinator → status → intelligence-harvest → intelligence-scan`

Correct order: `asana → tasks → releasinator → status → intelligence`

## Change 1 — Add asana as first pipeline in skills/dream/run.py

```python
PIPELINES = [
    {
        'name': 'asana',
        'script': os.path.join(REPO_ROOT, 'skills', 'asana', 'run.py'),
        'report': 'reports/asana/report.md',
        'label': 'Asana Snapshot',
    },
    { 'name': 'tasks', ... },
    { 'name': 'releasinator', ... },
    { 'name': 'status', ... },
    { 'name': 'intelligence', 'label': 'Intelligence', ... },  # renamed from intelligence-harvest
]
```

Remove `intelligence-scan` from PIPELINES (moving to sensor — see dream sensor restructure handoff).
Rename `intelligence-harvest` label to `'Intelligence'`.

## Change 2 — Add asana summary parser in build_pipeline_section()

```python
elif name == 'asana':
    m = re.search(r'projects_fetched:\s*(\d+)', content or '')
    count = m.group(1) if m else '?'
    lines.append(f'{count} projects fetched — stage breakdown in index.md')
```

## Change 3 — Update SKILL.md pipeline table

```
| asana        | reports/asana/report.md        | Fetches raw projects + tasks from Asana API   |
| tasks        | reports/tasks/report.md        | My Tasks (Asana + Jira)                       |
| releasinator | reports/releasinator/report.md | Release readiness — auto                      |
| status       | reports/status/report.md       | Platform Status                               |
| intelligence | —                              | Intelligence harvest                          |
```

## Verification
- [ ] Dream cycle runs asana first
- [ ] `reports/asana/raw/all_projects.json` written before tasks pipeline runs
- [ ] `intelligence-scan` removed from PIPELINES
- [ ] SKILL.md updated
