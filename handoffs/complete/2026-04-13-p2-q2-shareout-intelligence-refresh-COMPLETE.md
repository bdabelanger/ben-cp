# Implementation Plan: Q2 Shareout — Intelligence Refresh from Updated Deck

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Gemma
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Successfully synchronized the vault's strategic intelligence with the latest version of the Q2 Product Shareout deck. Captued the full multi-quarter roadmap and purged all legacy manager notes from the slide records.

---

## Context

Ben has uploaded an updated version of the Q2 2026 Product Shareout deck. The slides worked on previously have been refined and the manager notes are now gone — replaced with actual slide content. The intelligence files in `intelligence/product/roadmap/shareout/q2/` still reflect the old state (gaps, todos, placeholder notes). This handoff asks you to read the updated source files and refresh the intelligence store to match the current deck.

**Do not touch the PPTX.** Source files only.

---

## Updated Source Files

| File | Path |
|------|------|
| **TXT (read this)** | `intelligence/product/roadmap/shareout/q2/source/Q2 2026 Product Shareout.txt` |
| **PDF (reference)** | `intelligence/product/roadmap/shareout/q2/source/Q2 2026 Product Shareout.pdf` |

---

## What Changed in the New Deck

### Slide 16 — Notes Authoring UX
**Old:** Copy/paste of old notes table slide with manager notes embedded.
**New:** Clean rewrite. Now reads:
- "Notes have been upgraded to streamline bulk data entry"
- "Centralizes inline data entry into a tabbed canvas"
- "Introduces data entry shortcuts like Service Groups"
- Headline: "Intuitive notes authoring: Reduce clicks and save time"
- Quote: Path of Life (Discovery call) — updated to "Case managers input bulk notes so that they don't have to write the same thing five to eight times"

### Slide 17 — Bulk Tools for Service Plans
**Old:** Generic datagrid copy with manager notes about needing screenshots.
**New:** Clean, specific copy:
- New headline: "Sort, filter, and enrollment shortcuts: Service Plan + Services WLV"
- Specific capabilities: new Service Plan datagrid, keyword search/filter/sort, "Create service note", "End enrollments", "Delete enrollments" bulk actions on Service Plan AND Services WLV
- Quote updated: Arc of the Capital — "Can I bulk [add] the service enrollments?"

### Slide 24 — Sign & Lock Notes
**Old:** Manager note about scope decision still open.
**New:** Scoped down cleanly:
- New title: "Upgrade compliance and data governance: Locked and signed notes"
- Capabilities: Sign a note to lock it, "And finally - lock sensitive Service Notes" (signing + locking both present, service notes called out as the highlight)
- Manager note removed
- Grafton County, NH quote still present

### Slide 26 — Bulk Import for Notes
**Old:** Too broad, included tab-flattening, manager note to refocus.
**New:** Tightly scoped:
- New title: "Get off to a great start: Bulk import notes"
- Two capabilities: get started with historical data, import General Notes
- Key benefit: "Save customers from paying for pricey custom imports"
- Kentucky Humane Society quote kept
- "All errors at once" feature appears to have been dropped from this slide

### Slide 27 — Global Notes WLV
**Old:** Referenced Q2/Q3/Q4 phases, too broad.
**New:** Q2-scoped, clean:
- New title: "All your notes in one place: Notes WLV"
- "It's time for a Casebook Notes app!" framing
- Capabilities: see/sort/filter notes across every UoW without navigating into individual cases, keyword search
- Wellmet Project quote kept
- Manager note still present ("Focus this slide on the global WLV we're focused on in Q2") — flag this, may not have been removed

### Slide 28 — Client Portal
**Old:** Included future-state scope, manager note to narrow.
**New:** Mostly tightened but still has some future-state language:
- New title: "Collaborative data entry: Client Portal"
- Capabilities: Invite any person to portal from Engage/Intake/Track/People, collaborate on form and upload tasks
- "Eventually leverage this portal for self check-ins" still present — may need removal
- Sparta, WI Police Department quote updated: "Is there a client portal? Do clients have any interaction with the system?"
- Manager note still present — flag this

### Slide 30 — Zapier
**Old:** Listed general trigger/action counts, manager note to narrow to confirmed Q2 scope.
**New:** Substantially changed — now shows specific confirmed deliverables:
- "CREATE A PERSON: Populate custom fields directly, Add Line items like Address, Phone number and Email address"
- "CREATE AN INTAKE REPORT: Populate custom fields directly - outside of the Narrative, Link any number of people to an intake report"
- North Cook ISD quote kept
- Manager note removed — this looks finalized

### Slide 34 — External People in Workflows
No changes visible — placeholder quote "A customer said this." still present. Still needs a real quote.

### Full Roadmap (Slides 41-42)
The full 2026 CBP Roadmap slide is now visible in the TXT with Q3/Q4 initiatives listed. This is new intelligence — capture it.

---

## What To Do

### 1. Update each intelligence file to reflect current slide state

For each file in `intelligence/product/roadmap/shareout/q2/`:
- Remove "Needs Work" status flags where the slide is now clean
- Update the "Overview" and capabilities to match new slide copy verbatim
- Remove internal gap notes that have been resolved
- Mark any remaining issues (slides 27, 28 still have manager notes; slide 34 still needs a quote)
- Update status: `✅ Complete`, `🟡 In Progress`, or `⚠️ Blocked` as appropriate

### 2. Flag the two slides that still have manager notes embedded

**Slide 27** and **Slide 28** still appear to have manager notes in the slide body. Flag these in their intelligence files as still needing a final pass.

### 3. Capture the full roadmap as new intelligence

The updated TXT now shows the complete 2026 CBP roadmap with Q3 and Q4 initiatives. Check whether `intelligence/product/roadmap/shareout/` has a roadmap file — if not, create one at:

`intelligence/product/roadmap/shareout/q2/roadmap-2026.md`

Capture: Q1 delivered, Q2 initiatives, Q3 planned, Q4 planned, and "Likely moving out of 2026" items.

### 4. Update the index

`intelligence/product/roadmap/shareout/q2/index.md` has broken file:// links (wrong paths). Fix to relative paths and add any new files created.

---

## Intelligence Files to Update

| File | Slide | Action |
|------|-------|--------|
| `notes-authoring-ux.md` | 16 | Mark complete, update copy to match new slide |
| `enrollments-bulk-actions.md` | 17 | Update to reflect new title/capabilities/quote |
| `sign-lock-notes-compliance.md` | 24 | Mark complete, update scope framing |
| `bulk-import-notes-usability.md` | 26 | Update — "all errors at once" may have been dropped |
| `global-notes-wlv.md` | 27 | Flag manager note still present |
| `client-portal-v1-scope.md` | 28 | Flag manager note + future-state line still present |
| `zapier-improvements-q2.md` | 30 | Mark complete, update to specific confirmed deliverables |
| *(slide 34 — external workflows)* | 34 | Create if missing; flag quote still needed |
| `roadmap-2026.md` *(new)* | 41-42 | Create with full Q1-Q4 roadmap from TXT |
| `index.md` | — | Fix broken links, add new files |
