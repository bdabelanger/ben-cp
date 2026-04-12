# DoD Helper — Procedure

> Vault-native documentation. The Cowork runtime version lives in the plugin. This is the reference and edit target.

---

## Mode Detection

- **Single-task mode:** Ben shares an Asana or Jira URL → process that task only
- **Batch mode:** No URL → fetch all of Ben's open Asana tasks, process each

---

## Single-Task Flow

1. **Fetch** the task (via `get_task` for Asana, `getJiraIssue` for Jira)
2. **Read** existing description and notes
3. **Detect task type** — Feature, Bug, Research, Chore, etc.
4. **Check for existing DoD** — if present, offer to update rather than replace
5. **Check for subtasks** — if multi-step work, propose subtask breakdown before DoD
6. **Ask targeted questions** — use the question set for the detected task type (see below)
7. **Draft DoD** — structured, plain-language criteria
8. **Post back** — Asana: update task notes field. Jira: add comment (do not edit description)

---

## Question Sets by Task Type

**Feature / User Story:**
- Who is the user and what are they trying to accomplish?
- What does "working" look like from the user's perspective?
- Are there edge cases or error states to handle?
- What's the acceptance bar for QA?

**Bug:**
- What's the expected behavior?
- What's the actual behavior?
- Is there a reproduction path?
- What environments/browsers are affected?

**Research / Spike:**
- What question needs to be answered?
- What's the deliverable — a doc, a decision, a prototype?
- Who needs to review/approve the output?

**Chore / Task:**
- What does "done" look like concretely?
- Is there a verification step?

---

## DoD Format (Quality Bar)

- Plain dashes, no checkboxes
- No markdown headers inside the DoD block
- 3–7 criteria (not more)
- Plain label, not a markdown header: `Definition of Done` not `## Definition of Done`
- Example:

```
Definition of Done
- Feature works end-to-end in staging
- Edge case X handled with appropriate error message
- Unit tests added for core logic
- QA sign-off received
- No regressions in related flows
```

> **Why these rules:** Asana and Jira both render plain dashes cleanly. Checkboxes and markdown headers create rendering issues in both tools.

---

## Posting Behavior

| Destination | How to post |
| :--- | :--- |
| Asana | Update task `notes` field — append DoD block, preserve existing content |
| Jira | Add comment — do not edit the issue description |

---

## Batch Mode Flow

1. Fetch all of Ben's open Asana tasks (`get_my_tasks`)
2. For each task without an existing DoD:
   - Detect task type from title/description
   - Generate a draft DoD using reasonable defaults (no interview in batch mode)
   - Post back to each task
3. Summarize: N tasks updated, list titles
