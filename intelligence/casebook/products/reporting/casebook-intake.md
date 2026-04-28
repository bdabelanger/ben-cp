---
title: 'Dataset: Intake'
type: intelligence
domain: intelligence/casebook/reporting
---


# Dataset: Intake

## Context
The `intake` table captures data before it officially enters the `cases` workflow. It acts as a staging queue or historical log of initial contact.

## Schema Attributes
* `report_id` (PK): Unique alphanumeric identifier for the intake record.
* `resource_id` (FK): Links to `resource_labels`.
* *Other inferred fields:* Intake Date, Submission Source, Initial Priority, Intake Summary.

## Relationships
* **To Cases:** Connects via the **Case Assignees** table using `report_id`. 
* **To Notes:** Connects via the **Note Resources** bridge table, allowing contextual notes to be attached to an intake report before a case is even generated.
* **To Resource Labels:** Direct join using `resource_id`.

## Join Logic & Interpretability
* **Conversion Analysis:** To determine if an intake report resulted in an active case, execute an `INNER JOIN` with `case_assignees` on `report_id`. Records in `intake` lacking a match in `case_assignees` represent unconverted or pending reports.
* **Documentation:** Pre-case notes are attached to `intake` via the `note_resources` bridge. When a case is generated from an intake report, ensure queries look at *both* the intake notes and case notes for a complete history.