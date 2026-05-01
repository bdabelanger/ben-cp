---
status: ✅ COMPLETE — 2026-05-01
---

# Implementation Plan: Fix edit_handoff tool: preserve frontmatter and support append mode

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-29

---


## Problem

The `edit_handoff` tool is broken for non-completion edits. When called with `content`, it does a raw `fs.writeFile(sourcePath, a.content)` — a full overwrite with no frontmatter preservation. This caused Cowork to wipe the YAML frontmatter from two P1 handoffs during a session today. The files had to be restored via `git checkout`.

### Root cause (src/ben-cp.ts, line 659-660)

```typescript
} else {
  if (!a.content) throw new Error("Content required for non-completion edit.");
  await fs.writeFile(sourcePath, a.content, "utf-8");  // ← full overwrite, no frontmatter
  return { content: [{ type: "text", text: "Handoff updated." }] };
}
```

### Secondary problem: misleading schema

The tool schema exposes `next_tasks`, `completed_work`, and `session_goal` params — which **look** like they support partial progress updates. But for non-completion edits, those params are completely ignored. Only `mark_complete` + `summary` actually trigger changelog writing. Agents (including Claude) reasonably infer these params do something useful and pass them, getting no error and no effect.

---

## Required Changes

### 1. Preserve frontmatter on `content` edits

When `content` is provided (non-completion edit), read the existing file first, extract the frontmatter block, and write `frontmatter + new content` rather than replacing the whole file.

```typescript
} else {
  if (!a.content) throw new Error("Content required for non-completion edit.");
  const existing = await fs.readFile(sourcePath, "utf-8").catch(() => "");
  const fmMatch = existing.match(/^(---\n[\s\S]*?\n---\n)/);
  const frontmatter = fmMatch ? fmMatch[1] : "";
  await fs.writeFile(sourcePath, frontmatter + a.content, "utf-8");
  return { content: [{ type: "text", text: "Handoff updated." }] };
}
```

### 2. Add an `append` mode

Agents almost always want to **add** progress notes to a handoff, not replace its body. Add an `append` boolean param: when true, append `content` to the existing body rather than replacing it.

```typescript
// Schema addition:
append: { type: "boolean", description: "If true, append content to existing body rather than replacing it." }

// Implementation:
const existing = await fs.readFile(sourcePath, "utf-8").catch(() => "");
const fmMatch = existing.match(/^(---\n[\s\S]*?\n---\n)/);
const frontmatter = fmMatch ? fmMatch[1] : "";
const existingBody = fmMatch ? existing.slice(fmMatch[1].length) : existing;

if (a.append) {
  await fs.writeFile(sourcePath, frontmatter + existingBody.trimEnd() + "\n\n" + a.content, "utf-8");
} else {
  await fs.writeFile(sourcePath, frontmatter + a.content, "utf-8");
}
```

### 3. Clarify schema descriptions

Update the `content` param description to make the behavior explicit:

```
"content": "Replaces the body of the handoff (frontmatter is always preserved). For adding progress notes without replacing existing content, set append: true instead."
```

Update `next_tasks`, `completed_work`, `session_goal` descriptions to clarify they only take effect when `mark_complete: true`:

```
"next_tasks": "Next steps to record in changelog. Only used when mark_complete is true."
"completed_work": "Work completed this session. Only used when mark_complete is true."
"session_goal": "Session goal for changelog. Only used when mark_complete is true."
```

---

## Files to Modify

- `src/ben-cp.ts` — lines ~628–661 (`edit_handoff` handler)
- After changes, run `npm run build` and `ben-cp:refresh_mcp` to reload

---

## Amendment: Support `IN_PROGRESS` status and implementation plan phase

**Question from Cowork:** How should Code use `next_tasks`, `completed_work`, `session_goal` to add an implementation plan to a handoff *before* starting execution?

**Answer:** They can't right now — there's no first-class handoff lifecycle for "picking up" a task. The tool jumps from `READY` → `COMPLETE` with no in-between. This is the fix.

### Add `status: IN_PROGRESS` transition

When an agent picks up a handoff and wants to record their implementation plan before executing, `edit_handoff` should support:

```typescript
edit_handoff({
  path: "...",
  status: "IN_PROGRESS",         // new: updates frontmatter status field
  session_goal: "Implement X",  // new: written into the appended section
  append: true,
  content: `## Implementation Plan (Code, 2026-04-29)\n\n...steps...`
})
```

This should:
1. Update the frontmatter `status` field from `READY` → `IN_PROGRESS`
2. Update the `> **STATUS**` line in the body to `🔄 IN_PROGRESS — {date}`
3. Append the `content` block to the file body (using the `append` mechanic from Fix 2 above)
4. Optionally prepend `**Session Goal:** {session_goal}` to the appended content

### Updated status lifecycle

```
READY → IN_PROGRESS → COMPLETE
  ↑           ↑            ↑
add_handoff  pick up    mark_complete
             + plan       + summary
```

### `list_handoffs` should surface IN_PROGRESS

The current `status` filter only handles `READY` and `COMPLETE`. Add `IN_PROGRESS` as a valid filter value so agents can see what's actively being worked.

### Schema additions

```
"status": "Optional. Set to 'IN_PROGRESS' to mark handoff as picked up. Updates both frontmatter and body STATUS line."
"session_goal": "The goal for this session. Written as a header in the appended implementation plan section. Works on non-completion edits when append: true."
```

---

## Definition of Done

- Calling `edit_handoff` with `content` no longer strips frontmatter
- Calling `edit_handoff` with `append: true` appends to existing body
- Calling `edit_handoff` with `status: 'IN_PROGRESS'` transitions the handoff status in both frontmatter and body
- `session_goal` is written into the appended content block (not silently ignored)
- `list_handoffs` accepts `IN_PROGRESS` as a valid status filter
- Schema descriptions accurately describe what each param does
- Code can pick up a handoff, record an implementation plan, and execute — all without clobbering the original context


## Completion Summary
Upgraded the edit_handoff tool to use YAML-aware frontmatter parsing and stringification. It now preserves existing metadata and intelligently updates the status to 'COMPLETE' with a timestamp. Added a summary append feature for documentation during archival.