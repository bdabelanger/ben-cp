# Implementation Plan: Migrate Task Work to Roadmap Intelligence

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

## Context

Gemma has been performing intelligence authoring inside the `tasks/q2-shareout/` local working directory. While this was a useful scratchpad, this content now needs to be migrated to the canonical `intelligence/` domain and split between Strategic (Shareout) and Tactical (Project) records to maintain mutual exclusivity.

## Objectives

1. **Strategic Separation**: Move slide headlines, narratives, and customer quotes from the `.md` files in `tasks/q2-shareout/` to the corresponding files in `intelligence/product/roadmap/shareout/q2/`.
2. **Tactical Alignment**: If the task files contain technical details or GIDs not already present in the project files, merge them into the correct records in `intelligence/product/roadmap/projects/q2/`.
3. **Bridge Verification**: Update the "Project Interlinks" in the new strategic files to point to the real tactical project records.
4. **Task Finalization**: Once data is successfully migrated and indices are updated, the `tasks/q2-shareout/` directory can be archived and this handoff marked complete.

## Execution Steps

1. **Map Files**: Correlate each file in `tasks/q2-shareout/` to its strategic and tactical counterparts.
   - Example: `tasks/q2-shareout/notes-authoring-ux.md` maps to:
     - Strategic: `roadmap/shareout/q2/notes-authoring-experience.md`
     - Tactical: `roadmap/projects/q2/notes-notes-datagrid-(1209963394727039).md`
2. **Transfer Narrative**: Verbatim copy headlines and quotes into the strategic records.
3. **Correct Links**: The task files currently have broken relative links like `product/tasks/q2-shareout/...`. These MUST be corrected to point to `../../projects/q2/...`.
4. **Update Index**: Ensure the index in `roadmap/shareout/q2/` is updated with any new strategic records created during migration.
5. **Mark Complete**: Use `edit_handoff(mark_complete=true)` on this path when finished.

## Success Criteria

- [ ] No unique strategic content remains only in the `tasks/` folder.
- [ ] All Roadmap Shareout records have working links to their respective Projects.
- [ ] The `tasks/q2-shareout/` directory is verified as "Migrated" and ready for archive.
- [ ] This handoff is moved to the `complete/` archive.
