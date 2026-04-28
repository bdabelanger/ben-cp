---
title: 'Handoff & Implementation Plan: Unified Artifact Standard'
type: handoff
domain: handoffs/complete
---


# Handoff & Implementation Plan: Unified Artifact Standard

**Assignee:** Code Agent  
**Author:** Cowork (Gemini)  
**Priority:** P2 (Major)  
**Status:** Ready for Execution  

---

## 1. Problem Statement & Context
The repo's current workflow is fragmented across three locations (Root, `/tasks/`, and `/handoff/`). This creates cognitive load and violates the "Root Rule" (no new files at root). 

We need to consolidate the **Handoff** and **Implementation Plan** into a single "request-ready" artifact. Additionally, we must clarify terminology to prevent agents from overwriting human-led task lists.

## 2. Proposed Solution (The Logic)
- **Unified Flat Files**: For most P1/P2 work, the Handoff and Implementation Plan are merged into a single file located in `orchestration/handoff/`.
- **Bundle Exception**: Sub-directories in `handoff/` are now reserved for features requiring auxiliary files (images, scripts, etc.).
- **Terminology Split**: 
    - **"Steps"**: Refers to agent-led execution items within an implementation plan.
    - **"Tasks"**: Refers to human-led work residing in the `tasks/` directory.
- **Root Cleanliness**: All implementation logic is permanently moved out of the repo root.

## 3. Technical Requirements
- **Standardized Schema**: Every unified plan must follow the: *Context -> Logic -> Execution Steps* hierarchy.
- **H1/H2 Hierarchy**: Maintained for mobile voice summary compatibility (iPhone 16 Pro Max / NotebookLM).

## 4. Execution Steps
- [ ] **Update AGENTS.md**:
    - Codify the **Unified Flat File** as the primary standard for P1/P2 artifacts.
    - Define the directory-based "Feature Bundle" as the exception for multi-file complexity.
    - Explicitly define the mandatory schema for these unified artifacts.
- [ ] **Update cowork.md**:
    - Update the "Handoff Protocol" to reflect the unified standard.
    - Formally deprecate root-level plans (`GEMINI_IMPLEMENTATION_PLAN.md` / `CLAUDE_CODE_IMPLEMENTATION_PLAN.md`).
- [ ] **Terminology Enforcement**:
    - Ensure both files clearly distinguish between agent **"Steps"** and human **"Tasks."**
- [ ] **Cleanup**:
    - Delete or move any remaining `_IMPLEMENTATION_PLAN.md` files from the repo root to `handoff/complete/` or `archive/`.
- [ ] **Version Control**:
    - Update root `changelog.md` to **v1.18.7**.

## 5. Verification
- Confirm `AGENTS.md` and `cowork.md` are aligned on the "Unified Flat" standard.
- Verify the repo root contains zero implementation plan markdown files.