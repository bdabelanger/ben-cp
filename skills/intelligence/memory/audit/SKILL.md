---
name: audit
description: Instruction-driven vault auditor. Renamed from watchdog. Executes checks based on per-skill audit.md requirements and global mappings. Overseen by the Vault Auditor.
---

# SKILL: Audit

> **Role:** Custodian of Structural Truth and Compliance
> **Agent:** Vault Auditor
> **Entry point:** `skills/memory/audit/index.md`
> Last updated: 2026-04-12

---

## The Audit Protocol (Instruction-Driven)

Instead of hardcoded checks, the Audit skill now takes an **instruction** or **target**.

### Procedure:
1. **Identify Target**: Determine the skill or domain to audit.
2. **Read Requirements**: Load the `audit.md` file located within the target skill directory (e.g., `skills/product/audit.md`).
3. **Load Mappings**: Consult the root `mapping/` directory for health rules or logic stubs required by the audit.
4. **Execute**: Perform the validations described in the `audit.md` "Audit Procedure" section.
5. **Report**: Write findings to the centralized root directory: `outputs/memory/audit/audit-report-[TARGET]-[YYYY-MM-DD].md`.

---

## Standard Checks (Legacy Watchdog)
The original 8 structural hygiene checks are now considered a "Global Structural Audit" instruction.
- **Target**: `vault/root`
- **Requirements**: Defined in `skills/memory/audit/structural_requirements.md` (Legacy SKILL.md content).

---

## Output Contract
All audit logs, reports, and flags are stored in the root `outputs/` tree to ensure privacy and prevent repository bloat.
