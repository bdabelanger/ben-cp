# Implementation Plan: migrate-communication-to-notes-skill

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Successfully migrated the communication skill logic from its old location to a standardized notes structure, creating `orchestration/notes/SKILL.md` and updating cross-references in domain indexes.

**Changelog:** (see root changelog.md)


---

**Goal:** Refactor the `orchestration/communication` skill into a dedicated, standardized `orchestration/notes` structure to better reflect its function as the vault's primary collaborative scratchpad.

**Execution Plan (Migration):**
1. **Create New Structure:** Create the directory `orchestration/notes/` if it does not exist.
2. **Migrate Content:** Copy the content from `orchestration/communication/SKILL.md` into a new file: `orchestration/notes/SKILL.md`. (This preserves the current logic while changing the artifact name).
3. **Update References:** Systematically search and replace all references to `/orchestration/communication/` within other domain indexes (`intelligence/index.md`, etc.) with `/orchestration/notes/`.
4. **Finalize Skill:** Update `orchestration/notes/SKILL.md` to reflect its new, singular focus.

**Critical Context for Execution:** The Platform Weekly Status Report pipeline requires environment variables defined in the root `.env` file: `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/.env`. This must be provisioned before any report execution can succeed.

**Deliverables:** New `orchestration/notes/SKILL.md`, updated cross-references, and a decision on whether to deprecate the old `communication` directory structure.