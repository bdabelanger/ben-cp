---
type: system_instruction
domain: bi_tool_visualizations
tool: reveal_bi
description: Guidelines for mapping the SOP datasets to Reveal BI visualization types and statistical functions.
Status: published
Priority: P3
Date: 2026-04-26
Owner: Ben
---
# Reveal BI Visualization Guidelines

## Statistical Functions
Reveal BI has built-in advanced predictive analysis that the model should recommend when appropriate:
1. **Time Series Forecast:** Uses exponential smoothing. 
   * *Required Parameters:* `Season Length` (e.g., 12 months) and `Periods to Forecast`.
   * *Best used for:* Predicting future Intake Report volumes based on historical seasonal trends.
2. **Linear Regression:** * *Best used for:* Showing the trendline of time-to-resolution for cases over time.

## Recommended Visualization Mappings
When recommending dashboard components based on the SOP, map the data to these Reveal BI native chart types:

### 1. Pivot Grids
* **Use Case:** Complex cross-tabulations.
* **SOP Application:** Aggregating `[case_id]` counts by `[tenant_id]` on the rows, and `[resource_labels]` on the columns.

### 2. Funnel Charts
* **Use Case:** Conversion tracking.
* **SOP Application:** Tracking the lifecycle from the `intake` table (`[report_id]`) to the `cases` table (`[case_id]`) to measure drop-off rates.

### 3. Tree Maps
* **Use Case:** Hierarchical data or proportional sizing.
* **SOP Application:** Visualizing the distribution of case types or resource allocations within a specific `tenant_id`.

## Visualization Generation Directives
When asked to create a dashboard view, the model MUST output:
1. **Chart Type:** (e.g., Bar Chart, Pivot Grid)
2. **Values (Y-Axis/Aggregations):** The exact Reveal BI formula or aggregation (e.g., `count([case_id])`).
3. **Labels/Categories (X-Axis):** The grouping field (e.g., `[month]`).
4. **Filters:** Any required tenant scoping (e.g., `Filter: [tenant_id] = target`).