---
title: Handoff Mandatory Adoption of Artifact-Led Workflow
type: handoff
domain: handoffs/complete
---

# Handoff: Mandatory Adoption of Artifact-Led Workflow

## Goal
Codify and enforce the **Plan → Task → Walkthrough** workflow across all agentic operations within the ben-cp vault, governed by the newly established [Complexity Threshold Policy](file:///Users/benbelanger/My%20Drive%20(ben.belanger@casebook.net)/ben-cp/orchestration/handoff/2026-04-14-p2-Artifact-Led-Threshold-Policy.md).

## Context
To ensure human oversight, safety, and cross-agent continuity, we are moving away from ephemeral `notes.md` planning. This handoff executes the transition to the tiered artifact standards defined by Gemini.

## Required Changes

### 1. Update Core Documentation
- **Tiered Rigor**: Ensure `AGENTS.md` explicitly links to the [Decision Matrix](file:///Users/benbelanger/My%20Drive%20(ben.belanger@casebook.net)/ben-cp/orchestration/handoff/2026-04-14-p2-Artifact-Led-Threshold-Policy.md) to define when artifacts are mandatory.
- **Header Standards**: Update `skills/orchestration/handoff/index.md` to enforce **H1/H2 header hierarchies** for mobile accessibility (iPhone/NotebookLM optimization).

### 2. Audit Enforcement (Cowork Scrutiny)
- **Threshold Validation**: Cowork must now use the Decision Matrix to audit incoming handoffs. If a P1/P2 handoff lacks an `implementation_plan.md`, it is a hard block.
- **Mobile Fidelity**: Verify that all artifacts use the requested header structure for voice-optimized summaries.

### 3. Skill Integration
- **Transclusion Policy**: Add a "Transclusion" section to the handoff template, encouraging agents to include the original plan in final walkthroughs for "Single Source of Truth."

## Success Criteria
- [ ] AGENTS.md updated with the Tiered Threshold Matrix.
- [ ] No P1/P2 tasks bypass the `implementation_plan.md` stage.
- [ ] Walkthroughs for P1 tasks are formatted correctly for NotebookLM ingestion.

## Scrutiny & Discussion
The "Atomic" P4 rule allows for speed on maintenance. However, agents should not use P4 to "bury" logic changes that actually affect system behavior. When in doubt, escalate to P3 with a lightweight handoff.
