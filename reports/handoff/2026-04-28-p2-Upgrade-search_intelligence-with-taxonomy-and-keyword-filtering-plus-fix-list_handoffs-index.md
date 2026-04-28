# Implementation Plan: Upgrade search_intelligence with taxonomy and keyword filtering plus fix list_handoffs index.md

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

`search_intelligence` currently runs `grep -rli` — pure full-text. Intelligence files now have `taxonomy:` frontmatter. Upgrade to support taxonomy filter, keyword filter, or both. Also fix `list_handoffs` returning `index.md` as a result.

**Source file:** `src/ben-cp.ts`

## New search_intelligence signature

```typescript
{ query?: string, taxonomy?: string, domain?: string }
// At least one of query or taxonomy required — throw if neither provided
```

## Taxonomy filter behavior
- Parse `taxonomy:` from YAML frontmatter block (`---\n...\n---`)
- Split on comma, trim, match case-insensitively as substring
- `taxonomy: none` is a sentinel — never matches any taxonomy query
- Walk directory recursively; grep handles query path

## Combined mode
Both provided → intersect results (must match both)

## parseFrontmatter helper (add at module level)
```typescript
function parseFrontmatter(block: string): Record<string, string> {
  const result: Record<string, string> = {};
  for (const line of block.split('\n')) {
    const m = line.match(/^(\w[\w_-]*):\s*(.+)$/);
    if (m) result[m[1]] = m[2].trim().replace(/^['"]|['"]$/g, '');
  }
  return result;
}
```

## list_handoffs fix
Add `if (file === "index.md") continue;` at top of file loop in both root and `complete/` scans.

## Update tool definition
```typescript
{
  name: "search_intelligence",
  description: "Search intelligence by query, taxonomy, or both. At least one required.",
  inputSchema: { type: "object", properties: {
    query: { type: "string", description: "Full-text keyword search" },
    taxonomy: { type: "string", description: "Filter by taxonomy field (e.g. 'Notes', 'Service Plan')" },
    domain: { type: "string", description: "Scope to intelligence subdirectory" }
  }}
}
```

## Verification
- [ ] `search_intelligence({ taxonomy: "Notes" })` returns Notes-tagged files
- [ ] `search_intelligence({ query: "bulk", taxonomy: "Notes" })` returns intersection
- [ ] `search_intelligence({ query: "Notes" })` still works (existing behavior)
- [ ] `list_handoffs()` does not return `index.md`
- [ ] `npm run build` passes
