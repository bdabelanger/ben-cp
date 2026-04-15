# Implementation Plan: Artifact-Led Threshold Policy

> **Prepared by:** Code (Gemini) (2026-04-14)
> **Assigned to:** Cowork
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS: ✅ COMPLETE — 2026-04-14**

Successfully established the tiered documentation policy, allowing for atomic (P4) execution while mandating full rigor (P1/P2) for critical tasks. This optimizes for both speed and mobile accessibility.

---

---
project: Infrastructure / Governance
status: READY
version: 2026.04.14
tags: [policy, workflow, artifacts]
agent_sync: Gemini-Native
---
# Policy: Artifact-Led Complexity Thresholds

## Objective
To balance operational speed with documentation rigor. This policy defines which "Artifacts" are required based on the Priority (P) and Complexity of a task.

## The Decision Matrix

| Priority | Lifecycle Requirement | Artifacts Required |
| :--- | :--- | :--- |
| **P1 (Critical)** | **Full Rigor** | `implementation_plan.md`, `task_handoff.md`, `walkthrough.md` |
| **P2 (Major)** | **Standard** | `implementation_plan.md`, `task_handoff.md` |
| **P3 (Minor)** | **Lightweight** | `task_handoff.md` (Plan included as a section) |
| **P4 (Trivial)** | **Atomic** | Direct execution with a `changelog.md` entry only. |

## Definition of Artifacts

1. **`implementation_plan.md`**: Required for P1/P2. Must be reviewed by the User or a Peer Agent before code is touched. Focuses on "The Why" and "The Path."
2. **`task_handoff.md`**: The execution instructions. For P3, this contains the "Proposed Logic" at the top to bypass the need for a separate plan.
3. **`walkthrough.md`**: Required for P1. A post-execution summary including "Lessons Learned" and "Verification Results." Optimized for NotebookLM ingestion.

## Implementation Rules
- **No Ghost Plans**: Agents must not start P1/P2 work without a committed plan.
- **Transclusion**: For P2/P3 tasks, agents are encouraged to "transclude" (copy-paste) the plan into the final walkthrough to keep the "Truth" in one file.
- **Mobile Read-Only**: Handoffs and Walkthroughs must use H1/H2 headers to ensure the Gemini iPhone app can provide clear voice summaries.

## Success Criteria
- Reduced "hallucination loops" in P1 refactors.
- High-fidelity voice summaries on iPhone 16 Pro Max via NotebookLM/Gemini.
- 0% bureaucracy for P4 maintenance tasks.
