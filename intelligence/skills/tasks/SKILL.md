# Task Capture Skill

- **agent:** Code (Gemini)
- **type:** skill

---
title: Task Capture Skill — Standardized Intake
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

## Classification Logic

| Signal | Result |
| :--- | :--- |
| "bug", "broken", "regression" | Jira Bug |
| "user story", "story" | Jira Story |
| "research", "investigate" | Jira Research |
| "prep", "demo", "launch plan" | Asana Task (PM) |
| "new feature", "new initiative" | Asana Project + Jira Project |

---

## Routing (Asana)

| Keyword | Project GID |
| :--- | :--- |
| "GP", "Permissions" | PD - Small Projects (Default) |
| "Notes", "Service Record" | Engage - Notes |
| "Enroll", "Intake" | Enrollments |
| (Default) | PD - Small Projects |

