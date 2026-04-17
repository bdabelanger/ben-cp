# Implementation Plan: Gemma Local End-to-End Smoke Test

> **Prepared by:** Code (Gemini) (2026-04-17)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-17

Successfully executed E2E smoke test, validating the full pipeline from raw source data parsing to indexed knowledge creation and changelog logging for product/projects domain.

---

# Handoff: Gemma (Local) End-to-End Smoke Test — 2026-04-17

> **Priority:** P2
> **Assigned to:** Cowork (Review) → Local (Execution)
> **Status:** READY

## Context
This is a comprehensive smoke test designed to verify the operational readiness of the **Local (Gemma)** agent within the normalized vault architecture. It exercises Local's core strengths: long-form parsing, intelligence record creation, index maintenance, and vaulted observation logging.

## Logic
The test involves a multi-step workflow transitioning raw source data into structured intelligence:
1.  **Validation**: Verifying agent constraints and domain structure.
2.  **Extraction**: Parsing a technical source file (`asana-custom-fields.md`).
3.  **Codification**: Creating a new, high-fidelity intelligence record with YAML metadata.
4.  **Maintenance**: Updating the parent domain index and logging a note about the structural state.
5.  **Conclusion**: Finalizing the session with a multi-level changelog entry.

## Execution Steps
- [ ] **Step 1: Initialization** — Read `AGENTS.md` and `agents/local.md` to establish persona and tool constraints.
- [ ] **Step 2: Domain Audit** — Use `list_intelligence` on `product/projects/source` to index available technical templates.
- [ ] **Step 3: Source Parsing** — Read `intelligence/product/projects/source/asana-custom-fields.md`. Extract names, GIDs, and purpose for at least 5 core fields.
- [ ] **Step 4: Record Creation** — Create `intelligence/product/projects/asana_field_definitions.md` using `add_intelligence`. Include a "System GID" metadata block.
- [ ] **Step 5: Index Maintenance** — Use `edit_intelligence` to update `intelligence/product/projects/index.md` with a link to the new definitions file.
- [ ] **Step 6: Observation** — Append a note to `product/projects/notes` summarizing the delta between the raw source and the refined record.
- [ ] **Step 7: Logging** — Call `add_changelog` to record the completion of the smoke test in the `product/projects` scope and the root `changelog.md`.