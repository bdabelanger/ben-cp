# Implementation Plan: Note Authoring Canvas Intelligence Update

> **Prepared by:** Cowork (Gemini) (2026-04-15)
> **Assigned to:** Cowork (Claude)
> **Vault root:** ben-cp/
> **Priority:** P2
> **STATUS: 🔲 READY — reassigned 2026-04-25**

---

## Context
The **Note Authoring Canvas** represents a overhaul of how notes are created and managed (GIDs: 1211838817183809, 1211757637943244). It is a Q2 strategic initiative currently in **Beta/QA**, designed to set the foundation for the "Dynamic Pages" roadmap later this year.

## Logic
Update the Intelligence domain to reflect the "Canvas" as a mental model. This isn't just a new form; it's a "standardized look and feel" that reduces cognitive load by keeping data entry "eye-level" across all note types.

## Synthesized Intelligence for Entry
- **Core Vision**: "Speed through note writing." This update is framed as a massive leap forward in consistency and professional-grade performance.
- **Key Capabilities**:
    - **Standardized UI**: Every note type is now consistent and "eye-level," utilizing a tabbed structure that organizes familiar groups into a more mature interface.
    - **Service Shortcuts**: Incorporated all "Services" shortcuts into the authoring flow, including Service Groups, Rosters, Bulk actions, and Multiple resource linking.
    - **Canvas Model**: The tabbed interface is referred to as a "Canvas," preparing the platform for **Dynamic Pages support** where users will eventually add and arrange fields.
- **Team Recognition**: Pierre (Design), Bisoye, Russell, and Tuan (Implementation).
- **Customer Validation**:
    - **Path of Life**: Highlighted the efficiency gain, noting that users will no longer have to "write the same thing five to eight times" when performing bulk actions.
- **Strategic Goal**: Eliminate "Duplicating Effort" and solve for "Where is the effort?" during the note-taking process.

## Verbatim Source Material
### Slide Text
> "Speed through note writing: Note authoring canvas. Always consistent and eye-level. Bulk note authoring shortcuts. Canvas approach (prep for Dynamic pages). '[Case Workers] input bulk notes so that they don't have to write the same thing five to eight times.' — Path of Life"

### Speaker Notes
> "Just like the datagrid, note authoring is taking a massive leap forward. Pierre's design and Bisoye, Russell, and Tuan's implementation sets users up with a note that is always consistent and eye-level for every note type... The new tabs feel like a big change, but the underlying sections are structured in familiar groups... they feel more mature than their predecessor... Dynamic pages support which will allow customers to add and arrange fields in the top section of the note later this year."

## Execution Steps

> ⚠️ **Path Directive**: Two canonical Q2 records cover these GIDs. Use `edit_intelligence` — do NOT create new files.

1. **Intelligence Update (GID: 1211838817183809)**: Edit `intelligence/product/roadmap/projects/q2/notes-bulk-general-notes-(1211838817183809).md` — add the "Canvas" mental model framing, Path of Life quote, and team credits (Pierre, Bisoye, Russell, Tuan) under `## 🗣️ Key Narrative Points (From Shareout)`.
2. **Intelligence Update (GID: 1211757637943244)**: Edit `intelligence/product/roadmap/projects/q2/notes-bulk-service-notes-(1211757637943244).md` — add Service Shortcuts detail (Service Groups, Rosters, Bulk actions, Multi-resource linking) as key capabilities.
3. **Dynamic Pages Note**: In both records, add a `**Strategic Prerequisite:**` note: "Canvas model prepares platform for Dynamic Pages (later Q2) — users will eventually add and arrange fields in the top note section."
4. **Status Sync**: Confirm Stage metadata in both records reflects QA/Beta status. If not, update with current state.
