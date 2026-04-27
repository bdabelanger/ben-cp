---
title: Asana Custom Field GID Reference
type: schema
domain: skills/asana/schemas
---

# Asana Custom Field GID Reference

- **Agent:** Code
- **Source:** asana-custom-fields.md (task-capture skill)
- **Status:** ✅ Complete
- **Date Ingested:** 2026-04-27
- **Strategic Theme:** Data Integrity / API Automation
- **Target Audience:** All agents interacting with Asana via scripts or MCP.

> Use these GIDs directly when creating or updating Asana projects and tasks. Never search for them at runtime.

---

## Release Quarter

**Field GID:** `1208821111273828`

| Value | GID |
|---|---|
| Q1 2026 | `1211354478726842` |
| Q2 2026 | `1211441089905124` |
| Q3 2026 | `1211441089905125` |
| Q4 2026 | `1211441089905126` |

---

## Release Month(s)

**Field GID:** `1210909549820601`

| Value | GID |
|---|---|
| Jan 26 | `1211441356703315` |
| Feb 26 | `1211441356703316` |
| Mar 26 | `1211441356703317` |
| Apr 26 | `1211441356703318` |
| May 26 | `1211441356703319` |
| Jun 26 | `1211441356703320` |
| TBD | `1211711315692742` |

> **Note:** Do not set Release Date(s) — it is a sprint-cycle enum that updates with each release and will go stale. Release Month(s) is sufficient.

---

## Stage

**Field GID:** `1208822149019495`

| Value | GID |
|---|---|
| Backlog | `1208822011920664` |
| Discovery | `1208822149019498` |
| Development | `1208822149019499` |
| In QA | `1209847080766035` |
| In UAT | `1209847080766036` |
| Beta | `1208822149019500` |
| GA | `1208822149019501` |

---

## Team

**Field GID:** `1208820967756795`

| Value | GID |
|---|---|
| Platform | `1208820967756799` |
| Reporting | `1208820967756798` |
| Specialty | `1209101939195843` |
| DevOps | `1209860073668304` |

---

## Type

**Field GID:** `1209127915359058`

| Value | GID |
|---|---|
| Strategic | `1209127915359061` |
| Upgrade / Tech Mod | `1209127915359062` |
| BAU | `1209127915359063` |
| 5% | `1209127915359064` |

---

## Roadmap Category

**Field GID:** `1211763621285210`

| Value | GID |
|---|---|
| Case Management | `1211763621285218` |
| Configurability | `1212990185667311` |
| Security & Compliance | `1211763621285215` |
| Interoperability | `1211763621285217` |
| Navigation | `1212555058482965` |
| Workflows | `1211763621285213` |
| Technology | `1211763621285219` |

---

## Priority

**Field GID:** `1208818049849054`

| Value | GID |
|---|---|
| High | `1208818049849057` |
| Medium | `1208818049849058` |
| Low | `1208818049849059` |

---

## People

- **Product Assignee field GID:** `1211092108897416`
- **Ben Belanger user GID:** `1208822152029926`

---

## Documentation & Link Fields

| Field | GID | Notes |
|---|---|---|
| JIRA Link | `1208818005809198` | Text field. Store full URL: `https://casecommons.atlassian.net/browse/CBP-XXXX` |
| PRD | `1211632504010030` | Confluence link |
| Launch Plan | `1211632748689814` | Confluence link — must be set manually in Asana UI |

---

## Key Date Fields

| Field | GID |
|---|---|
| Discovery Start | `1208817993811507` |
| Dev Start | `1208818118276550` |
| QA Start | `1211631943113717` |
| UAT Start | `1210467277124544` |
| Beta Start | `1208818118032458` |
| GA | `1208818124273418` |

---

## Defaults for New Asana Projects

- **Stage** → Backlog (`1208822011920664`)
- **Team** → Platform (`1208820967756799`) unless context clearly suggests otherwise
- **Product Assignee** → Ben (`1208822152029926`)
- **Release Quarter** → set if mentioned, otherwise omit
- **Release Month** → TBD (`1211711315692742`) if quarter is set but month isn't specified

---

## Key Constraints

- `create_task_preview` does not reliably set `due_on` or assign tasks to specific projects — use direct Asana REST API POST via authenticated Chrome tab for full field support.
- Multi-homing tasks requires the confirmed task GID (from Asana URL) before `update_task` can add it to additional projects.
- Asana project-level custom fields (Release Quarter, Stage, Roadmap, JIRA Link, Product Assignee, Launch Plan) **cannot be set via MCP tools** — must be updated manually in the Asana UI.
