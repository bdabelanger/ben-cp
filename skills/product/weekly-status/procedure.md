# Weekly Status Report — Procedure

> Vault-native documentation. The Cowork runtime version lives in the plugin. This is the reference and edit target.

---

## Mode Detection

- **Single-project mode:** Ben shares an Asana project URL → extract project GID → fetch only that project → full card + data quality for that project only. Report header: `# Platform Status — [Project Name] — [Date]`
- **Batch mode:** No URL → fetch all Platform team projects → full weekly report

---

## Step 1 — Fetch Platform Asana Projects

Use `search_objects` with `resource_type: "project"` and `opt_fields: "name,custom_fields,due_on,permalink_url,current_status_update.status_type"`.

Filter in Python: keep projects where Team field GID `1208820967756795` has `enum_value.gid == "1208820967756799"` (Platform). Expected ~79 projects.

> If `search_objects` returns fewer than expected, paginate via `get_projects` with `limit=100` using `next_page.offset` until `next_page` is null.

**Extract per project:**
- JIRA Link (GID `1208818005809198`) — full URL; extract CBP key from end
- PRD (GID `1211632504010030`) — include if populated
- permalink_url
- Stage (GID `1208822149019495`)
- Stage milestone dates: QA Start `1211631943113717`, UAT Start `1210467277124544`, Beta Start `1208818118032458`, GA `1208818124273418`, GA Month `1210909549820601`
- `current_status_update.status_type` → `last_status_type`

**Exclude:** projects where `current_status_update.status_type == "complete"`

**Bucket by Stage:**
| Bucket | Stages |
| :--- | :--- |
| 🟢 Active | Development, In QA, In UAT, Beta, GA |
| 🟣 Discovery | Discovery, Study |
| ⚪ Backlog | On hold, Backlog |

**Sort:** GA Month ascending (soonest first), then Stage descending as tiebreaker (GA → Beta → In UAT → In QA → Development → Discovery → Study → Backlog → On hold → N/A).

---

## Step 2 — Fetch Jira Child Issues

For Active projects with a Jira link, fetch all child issues via `searchJiraIssuesUsingJql`:

```
project = CBP AND parent in (CBP-XXXX, CBP-YYYY, ...) ORDER BY parent ASC, status ASC
```

**Important:** Batch parent tickets in groups of 5–6 to avoid silent result truncation at 100 results.

**Fields:** `summary`, `status`, `assignee`, `issuetype`, `timeoriginalestimate`, `timespent`, `parent`, `fixVersions`, `priority`

**Exclude:** `issuetype.name == "QAFE"` — filter out after fetching, before any processing.

**Status bucketing — overrides first:**
| Status name | Override bucket |
| :--- | :--- |
| Blocked - Needs Review | To Do |
| Blocked - Third-Party | To Do |
| QA Revise | In Progress |

Then by `statusCategory`: In Progress → in-flight, To Do → backlog, Done → done.

**Time conversion:** seconds ÷ 28800 = days (8h/day)

**Fix versions:** strip `Platform-` prefix for display. Join multiples with ` / `.

---

## Step 3 — Render Active Project Cards

Each Active project renders as a card:

```
### [Project Name](asana-url) · [CBP-KEY](jira-url) · Stage
PRD: url                          ← omit if blank

`▓▓▓▒▒░░░ 3 done · 2 in progress · 3 to do`

`██████░░░░ 18.2d act / 25.0d est (73%)`

* ✅ QA - Mar 20
* ⚠️ UAT - Apr 3
* ❓ Beta - not set
* ⚠️ GA - Apr 9

⚠️ Flag text

**Done:** N issues (~Xd est, ~Yd logged)
**In Progress:** N issues · ~Xd est remaining
- [CBP-KEY](url) — Summary — Assignee · Status · Xd est / Yd act · P2 · 2026-3-2
**To Do:** N issues
- [CBP-KEY](url) — Summary — Assignee · Status · Unestimated 👀 · P2 · 👀 Unprioritized
```

**Card rules:**
- Progress bar: 1 char per ticket. `▓`=Done `▒`=In Progress `░`=To Do. Inline code block.
- Time bar: always show. 10-char bar filled to act/est ratio. `⚠️` prefix if over budget. `👀 no time data` if no data. `👀 Xd logged / no estimates` if actuals only.
- Milestone bullets: all four in order (QA → UAT → Beta → GA). Beta optional if not set. Use ❓ for unset dates. Emoji and ❓ are mutually exclusive per milestone.
- Milestone emoji logic — requires today's date AND current stage rank (Dev=1, In QA=2, In UAT=3, Beta=4, GA=5):
  - ✅ date past AND stage rank ≥ required rank
  - ❌ date past AND stage rank < required rank
  - ⚠️ date future AND previous milestone was ❌ (cascades forward)
  - 🎯 date future, no at-risk conditions
- In Progress bullets sort by priority (P1 first). Include status name, time, priority, fix version.
- To Do bullets same format.
- Done: summary line only — no individual bullets.
- Assignee: first name only. "Unassigned" if none.
- Summaries: truncate to ~70 chars.

**Flags (surface when actionable):**
- ⚠️ N unassigned stories with [Milestone] in Xd — assign soon (fires within 7 days of next milestone)
- Pipeline slip: next milestone passed >7 days ago with open stories → frame as question, not verdict
- Ballooning: total timespent > total timeoriginalestimate by >25% with open work → narrative note, not flag line
- `last_status_type` of `at_risk` or `off_track` → mention alongside fresh flags, or briefly alone if no fresh flags

**Minimal card** (no Jira link or 0 open stories): header + `👀 no time data` time bar + ⚠️ warning. No progress bar or story sections.

---

## Step 4 — Report Structure

```
# Platform Weekly Status — [Date]

## ⚙️ Data Quality
## 📋 Summary
---
## 🟢 Active Projects
## 🟣 Discovery
## ⚪ Backlog
```

**⚙️ Data Quality** (computed from In Progress issues only):
- **Estimates:** X of Y in-progress issues have estimates (Z%). Sub-bullet per engineer: `estimated/total (pct%)`. 👀 if 0% or <20% with ≥3 issues.
- **Actuals:** X of Y issues in QA have time tracked (Z%). QA statuses only (Merged to QA, In QA, QA Revise). Sub-bullet per engineer. 👏 for highest %. 👀 for 0 or <20% with ≥3 issues. Designer/QA lead 👀 is expected — don't call it out.
- **Unprioritized:** X of Y 👀 in-progress issues have no fix version set (Z%). Sub-bullet per Asana project: `Project: unprio/total (pct%)` + 👀 if 100%.

**📋 Summary** — PM narrative, first person. Link every project name and CBP key. Per project: three-number breakdown (X done · Y in progress · Z to do) + priority breakdown of open work (👀 P1, P2, P3). 🎯 prefix for human action items. Next Steps: 2–4 bullets, all 🎯, sorted P1 first.

**🟣 Discovery** — one-liner per project. Jira link optional — include if set, no warning if missing.

**⚪ Backlog** — one-liner per project. No warnings, no Jira lookup.

---

## Key Notes

- Jira uses "Project" as the top-level issue type (not Epic) in this workspace
- `search_objects` is recency-biased — paginate if project count seems low
- Parse large payloads with Python, not jq
- Fix versions = releases, not sprints — use "release" in narrative text
- `Release Date(s)` field is a historical log — never use for overdue logic
