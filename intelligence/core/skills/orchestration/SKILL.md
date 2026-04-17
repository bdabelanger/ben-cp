---
name: orchestration
description: The execution engine of the vault. Manages coordination, tracking, and governance protocols.
preferred_agent: mission-integrity
---

# SKILL: Orchestration Domain

> **Purpose:** Manages the operational standards of the vault.
> **Preferred Agent:** Intelligence (Synthesize)
> **Domain Tree:** `collaboration/`, `changelog/`, `access/`

---

## Governance Standards

The Orchestration domain defines the mandatory protocols for all agents operating in the vault:

### 1. Coordination (Collaboration)
- Every session starts with a **Handoff Check**.
- Significant context is captured in **human user notes**.
- Tasks are moved through the **Handoff Protocol**.

### 2. Tracking (Changelog)
- Every significant change is recorded in a **subdirectory changelog**.
- Every session is summarized in the **root changelog**.
- The **Changelog Auditor** verifies that diffs match documentation.

### 3. Governance (Access)
- Access is restricted per **AGENTS.md**.
- The **Access Auditor** identifies permission drift or security risks.
- Overwrites and deletions are P1 violations.

---

## Operational Mandate

Any agent operating within the Orchestration domain is responsible for maintaining the stability and transparency of the vault. If a governance or tracking protocol fails, it is an automatic P1 blocker.
