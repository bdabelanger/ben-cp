---
title: Implementation Plan Archive skills intelligence - Unused Legacy Directory
type: handoff
domain: handoffs
---

# Implementation Plan: Archive skills intelligence - Unused Legacy Directory

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: 🔲 READY

---

## Context

`skills/intelligence/` is a legacy directory from a previous architectural era. It contains concepts ("Vault Auditor", "Daily Progress Summary", "cognitive core", memory/analysis/report pipeline) that no longer reflect how the vault works. Nothing active points to it — the only reference is a stale migration debt entry in `intelligence/governance/policy.md`.

## Goal

Archive `skills/intelligence/` and clean up the stale reference.

## Execution Steps

1. Move `skills/intelligence/` to `skills/archive/intelligence/` (or delete entirely — read the files and use judgment on whether any content is worth preserving)
2. In `intelligence/governance/policy.md`, remove the stale `notes.md` entries under "Stale Ephemeral Session Files" that reference `skills/intelligence/` paths
3. Update `skills/index.md` if it lists `intelligence/` as a subdirectory

## Verification

- `skills/intelligence/` no longer exists at its original path
- No broken links pointing to `skills/intelligence/` (run links sensor or grep)
- `intelligence/governance/policy.md` migration debt section is clean
