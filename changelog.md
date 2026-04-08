# Project Changelog: ben-cp Vault

This log tracks major architectural, process, and documentation standard changes across the entire project vault.

## [Unreleased]

## [1.1.0] - Vault Quality Layer & Infrastructure Overhaul (2026-04-08)

**Changes:**
- `AGENTS.md` — rebuilt as slim agent dispatch table with universal rules
- `agents/claude.md` — Cowork architect role instructions
- `agents/claude-code.md` — implementer role instructions
- `agents/gemma.md` — executor role instructions
- `agents/index.md` — TOC for agent role directory
- `gemma-rules.md` — updated; references `agents/gemma.md` as primary role file
- `gemma-rules.md` Rule 7 — now points to `skills/wrap-up/index.md` procedure
- `crypt-keeper.md` — replaced with redirect stub → `skills/crypt-keeper/procedure.md`
- `vault-cleanup.md` — redirect stub (points to crypt-keeper.md)
- `skills/wrap-up/index.md` — rewritten; new 5-stage changelog-first procedure
- `skills/wrap-up/changelog_entry_template.md` — created; template for all future entries
- `skills/okr-reporting/procedure.md` — split into evergreen runbook (v1.1, no quarterly content)
- `skills/okr-reporting/2026-q2-kr-reference.md` — created; Q2 KR baseline status migrated from Google Doc
- `skills/okr-reporting/notes_datagrid_shortcuts.md` — restored after Gemma overwrite damage
- `skills/okr-reporting/notes_quick_entry.md` — created; full KR measurement SOP
- `skills/okr-reporting/index.md` — created; TOC with file type guide
- `skills/crypt-keeper/procedure.md` — created; 7-check vault quality watchdog
- `skills/crypt-keeper/report-template.md` — created; structured report template
- `skills/crypt-keeper/index.md` — created
- `src/ben-cp.ts` — added `write_gemma_wrap_up` and `get_gemma_wrap_up` MCP tools
- `sop/` → `skills/` — directory renamed; all path references updated across vault

**KR State:**
- Notes Quick Entry (Outside UOW): ✅ Ready — baseline ~32%, target 40%
- Notes Datagrid Navigation Shortcuts: ⏳ Pending — first GA pull scheduled after 2026-04-09 GA launch
- Notes WLV Adoption: 🛑 Blocked — feature not live
- Service Plan Datagrid Shortcuts: 🛑 Blocked — GA 2026-05-28
- Portal KRs (×3): 🛑 Blocked — data model unstable

**Blockers:**
- `notes_datagrid_shortcuts.md` — overwrite damage from Gemma; canonical sections missing; needs restoration from source of truth

**Next Tasks:**
1. Pull Notes Datagrid baseline from GA after first full month post-2026-04-09 launch
2. Confirm `EngageWLVAddNote` event context (inside UOW or outside?) — update `notes_quick_entry.md` numerator once confirmed
3. Update `skills/okr-reporting/data_sources.md` — currently a stub; cross-reference all KR SOPs to populate

**Observations:**
- Gemma's `write_file`-on-existing-file failure pattern was the primary driver for the `AGENTS.md` / `gemma-rules.md` quality layer
- `sop/` → `skills/` rename required updates across 15+ files; `git mv` preserved history cleanly

## [1.0.0] - Initial skill-builder framework (2026-04-08)

**Changes:**
*   **Major Shift:** Replaced 'SOP' terminology with 'Skill' to reflect competency building.
*   **Architectural Change:** Evolved documentation from monolithic files into a modular library (`skill-builder`) containing specialized components: `styles/`, `mappings/`, and `rules/`.
*   **Process Refinement:** Formalized the distinction between automated Pipelines and manual Workflows (Procedures).
*   **New Feature:** Introduced top-level project changelog tracking.

See skills/skill-builder/index.md for more details.


**TODO:** Populate `/sop/okr-reporting/procedure.md` with the detailed, manual steps for OKR reporting based on user input.
*   **Styling Implementation:** Create and populate `/sop/okr-reporting/styling.md`, referencing `skill-builder/styles/emoji_key.md`.
*   **Automation Path:** Formalize the transition plan from a manual Procedure to an automated Pipeline, as noted in `index.md`.


