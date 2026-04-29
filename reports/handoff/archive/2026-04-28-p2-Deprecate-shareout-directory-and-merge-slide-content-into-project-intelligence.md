# Implementation Plan: Deprecate shareout directory and merge slide content into project intelligence

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Decision

`intelligence/product/shareout/q2/` is deprecated. Slide content belongs on project overviews. Each slide file links to a project via `**Tactical Link:**` — merge content there under a `## Shareout` section.

## Part 1 — Merge slides into project overview.md files

| Shareout file | Target |
|---|---|
| `slide-7-notes-datagrid.md` | `projects/q2/notes-notes-datagrid/overview.md` |
| `notes-authoring-experience.md` | `projects/q2/notes-notes-datagrid/overview.md` |
| `slide-24-sign-and-lock-notes.md` | `projects/q2/notes-signing-service-note-locking/overview.md` |
| `slide-26-bulk-import-notes.md` | `projects/q2/data-import-bulk-import-for-notes/overview.md` |
| `slide-27-global-notes-wlv.md` | `projects/q2/notes-global-notes-wlv-(1210368097846960).md` |
| `slide-28-client-portal.md` | `projects/q2/portal-client-dashboard/overview.md` |
| `slide-30-zapier-improvements.md` | `projects/q2/integrations-zapier-improvements/overview.md` |
| `bulk-service-plan-tools.md` | `projects/q2/enrollment-dialog-bulk-services-section/overview.md` |
| `slide-19-reporting-packages-workforce.md` | Create `projects/q2/reporting-workforce-analytics.md` with `taxonomy: Reporting` |
| `slide-34-external-people-in-workflows.md` | Create `projects/q2/track-external-people-in-workflows.md` with `taxonomy: Track, Workflows` |

Append this section to each target:
```markdown
## Shareout

> **Headline:** [headline from shareout file]
> **Theme:** [theme/OKR if present]

### Customer quotes
- "[quote]" — [source]

### Positioning
[key benefits / scope notes condensed]
```

## Part 2 — Relocate cross-cutting files

| Current | New |
|---|---|
| `shareout/q2/roadmap-2026.md` | `intelligence/product/roadmap-2026.md` |
| `shareout/q2/speaker-notes-draft.md` | `intelligence/product/speaker-notes-q2.md` |
| `shareout/q2/notes-q2-2026-product-shareout.md` | `intelligence/product/shareout-q2-summary.md` |

## Part 3 — Move source files

```bash
mv intelligence/product/shareout/q2/source/ intelligence/product/source/shareout-q2/
```

## Part 4 — Delete shareout directory

```bash
rm -rf intelligence/product/shareout/
```

## Part 5 — Update root index.md tree

Remove `shareout/` from intelligence tree.

## Verification
- [ ] Each project overview.md has `## Shareout` section with headline + quote
- [ ] `reporting-workforce-analytics.md` created with `taxonomy: Reporting`
- [ ] `track-external-people-in-workflows.md` created with `taxonomy: Track, Workflows`
- [ ] Cross-cutting files relocated to `intelligence/product/`
- [ ] `intelligence/product/shareout/` directory gone
- [ ] `reindex.py` runs clean
