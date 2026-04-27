---
title: Dataset People
type: intelligence
domain: intelligence/casebook/reporting
---

# Dataset: People

## Context
The `people` table is the single source of truth for individual human data. It is decoupled from `cases` to allow a single person to exist across multiple current or historical cases. The `People` dataset contains the demographic, contact, and profile information for all individuals interacting with the system, whether they are clients, providers, or subjects of a case.

## Schema Attributes
* `person_id` (PK): Unique alphanumeric identifier for an individual.
* `resource_id` (FK): Links to `resource_labels`.
* *Other inferred fields:* First Name, Last Name, Date of Birth, Demographic details.

## Relationships
* **To Cases:** Connects via the **Case Involvements** table using `person_id`. This is a many-to-many relationship (one person can be involved in multiple cases, and one case can involve multiple people).
* **To Intake Reports:** Connects via the **Intake People** table using `person_id`. This is a many-to-many relationship (one person can be involved in intake reports, and one intake report can involve multiple people).
* **To Resource Labels:** Direct join using `resource_id`.

## Join Logic & Interpretability
* **Relationship to Cases:** Many-to-Many. Always use `case_involvements` to connect a `person_id` to a `case_id`. Do not assume a 1:1 relationship between a person and a case.
* **Common Analytical Groupings:** This table is primarily used for demographic filtering (grouping active cases by the age, location, or status of the involved individuals).