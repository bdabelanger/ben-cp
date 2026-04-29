# Implementation Plan: Enhance Tasks Report Output Specification

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** Cowork
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: 🔲 READY — pick up 2026-04-29

---

**Goal:** Modify the 'tasks' report generation pipeline (Skill: `tasks`) to provide a more actionable output for human review and agent consumption.

**Required Changes:**
1.  **Content Inclusion:** The report must include the actual task content/description for each listed item, not just the title.
2.  **Cross-System Linking:** For every Asana task, the report must list all associated Jira issues (and vice versa).
3.  **Sorting Logic:** All tasks must be sorted first by **Due Date**, and secondarily by **Priority** (P1 > P2 > P3...).
4.  **Presentation Layer Rule:** The default output of the report should *only* surface prioritized titles and links, suppressing full content unless explicitly requested by a human user.
5.  **Utility vs. Actionable Data:** Task counts are useful for high-level dashboards but should not be the primary focus of the actionable task list.

This change requires modification to the `tasks/SKILL.md` or associated pipeline scripts within the repository structure. Please coordinate with Code Agent for implementation.