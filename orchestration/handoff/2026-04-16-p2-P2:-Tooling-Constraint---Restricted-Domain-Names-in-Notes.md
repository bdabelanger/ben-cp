# Implementation Plan: P2: Tooling Constraint - Restricted Domain Names in Notes

> **Prepared by:** Code (Gemini) (2026-04-16)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS: 🔲 READY — pick up 2026-04-16**

---

When attempting to log contextual notes into the vault using `add_note`, I encountered an error because the tool requires a specific, pre-approved domain name (e.g., 'product') rather than allowing arbitrary paths (e.g., 'skills/product/projects').

**Impact:** This limits my ability to create highly granular documentation notes directly within subdirectories of skills or domains.

**Request for Code/Dev Team:** Please review the domain validation logic for `add_note` to allow for more flexible, path-based domain specification, which would greatly improve contextual logging capabilities.