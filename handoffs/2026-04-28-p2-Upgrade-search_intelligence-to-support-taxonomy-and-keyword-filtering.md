# Implementation Plan: Upgrade search_intelligence to support taxonomy and keyword filtering

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

`search_intelligence` currently runs `grep -rli` — pure full-text search across `.md` files. Intelligence files now have a `taxonomy` frontmatter field (e.g. `taxonomy: Notes, Workload View`) that enables structured filtering. The upgrade should support both modes while keeping full-text as the fallback.

**Source file:** `src/ben-cp.ts`  
**Current implementation:** find the `search_intelligence` handler — it's a single `grep -rli` execFile call.

---

## New Tool Signature

```typescript
// All params optional except at least one of query or taxonomy must be provided
{
  query?: string,     // full-text keyword search (existing behavior)
  taxonomy?: string,  // match against frontmatter taxonomy field
  domain?: string     // scope to subdirectory (existing behavior)
}
```

Validation: throw if neither `query` nor `taxonomy` is provided.

---

## Behavior

### taxonomy filter
Parse the `taxonomy:` line from each file's YAML-style frontmatter header:

```
---
title: ...
taxonomy: Notes, Workload View
---
```

The `taxonomy` field is a comma-separated string. Split on `,`, trim whitespace, and match case-insensitively against each term.

A file matches if **any** of its taxonomy terms contains the search value as a substring.  
e.g. `taxonomy=Notes` matches `taxonomy: Notes, Workload View` and `taxonomy: Cases - Notes`.

### query filter
Existing `grep -rli` behavior — unchanged.

### Combined (both provided)
Return files that match **both** — taxonomy AND full-text query.

### domain
Existing scoping behavior — unchanged. Applied before either filter.

---

## Implementation Approach

Replace the single `grep` call with a two-phase approach:

**Phase 1 — Candidate collection:**
- If `taxonomy` provided: walk the directory tree, read each `.md` file, parse frontmatter, filter by taxonomy match. Collect matching paths.
- If `query` provided: run `grep -rli` as today. Collect matching paths.
- If both: intersect the two sets.

**Phase 2 — Return results:**
- Return relative paths as before (array of strings).

### Frontmatter parsing helper
Extract the `taxonomy` value from frontmatter. Frontmatter is a block between `---` delimiters at the top of the file, OR a series of `> **key:** value` lines (legacy format). Check both.

```typescript
function parseTaxonomy(content: string): string[] {
  // YAML frontmatter style
  const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (yamlMatch) {
    const taxLine = yamlMatch[1].match(/^taxonomy:\s*(.+)$/m);
    if (taxLine) return taxLine[1].split(',').map(t => t.trim());
  }
  // Legacy bold style (fallback)
  const boldMatch = content.match(/- \*\*taxonomy:\*\*\s*(.+)/i);
  if (boldMatch) return boldMatch[1].split(',').map(t => t.trim());
  return [];
}
```

### Directory walk helper
Recursive async walk that collects all `.md` files under a path — needed for taxonomy filtering since grep handles this for us in the query case but we need it ourselves for taxonomy.

---

## Tool Definition Update

Update the `search_intelligence` tool's `inputSchema` in `ListToolsRequestSchema`:

```typescript
{
  name: "search_intelligence",
  description: "Search intelligence by query, taxonomy, or both. At least one of query or taxonomy is required. domain optionally scopes the search.",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string", description: "Full-text keyword search" },
      taxonomy: { type: "string", description: "Filter by taxonomy frontmatter field (e.g. 'Notes', 'Service Plan')" },
      domain: { type: "string", description: "Scope to intelligence subdirectory" }
    }
  }
}
```

---

## Fix: list_handoffs returns index.md as a result

**Also fix this in the same PR.** In the `list_handoffs` handler, `index.md` is being returned as a handoff entry because it lives in the `handoffs/` directory and ends in `.md`. It has no valid status line so it defaults to `assigned_to: "Any"`, polluting results and misleading agents.

One-line fix — add a skip guard at the top of the file loop:

```typescript
for (const file of files) {
  if (!file.endsWith(".md")) continue;
  if (file === "index.md") continue;  // ← add this
  // ... rest of handler
}
```

Apply to both the root `handoffs/` scan and the `complete/` subdirectory scan.

---

## Example Calls

```
search_intelligence({ taxonomy: "Notes" })
→ all files tagged with Notes in any taxonomy position

search_intelligence({ taxonomy: "Service Plan" })
→ all files tagged Service Plan

search_intelligence({ query: "bulk", taxonomy: "Notes" })
→ files about bulk AND tagged Notes

search_intelligence({ query: "Notes", domain: "product/projects/q2" })
→ existing behavior, scoped to q2
```

---

## Files to Touch

- `src/ben-cp.ts` — `search_intelligence` handler + tool definition + `list_handoffs` index.md skip
- Rebuild: `npm run build` (or equivalent per `package.json`)

---

## Notes

- Do NOT change the return format — still an array of relative path strings
- `taxonomy: none` files (Accessibility, Web Applications) should not match any taxonomy query — `none` is a sentinel value, not a term
- Keep `grep` for the query path — don't replace it with a JS walk, it's fast and handles encoding edge cases well
