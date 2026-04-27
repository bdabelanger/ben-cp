# Implementation Plan: Build Standup Note Harvester Skill — Gmail Gemini Notes → Tasks

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

# Build Standup Note Harvester Skill — Gmail Gemini Notes → Tasks

> **Prepared by:** Cowork (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

Ben's daily standups are recorded by Gemini, which emails a structured meeting notes summary to `ben.belanger@casebook.net` after each meeting. Ben wants to stay present in standups rather than context-switching to capture tasks — so this skill reads those emails and automatically acts on the action items Gemini identified, routing them to the right system (Asana or Jira) using the same classification logic as the task-capture skill.

The Gmail MCP connector is not yet set up. For now this skill uses the **Atlassian MCP + Jira API** for Jira items and the **Asana MCP** for Asana items. Gmail access will be via Google MCP when available — the skill should be designed so Gmail reading is a swappable input layer.

---

## Email Format — What Gemini Produces

Gemini sends a consistent email after each standup from `gemini-notes@google.com`. Subject line format:
```
Notes: "🧍 CBP - Standup" {Month} {Day}, {Year}
```

The email body has two structured sections that matter:

### Section 1: Summary (narrative, ignore for task creation)
Free-form prose summarizing the meeting. Skip this.

### Section 2: "Suggested next steps" (parse this)
Bullet list. Each item follows this exact pattern:
```
[Person Name] Action verb: Description sentence. Additional context sentence.
```

Examples from a real email:
```
[Ben Belanger] Review Ticket: Review ticket 2990 issues. Provide tiebreaker decision for clarification points.
[Russell Ward] Implement Deletable: Implement 'deletable' prop on compact attachment. Hide trash can icon for view-only users.
[Bisoye Atolagbe] Send PR: Send PR 3235 link to Howard Yee. Request review and administrative merge.
[Blessing Adesina, Bisoye Atolagbe] Fix Multi-select: Partner on PR fix for multi-select defaults. Ensure quick verification and merge.
[The group] File Bug: File bug report regarding the link styling regression.
```

Key parsing observations:
- Assignee(s) are always in `[Square Brackets]` at the start
- `[The group]` = unassigned / team-wide item — treat as Asana task assigned to Ben for triage
- Multiple assignees are comma-separated inside the brackets
- The action label before the colon is a short verb phrase (ignore for routing — use full description)
- Jira ticket numbers appear inline as bare numbers (e.g. "ticket 2990", "PR 3235") — extract these for linking

---

## Classification Logic

Use the same routing rules as the task-capture skill, applied per action item:

| Signal | Route to |
|---|---|
| Assigned to Ben only | Asana task on relevant project OR Jira depending on nature |
| Assigned to an engineer (Russell, Bisoye, Blessing, Tuan, Pierre) | Jira task/bug, assigned to that engineer |
| Assigned to CX/QA (Yi, Sindhu, Uday, Sai) | Jira task or Asana task |
| Assigned to `[The group]` | Asana task assigned to Ben for triage |
| Multi-assignee | Create one item, list all assignees in description |
| Contains "bug", "regression", "broken", "fix", "error" | Jira Bug |
| Contains "PR", "merge", "implement", "deploy" | Jira Task |
| Contains "review", "clarify", "coordinate", "notify", "check", "demo" | Asana task assigned to Ben |
| Contains Jira ticket number (e.g. "ticket 2990", "CBP-2990") | Link to that Jira issue in description |

**Default for ambiguous Ben-only items:** Asana task in PD - Small Projects (`1208693459152262`).

**Do not create subtasks** (Backend, Frontend, GraphQL, QA) — those are engineer-created.

---

## People → Jira Account ID Mapping

| Name | Jira Account ID |
|---|---|
| Ben Belanger | `629dfdc29b728c006a928e90` |
| Russell Ward | (look up via `lookupJiraAccountId`) |
| Bisoye Atolagbe | (look up via `lookupJiraAccountId`) |
| Blessing Adesina | (look up via `lookupJiraAccountId`) |
| Tuan | (look up via `lookupJiraAccountId`) |
| Yi Liu | (look up via `lookupJiraAccountId`) |

**On first run:** Look up each engineer's Jira account ID once and cache in `skills/standup-harvester/schemas/people.json`. Reuse on subsequent runs — don't look up on every execution.

**Asana assignee:** Always Ben (`1208822152029926`) unless item is clearly a PM action for a specific other person (rare — use judgment).

---

## Jira Constants

- Cloud ID: `d4deabe8-6b83-4008-8fae-dfe274d33bfe`
- Project key: `CBP`
- Jira base URL: `https://casecommons.atlassian.net`
- Issue URL format: `https://casecommons.atlassian.net/browse/CBP-XXXX`

**Issue type IDs:**
| Type | ID |
|---|---|
| Task | 10009 |
| Bug | 10011 |
| CX Bug | 10013 |

**Jira newline bug:** `createJiraIssue` double-escapes newlines. Always follow up with `editJiraIssue` using the `fields` object to fix formatting on every multi-line issue.

---

## Asana Constants

- Workspace GID: `1123317448830974`
- Ben's assignee GID: `1208822152029926`
- PD - Small Projects GID: `1208693459152262`
- Full custom field GID reference: `skills/asana/schemas/asana-custom-fields.md`

---

## Skill Invocation

Ben will say something like:
> "Harvest tasks from today's standup notes"
> "Process my standup email from April 27"
> "Pull action items from this morning's standup"

The skill should:
1. Find the most recent Gemini standup email (or the one matching a given date)
2. Parse the "Suggested next steps" section
3. Classify and route each action item
4. Create the items in Jira and/or Asana
5. Confirm concisely — one line per item created

---

## Gmail Access (Interim Approach)

Until a Gmail MCP is connected, the skill should instruct the agent to:
1. Ask Ben to forward or paste the email content if Gmail MCP is unavailable
2. OR use the Google MCP connector if available in the session
3. The parsing and routing logic is the same regardless of input source

Design the SKILL.md so the Gmail-reading step is clearly separated from the parse-and-route step — this makes it easy to swap in a Gmail MCP later without rewriting the whole skill.

---

## Jira Task Template (for standup-harvested items)

Keep it lightweight — these are action items, not full user stories:

```
## Summary
[Product Area if known] - [Action item text verbatim from Gemini notes]

## Context
Harvested from Gemini standup notes — {meeting date}

## Assignee
{Name from brackets}

## Action
{Full description from the next steps item}

## Links
- Meeting notes email: {Gmail link if available}
- Related Jira issue: {CBP-XXXX if a ticket number was mentioned}
```

---

## Asana Task Format (for standup-harvested items)

- **Name:** `[Standup {date}] {Action label}: {brief description}`
- **Notes:** Full description from the next steps item + meeting date
- **Assignee:** Ben (`1208822152029926`)
- **Project:** Best-match existing project, or PD - Small Projects as fallback
- **Due:** Same day as meeting (today) unless context suggests otherwise

---

## Output / Confirmation Format

After processing, confirm concisely:

```
✅ Standup harvest complete — Apr 27, 2026 (8 action items)

Jira (3):
  ✅ [Task] CBP-3261 — "Implement 'deletable' prop on compact attachment" → Russell
  ✅ [Bug] CBP-3262 — "Link styling regression — links appear underlined and purple" → [The group]
  ✅ [Task] CBP-3263 — "Check environment for null ID error reproducibility" → Sai

Asana (5):
  ✅ #GID — "[Standup 4/27] Review: Ticket 2990 issues + tiebreaker decision" → Ben
  ✅ #GID — "[Standup 4/27] Initiate: Release Nator process + UAT coordination" → Ben
  ✅ #GID — "[Standup 4/27] Review: Merged service note fixes vs CSMS expectations" → Ben
  ✅ #GID — "[Standup 4/27] Clarify: AC for Sodiq — address field required status" → Ben
  ✅ #GID — "[Standup 4/27] Send PR: CBP-3235 link to Howard Yee for admin merge" → Bisoye (noted)

⚠️ Skipped: [Yi Liu] Assist Case — routed to Asana for Ben to delegate manually
```

---

## SKILL.md Instructions to Agent

The SKILL.md should instruct the agent to:

1. **Get the email** — via Google MCP `get_email` or by asking Ben to paste it
2. **Extract** the "Suggested next steps" section
3. **Parse** each bullet: assignee(s), action label, full description, any Jira ticket numbers mentioned
4. **Classify** each item using the routing table above
5. **Create** items via Atlassian MCP (Jira) and Asana MCP, applying the lightweight templates
6. **Fix Jira formatting** — always follow `createJiraIssue` with `editJiraIssue` for multi-line descriptions
7. **Confirm** with the summary format above
8. **Never ask clarifying questions** unless an item is completely unactionable — make a call and note it

---

## People Cache File to Create

On first run, create `skills/standup-harvester/schemas/people.json`:

```json
{
  "Ben Belanger": {
    "jira_account_id": "629dfdc29b728c006a928e90",
    "asana_gid": "1208822152029926",
    "role": "PM"
  },
  "Russell Ward": { "jira_account_id": null, "role": "engineer" },
  "Bisoye Atolagbe": { "jira_account_id": null, "role": "engineer" },
  "Blessing Adesina": { "jira_account_id": null, "role": "engineer" },
  "Tuan": { "jira_account_id": null, "role": "engineer" },
  "Yi Liu": { "jira_account_id": null, "role": "cx" },
  "Sindhu": { "jira_account_id": null, "role": "cx" },
  "Uday": { "jira_account_id": null, "role": "cx" },
  "Sai Krishnan": { "jira_account_id": null, "role": "engineering" }
}
```

Populate `null` values via `lookupJiraAccountId` on first run and save the file. Subsequent runs skip the lookup.

---

## Verification Checklist

- [ ] Parser correctly extracts all "Suggested next steps" items from the sample email
- [ ] `[The group]` items are routed to Asana as Ben-owned triage tasks
- [ ] Multi-assignee items list all names in description
- [ ] Jira ticket numbers mentioned inline (e.g. "ticket 2990") are extracted and linked
- [ ] Jira formatting fix (`editJiraIssue`) is applied after every `createJiraIssue`
- [ ] People cache file is written on first run and reused on subsequent runs
- [ ] Ben-only review/coordination items go to Asana, not Jira
- [ ] Engineer implementation/bug items go to Jira with correct assignee
- [ ] Confirmation output matches the format above — concise, one line per item
- [ ] Skill works when email is pasted as text (Gmail MCP not required)
