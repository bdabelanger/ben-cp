
---

## 📊 Directional Baseline Signal (March Data)

> [!NOTE]
> ⚠️ **STATUS:** Early Signal — This data is from March and represents a pre-GA, beta cohort signal only. It should not be used for official Q2 reporting until the full GA population baseline is established.

**Data Points Pulled (March):**
*   **Denominator Count:** 85 Tenants who had beta access in March and submitted a note (Unique tenants with `noteSubmit` event).
*   **Numerator Count:** 68 Tenants who had beta access in March and used one of the new datagrid shortcuts (Unique tenants triggering one of the 5 instrumented shortcut events - `NotesWLVFilterAdded|NotesQuickFilterApplied|NotesWLVColumnToggleHidden|NotesWLVColumnToggleVisible|NotesWLVDensityChange`).

**Calculated Signal (%):** Approximately 19.0%.

**Next Steps:** This signal is lower than reality since the feature is in beta rollout, with much lower number of current tenants with the feature on than 356.