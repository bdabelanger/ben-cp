# Implementation Plan: Frontmatter-native tools, index.md retirement, and reindex sensor

> **Prepared by:** Cowork (Claude) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

Successfully refactored ben-cp tools to be frontmatter-native, retired 54 subdirectory index.md files (preserving content in overview.md), and integrated the reindex sensor as the master manifest generator for the dream cycle. Verified with a clean 14/14 dream run.

---

## Decision

**Index files are retired. Root `index.md` is the one exception — a single human-readable map, kept current by the dream cycle.**

Directories are the structure. Frontmatter is the metadata. The `reindex` sensor runs first each dream cycle, walks the full repo once, builds a manifest, and shares it with all other sensors — no more redundant filesystem walks.

After this handoff:
- No tool reads or writes subdirectory `index.md` files
- No sensor enforces their presence
- `add_intelligence` stops auto-appending to `index.md`
- 54 subdirectory `index.md` files are deleted
- Root `index.md` is the sole surviving index — auto-updated nightly by dream

---

## Part 1 — `src/ben-cp.ts` changes

### 1a — Shared `parseFrontmatter` helper

Add once at module level — reused by all tools below:

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

### 1b — `list_handoffs`: frontmatter-native + skip index.md

Parse YAML frontmatter first; fall back to prose regex for older handoffs. Skip `index.md` in both root and `complete/` scans.

```typescript
for (const file of files) {
  if (!file.endsWith(".md")) continue;
  if (file === "index.md") continue;
  // ...
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const fm = parseFrontmatter(fmMatch[1]);
    priority   = fm.priority   ?? "TBD";
    status     = fm.status     ?? "READY";
    assignedTo = fm.assigned_to ?? "Any";
    date       = fm.date ?? file.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? "unknown";
  } else {
    // existing prose regex fallback
  }
}
```

### 1c — `list_intelligence`: frontmatter-native, recursive, filtered

Current behavior requires `domain` and returns filenames from one level. Replace with recursive walk + frontmatter parsing.

New signature (all optional):
```typescript
{ domain?: string, type?: string, taxonomy?: string }
// include_directories: keep param, ignore it (backward compat)
```

Return shape:
```typescript
[{
  path: "product/projects/q2/notes-locked-notes/index.md",
  title: "Notes - Locked Notes",
  type: "index",
  domain: "intelligence/product/projects/q2/notes-locked-notes",
  taxonomy: "Notes",
  links: { asana: "...", jira: "..." }
}]
```

Notes:
- Skip `changelog.md` unless `type=changelog` explicitly requested
- Parse `links:` as nested sub-object
- Files without frontmatter: include with `title` = filename, other fields null
- Return paths relative to `intelligence/` root

### 1d — `list_skills`: frontmatter-native

Walk `skills/`, find `SKILL.md` per directory, parse frontmatter, return structured objects:
```typescript
[{ path: "dream/SKILL.md", title: "Dream Cycle — Skill", type: "skill", domain: "skills/dream" }]
```

### 1e — `get_intelligence` parse mode: prefer frontmatter

Parse YAML frontmatter first; fall back to `- **key:** value` bold-line scraping only if absent.

### 1f — `add_intelligence`: remove index.md auto-append

Remove the block that appends `- [title](filename)` to `index.md` after creating a record.

---

## Part 2 — Delete all subdirectory index.md files

54 files. Root `index.md` is **not** deleted — it is the one surviving index.

### Delete unconditionally

```
handoffs/index.md
intelligence/index.md
intelligence/casebook/admin/index.md
intelligence/casebook/subscriptions/index.md
intelligence/governance/index.md
intelligence/product/okrs/index.md
intelligence/product/okrs/q2/index.md
intelligence/product/okrs/q2/elevate-notes/index.md
intelligence/product/okrs/q2/planning-services-at-scale/index.md
intelligence/product/okrs/q2/reduce-admin-burden/index.md
intelligence/product/projects/index.md
intelligence/product/projects/asana-custom-fields/index.md
intelligence/product/projects/asana-custom-fields/source/index.md
intelligence/product/projects/source/index.md
intelligence/product/releases/index.md
intelligence/product/shareout/q2/source/index.md
intelligence/product/projects/q2/data-import-clearer-ids/index.md
intelligence/product/projects/q2/notes-bulk-general-notes/index.md
intelligence/product/projects/q2/notes-bulk-service-notes/index.md
intelligence/product/projects/q2/services-multiple-rosters-for-enrollments-and-notes/index.md
intelligence/skills/tasks/index.md
agents/art/index.md
agents/index.md
agents/logs/index.md
agents/sessions/index.md
skills/asana/index.md
skills/asana/schemas/index.md
skills/dream/index.md
skills/handoff/index.md
skills/index.md
skills/intelligence/index.md
skills/releasinator/index.md
skills/rovo/index.md
skills/status/index.md
skills/status/schemas/index.md
skills/status/scripts/index.md
skills/styles/index.md
skills/tasks/index.md
skills/transcripts/index.md
reports/status/data/raw/index.md
reports/tasks/data/archive/q2-shareout/index.md
reports/tasks/data/raw/index.md
```

