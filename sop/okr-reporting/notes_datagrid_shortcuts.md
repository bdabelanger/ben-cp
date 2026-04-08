
---

## 📊 Directional Baseline Signal (March Data)

> [!NOTE]
> ⚠️ **STATUS:** Early Signal — This data is from March and represents a pre-GA, beta cohort signal only. It should not be used for official Q2 reporting until the full GA population baseline is established.

**Data Points Pulled (March):**
*   **Denominator Count:** 85 Tenants who had beta access in March and submitted a note (Unique tenants with `noteSubmit` event).
*   **Numerator Count:** 68 Tenants who had beta access in March and used one of the new datagrid shortcuts (Unique tenants triggering one of the 5 instrumented shortcut events - `NotesWLVFilterAdded|NotesQuickFilterApplied|NotesWLVColumnToggleHidden|NotesWLVColumnToggleVisible|NotesWLVDensityChange`).

**Calculated Signal (%):** Approximately 19.0%.

**Next Steps:** This signal is lower than reality since the feature is in beta rollout, with much lower number of current tenants with the feature on than 356.

---

## 📊 Data Sources

For establishing official Q2/Q3 baselines, all data pulls must reference the master inventory at `/Users/benbelanger/GitHub/ben-cp/sop/okr-reporting/data_sources.md`. Specific instrumentation for this KR is tracked via:
*   **GA4 Property Link:** https://analytics.google.com/analytics/web/#/analysis/a122185697p384028779/edit/aK7_-dWoRZSgOlSAKdeIRQ
*   **Measurement Focus:** Tenant-level event tracking for shortcut usage and note submission.