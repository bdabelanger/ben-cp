---
title: 'Implementation Plan: Gemma Remediation: Datagrid Intelligence Mis-Write Correction'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Gemma Remediation: Datagrid Intelligence Mis-Write Correction

> **Prepared by:** Code (Gemini) (2026-04-15)
> **Assigned to:** Cowork
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE

All remediation steps executed directly by Cowork: skills/ violations removed, shadow intelligence/casebook/notes/ files deleted, canonical Q2 record updated with salvaged narrative. local.md Rule 5 upgraded to a 3-step pre-write verification gate with explicit domain routing table. Original datagrid handoff marked complete."

---

## Cowork Implementation Plan: Gemma Remediation — Datagrid Intelligence Mis-Write

> **Prepared by:** Cowork (2026-04-15)
> **Assigned to:** Cowork
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — Structural violation cleanup + intelligence correction
> **STATUS**: ✅ COMPLETE

---

## Context

During the execution of `2026-04-15-p2-notes-datagrid-intelligence.md`, Gemma (Local) went off the rails in two key ways:

1. **Wrong domain**: She created `intelligence/casebook/notes/{datagrid.md, notes-wlv.md, index.md}`. The canonical home for all Q2 project intelligence records is `intelligence/product/roadmap/projects/q2/`. The correct target file already exists: `notes-notes-datagrid-(1209963394727039).md`. A real `notes-global-notes-wlv-(1210368097846960).md` also already exists and is authoritative — her stub is a shadow duplicate.

2. **Directory boundary violations**: She wrote changelogs to `skills/casebook/notes/changelog.md` and `skills/root/changelog.md`. Per AGENTS.md, writing data files or run artifacts into `skills/` is a hard violation.

The verbatim source material and narrative Gemma captured (from the Q2 Shareout) has real intelligence value and must be **merged into the correct existing records** — not abandoned.

---

## Logic

- **Merge, don't discard**: The verbatim quotes, customer proof points, and narrative framing in Gemma's `intelligence/casebook/notes/datagrid.md` are valid. Merge them into the existing canonical record at `intelligence/product/roadmap/projects/q2/notes-notes-datagrid-(1209963394727039).md` under a `## 🗣️ Key Narrative Points (From Shareout)` section (the pattern already used in that file).
- **No shadow records**: The `notes-wlv.md` stub Gemma created has no new information beyond what exists in the real record. It should be deleted, not migrated.
- **Delete violations cleanly**: The `skills/casebook/` and `skills/root/` directories must be removed entirely (they are untracked in git — no `git rm` needed, just filesystem delete).
- **Purge the wrong intelligence/casebook/notes/ additions**: Remove `datagrid.md`, `notes-wlv.md`, and the erroneous `index.md` Gemma created. Verify whether `intelligence/casebook/notes/` had a pre-existing `index.md` before Gemma overwrote it.

---

## Execution Order

1. **Task 1** — Read & Verify Existing Records
2. **Task 2** — Merge Datagrid Narrative into Canonical Q2 Record
3. **Task 3** — Delete Violation Files (skills/ directory)
4. **Task 4** — Clean intelligence/casebook/notes/ (remove shadow records)
5. **Task 5** — Update Datagrid Handoff Status
6. **Task 6** — Changelog + Completion

---

## Task 1: Read & Verify Existing Records

Before touching anything, read all of these to confirm current state:
- `intelligence/product/roadmap/projects/q2/notes-notes-datagrid-(1209963394727039).md` — the canonical record to be updated
- `intelligence/product/roadmap/projects/q2/notes-global-notes-wlv-(1210368097846960).md` — confirm it is authoritative; Gemma's stub adds nothing
- `intelligence/casebook/notes/index.md` — determine if this file existed BEFORE Gemma's session (check git: `git log --oneline intelligence/casebook/notes/index.md`)
- `intelligence/casebook/notes/datagrid.md` — read Gemma's content so you can extract what to merge

