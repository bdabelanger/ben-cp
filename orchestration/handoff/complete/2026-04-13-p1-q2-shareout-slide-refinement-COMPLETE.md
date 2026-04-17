# Implementation Plan: Q2 2026 Product Shareout — Slide Refinement

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Gemma
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1
> **STATUS**: ✅ COMPLETE

Synthesized customer quotes and live project status into a cohesive set of slide records for the Q2 Product Shareout. Flagged remaining gaps (Margaux input, visuals) for human resolution.

---

## Source Files (all in vault)

| File | Path |
|------|------|
| **PPTX (edit this)** | `orchestration/pipelines/outputs/dream/Q2 2026 Product Shareout.pptx` |
| **PDF (reference)** | `orchestration/pipelines/outputs/dream/Q2 2026 Product Shareout.pdf` |
| **TXT extract** | `orchestration/pipelines/outputs/dream/Q2 2026 Product Shareout.txt` — full slide text already extracted, read this first |
| **Live project status** | `orchestration/pipelines/outputs/dream/reports/product-projects.md` |

Run `python3 tools/product/projects/report.py` to refresh live project status before starting.

---

## Tools Available

### PPTX Skill
- Extract text: `python -m markitdown "orchestration/pipelines/outputs/dream/Q2 2026 Product Shareout.pptx"`
- Edit: unpack → manipulate XML → repack (see pptx skill for full editing workflow)
- Visual QA: convert to images via LibreOffice + pdftoppm, inspect each slide, fix, re-verify
- **Always complete at least one fix-and-verify cycle before declaring done**

### Live Data MCPs
- **Jira:** `mcp__369ca651__searchJiraIssuesUsingJql` — verify what's actually shipping
- **Asana:** `mcp__300a198f__get_project` / `get_tasks` — pull live project status updates
- **Confluence:** `mcp__369ca651__searchConfluenceUsingCql` — find customer quotes

---

## Ben's Exact Notes Per Slide

These are Ben's verbatim manager notes captured from the deck. Treat these as the brief.

### Slide 7 — Notes Table (Q1)
> "Slide should just focus on notes table (authoring will be in the Q2 section). Would be cool to have a <1 minute recorded video showing:
> - Quick filtering for a set of notes
> - Filtering further on start date
> - Scanning the narrative preview column
> - Opening a preview of a nice, rich-text note w/service data"

**Current content (from TXT):** Talks about bulk data entry, start/end dates on datagrid, service groups, quotes from Path of Life and North Cook ISC. Copy is mostly right but may reference authoring UX — strip that out.
**Action:** Rewrite to focus purely on the notes table/datagrid experience. Add video callout placeholder if Ben confirms a video is being produced.

---

### Slide 13 — Polish / Reporting (Q1)
> "@margaux.troiano@casebook.net (and @ben.belanger@casebook.net if you have anything you'd like to highlight here)"

**Current content:** Talks about Dynamic WLV headers, drill-back from reports, VPAT/accessibility gaps. Has a quote from Los Alamos JJAB.
**Action:** This slide is blocked — flag it and don't edit content without direction from Ben and Margaux.

---

