# Implementation Plan: Redesign handoff tool API: edit_handoff + archive_handoff + standard sections

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-29

---


## Context

The handoff tool API has grown organically and now has three problems:

1. **`edit_handoff` does too much** — it handles both mid-session edits and completion/archiving as two modes of one tool. The `mark_complete` path does archiving + changelog; the `content` path does a destructive full overwrite. These are fundamentally different operations and shouldn't share a tool.

2. **No standard sections** — agents have no guidance on *what to append* at each lifecycle stage. Every agent invents its own structure. This makes handoffs inconsistent and harder to parse programmatically.

3. **Lifecycle has a gap** — handoffs jump from `READY` → `COMPLETE` with nothing in between. There's no `IN_PROGRESS` state, so agents can't signal "I've picked this up and here's my plan" before executing.

The fix has three parts: rename the completion operation, add `IN_PROGRESS` support, and define standard named sections that agents append dynamically.

---

## Part 1 — Split `edit_handoff` and introduce `archive_handoff`

### New tool: `archive_handoff`

Extract the `mark_complete` path from `edit_handoff` into its own tool. Naming it `archive_handoff` makes the operation obvious — it moves the file, writes the changelog, and closes the handoff.

**Schema:**
```typescript
{
  name: "archive_handoff",
  description: "Mark a handoff complete and archive it. Moves the file to reports/handoff/archive/, updates STATUS to COMPLETE, and writes a changelog entry. Use only when all execution steps are done.",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string", description: "Handoff filename (omit handoff/ prefix)" },
      summary: { type: "string", description: "One-paragraph summary of what was done and any flags for human user" },
      session_goal: { type: "string", description: "Goal of the session, used as changelog entry title" },
      completed_work: { type: "array", items: { path, change, status }, description: "Files changed this session" },
      next_tasks: { type: "array", items: "string", description: "Follow-on tasks for the next agent or human" },
      version_bump: { type: "string", enum: ["major", "minor", "patch"] }
    },
    required: ["path", "summary", "session_goal", "completed_work", "next_tasks"]
  }
}
```

### Updated `edit_handoff`

Remove `mark_complete`, `summary`, and changelog params from `edit_handoff` — those now belong to `archive_handoff`. Add `append` and `status` params. The tool becomes purely about updating a live handoff body.

**Updated schema:**
```typescript
{
  name: "edit_handoff",
  description: "Update a live handoff. Use append: true to add a section without replacing existing content (frontmatter is always preserved). Use status: 'IN_PROGRESS' to signal the handoff has been picked up.",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string" },
      content: { type: "string", description: "Section content to write. Replaces body unless append: true." },
      append: { type: "boolean", description: "If true, appends content to existing body. Use this for adding implementation plans, review notes, or progress updates." },
      status: { type: "string", enum: ["IN_PROGRESS"], description: "Set to IN_PROGRESS when picking up a handoff. Updates both frontmatter status field and body STATUS line." },
      session_goal: { type: "string", description: "Written as a bold header above the appended content block. Only used when append: true." }
    },
    required: ["path"]
  }
}
```

### Updated `list_handoffs`

Add `IN_PROGRESS` as a valid `status` filter value so agents can see what's actively in flight.

---

## Part 2 — Standard sections

Three immutable, append-only section types. Once written, a section is never edited — new sections stack below. This creates an auditable, chronological record of a handoff's life.

---

### Section 1: `## Implementation Plan` — required before any execution begins

**Who:** The executing agent (Code or Local) on pickup.
**When:** Before touching any files. If a handoff arrives without one, the agent MUST write it first.
**Rules:** Not editable after appended. If the plan changes, append a new `## Update` section explaining the deviation.
**Status transition:** Appending this section moves status to `IN_PROGRESS`.

```markdown
## Implementation Plan ([Agent], [YYYY-MM-DD])

**Session Goal:** [one line]

### Steps
1. [Step 1]
2. [Step 2]
...

### Files to modify
- `path/to/file.ts` — what changes
```

Tool call pattern:
```
edit_handoff(path, status='IN_PROGRESS', append=True, session_goal='...', content='## Implementation Plan...')
```

---

### Section 2: `## Review: [State]` — Cowork review gate

**Who:** Any agent can open a review. Only Cowork can close one.
**When:** Any agent needing input, approval, or unblocking appends `## Review: [Requested]`. Cowork responds by appending `## Review: [Approved]` or `## Review: [Needs Revision]`.
**Rules:** Not editable after appended. Reviews stack — a handoff may have multiple `[Requested]` / `[Approved]` / `[Needs Revision]` entries. Execution may not proceed past a `[Needs Revision]` until a subsequent `[Approved]` is appended.
**Completion gate:** Only Cowork can trigger `archive_handoff`. Cowork does so only after a final `## Review: [Approved]` confirming all requirements are met.

