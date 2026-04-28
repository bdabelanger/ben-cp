# Implementation Plan: Frontmatter-native tools, index.md retirement, and reindex sensor wiring

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Decision

Index files are retired. Root `index.md` is the sole surviving index — kept current by dream cycle. Directories are the structure. Frontmatter is the metadata.

All changes in `src/ben-cp.ts`. Rebuild after.

## Part 1 — Shared parseFrontmatter helper

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

## Part 2 — list_handoffs: frontmatter-native + skip index.md

Parse YAML frontmatter first; fall back to prose regex for older files. Skip `index.md` in both root and `complete/` scans.

```typescript
if (file === "index.md") continue;
const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
if (fmMatch) {
  const fm = parseFrontmatter(fmMatch[1]);
  priority = fm.priority ?? "TBD";
  status = fm.status ?? "READY";
  assignedTo = fm.assigned_to ?? "Any";
  date = fm.date ?? file.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? "unknown";
} else { /* existing prose regex fallback */ }
```

## Part 3 — list_intelligence: frontmatter-native, recursive, filtered

New signature (all optional): `{ domain?: string, type?: string, taxonomy?: string }`

Walk `intelligence/` recursively, parse frontmatter, return structured objects:
```typescript
[{ path, title, type, domain, taxonomy, links: { asana, jira } }]
```
Skip `changelog.md` unless `type=changelog` explicitly requested. Parse `links:` as nested sub-object. Files without frontmatter: include with `title` = filename, other fields null.

## Part 4 — list_skills: frontmatter-native

Walk `skills/`, find `SKILL.md` per directory, parse frontmatter:
```typescript
[{ path: "dream/SKILL.md", title: "Dream Cycle — Skill", type: "skill", domain: "skills/dream" }]
```

## Part 5 — get_intelligence parse mode: prefer frontmatter

Parse YAML frontmatter first; fall back to `- **key:** value` bold-line scraping.

## Part 6 — add_intelligence: remove index.md auto-append

Remove the block that appends `- [title](filename)` to `index.md`.

## Part 7 — Delete all subdirectory index.md files (54 total)

Root `index.md` is NOT deleted. Delete all others. See full list below — run as a shell loop:

```bash
# Safe to delete unconditionally (navigation-only)
find intelligence/ skills/ agents/ reports/ -name "index.md" ! -path "./index.md" -delete

# Review before deleting (may have unique content — read first, migrate to overview.md if worth keeping)
# intelligence/casebook/index.md
# intelligence/casebook/reporting/index.md  
# intelligence/product/index.md
# intelligence/product/shareout/q2/index.md
```

## Part 8 — pulse.py: remove index.md check

Remove `check_index_coverage()` and `dirs_missing_index` from `pulse.py`. Update `skills/dream/SKILL.md` to remove index.md from Bucket A triage list.

## Part 9 — reindex.py: wire as first sensor + share manifest

Add `'reindex'` as first entry in SENSORS list in `skills/dream/run.py`. Update `frontmatter.py` and `links.py` to read from `reindex_report.json` manifest instead of re-walking filesystem. See `skills/dream/scripts/reindex.py` — already written.

## Verification
- [ ] `list_handoffs()` returns no `index.md` entry
- [ ] `list_intelligence()` with no args returns results across all intelligence/
- [ ] `list_intelligence({ taxonomy: "Notes" })` returns Notes-tagged files
- [ ] `list_skills()` returns structured objects
- [ ] `add_intelligence` no longer writes to index.md
- [ ] All 54 subdirectory index.md files deleted
- [ ] Root index.md untouched
- [ ] `reindex.py` runs first in dream cycle
- [ ] `npm run build` passes