### Slide 16 — Notes Authoring UX (Q2)
> "Slide should just focus on notes authoring (table will be in Q1 section). Would be cool to have a <1 minute recorded video showing (not mandatory though; may be too late to produce at this point):
> - Adding services and people to a note using new UX
> - Tabbed design
> - Shortcuts for loading services and people quickly (whatever we're doing from the list below)
>   - Service Groups in notes
>   - People + 'attended = yes' auto-completer
>   - Whatever we're going to do to ease data entry around note vs. service dates
>
> Note: this is just a copy/paste of the old notes slide, so you'll probably need to remove all the references to the notes table and focus on authoring on this slide"

**Current content (from TXT):** Currently a near-identical copy of Slide 7 — same capabilities/benefits copy about bulk data entry and datagrid. Has manager notes embedded as slide text. Quote from Path of Life is present.
**Action:** Full rewrite. Drop all datagrid/table references. New copy should cover:
- Tabbed authoring design
- Inline adding of services and people
- Service Groups shortcut
- `attended = yes` auto-completer for people
- Note date vs. service date handling
- Optional: video callout ("Watch a 1-min walkthrough →")
Keep the Path of Life quote if it still applies to authoring; swap for a more authoring-specific quote if available.

---

### Slide 17 — Bulk Tools for Service Plans (Q2)
> "I would play with slide a bit and cover the following topics (with screenshots of each):
> - New Service Plan UX
> - New Enrollments UX
> - Bulk Actions added to both the new service plan UX as well as the Services WLV
>   - The one I am most thinking about and interested in is bulk ending enrollments"

**Current content (from TXT):** Has capabilities around datagrid service plan components, filter/sort/search enrollments, bulk actions for service notes and ending enrollments. Quotes from MomsBloom and Arc of the Capital.
**Action:** Ask Ben if screenshots are ready. If not, draft the copy restructured around those 3 topics with `[SCREENSHOT: New Service Plan UX]`, `[SCREENSHOT: New Enrollments UX]`, `[SCREENSHOT: Bulk end enrollments]` placeholders. The existing quotes are good — keep both.

---

### Slide 19 — Workforce Reporting Package (Q2)
**Current content (from TXT):** Describes what the package shows — workload visibility, task ownership, process bottlenecks. Has placeholder `"A customer said this." – Customer`.
**Action:** Search Confluence for a real customer quote about reporting/workforce analytics/task tracking. Check the Asana project "Reporting - Tasks/Work package" for status updates that may contain customer context. If nothing found, flag for Ben to pull from CS/sales.

---

### Slide 24 — Sign & Lock Notes (Q2)
> "Okay to focus on both service note locking and signing, but perhaps we guarantee at least service note locking to beta in June?"

**Current content (from TXT):** Covers signing a note to lock it, removing signature to reopen, locking sensitive service notes. Quote from Grafton County, NH already present and strong.
**Action:** Reframe scope commitment. Draft copy that:
- Guarantees service note locking to beta in June
- Positions note signing as follow-on (coming next, not guaranteed June)
- Keeps the Grafton County quote
Check CBP-2923 in Jira to confirm current implementation status before committing to the June framing.

---

### Slide 26 — Bulk Import for Notes (Q2)
> "Update this slide to focus on what we're delivering — bulk import for notes and returning all error messages at once"

**Current content (from TXT):** Currently covers: Import General Notes with historical data, flatten tabs for easier import experience, "Display all errors at once." Quote from Kentucky Humane Society.
**Action:** Rewrite to lead with the two confirmed deliverables:
1. **Bulk import for General Notes** (with historical data)
2. **All validation errors returned at once** (not one-at-a-time — this is the key UX win)
Drop the tab-flattening content unless there's room. Keep the Kentucky Humane Society quote. Check Jira CBP-498 to confirm current status.

---

### Slide 27 — Global Notes WLV (Q2)
> "Focus this slide on the global WLV we're focused on in Q2."

**Current content (from TXT):** Mentions Q2/Q3/Q4 phases. Covers view/sort/filter outside of a UoW, keyword search, quick filter on your own content. Quote from Wellmet Project ("I don't want them to have to go into 12 cases…") already present and great.
**Action:** Remove Q3/Q4 references entirely. Narrow to Q2 scope: single global view to see, sort, and filter notes across all units of work without navigating into each. Keep the Wellmet quote. Keep it tight — this is a focused v1, not a vision slide.

---

### Slide 28 — Client Portal v1 (Q2)
> "Focus this slide on the v1 scope of client portal"

**Current content (from TXT):** Currently includes future-state scope (tasks, self check-ins to service events). Has quote from Sparta, WI Police Department already present. Lists: editable profiles, forms, eventually tasks, collaborate with clients to populate tasks.
**Action:** Rewrite to scope down to v1 only:
- Person profiles (editable)
- Form submission
- Collaborative data collection between worker and client
Remove "eventually tasks", self check-ins, and any other future-state language. Keep Sparta, WI Police Dept quote. Cross-check with Duc's latest Asana status update for confirmed v1 scope.

---

### Slide 30 — Zapier Improvements (Q2)
> "Focus this slide on what we think we'll deliver in Q2"

**Current content (from TXT):** Already has the right capabilities listed:
- New triggers like "Service enrollment created in Casebook"
- 4 new write actions like "Create a Note"
- 5 new lookup actions like "Search Cases"
- Enhance 3 existing write actions (Case, Intake Report, Person) with custom fields + line items
- Quote from North Cook ISD already present

**Action:** The content is directionally correct but flagged as needing focus on confirmed Q2 scope. Check Jira for Eric's current progress (demo was scheduled for Thursday as of 2026-04-13). If any items above aren't confirmed for Q2, pull them. Tighten the copy to match what's actually in flight.

---

### Slide 34 — External People in Workflows (Q2)
**Current content (from TXT):** Capabilities are solid — assign workflow tasks to case persons (Engage, Intake persons, Provider staff), one/multiple/all, optional auto-send notifications. Has placeholder `"A customer said this." – Customer`.
**Action:** Search Confluence for a customer quote about external workflow assignment, provider staff involvement, or routing tasks to people outside the team. Check Asana project "Workflows - Assign WF Tasks to External Users" for status updates. If nothing found, flag for Ben.

---

## Recommended Order of Operations

1. **Read the TXT** — `orchestration/pipelines/outputs/dream/Q2 2026 Product Shareout.txt` — use this as your slide reference
2. **Refresh live status** — `python3 tools/product/projects/report.py` → read `reports/product-projects.md`
3. **Check Jira for CBP-498 (slide 26), CBP-2923 (slide 24), Zapier epic (slide 30)** — verify scope before writing
4. **Search Confluence for quotes** — slides 19 and 34
5. **Draft all 9 slides** — show before/after for each
6. **Confirm with Ben:** slide 13 input from Margaux, slide 17 screenshots, scope calls on 24/28/30
7. **Edit the PPTX** — one slide at a time via pptx skill
8. **Visual QA** — convert to images, inspect, fix, re-verify each edited slide

---

## What Gemma Can Own vs. What Needs Ben

| Slide | Can draft fully | Needs Ben/data |
|-------|----------------|----------------|
| 7 | ✅ Copy rewrite | Video (if being produced) |
| 13 | ❌ Blocked | Needs Margaux + Ben input |
| 16 | ✅ Copy rewrite | Video (optional) |
| 17 | ✅ Copy structure | Screenshots from Ben |
| 19 | 🔍 Search first | Quote if search fails |
| 24 | ✅ Scope framing | Jira check before committing |
| 26 | ✅ Copy rewrite | Jira check for status |
| 27 | ✅ Copy rewrite | None |
| 28 | ✅ Copy rewrite | Asana check for v1 scope |
| 30 | ✅ Copy tighten | Jira check for Eric's progress |
| 34 | 🔍 Search first | Quote if search fails |
