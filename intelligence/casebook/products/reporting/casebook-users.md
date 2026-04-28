---
title: 'Dataset: Users'
type: intelligence
domain: intelligence/casebook/reporting
---


# Dataset: Users

## Context
The `users` table contains the system-level accounts (staff, caseworkers, administrators) who log into the platform. This is distinct from the `people` dataset; `users` manage the system, while `people` are the subjects/clients within the system.

## Schema Attributes
* `user_id` (PK): Unique identifier for the system account.
* `tenant_id` (FK): The organization to which this user belongs.
* *Inferred fields:* Email, Role/Permission Level, Last Login.

## Join Logic & Interpretability
* **To Cases/Intake:** Often joined to track ownership or assignment (e.g., `cases.assigned_user_id` = `users.user_id`).
* **Tenant Boundary:** A user belongs to one tenant. Queries must ensure user actions are only evaluated within their respective `tenant_id` context.