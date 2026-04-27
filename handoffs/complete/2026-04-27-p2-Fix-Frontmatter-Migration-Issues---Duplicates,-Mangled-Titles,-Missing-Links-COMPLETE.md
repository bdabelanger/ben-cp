# Implementation Plan: Fix Frontmatter Migration Issues - Duplicates, Mangled Titles, Missing Links

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully sanitized frontmatter and body content vault-wide. Removed redundant metadata blocks, restored proper punctuation to titles, and migrated external platform URLs into the structured `links` frontmatter block for better agentic retrieval. Scan

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: 🔲 READY

---

## Context

Spot-checking the frontmatter migration revealed three issues:

### Issue 1 — Duplicate body content
`intelligence/product/projects/q2/notes-notes-datagrid/index.md` has its entire metadata bullet block repeated twice before the `## Overview` section. Looks like a migration script artifact — the original body was preserved and the content was also prepended again.

### Issue 2 — Mangled title
`intelligence/product/okrs/q2/elevate-notes/index.md` has `title: Initiative Elevate Notes to a First-Class Experience  Index` — double space, colon and em-dash stripped from the original `Initiative: Elevate Notes to a First-Class Experience — Index`.

### Issue 3 — Links not migrated to frontmatter
The `links:` frontmatter block from the schema is not being populated. Files like `intelligence/product/projects/q2/notes-notes-datagrid/index.md` have Asana, Jira, and Confluence URLs in the body but nothing in frontmatter `links:`. The migration added `title`, `type`, and `domain` but skipped `links`.

## Goal

Fix all three issues across the vault.

## Execution Steps

1. **Duplicate body content** — scan for files where the same block of content appears twice in sequence (likely all q2 project index files). Remove the duplicate. Keep the body version that is better formatted; if identical, remove the first occurrence.

2. **Mangled titles** — audit all files where `title` in frontmatter doesn't match the `# H1` heading. The H1 is authoritative — update frontmatter `title` to match it exactly (strip markdown formatting like `**`, but preserve punctuation including colons and em-dashes).

3. **Links migration** — for each file, parse known URL patterns from the body and populate the frontmatter `links:` block:
   - Asana URLs (`app.asana.com`) → `links.asana`
   - Jira URLs (`casecommons.atlassian.net/browse/`) → `links.jira`
   - Confluence URLs (`casecommons.atlassian.net/wiki/`) → `links.confluence`
   - Figma URLs (`figma.com`) → `links.figma`
   - GitHub URLs (`github.com`) → `links.github`
   - Google Drive URLs (`drive.google.com`) → `links.google-drive`
   Only add `links:` block if at least one URL is found.

## Verification

- `notes-notes-datagrid/index.md` has no duplicate content
- `elevate-notes/index.md` title matches H1 exactly
- Spot-check 5 project index files — each should have a populated `links.asana` and `links.jira` in frontmatter
- Re-run `generate_report(skill='dream')` and confirm frontmatter sensor issue count drops further
