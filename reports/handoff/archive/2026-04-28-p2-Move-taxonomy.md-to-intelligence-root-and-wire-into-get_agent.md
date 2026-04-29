# Implementation Plan: Move taxonomy.md to intelligence root and wire into get_agent

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

`taxonomy.md` currently lives at `intelligence/casebook/taxonomy.md`. It is cross-cutting — used by `capture_task`, `search_intelligence`, `list_intelligence`, `frontmatter.py`, and `reindex.py`. It belongs at `intelligence/taxonomy.md`. Also wire it into `get_agent` so every agent session has the product-feature map automatically.

## Changes

### 1 — Move the file
```bash
mv intelligence/casebook/taxonomy.md intelligence/taxonomy.md
```

### 2 — Update loadTaxonomy() in src/ben-cp.ts
```typescript
const taxonomyPath = path.resolve(rootPath, "intelligence/taxonomy.md");
```

### 3 — Update load_taxonomy_terms() in skills/dream/scripts/reindex.py
```python
path = os.path.join(REPO_ROOT, 'intelligence', 'taxonomy.md')
```

### 4 — Update get_agent to return taxonomy
```typescript
const [agentContent, indexContent, taxonomyContent] = await Promise.all([
  fs.readFile(agentPath, "utf-8"),
  fs.readFile(indexPath, "utf-8").catch(() => ""),
  fs.readFile(path.resolve(rootPath, "intelligence/taxonomy.md"), "utf-8").catch(() => ""),
]);
return { content: [{ type: "text", text:
  `# Role: ${agent_id}\n\n${agentContent}\n\n---\n\n# Repo Index\n\n${indexContent}\n\n---\n\n# Product-Feature Taxonomy\n\n${taxonomyContent}`
}]};
```

### 5 — Update root index.md tree
Move `taxonomy.md` from under `casebook/` to intelligence root in the hand-authored tree section.

### 6 — Update intelligence/product/taxonomy.md redirect stub
```markdown
**Canonical location:** [`../taxonomy.md`](../taxonomy.md)
```

## Verification
- [ ] `intelligence/taxonomy.md` exists; `intelligence/casebook/taxonomy.md` gone
- [ ] `loadTaxonomy()` reads from new path without error
- [ ] `load_taxonomy_terms()` in reindex.py reads from new path
- [ ] `get_agent("cowork")` response includes taxonomy content
- [ ] `npm run build` passes
- [ ] `python3 skills/dream/scripts/reindex.py` runs clean
