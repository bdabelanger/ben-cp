---
title: Task Capture — Skill & Procedure
type: skill
domain: skills/tasks
---

# Task Capture Skill

> **Tool:** `capture_task` (MCP)
> **Agent:** Code / Cowork
> **Output:** Created Asana task or Jira issue (with link)

---

## What it does

This is the primary entry point for capturing work items into Asana and Jira. It takes raw text from a user or another agent, automatically classifies it, routes it to the correct project, and applies the appropriate template.

### Features
- **Automatic Classification**: Detects if an item is a Bug, Story, Research, or PM Task.
- **Routing**: Maps keywords (e.g., "GP", "Notes", "Enroll") to specific Asana projects.
- **Templating**: Applies rich markdown templates (e.g., "Steps to Reproduce" for bugs) automatically.
- **Double-Sync**: For new initiatives, it creates both an Asana project and a linked Jira Project issue.

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

## Usage

Agents should use the `capture_task` tool directly.

```json
{
  "text": "The granular permissions modal is failing to save on the latest UAT build."
}
```

### Optional Fields
- `acceptance_criteria`: List of ACs (markdown bulleted list)
- `figma_link`: URL to Figma designs
- `asana_link`: URL to an existing Asana project (overrides auto-routing)

---

## Jira Issue Type Mapping

| Work item | Jira issue type | Template |
| :--- | :--- | :--- |
| Feature / Story | User Story | `../../intelligence/product/projects/source/user-story-template.md` |
| Task / chore | Task | `../../intelligence/product/projects/source/task-template.md` |
| Internal bug | Bug | `../../intelligence/product/projects/source/bug-template.md` |
| CX-reported bug | CX Bug | `../../intelligence/product/projects/source/cx-bug-template.md` |
| Research / Spike | Research | `../../intelligence/product/projects/source/research-template.md` |

---

## Execution Steps (Manual/Agentic)

1. **Classify** the work item using the routing decision tree above.
2. **Identify destination** — Asana, Jira, or both.
3. **Select template** from `../../intelligence/product/projects/source/` based on issue type.
4. **Apply metadata** — assignee, priority, fix version (release), parent epic, custom fields.
5. **Create the item** via MCP tool (`capture_task` or specialized Atlassian tools).
6. **Confirm concisely** — one line: item type, key/GID, title. No preamble.

---

## Workspace & Project Config

- **Asana workspace GID:** `1123317448830974`
- **Jira cloud ID:** `casecommons.atlassian.net`
- **Jira project:** `CBP`

---

## Confirmation Format

```
✅ [Jira Bug] CBP-XXXX — "Summary text here"
✅ [Asana Task] #GID — "Task name here"
```
