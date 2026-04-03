# Schema Relationships & Data Joins

This document serves as a quick reference for spinning up SQL joins or BI tool data models based on the Joining Guide.

## Core Join Map
* **Cases + Intake:** `Cases` <-(Case Assignees)-> `Intake` (Key: `report_id`)
* **Cases + People:** `Cases` <-(Case Involvements)-> `People` (Key: `person_id`)
* **Cases + Resources:** `Cases` <-> `Resource Labels` (Key: `resource_id`)
* **Contextual Notes:** `Notes` <-(Note Resources)-> `Cases` OR `Intake` OR `Providers`

## BI Tool Modeling Strategy
When importing this into a tool like Tableau, PowerBI, or Looker:
1.  Use **People** as your central fact table.
2.  Ensure that bridge/junction tables are used to prevent Cartesian explosion (many-to-many duplication) when aggregating counts.
3.  Implement the "Correct Concat" logic at the view/query level for Resource Labels so visualizations read cleanly.