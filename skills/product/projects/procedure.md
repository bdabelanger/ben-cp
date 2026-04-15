# Task Capture — Procedure

> Vault-native documentation. The Cowork runtime version (agent-instruction framing) lives in the plugin. This document is the reference and edit target.

---

## Classification System

Work items fall into two destinations, sometimes both:

| Item type | Destination |
| :--- | :--- |
| Initiative / Epic-level work | Asana (Platform team project) |
| User Story / Feature | Jira (CBP project) — may also create Asana task |
| Bug (internal) | Jira Bug issue type |
| Bug (CX-reported) | Jira CX Bug issue type |
| Task / chore | Jira Task or Asana task depending on scope |
| Research / Spike | Jira Research issue type |

**Routing decision tree:**
1. Is this a new initiative or project-level work? → Asana
2. Is this a story, bug, or spike against an existing CBP epic? → Jira
3. Does it need both? → Create Asana task linked to Jira ticket

---

## Workspace & Project Config

**Asana workspace GID:** `1123317448830974`
**Jira cloud ID:** `casecommons.atlassian.net`
**Jira project:** `CBP`

### Asana Custom Field GIDs

See `intelligence/product/projects/data_sources.md` for full GID table mapping. Key fields:

| Field | GID |
| :--- | :--- |
| JIRA Link | `1208818005809198` |
| Team (Platform) | `1208820967756795` → enum `1208820967756799` |
| Stage | `1208822149019495` |
| PRD | `1211632504010030` |
| Launch Plan | `1211632748689814` |

---

## Jira Issue Type Mapping

| Work item | Jira issue type | Template |
| :--- | :--- | :--- |
| Feature / Story | User Story | `../../../intelligence/product/projects/source/user-story-template.md` |
| Task / chore | Task | `../../../intelligence/product/projects/source/task-template.md` |
| Internal bug | Bug | `../../../intelligence/product/projects/source/bug-template.md` |
| CX-reported bug | CX Bug | `../../../intelligence/product/projects/source/cx-bug-template.md` |
| Research / Spike | Research | `../../../intelligence/product/projects/source/research-template.md` |

---

## Execution Steps

1. **Classify** the work item using the routing decision tree above.
2. **Identify destination** — Asana, Jira, or both.
3. **Select template** from `../../../intelligence/product/projects/source/` based on issue type.
4. **Apply metadata** — assignee, priority, fix version (release), parent epic, custom fields.
5. **Create the item** via MCP tool (`create_task_preview` for Asana, `createJiraIssue` for Jira).
6. **Confirm concisely** — one line: item type, key/GID, title. No preamble.

---

## Confirmation Format

```
✅ [Jira Bug] CBP-XXXX — "Summary text here"
✅ [Asana Task] #GID — "Task name here"
```

---

## Known Limitations

- Asana task creation via MCP requires the project GID — do not create tasks without a destination project.
- Jira issue type IDs vary by project; always use the CBP project's issue type list.
- The Asana ↔ Jira linking protocol: set the JIRA Link custom field on the Asana project, not on individual tasks. Individual task ↔ issue links are tracked via Jira's remote issue link feature.
- `QAFE` issue types are excluded from all reports — do not create QAFE issues via this skill.
