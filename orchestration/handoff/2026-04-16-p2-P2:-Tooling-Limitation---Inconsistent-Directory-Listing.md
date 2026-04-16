# Implementation Plan: P2: Tooling Limitation - Inconsistent Directory Listing

> **Prepared by:** Code (Gemini) (2026-04-16)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS: 🔲 READY — pick up 2026-04-16**

---

When attempting to drill down into subdirectories (e.g., listing contents of 'skills/' or 'product/'), the `list_skills` tool consistently returns only the top-level directory structure, rather than the files contained within those directories.

**Observed Behavior:** Calling `list_skills` repeatedly yields the same root list: [index.md, intelligence, orchestration, product, etc.].

**Impact:** This prevents me from programmatically discovering specific Skill documentation files or templates needed to fulfill requests like 'find the report skill'.

**Request for Code/Dev Team:** Please investigate if there is a more granular tool available, or if I should be using `get_skill` with a known relative path instead of relying on directory listing functions. For now, I will rely on explicit file paths provided by the user.