### Delete — content already in frontmatter

```
intelligence/product/projects/q2/index.md
intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md
intelligence/product/projects/q2/enrollment-dialog-bulk-services-section/index.md
intelligence/product/projects/q2/integrations-zapier-improvements/index.md
intelligence/product/projects/q2/notes-locked-notes/index.md
intelligence/product/projects/q2/notes-notes-datagrid/index.md
intelligence/product/projects/q2/notes-signing-service-note-locking/index.md
intelligence/product/projects/q2/portal-client-dashboard/index.md
intelligence/product/projects/q2/services-service-plan-datagrid-with-bulk-actions/index.md
intelligence/product/projects/q2/services-wlv-bulk-actions/index.md
```

### Review before deleting — may have unique content

Read each. If content is worth keeping, save as `overview.md` with `type: overview` frontmatter. Otherwise delete.

```
intelligence/casebook/index.md         (MCP repo table + subdirectory descriptions)
intelligence/casebook/reporting/index.md   (file listing with descriptions)
intelligence/product/index.md          (roadmap/OKR links)
intelligence/product/shareout/q2/index.md  (shareout context)
```

---

## Part 3 — Wire `reindex` sensor into dream cycle

`skills/dream/scripts/reindex.py` has been written and is ready. It walks the repo once, parses all frontmatter, validates taxonomy, writes a manifest JSON, and updates the root `index.md` stats footer.

### 3a — Add reindex as first sensor in `run.py`

```python
SENSORS = [
    'reindex',   # must run first — builds manifest for other sensors
    'pulse', 'links', 'frontmatter', 'drift',
    'handoffs', 'index', 'agents',
    'tasks', 'changelog', 'context', 'access',
    'paths', 'scripts',
]
```

### 3b — Update `frontmatter.py` to read reindex manifest

Replace the filesystem walk with manifest consumption:

```python
manifest_path = os.path.join(OUTPUTS_DIR, 'reindex_report.json')
try:
    with open(manifest_path) as f:
        files = json.load(f)['manifest']['files']
except (OSError, KeyError):
    files = walk_and_parse_own()  # fallback

for rel, meta in files.items():
    if not meta['has_frontmatter']:
        issues.append({"file": rel, "issue": "missing_frontmatter"})
    # use meta['type'], meta['taxonomy'] for existing checks
    # taxonomy unknown_term issues already in reindex manifest — consume directly
```

### 3c — Update `links.py` to use reindex file list

```python
manifest_path = os.path.join(OUTPUTS_DIR, 'reindex_report.json')
try:
    with open(manifest_path) as f:
        md_files = [os.path.join(REPO_ROOT, p) for p in json.load(f)['manifest']['files']]
except (OSError, KeyError):
    md_files = collect_md_files()  # fallback
```

### 3d — Add reindex to dream report highlights

In `build_highlights()`:
```python
if name == 'reindex' and data['status'] != 'FAILED':
    r = data['report']
    missing = r.get('summary', {}).get('frontmatter_missing', 0)
    unknown = r.get('summary', {}).get('unknown_taxonomy_terms', 0)
    if missing:
        lines.append(f'- **{missing} files** missing frontmatter')
    if unknown:
        lines.append(f'- **{unknown} files** with unknown taxonomy terms')
```

### 3e — Add reindex to SKILL.md sensor table

```
| reindex | `dream/reindex_report.json` | Walks repo, validates frontmatter + taxonomy, regenerates root index.md |
```

### 3f — Update `index.md` frontmatter date in reindex.py

In `regenerate_index()`, also update the `updated:` field:
```python
today = datetime.now().strftime('%Y-%m-%d')
updated = re.sub(r'^updated:.*$', f'updated: {today}', updated, flags=re.MULTILINE)
```

---

## Part 4 — pulse.py: remove index.md check

- Remove `check_index_coverage()` function
- Remove `dirs_missing_index` from report summary and output
- Update `skills/dream/SKILL.md`: remove "Missing `index.md` files" from Bucket A triage list and pulse sensor description

---

## Verification Checklist

- [ ] `list_handoffs()` returns no `index.md` entry
- [ ] `list_handoffs()` reads frontmatter fields correctly; falls back for older handoffs
- [ ] `list_intelligence()` with no args returns results across all of `intelligence/`
- [ ] `list_intelligence({ taxonomy: "Notes" })` returns only Notes-tagged files
- [ ] `list_intelligence({ type: "prd" })` returns only PRD files
- [ ] `list_skills()` returns structured objects with title and domain
- [ ] `get_intelligence(path, parse=true)` reads YAML frontmatter
- [ ] `add_intelligence` no longer writes to any `index.md`
- [ ] All 54 subdirectory `index.md` files deleted or migrated
- [ ] Root `index.md` untouched (not deleted)
- [ ] `python3 skills/dream/scripts/reindex.py` runs cleanly; `reindex_report.json` written
- [ ] Root `index.md` stats footer updated after reindex run
- [ ] `reindex` runs first in dream cycle; `frontmatter.py` and `links.py` consume manifest
- [ ] `pulse.py` no longer reports `dirs_missing_index`
- [ ] `npm run build` passes
