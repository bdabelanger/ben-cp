# Implementation Plan: Define Casebook Product-Feature Taxonomy for Task Capture

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Ben + Cowork
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

The `capture_task` MCP tool infers a product area label from capture text to build Jira issue summaries in the format:

```
Product - Feature — Summary description
```

Currently the inference map is a rough keyword approximation. Before wiring it into the live tool, Ben needs to define the authoritative Casebook product/feature taxonomy so the map is accurate and maintainable.

---

## Problem

- `[New Initiative]` and `[Captured]` are placeholder prefixes — not meaningful product areas
- Casebook has a product/feature hierarchy (e.g. Engage → Notes, Enrollments, WLV) that isn't formally documented in the vault
- The inference map in `capture_task` should reference a vault intelligence record, not hardcoded guesses

---

## Format Convention (confirmed by Ben, 2026-04-27)

- **Hyphenate** product and feature: `Engage - Notes`
- **Comma-separate** multiple areas (no "and"): `Engage - Notes, Enrollments`
- **Em-dash** before the summary: `Engage - Notes — Date field not saving`
- **No brackets** around the product area

---

## Work Required

### Step 1 — Ben: Define the taxonomy
Provide the canonical product/feature map. Questions to answer:
- What are the top-level products? (e.g. Engage, Platform, ?)
- What features live under each product?
- Are there standalone areas with no parent product (e.g. Reporting, Integrations, Security)?
- What's the correct label for Enrollments — `Engage - Enrollments` or just `Enrollments`?

### Step 2 — Cowork: Codify as intelligence record
Create `intelligence/product/taxonomy.md` with the full map in a structured format Code can parse.

### Step 3 — Code: Wire into `capture_task`
Replace the hardcoded keyword map in `src/ben-cp.ts` with a function that reads from the intelligence record (or a compiled constant derived from it).

---

## Shell Taxonomy (to be validated by Ben)

| Signal keywords | Inferred area |
|---|---|
| notes, autosave, service record, case note | `Engage - Notes` |
| enrollments, bulk data, enroll | `Enrollments` |
| wlv, workload | `Engage - WLV` |
| datagrid, data grid | `Engage - DataGrid` |
| dynamic pages | `Engage - Dynamic Pages` |
| navigation, search, nav | `Platform - Navigation` |
| gp, granular perm | `Platform - GP` |
| reporting, reveal, redshift | `Reporting` |
| zapier, api, nylas, integrat | `Integrations` |
| security, soc, cjis, prowler | `Security & Compliance` |
| kafka, rails, node, ec2, infra, karpenter | `Infrastructure` |
| workflows, workflow | `Platform - Workflows` |
| *(no match)* | `Platform` |

