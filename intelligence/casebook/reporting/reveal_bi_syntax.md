---
title: Reveal BI Formula Syntax  Rules
type: intelligence
domain: intelligence/casebook/reporting
---

# Reveal BI Formula Syntax & Rules

## Core Syntax Rules
When generating formulas, calculated fields, or custom metrics for Reveal BI, the model MUST adhere to the following syntax:
1. **Field References:** All dataset columns/fields must be enclosed in square brackets. 
   * *Correct:* `[case_id]`
   * *Incorrect:* `case_id`, `{case_id}`
2. **Text Strings:** Any raw text string or format parameter must be wrapped in double quotes. 
   * *Correct:* `"dd/mm/yyyy"`, `"Active"`
3. **Pre-Calculated vs. Post-Calculated:** Reveal BI applies formulas to either raw row-level data or aggregated visualization data. Ensure formulas logically reflect this (e.g., use row-level `[budget]` vs. aggregated `Sum of Budget`).

## Supported Function Categories

### 1. Logic & Conditional (IF/THEN)
Reveal BI uses a standard nested `if` structure.
* **Syntax:** `if(condition, true_value, false_value)`
* **Example (Case Status):** `if([close_date] = empty(), "Active", "Closed")`
* **Supported Logic:** `and()`, `or()`, `not()`, `true()`, `false()`, `empty()`, `isempty()`

### 2. Aggregation with Conditions
Reveal uses specific `IF` suffixed functions instead of complex CASE statements for conditional aggregations.
* **Supported:** `averageif`, `countif`, `maxif`, `minif`, `sumif`
* **Syntax:** `FUNCTIONIF({expression}, {if-condition})`
* **Example (Count Active Cases):** `countif([case_id], isempty([close_date]))`

### 3. String Manipulation
Crucial for parsing the `resource_labels` or concatenating names.
* **Supported:** `concatenate`, `find`, `len`, `lower`, `mid`, `replace`, `trim`, `upper`
* **Example (Full Name):** `concatenate([first_name], " ", [last_name])`

### 4. Date Functions
* **Supported:** `datediff`, `formatdate`, `fquarter`, `fyear`, `today()`, `now()`, `month()`, `year()`
* **Example (Days Open):** `datediff([open_date], today(), "d")`