```markdown
## Review: [Requested] ([Agent], [YYYY-MM-DD])

**Question / context:**
[What the agent needs — approval to proceed, answer to a question, sign-off on output]
```

```markdown
## Review: [Approved] (Cowork, [YYYY-MM-DD])

[Confirmation and any notes. If this is the final approval, Cowork follows with archive_handoff.]
```

```markdown
## Review: [Needs Revision] (Cowork, [YYYY-MM-DD])

**Required changes:**
[Specific changes needed before this can be approved]
```

---

### Section 3: `## Update` — mid-session progress, blockers, or deviations

**Who:** Any agent, any time.
**When:** Agent needs to report progress, log a blocker, explain a deviation from the plan, or signal a pause.
**Rules:** Not editable after appended. Updates stack chronologically. If blocked, follow with a `## Review: [Requested]` to pull in Cowork.

```markdown
## Update ([Agent], [YYYY-MM-DD])

**Status:** [In progress / Paused / Blocked / Deviated from plan]

[What happened, what's done, what's not, and why]

**Completed so far:**
- [x] Step 1
- [ ] Step 2

**Blocker / deviation:** [description — follow with Review: Requested if Cowork input needed]
```

---

### Lifecycle with sections

```
READY
  └─ edit_handoff → ## Implementation Plan   (status → IN_PROGRESS)

IN_PROGRESS
  ├─ edit_handoff → ## Update                (anytime)
  ├─ edit_handoff → ## Review: [Requested]   (any agent needs input)
  ├─ edit_handoff → ## Review: [Approved]    (Cowork only)
  └─ edit_handoff → ## Review: [Needs Revision] (Cowork only)

IN_PROGRESS + final Review: [Approved]
  └─ archive_handoff                          (Cowork only → COMPLETE)
```

**Key rule:** `archive_handoff` is Cowork-only and requires a `## Review: [Approved]` confirming completion in the handoff body before archiving.

---

## Part 3 — AGENTS.md and SKILL.md updates

### `skills/handoff/SKILL.md`

Replace the **Tool Utility** table and add a **Standard Sections** reference using the three section names and rules defined in Part 2.

| Tool | Who | When |
|---|---|---|
| `add_handoff` | Any agent | Create a new handoff |
| `list_handoffs` | Any agent | Discover open work — filter by READY / IN_PROGRESS / ALL |
| `get_handoff` | Any agent | Read a handoff before picking it up |
| `edit_handoff` | Any agent | Append a standard section: `## Implementation Plan`, `## Review: [State]`, or `## Update` |
| `archive_handoff` | **Cowork only** | Mark complete after final `## Review: [Approved]` — moves to archive/, writes changelog |

### `AGENTS.md` — MCP Tools table

Replace current `edit_handoff` row and add `archive_handoff`:

```
| `edit_handoff`   | Append standard sections to a live handoff (Implementation Plan, Review, Update). Always append: true. Never edit existing sections. |
| `archive_handoff` | Cowork-only. Mark complete and archive after final Review: [Approved]. Writes changelog. |
```

Also add to **Cowork agent role** (`governance/agents/cowork.md`): Cowork is the sole agent authorized to append `## Review: [Approved]`, `## Review: [Needs Revision]`, and to call `archive_handoff`.

---

## Execution Steps

1. **`src/ben-cp.ts`** — implement `archive_handoff` tool handler (extract from `edit_handoff` `mark_complete` path)
2. **`src/ben-cp.ts`** — update `edit_handoff` handler: add `append`, `status: IN_PROGRESS`, `session_goal`; remove `mark_complete` + changelog params; preserve frontmatter on all writes
3. **`src/ben-cp.ts`** — add `IN_PROGRESS` to `list_handoffs` status filter
4. **`src/ben-cp.ts`** — register `archive_handoff` in the tools list
5. **`skills/handoff/SKILL.md`** — add Lifecycle section, Standard Sections, update Tool Utility table
6. **`AGENTS.md`** — update MCP Tools table rows for `edit_handoff` and `archive_handoff`
7. `npm run build` + `ben-cp:refresh_mcp`

## Definition of Done

- `edit_handoff` no longer has `mark_complete` or changelog params
- `edit_handoff` with `append: true` appends without clobbering frontmatter or body
- `edit_handoff` with `status: 'IN_PROGRESS'` updates frontmatter and body STATUS line
- `archive_handoff` archives the file, writes changelog; is Cowork-only in documentation
- `list_handoffs` accepts `IN_PROGRESS` as a status filter
- `SKILL.md` documents the lifecycle diagram, three standard sections with rules, and updated Tool Utility table
- `AGENTS.md` MCP Tools table reflects `edit_handoff` and `archive_handoff` with who/when
- `governance/agents/cowork.md` documents Cowork as sole approver and archiver
