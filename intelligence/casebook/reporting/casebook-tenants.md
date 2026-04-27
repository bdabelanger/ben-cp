---
title: 'Dataset: Tenants'
type: intelligence
domain: intelligence/casebook/reporting
---


# Dataset: Tenants

## Context
The `tenants` table represents the highest level of hierarchy in the multi-tenant architecture. Every organization using the platform has a unique `tenant_id`. In a shared database model, this ID is the fundamental partition key for data isolation.

## Schema Attributes
* `tenant_id` (PK): Unique identifier for the organization/agency.
* *Inferred fields:* Organization Name, Subscription Tier, Active Status, Onboarding Date.

## Join Logic & Interpretability
* **Global Scoping:** This table rarely needs to be joined directly in day-to-day operational queries. Instead, its primary key (`tenant_id`) exists as a foreign key on almost every other table in the system (Cases, People, Intake, etc.).
* **Admin Reporting:** Join this table when generating cross-organizational platform metrics (e.g., "Which tenants have the highest volume of active cases?").


## Multi-Tenancy Architecture Rules

## Core Directive: The Tenant Partition
This System of Record utilizes a shared database multi-tenant architecture. Data for all organizations coexists in the same tables, partitioned logically by a `tenant_id` column.

## Mandatory Query Generation Rules
1. **Absolute Scoping:** EVERY query generated for operational reporting MUST include a `WHERE tenant_id = [TARGET_TENANT]` clause or be joined in a way that strictly filters by the target tenant.
2. **No Cross-Pollination:** Never generate queries that aggregate or expose data across different `tenant_id`s unless specifically requested by a super-admin for platform-wide analytics.
3. **Implicit Columns:** Assume all primary operational tables (`cases`, `people`, `intake`, `notes`) possess a `tenant_id` column, even if not explicitly listed in their individual schema definitions.