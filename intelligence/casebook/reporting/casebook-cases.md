---
entity: cases
type: fact_table
primary_key: case_id
foreign_keys:
  - resource_id
bridge_tables:
  - case_involvements
  - case_assignees
  - note_resources
description: The central anchor entity for active case management.
Status: published
Priority: P3
Date: 2026-04-26
Owner: Ben
---
# Dataset: Cases

## Context
The `Cases` dataset serves as the central hub for tracking active investigations, services, or resource allocations. It acts as the primary anchor point for bridging individuals, initial intake reports, and associated resources.

## Schema Attributes
* `case_id` (PK): Unique alphanumeric identifier.
* `resource_id` (FK): Links to `resource_labels`.
* *Other inferred fields:* Case Status, Open Date, Close Date, Case Type.

## Relationships
* **To People:** Connects via the **Case Involvements** bridge table using `person_id`.
* **To Intake:** Connects via the **Case Assignees** table using `report_id`.
* **To Notes:** Connects via the **Note Resources** bridge table.
* **To Resource Labels:** Direct join using `resource_id`.

## Join Logic & Interpretability
When querying `cases`, be aware that resources, people, and intake reports are separated into distinct tables. 
* To find who is involved in a case, traverse: `cases.case_id` -> `case_involvements` -> `people.person_id`.
* To retrieve labels, apply the "Correct Concat" function to roll up multiple `resource_id` rows into a single comma-separated string per `case_id` to maintain row granularity.


## Dataset: Cases

## Overview

## Key Identifiers & Fields
* `case_id` (Primary Key): Unique identifier for each case.
* `resource_id` (Foreign Key): Used to join with **Resource Labels**.

## Suggested Queries for Manual Creation
1.  **Active Cases Query:** Filter for unresolved cases to determine current workload.
2.  **Resource Label Concat Query:** Utilize the "Correct Concat" calculation referenced in the Joining Guide to group all resource labels associated with a single `case_id`.
3.  **Time-to-Resolution Query:** Calculate the average time between an Intake Date and a Case Closure Date.

## Visualization Ideas
* **Bar Chart:** Count of active cases grouped by Resource Label.
* **Line Graph:** Trend of new cases created month-over-month.