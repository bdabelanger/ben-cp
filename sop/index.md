# General SOP Index

This document serves as the primary entry point for all Standard Operating Procedures (SOPs). Navigate to the relevant subdirectory or specific guide below based on your task.

## 🧭 Core Process Guides

*   **Platform Weekly Status Report:** To trigger the automated multi-step orchestrator and generate the weekly status report (and to review the strict rules for this workflow), see the dedicated guide: [Status Report Orchestrator SOP](/Users/benbelanger/GitHub/ben-cp/sop/project-status-reports/index.md)
*   **Rovo Issue Management:** For procedures related to finding, identifying, and retrieving information about "CBP-XXXX" issues using Atlassian Rovo tools (searchAtlassian, getJiraIssue, etc.), see the detailed guide in the Rovo subdirectory: [Rovo SOP Guide](/Users/benbelanger/GitHub/ben-cp/sop/rovo/rovo-sop.md)

## 📂 Sub-Category Guides

*   **Data Modeling & Reporting:** Procedures for SQL join maps, BI modeling strategies, and schema relationships are located here: [Reporting Guide](/Users/benbelanger/GitHub/ben-cp/sop/casebook-reporting/index.md)
*   **Case Intake:** Guidance on initial case intake procedures (refer to specific file in the reporting subdirectory for details): [Intake Guide](/Users/benbelanger/GitHub/ben-cp/sop/casebook-reporting/casebook-intake.md)
*   **People Data:** Schema and relationship definitions for client, provider, and subject demographics: [People Data](/Users/benbelanger/GitHub/ben-cp/sop/casebook-reporting/casebook-people.md)
*   **System Users:** Guides for managing system accounts (caseworkers, admins) scoped to a tenant: [User Management](/Users/benbelanger/GitHub/ben-cp/sop/casebook-reporting/casebook-users.md)
*   **Tenant Security & Scoping:** Mandatory rules for multi-tenancy architecture and data isolation: [Tenant Rules](/Users/benbelanger/GitHub/ben-cp/sop/casebook-reporting/casebook-tenants.md)

***

## 🔗 Cross-Cutting Concerns

*   **Polymorphic Linking:** The `resource_id` field functions as a polymorphic foreign key, where the actual entity is determined by the accompanying `resource_type`. This allows entities like 'Notes' to link contextually across various core tables (Cases, Intake, People) using a single ID structure.
*   **Multi-Tenancy Directive:** ALL operational queries MUST include a strict filter on `tenant_id` for data isolation.

## 🛠️ File Management & Tone Guide

**Tone Expectation:** Aim for 'witty brevity'—think sharp, not stoic. A little flair goes a long way.

**File Safety:** Before making any edits or writing to any SOP file via the filesystem tools, ALWAYS use 'read_text_file' first to pull a fresh copy of the content. This prevents overwriting recent changes.