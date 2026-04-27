# Implementation Plan: Improve Transcripts Skill — Rich Meeting Support + capture_task Clarification

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

The transcripts skill (`skills/transcripts/SKILL.md`) was tested on a rich discovery review meeting (Weekly Discovery Review - Reporting, Apr 22, 2026) and produced poor output. The skill is designed for structured standup emails with `[Name] Action: Description` formatting, but was applied to a full narrative meeting transcript. The result was 6 tasks with:

- Titles that just repeated the next-steps bullet verbatim
- Summary and Introduction sections that duplicated the title
- Empty Acceptance Criteria (`- [ ]` with nothing in it)
- Blank Figma and Asana Project link fields
- No due dates
- No meeting context, design decisions, or open questions captured
- All tasks dumped into PD - Small Projects regardless of topic

Additionally, Code invoked a `capture_task` tool that does not appear to exist as a standalone skill. There is `skills/tasks/SKILL.md` (deliverable governance) and `skills/transcripts/SKILL.md` (standup harvester), but no `capture_task` skill. Code appears to have improvised a hybrid.

## Root Cause Analysis

1. **Wrong input type**: The transcript skill is built for standup emails, not rich design review meetings. It has no instruction to extract narrative context — it only parses the "Next steps" block.
2. **Missing mode**: There is no "rich meeting" mode that produces a handoff for Cowork rather than tasks directly. The skill SKILL.md itself says task creation should be interactive — *"Cowork then picks up the handoff and works through each item interactively with Ben."* Code bypassed this.
3. **Template quality**: The task template (Summary → Introduction → Acceptance Criteria → Links) produces hollow output when the harvester doesn't populate it. Empty checkboxes and blank link fields should either be conditionally populated or omitted.
4. **No routing logic**: The skill has no mechanism to determine which Asana project a task belongs to beyond the PD - Small Projects fallback. For meeting-specific tasks, this is almost always wrong.
5. **`capture_task` undefined**: If this is a new tool name post-refactor, it needs a SKILL.md. If it was an alias, it needs to be removed or redirected.

## Execution Steps

- [ ] **Add a "rich meeting" mode to the transcript skill**: When input is a full meeting transcript (not a standup email), the skill should produce a handoff for Cowork rather than creating tasks directly. Cowork will then work through items interactively with Ben.
- [ ] **Improve context extraction**: For rich meeting mode, the harvester should include per-item context from the meeting narrative — not just the next-steps bullet. At minimum: meeting title, date, relevant discussion snippet, and any open questions tied to the action item.
- [ ] **Fix the task template**: Make Acceptance Criteria, Figma, and Asana Project link fields conditional — only include them if populated. An empty `- [ ]` checkbox and blank link fields add noise and signal low quality.
- [ ] **Add routing hints for project assignment**: Extend `skills/transcripts/schemas/people.json` or add a separate config to map meeting topics/attendees to likely Asana projects. This prevents everything defaulting to PD - Small Projects.
- [ ] **Clarify or create `capture_task`**: Either document it as a named skill with a SKILL.md, or remove the reference. If it was renamed from `standup`, update any agent instructions that may reference the old name.

## Verification

- [ ] Running the skill on a standup email produces the same quality output as before
- [ ] Running the skill on a rich meeting transcript produces a handoff for Cowork (not tasks directly)
- [ ] Cowork can pick up the handoff and interactively create well-contextualized tasks with Ben
- [ ] Task template no longer includes empty Acceptance Criteria or blank link fields when unpopulated
