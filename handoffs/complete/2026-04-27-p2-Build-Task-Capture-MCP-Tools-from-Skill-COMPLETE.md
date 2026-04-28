# Implementation Plan: Build Task Capture MCP Tools from Skill

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

5 MCP tools implemented and compiled: capture_task (classifier + router), create_asana_project, create_asana_task, create_jira_issue (with ADF + double-newline fix), link_asana_jira. .env loaded at server startup via loadEnv(). All constants from handoff hard-coded (GIDs, cloud IDs, account IDs). Build clean.

---

# Build Task Capture MCP Tools from Skill

> **Prepared by:** Cowork (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

Ben has a working Claude Chat "Task Capture" skill he uses to route raw notes into Asana and Jira with the right metadata, without switching contexts. The skill is battle-tested and well-documented. The goal is to build this out as proper MCP-callable tools so it works natively in Cowork/Code sessions without relying on the Chat interface.

The skill covers:
- Classifying captures (new initiative, PM readiness, engineering work, cross-system)
- Routing to Asana (projects, tasks, custom fields) and/or Jira (stories, bugs, CX bugs, research, tasks, QAFE)
- Applying the correct template and metadata
- Confirming what was created — concisely

---

## Source Material

All reference material is already in the repo:

### Skill Logic
The full system prompt lives in the skill instructions shared with this handoff. Key logic to encode:

**Classification rules:**
- New roadmap initiative → new Asana project + matching Jira "Project" issue, link via JIRA Link field
- PM readiness task → Asana task in matching project (or PD - Small Projects as fallback), assign to Ben
- Engineering work → Jira CBP issue with correct type + template
- Cross-system → both Asana project + Jira Project, linked

**Phase signals to watch for:**
- UAT signals ("blocker", "broken", "not working", "regression", "can't", "failing") → default Jira Bug, high priority, fast
- Release signals ("prep", "demo", "connect with", "KB", "launch plan") → default Asana task on relevant project, assigned to Ben

**Project routing hints:**
- GP / Granular Permissions → search GP-prefixed projects first
- Notes, WLV, DataGrid, Dynamic pages → match by name
- Security, Prowler, SOC, CJIS → security cluster
- Reporting, Reveal, Redshift → reporting cluster
- Integrations, Zapier, API, Nylas → integrations cluster
- Infrastructure, Kafka, Rails, Node, EC2, Karpenter → DevOps cluster
- Vague or no match → PD - Small Projects (`1208693459152262`)

### Asana GIDs
Full authoritative reference: `skills/asana/schemas/asana-custom-fields.md`

Key constants to hard-code:
- Workspace GID: `1123317448830974`
- Ben's assignee GID: `1208822152029926`
- PD - Small Projects GID: `1208693459152262`
- Asana REST API base: `https://app.asana.com/api/1.0`

### Jira Constants
- Cloud ID: `d4deabe8-6b83-4008-8fae-dfe274d33bfe`
- Project key: `CBP`
- Ben's Jira account ID: `629dfdc29b728c006a928e90`
- Issue URL format: `https://casecommons.atlassian.net/browse/CBP-XXXX`

### Jira Issue Type IDs
| Type | ID |
|---|---|
| Project | 10000 |
| User Story | 10057 |
| Bug | 10011 |
| CX Bug | 10013 |
| Research | 10064 |
| Task | 10009 |
| QAFE | 10065 |

Do not create subtypes (Backend, Frontend, GraphQL, QA) — those are engineer-created.

### Issue Templates
Encode these as template strings the tools apply when creating issues. Templates:

**User Story** — Summary: `[Product Area] - [description]`
Fields: PRD link, Introduction (Figma/Loom), user story statement, Use cases (Given/When/Then), Edge cases, Out of scope.

**Bug** — Summary: `[Product Area] - [description]`
Fields: Description, Steps to reproduce, Expected/Actual behavior, Environment, Severity checkbox, Links (Asana project, related story), Estimate, phase found.

**CX Bug** — Summary: `[Product Area] - [description]`
Fields: Customer/tenant info, Description, Steps to reproduce, Expected/Actual, Workaround available, Release blocker, Links, Priority.

**Research** — Summary: `[Product Area] - [description]`
Fields: Objective, Background/Context, Scope (in/out), Approach checkboxes, Definition of Done, Links, Estimate, target completion.

**Task/Sub-task** — Summary: `[Product Area] - [description in sentence case]`
Fields: Introduction, what needs doing and why, Acceptance criteria checklist, Links (Asana project, Figma).

---

## Tools to Build

### `capture_task`
The primary entry point. Takes raw text input from Ben and:
1. Classifies the capture type
2. Infers the target system(s)
3. Calls the appropriate sub-tools
4. Returns a concise confirmation (system, item name, key fields set)

No clarifying questions unless the capture is truly ambiguous with no reasonable inference. Make a call, act, confirm.

### `create_asana_project`
Creates a new Asana project for a roadmap initiative.
- Applies defaults: Stage=Backlog, Team=Platform, Product Assignee=Ben
- Sets Release Quarter/Month if mentioned
- Sets JIRA Link field after Jira Project issue is created
- Note: some fields (Launch Plan, Release Quarter, Stage) cannot be set via MCP — flag these to Ben for manual update in Asana UI

### `create_asana_task`
Creates a PM readiness task in an existing Asana project.
- Searches for matching project by name, falls back to PD - Small Projects
- Always assigns to Ben
- Sets due date if mentioned

### `create_jira_issue`
Creates a Jira issue in CBP with the appropriate template applied.
- Accepts type (User Story / Bug / CX Bug / Research / Task / QAFE)
- Applies the correct template structure to the description field
- **Critical:** After creating via `createJiraIssue`, always follow up with `editJiraIssue` using the `fields` object to fix formatting — `createJiraIssue` double-escapes newlines, rendering descriptions as single lines
- Checkbox syntax (`- [ ]`) is escaped rather than rendered — note in confirmation that manual conversion is needed in Jira UI

### `link_asana_jira`
Sets the JIRA Link custom field on an Asana project.
- Field GID: `1208818005809198`
- Stores full URL: `https://casecommons.atlassian.net/browse/CBP-XXXX`

---

## Known Bugs / Workarounds to Encode

| Bug | Workaround |
|---|---|
| `createJiraIssue` double-escapes newlines | Always follow up with `editJiraIssue` on every multi-line issue |
| Checkbox syntax escaped in Jira | Note in confirmation — user converts manually in Jira UI |
| `create_task_preview` ignores `due_on` and project assignment | Use direct Asana REST API POST via authenticated Chrome tab |
| Atlassian MCP sometimes unresponsive mid-session | Fresh conversation session resolves; fallback is drafting content for manual entry |
| Asana project-level custom fields not settable via MCP | Flag to Ben for manual update in Asana UI; still set task-level fields via API |

---

## Asana Project GIDs (for routing)

| Project | GID |
|---|---|
| Notes - Services section | `1211726272848115` |
| Enrollments bulk data entry | `1211631356870657` |
| Notes consistent dates | `1211631360190574` |
| PD - Small Projects (catch-all) | `1208693459152262` |

---

## Confirmation Format

Keep confirmations tight. Example:

```
✅ Asana project created: "Notes - Autosave"
   Stage: Backlog | Team: Platform | Assignee: Ben
   ⚠️ Set Release Quarter, Launch Plan manually in Asana UI

✅ Jira Project created: CBP-3102
   https://casecommons.atlassian.net/browse/CBP-3102
   JIRA Link field set on Asana project.
```

---

## Verification Checklist

- [ ] `capture_task` correctly classifies at least: new initiative, PM readiness, bug, CX bug, user story, research, cross-system
- [ ] Phase signal detection works (UAT → Jira Bug fast; Release → Asana task)
- [ ] Jira descriptions render correctly after the double-newline fix is applied
- [ ] Asana custom field GIDs match `skills/asana/schemas/asana-custom-fields.md`
- [ ] JIRA Link field is populated on Asana project after cross-system creation
- [ ] Fallback routing to PD - Small Projects works when no project match found
- [ ] Confirmation output is concise — no unnecessary prose