**Key check**: Run `git log --oneline -- intelligence/casebook/notes/index.md` to determine if this file was pre-existing. If it was, restore from git after removing Gemma's version. If it was created by Gemma (untracked), simply delete it.

---

## Task 2: Merge Datagrid Narrative into Canonical Q2 Record

Edit `intelligence/product/roadmap/projects/q2/notes-notes-datagrid-(1209963394727039).md` to add a new subsection at the bottom of the existing `## 🗣️ Key Narrative Points (From Shareout)` section (or append after it):

### Content to Merge

Add the following under the existing Key Narrative Points:

```markdown
### 💬 Verbatim Shareout Source Material

**Slide Text:**
> "Notes datagrid: Find and review notes wicked fast. Sort, filter, quick filter. Hide and reorder columns. Standardized handling of dates. See all notes without leaving the page. ROI for their hard work on notes."

**Speaker Notes:**
> "The Casebook Notes experience has gotten better and better over the years. This version will feel like a giant leap - like when we launched group service notes in 2022. CAPABILITIES: There is SO much you can do - sort, filter, quick filter, hide and reorder columns. Simple improvements like standardizing our handling of dates matters and I want to thank the CX team especially for bringing that level of detail to us to tidy up alongside this fresh coat of paint."

**Customer Proof Point (North Cook ISC):**
> "The ability to sort by the two types of dates has been very helpful… the chronological view and viewing the student's life…"

**Strategic Framing:** Considered a "giant leap" for the platform, comparable in impact to the 2022 launch of group service notes.
```

---

## Task 3: Delete Violation Files (skills/ directory)

These directories are **untracked** in git (confirmed via `git status`) — delete them directly:

```bash
rm -rf "skills/casebook/"
rm -rf "skills/root/"
```

Verify with `git status` afterward to confirm they are gone and no tracked files were affected.

---

## Task 4: Clean intelligence/casebook/notes/ (Remove Shadow Records)

**Step 4a**: Run `git log --oneline -- intelligence/casebook/notes/index.md` to check if index.md was pre-existing.

**Step 4b**: Delete Gemma's shadow files:
```bash
rm "intelligence/casebook/notes/datagrid.md"
rm "intelligence/casebook/notes/notes-wlv.md"
```

**Step 4c**: If `index.md` was created by Gemma (untracked, no git history), delete it too:
```bash
rm "intelligence/casebook/notes/index.md"
```
If it was pre-existing (has git history), restore the original:
```bash
git checkout -- intelligence/casebook/notes/index.md
```

**Step 4d**: Verify `intelligence/casebook/notes/` is clean and consistent with its pre-Gemma state.

---

## Task 5: Update Datagrid Handoff Status

The original handoff `orchestration/handoff/2026-04-15-p2-notes-datagrid-intelligence.md` was never properly completed (Gemma wrote to the wrong location and marked the wrong thing done). Update its STATUS block to reflect it was re-executed under remediation, and mark it complete via `edit_handoff`.

---

## Task 6: Changelog + Completion

Write changelog entries:
- Root `changelog.md` — concise one-liner: "Remediated Gemma's datagrid mis-write: merged shareout narrative into canonical Q2 record, deleted skills/ violations, removed shadow intelligence/casebook/notes/ records."
- No subdirectory changelog required (this is a correction/cleanup, not a new skill).

Mark this handoff COMPLETE and move to `orchestration/handoff/complete/`.

---

## Notes for This Agent

- **Do not create new intelligence records** — only edit the existing canonical Q2 record.
- **The `intelligence/casebook/` domain is valid** for Casebook product knowledge (schema, domain concepts). However, Notes *project status records* belong in `product/roadmap/projects/q2/`. Do not blur this line.
- **Cross-linking**: The real cross-link from the datagrid record to WLV (`notes-global-notes-wlv-(1210368097846960).md`) should be added as a `**Related:**` inline reference within the merged narrative section — not via `connect_intelligence` (that tool creates a separate relationship record, which is overkill here).
- The `skills/casebook/` and `skills/root/` directories are **entirely Gemma's creation** — they have no tracked git history and can be deleted safely.