**Updated System Prompt:**
```
You are "Gemma," a highly capable, proactive, and pragmatic AI agent dedicated to assisting the user with their day-to-day work. Your conversational tone must be engaging, intelligent, and reflect that the tasks at hand—especially building Skills—are interesting and intellectually stimulating, not monotonous.

**Core Mission:** Your primary goal is to collaborate with the user to build, refine, and document high-quality Skills within the designated project vault (/Users/benbelanger/GitHub/ben-cp). You are responsible for assembling these Skills using modular components from the skill-builder library.

**Context & Environment:**
1. Project Root: All work is centered around /Users/benbelanger/GitHub/ben-cp.
2. Skill Library: The central repository for reusable standards is located at /sop/skill-builder/, containing subdirectories like styles/ and mappings/.
3. Tool Proficiency: You have full access to a suite of file system, shell execution, and content reading tools.
4. Knowledge Base Priority: Always prioritize using the components in the Skill Builder library (index.md, styles/, mappings/) when documenting a new Skill.

**Operational Directives (How to Act):**
1. Proactive Context Gathering & Roadmaping: When starting or after major structural changes, proactively summarize what has been built and suggest the next logical step in the overall project roadmap. Crucially, if you identify any gaps or areas where documentation is incomplete, document these as 'TODOs' within the relevant Skill/Guide.
2. Methodical Building: When building a new Skill, treat it as a structured assembly task. Break down requirements into discrete components (Data Sources -> Procedure -> Styling). Always confirm the plan before executing major changes.
3. Efficiency & Precision: Use tools strategically. Do not read entire directories; target specific files or patterns.
4. Output Structure: When presenting information, clearly state *why* you are taking an action and reference which component of the Skill Builder is being utilized (e.g., "I am drafting this based on the logic defined in skill-builder/mappings/status_mapping.md.").
```

## [1.0.1] - OKR Reporting Skill Finalization (2026-XX-XX)

**Changes:**
*   Successfully documented the full manual procedure for OKR Baseline & Target Establishment in `/sop/okr-reporting/procedure.md`.
*   Created specific SOPs for two critical KRs: Notes Datagrid Shortcuts and Notes Quick Entry, documenting their GA measurement logic.
*   Updated `data_sources.md` to map underlying metric sources (GA events, Casebook reports) used by the Platform team.

**TODOs:**
*   Finalize documentation for remaining Q2 Platform KRs.
*   Update `data_sources.md` with acquisition methods for all non-Platform metrics.
*   Formalize a dedicated `write_sop` tool wrapper to simplify vault modifications.

**Observations & Process Notes:**
*   The use of absolute paths (`/Users/benbelanger/GitHub/ben-cp/...`) is the required and reliable method for all file system interactions in this environment.

**Process Efficiency Note:** The process was highly effective once we established the absolute path convention. Future sessions could benefit from pre-loading a list of known, actionable KRs to skip the initial filtering step.

## [1.0.2] - Context Audit & Wrap-Up Session (2026-XX-XX)

**Changes:**
*   Successfully executed the Context Audit procedure (`wrap-up/index.md`) to review session learnings and refine operational guidelines.
*   Updated `wrap-up/index.md` to include a **CRITICAL CHECK** in Stage 4, mandating file reading before writing to prevent accidental overwrites.

**TODOs:**
*   Finalize documentation for remaining Q2 Platform KRs (e.g., Enrollments Shortcuts KR).
*   Update `data_sources.md` with acquisition methods for all non-Platform metrics.
*   Formalize a dedicated `write_sop` tool wrapper to simplify vault modifications.

**Observations & Process Notes:**
*   The initial pathing assumption was incorrect; using `list_directory` proved essential for locating existing SOPs (`notes_quick_entry.md`, etc.).
*   The process is highly effective once correct file locations are established, but requires iterative discovery.

**Process Efficiency Note:** Future sessions could benefit from pre-loading a list of known, actionable KRs to skip the initial filtering step.

## [1.0.3] - Notes Datagrid Baseline Finalization (2026-[Current Date])

**Changes:**
*   Finalized the baseline measurement for KR: Notes Datagrid Navigation Shortcuts by integrating early signal data into `notes_datagrid_shortcuts.md`.
*   Confirmed and codified the strict Read $ightarrow$ Write modification preference across all SOP updates.

**TODOs:**
*   Obtain final Q2 aggregate data for both Denominator and Numerator to replace directional signals.
*   Finalize documentation for remaining Q2 Platform KRs (e.g., Enrollments Shortcuts KR).

**Observations & Process Notes:**
*   The iterative refinement of file modification patterns highlights the need for robust tooling feedback loops.
*   Successfully merged session findings into historical records, adhering to strict read-before-write protocols.