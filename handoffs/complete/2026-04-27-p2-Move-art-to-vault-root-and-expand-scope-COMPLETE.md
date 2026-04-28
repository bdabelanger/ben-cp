> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Moved intelligence/art/ to agents/art/. Updated frontmatter of art pieces. Created agents/art/index.md. Updated art tool paths in src/ben-cp.ts. Updated AGENTS.md and policy.md.Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/handoffs/2026-04-27-p2-Move-art-to-repo-root-and-expand-scope.mdScan

---

## Context

`intelligence/art/` is misplaced — art is agent creative output, not intelligence. It should live at `agents/art/` alongside other agent-produced artifacts. The scope should also be broadened: currently only short poems exist, but art should encompass anything expressible in text.

## Goal

1. Move `intelligence/art/` → `agents/art/`
2. Update `AGENTS.md` repo tree and any references
3. Update the `add_art` / `list_art` / `get_art` MCP tool paths in `src/` to point at `agents/art/`
4. Create `agents/art/index.md` reflecting the broader scope

## Art Scope (update any SKILL or index documentation to reflect this)

Art is any text-based creative work. Types include but are not limited to:

- Poems
- Short stories
- Essays
- Dialogues / scripts
- Song lyrics
- Manifestos
- Letters
- Jokes / absurdist pieces
- Fables / parables
- Monologues

Any agent may create art at any time — not just during dedicated creative sessions. If something feels worth making, make it.

## File Format

Each art piece is a standalone `.md` file. Frontmatter should follow the repo standard:

```yaml
---
title: 
type: art
domain: agents/art
artist: 
date: YYYY-MM-DD
form: poem | story | essay | dialogue | lyrics | manifesto | letter | joke | fable | monologue | other
---
```

## Execution Steps

1. Create `agents/` directory at repo root if it doesn't exist
2. Move all files from `intelligence/art/` to `agents/art/`
3. Update frontmatter on existing files to add `type: art`, `domain: agents/art`, and `form: poem`
4. Delete `intelligence/art/`
5. Create `agents/art/index.md` with a listing of all pieces
6. Update `src/ben-cp.ts` art tool paths from `intelligence/art/` to `agents/art/`
7. Update `AGENTS.md` repo tree
8. Update any other references to `intelligence/art/` across the repo

## Verification

- `agents/art/` exists with all 4 existing pieces
- `intelligence/art/` no longer exists
- `list_art` MCP tool returns the 4 existing pieces from the new location
- `add_art` writes to `agents/art/` correctly
- No broken links (run links sensor or grep)
