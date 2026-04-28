# Platform Weekly Status — April 28, 2026

## 📋 Summary
1. [Notes - Notes datagrid](#CBP-2736) [stage:GA]||👀 1 P1, 6 P2, 4 P3, 1 P4 left
2. [Web applications - Material UI upgrade (all components)](#CBP-2917) [stage:GA]||1 P2 left
3. [Enrollment dialog - Bulk Services section](#CBP-2992) [stage:Beta]||2 P2 left
4. [Notes - Bulk "General Notes"](#CBP-2752) [stage:Beta]||1 P3 left
5. [Notes - Locked Notes](#CBP-2923) [stage:In UAT]||3 P2 left
6. [Services - Service plan datagrid with bulk actions](#CBP-3066) [stage:Development]||9 P2 left
7. [Services WLV - Bulk actions](#CBP-3121) [stage:Development]||5 P2 left
8. [Notes - Bulk Service Notes](#CBP-2924) [stage:Development]||👀 2 P1, 10 P2, 7 P3, 1 P4 left
9. [Integrations - Zapier improvements](#CBP-3158) [stage:Development]||2 P2 left

---
## 📋 Detailed Status

#### GA

### [Notes - Notes datagrid](https://app.asana.com/1/1123317448830974/project/1209963394727039) · CBP-2736 · GA
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>On track to release single-clicking on notes title to open authoring UX and rows per page PERF improvement.</div>
PRD: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/3812753669

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* ✅ Beta Start - Apr 1
* ✅ GA - Apr 27
[jira:CBP-2736]

**Status** (Grain: Stories)
`▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░▒░░▒▒▓▓▒▓▒▒░▒ 22 done · 7 in progress · 5 to do`

**Readiness** (Grain: Stories)
`Readiness: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓!!!!!------- (5 Lagging · 7 Unmapped · 22 Done)`

**Estimate** (Grain: Days)
`35.1d estimated · 18.2d actual · 4.0d remaining (63%)`

> **🛑 Off Track / ⚠️ At Risk Escalation**: 41% of open issues are Lagging or Stalled.

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 0 | 0 | 5 | 7 |


**Done:** 22 issues
~~31.1d estimated · 18.2d actual

**In Progress:** 7 issues · ~4.0d est remaining
- 🛑 [CBP-3183](https://casecommons.atlassian.net/browse/CBP-3183) — Notes - Lagging Case Details page when page size = 50||Russell · Product approved · 👀 Unestimated · 👀 No actual · P1 · Release: 2026-4-2
- 🛑 [CBP-3105](https://casecommons.atlassian.net/browse/CBP-3105) — Notes - Migrate Start/End dates from service interactions to service notes||Tuan · Product approved · 1.0d estimated · 👀 No actual · P2 · Release: 2026-4-2
- 👀 [CBP-3107](https://casecommons.atlassian.net/browse/CBP-3107) — Notes - Rename date fields for Services section||Bisoye · Merged to QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 🛑 [CBP-3150](https://casecommons.atlassian.net/browse/CBP-3150) — Notes - Synchronize note_people and service_interaction_people attributes||Tuan · Merged to QA · 2.0d estimated · 👀 No actual · P2 · Release: 2026-5-1
- 🛑 [CBP-3254](https://casecommons.atlassian.net/browse/CBP-3254) — FE - write the note start/end date on the old service note module||Tuan · Product approved · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-4-2
- 👀 [CBP-3186](https://casecommons.atlassian.net/browse/CBP-3186) — Notes - Clean up "Locked Note" FE handling||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · 👀 No release
- 🛑 [CBP-3059](https://casecommons.atlassian.net/browse/CBP-3059) — Notes datagrid - Display Services data in Note preview as structured list||Blessing · Merged to QA · 1.0d estimated · 👀 No actual · P4 · Release: 2026-5-1

**To Do:** 5 issues
- 👀 [CBP-3055](https://casecommons.atlassian.net/browse/CBP-3055) — Notes - Enable row pinning in Notes Datagrid||Bisoye · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3191](https://casecommons.atlassian.net/browse/CBP-3191) — Notes - Synchronize note_resources and service_interaction_people_resources attributes||Ben · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3054](https://casecommons.atlassian.net/browse/CBP-3054) — Notes - Enable multi-filter stacking in Notes Datagrid||Bisoye · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release
- 👀 [CBP-3060](https://casecommons.atlassian.net/browse/CBP-3060) — Notes - Evaluate nested DataGrid approach for Services data in Note preview||Pierre · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release
- 👀 [CBP-3062](https://casecommons.atlassian.net/browse/CBP-3062) — Notes - Enhance Service(s) column display in Notes Datagrid collapsed state||Pierre · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release

### [Web applications - Material UI upgrade (all components)](https://app.asana.com/1/1123317448830974/project/1212552174642233) · CBP-2917 · GA
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p><ul><li>On track to roll out MUI across Home web</li><li>People remains + any enhancements / bug fixes</li></ul></div>

**Launch Plan**
* ✅ QA Start - Mar 16
* ✅ UAT Start - Apr 3
* 🎯 GA - Jun 1
[jira:CBP-2917]

**Status** (Grain: Stories)
`▓▓▓▓▓▓▓▓▓░ 9 done · 0 in progress · 1 to do`

**Readiness** (Grain: Stories)
`Readiness: ▓▓▓▓▓▓▓▓▓▒ (1 Aligned · 9 Done)`

**Estimate** (Grain: Days)
`6.0d estimated · 3.5d actual · 0.0d remaining (58%)`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 1 | 0 | 0 | 0 |


**Done:** 9 issues
~~6.0d estimated · 3.5d actual

**To Do:** 1 issues
- [CBP-3221](https://casecommons.atlassian.net/browse/CBP-3221) — SWW occurs on clicking add service note option via new service plan grid||Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-5-1

#### Beta

### [Enrollment dialog - Bulk Services section](https://app.asana.com/1/1123317448830974/project/1211631356870657) · CBP-2992 · Beta
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Single-click editing looking good; need to make decision on extending behavior to other datagrids. <a href="https://app.asana.com/1/1123317448830974/profile/1208828066029280" data-asana-gid="1208822152029926" data-asana-accessible="true" data-asana-type="user" data-asana-dynamic="true">@Ben Belanger</a> on the hook for wrangling stakeholders to extend behavior to other grids.</div>
PRD: https://casecommons.atlassian.net/wiki/x/BQBN2w

**Launch Plan**
* ✅ QA Start - Feb 26
* ✅ UAT Start - Mar 12
* ✅ Beta Start - Mar 18
* 🎯 GA - May 29
[jira:CBP-2992]

**Status** (Grain: Stories)
`▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░▓ 19 done · 0 in progress · 2 to do`

**Readiness** (Grain: Stories)
`Readiness: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓-- (2 Unmapped · 19 Done)`

**Estimate** (Grain: Days)
`❌ 1.0d estimated · 3.0d actual · 1.0d remaining (400%)`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 0 | 0 | 0 | 2 |


**Done:** 19 issues
~~33.0d estimated · 3.0d actual

**To Do:** 2 issues
- 👀 [CBP-3094](https://casecommons.atlassian.net/browse/CBP-3094) — FE - Service Enrollment - Default value is not reflected in the Add Service enrollment (For ex: Method of delivery)||Ben · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3095](https://casecommons.atlassian.net/browse/CBP-3095) — FE - Service Enrollment - Service Type changed is not reflected in the View Service Enrollment||Tuan · To do · 1.0d estimated · 👀 No actual · P2 · 👀 No release

### [Notes - Bulk "General Notes"](https://app.asana.com/1/1123317448830974/project/1211838817183809) · CBP-2752 · Beta
[status:on_track:On Track]
<!-- raw --><div class='status-body'><i><strong>5-1 release</strong>: Single-click editing is required before we expand to more customers in beta rollout. We also get attendance toggle + long text handling in Notes.</i> <strong><p><strong>Summary</strong></p></strong> No update - all remains well. Copy/pasting last week's update: Remains released to 4 tenants. No feedback thus far. <strong><p><strong>Next steps</strong></p></strong> No other work planned for General Notes currently. This will get a much more significant text once Service Notes/Locked Notes roll out in 4/23 release <ol><li>Task: Before Service Notes phase I will aim to bring us up to ~10 beta tenants with CSM approval</li></ol></div>
PRD: https://casecommons.atlassian.net/wiki/x/TYD0BwE

**Launch Plan**
* ✅ QA Start - Apr 6
* ✅ UAT Start - Apr 16
* ✅ Beta Start - Apr 1
* 🎯 GA - Jun 1
[jira:CBP-2752]

**Status** (Grain: Stories)
`▓▓▓▓░▓▓▓▓▓▓▓ 11 done · 0 in progress · 1 to do`

**Readiness** (Grain: Stories)
`Readiness: ▓▓▓▓▓▓▓▓▓▓▓- (1 Unmapped · 11 Done)`

**Estimate** (Grain: Days)
`15.9d estimated · 8.8d actual · 0.0d remaining (55%)`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 0 | 0 | 0 | 1 |


**Done:** 11 issues
~~15.9d estimated · 8.8d actual

**To Do:** 1 issues
- 👀 [CBP-2862](https://casecommons.atlassian.net/browse/CBP-2862) — Columns on people grid of New note modal doesn't support scroll unless few people are added||Sindhu · To do · 👀 Unestimated · 👀 No actual · P3 · 👀 No release

#### In UAT

### [Notes - Locked Notes](https://app.asana.com/1/1123317448830974/project/1211786365522017) · CBP-2923 · In UAT
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Still on track for extending existing locked notes feature to new notes UX.</div>
PRD: https://casecommons.atlassian.net/wiki/x/TYD0BwE

**Launch Plan**
* ✅ QA Start - Apr 6
* ✅ UAT Start - Apr 16
* 🎯 Beta Start - Apr 28
* 🎯 GA - May 14
[jira:CBP-2923]

**Status** (Grain: Stories)
`▒▒▒ 0 done · 3 in progress · 0 to do`

**Readiness** (Grain: Stories)
`Readiness: ▒▒▒ (3 Aligned)`

**Estimate** (Grain: Days)
`👀 6.0d estimated · 0.0d actual · 6.0d remaining (100%)`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 3 | 0 | 0 | 0 |


**In Progress:** 3 issues · ~2.4d est remaining
- [CBP-2756](https://casecommons.atlassian.net/browse/CBP-2756) — Notes - Show "Access" section for all note types||Russell · Product approved · 4.0d estimated · 3.6d actual · P2 · Release: 2026-4-2
- [CBP-2990](https://casecommons.atlassian.net/browse/CBP-2990) — Notes - Search and populate the "Access" section||Russell · In development · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-4-2
- [CBP-3125](https://casecommons.atlassian.net/browse/CBP-3125) — FE - Issues found on the Note v2 access(locking note)||Russell · Merged to QA · 2.0d estimated · 👀 No actual · P2 · Release: 2026-4-2

#### Development

### [Services - Service plan datagrid with bulk actions](https://app.asana.com/1/1123317448830974/project/1211631360190563) · CBP-3066 · Development
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Blessing has completed work on the SP datagrid - ready for testing, but behind Notes in 4-2 release... will drop in May <ul><li>All the bells and whistles including bulk actions - more than we had in Notes even</li><li><em>Note: Blessing had great data quality for this showing dev work coming in under estimate </em>🙂 </li></ul> <p><strong>Next steps</strong></p><ol><li>I will give this an &quot;epic-level&quot; review before QA so that Blessing can tidy up anything obvious that I notice ahead of testing</li><li>In the meantime, Blessing's moving on to Services WLV bulk actions on Monday</li></ol></div>

**Launch Plan**
* 🎯 QA Start - May 4
* 🎯 UAT Start - May 7
* 🎯 Beta Start - May 18
* 🎯 GA - May 28
[jira:CBP-3066]

**Status** (Grain: Stories)
`▒▒▒▒▒▒▒▒▒ 0 done · 9 in progress · 0 to do`

**Readiness** (Grain: Stories)
`Readiness: ▒▒▒▒▒▒▒▒- (8 Aligned · 1 Unmapped)`

**Estimate** (Grain: Days)
`👀 8.1d estimated · 0.0d actual · 8.1d remaining (100%)`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 8 | 0 | 0 | 1 |


**In Progress:** 9 issues · ~8.1d est remaining
- [CBP-3067](https://casecommons.atlassian.net/browse/CBP-3067) — Service plan - Display enrollments as a datagrid with sorting and toolbar||Blessing · In QA · 3.0d estimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3069](https://casecommons.atlassian.net/browse/CBP-3069) — Service plan - Stacking filters||Blessing · Merged to QA · 2.0d estimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3072](https://casecommons.atlassian.net/browse/CBP-3072) — Service plan - Cache user preferences||Blessing · In QA · 1.0d estimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3073](https://casecommons.atlassian.net/browse/CBP-3073) — Service plan - Row pinning||Blessing · In QA · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3076](https://casecommons.atlassian.net/browse/CBP-3076) — Service plan - Quick filter||Blessing · In QA · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3099](https://casecommons.atlassian.net/browse/CBP-3099) — GQL Service plan - Implement filter logic for service offerings ||Blessing · In QA · 2.0d estimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3100](https://casecommons.atlassian.net/browse/CBP-3100) — Add service plan datagrid feature flag for Engage, Intake and People||Blessing · In QA · 0.1d estimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3144](https://casecommons.atlassian.net/browse/CBP-3144) — Service plan - Bulk row selection, bulk actions menu UI, and bulk action implementations||Blessing · Merged to QA · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-5-1
- 👀 [CBP-3230](https://casecommons.atlassian.net/browse/CBP-3230) — Bulk update and delete mutations for service offering enrollments||Blessing · Merged to QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release

### [Services WLV - Bulk actions](https://app.asana.com/1/1123317448830974/project/1211733450555414) · CBP-3121 · Development
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Re-baselined <p><strong>Next steps</strong></p>Blessing will move on to this work after wrapping Service Plan datagrid</div>

**Launch Plan**
* ❌ QA Start - Apr 20
* ⚠️ UAT Start - Apr 30
* ⚠️ GA - May 28
[jira:CBP-3121]

**Status** (Grain: Stories)
`▒░░░░ 0 done · 1 in progress · 4 to do`

**Readiness** (Grain: Stories)
`Readiness: ----- (5 Unmapped)`

**Estimate** (Grain: Days)
`not set`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 0 | 0 | 0 | 5 |

⚠️ QA Start was 8d ago but 5 stories still open — worth a check?

**In Progress:** 1 issues
- 👀 [CBP-3151](https://casecommons.atlassian.net/browse/CBP-3151) — Services WLV - Implement bulk actions menu||Blessing · In development · 👀 Unestimated · 👀 No actual · P2 · 👀 No release

**To Do:** 4 issues
- 👀 [CBP-3152](https://casecommons.atlassian.net/browse/CBP-3152) — Services WLV - "Add service enrollment" bulk action||Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3153](https://casecommons.atlassian.net/browse/CBP-3153) — Services WLV - "Add service note" bulk action||Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3154](https://casecommons.atlassian.net/browse/CBP-3154) — Services WLV - "End all enrollments" bulk action||Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3155](https://casecommons.atlassian.net/browse/CBP-3155) — Services WLV - "Delete services" bulk action||Blessing · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release

### [Notes - Bulk Service Notes](https://app.asana.com/1/1123317448830974/project/1211757637943244) · CBP-2924 · Development
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Still on track for handling all major functionality and resolving feedback. <strong></strong></div>
PRD: https://casecommons.atlassian.net/wiki/x/TYD0BwE

**Launch Plan**
* ❌ QA Start - Apr 6
* ❌ UAT Start - Apr 16
* ⚠️ Beta Start - May 18
* ⚠️ GA - Jun 1
[jira:CBP-2924]

**Status** (Grain: Stories)
`░▒▒▓░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 1 done · 18 in progress · 2 to do`

**Readiness** (Grain: Stories)
`Readiness: ▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒------ (14 Aligned · 6 Unmapped · 1 Done)`

**Estimate** (Grain: Days)
`👀 34.6d estimated · 0.0d actual · 34.6d remaining (100%)`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 14 | 0 | 0 | 6 |

⚠️ QA Start was 22d ago but 20 stories still open — worth a check?

**Done:** 1 issues

**In Progress:** 18 issues · ~4.0d est remaining
- 👀 [CBP-2803](https://casecommons.atlassian.net/browse/CBP-2803) — BE - Inconsistent Service Notes Display Between Case/Intake and Provider Notebooks||Tuan · In development · 5.0d estimated · 2.0d actual · P1 · 👀 No release
- [CBP-3075](https://casecommons.atlassian.net/browse/CBP-3075) — Service Note UI/UX Issues and Bugs as the initial testing||Bisoye · Merged to QA · 4.0d estimated · 👀 No actual · P1 · Release: 2026-5-1
- [CBP-2952](https://casecommons.atlassian.net/browse/CBP-2952) — Notes - Show "Services" and hide "People" sections for Service Notes||Bisoye · In QA · 3.0d estimated · 3.0d actual · P2 · Release: 2026-5-1
- [CBP-2985](https://casecommons.atlassian.net/browse/CBP-2985) — Notes - Search and populate the "Services" section||Bisoye · In QA · 10.0d estimated · 8.0d actual · P2 · Release: 2026-5-1
- [CBP-3109](https://casecommons.atlassian.net/browse/CBP-3109) — Service Note - Error toast "Please add at least one service interaction" should be clarified||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-5-1
- 👀 [CBP-3113](https://casecommons.atlassian.net/browse/CBP-3113) — Service Notes - Rostering in new Note dialog||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3141](https://casecommons.atlassian.net/browse/CBP-3141) — Service Notes - "Link" action for service interaction people||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- [CBP-3145](https://casecommons.atlassian.net/browse/CBP-3145) — Notes - Service note datagrid UX improvements||Russell · Merged to QA · 3.0d estimated · 4.0d actual · P2 · Release: 2026-5-1
- [CBP-3146](https://casecommons.atlassian.net/browse/CBP-3146) — Notes - Tabbed UI in new Note dialog||Russell · Merged to QA · 3.0d estimated · 7.0d actual · P2 · Release: 2026-5-1
- 👀 [CBP-3174](https://casecommons.atlassian.net/browse/CBP-3174) — [Data Grid] - Single-click editable mode for MUI DataGridPro||Russell · Merged to QA · 1.0d estimated · 1.0d actual · P2 · 👀 No release
- [CBP-3235](https://casecommons.atlassian.net/browse/CBP-3235) — Service Notes - CSM feedback||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P2 · Release: 2026-5-1
- [CBP-3042](https://casecommons.atlassian.net/browse/CBP-3042) — FE - Notes V2 - Service Note - "Add Service" option appears as mandatory, but no validation message is displayed||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-5-1
- [CBP-3063](https://casecommons.atlassian.net/browse/CBP-3063) — Notes - Show and save Service Group column in Service Notes||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-5-1
- [CBP-3108](https://casecommons.atlassian.net/browse/CBP-3108) — Service Note - Autocompleter freeze causes same person to be added multiple times||Bisoye · In QA · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-5-1
- [CBP-3110](https://casecommons.atlassian.net/browse/CBP-3110) — Service Note - Clicking provider name in add-services flow adds service instead of opening provider||Tuan · Merged to QA · 1.0d estimated · 1.0d actual · P3 · Release: 2026-5-1
- [CBP-3111](https://casecommons.atlassian.net/browse/CBP-3111) — Service Note - Note type switch confirmation dialog repeats identical text in header and body||Bisoye · Product approved · 👀 Unestimated · 👀 No actual · P3 · Release: 2026-4-2 / 2026-5-1
- [CBP-3112](https://casecommons.atlassian.net/browse/CBP-3112) — FE - Service Note - Trash icon on service interaction row shows incorrect tooltip "Delete enrollment"||Bisoye · Product approved · 0.1d estimated · 0.1d actual · P3 · Release: 2026-4-2
- [CBP-2831](https://casecommons.atlassian.net/browse/CBP-2831) — Issue with End Date Validation in Service Notes||Uday · Product approved · 👀 Unestimated · 👀 No actual · P4 · Release: 2026-4-2

**To Do:** 2 issues
- 👀 [CBP-2573](https://casecommons.atlassian.net/browse/CBP-2573) — Duplicate Service interactions when adding multiple services on a note (intermittently)||Yi · To do · 2.5d estimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-1503](https://casecommons.atlassian.net/browse/CBP-1503) — raisethebarr - Rostered people are not populated on service note of Notebook page navigated via enrollment with rostered service||👀 Unassigned · Blocked - Needs Review · 2.0d estimated · 👀 No actual · P3 · 👀 No release

### [Integrations - Zapier improvements](https://app.asana.com/1/1123317448830974/project/1213496879668016) · CBP-3158 · Development
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Eric has not committed any code and he scheduled a demo out next Thursday. This week's report was again high level so I hope he has not filed any new hours for the week. I've set an expectation that he and I will meet with Yi before Thursday and I gather that he's again going to take on his work during the weekend. <p><strong>Next steps</strong></p><ol><li>Demo scheduled for Thursday where expectations have been set that Eric will be showing a working approach for dynamic schema rendering</li></ol></div>
PRD: https://casecommons.atlassian.net/wiki/x/AoCwBQE

**Launch Plan**
* 🎯 QA Start - May 11
* 🎯 UAT Start - May 28
* 🎯 GA - Jun 11
[jira:CBP-3158]

**Status** (Grain: Stories)
`░░ 0 done · 0 in progress · 2 to do`

**Readiness** (Grain: Stories)
`Readiness: -- (2 Unmapped)`

**Estimate** (Grain: Days)
`not set`

**Readiness Details**
| 🎯 Aligned | ⚠️ Stalled | 🛑 Lagging | 👀 Unmapped |
|---|---|---|---|
| 0 | 0 | 0 | 2 |


**To Do:** 2 issues
- 👀 [CBP-3159](https://casecommons.atlassian.net/browse/CBP-3159) — Zapier - Create/Update a Person Write Action||eric.engoron · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release
- 👀 [CBP-3231](https://casecommons.atlassian.net/browse/CBP-3231) — Admin - Dynamic pages custom fields accessible to non-admins||Tuan · To do · 👀 Unestimated · 👀 No actual · P2 · 👀 No release

#### Discovery

### [Accessibility - 2026 VPAT accessibility audit](https://app.asana.com/1/1123317448830974/project/1213564552809143) · CBP-3085 · Discovery
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Nothin' doin' at the moment but will be prioritized later this quarter, likely with Sodiq and Russell to lead through <p><strong>Next steps</strong></p>None yet</div>

**Launch Plan**
* 🎯 QA Start - May 18
* 🎯 UAT Start - Jun 11
* 🎯 GA - Jun 11
[jira:CBP-3085]

### [Notes - Global Notes WLV](https://app.asana.com/1/1123317448830974/project/1210368097846960) · Discovery
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Nothin' doin' at the moment but will be prioritized later this quarter, likely with Bisoye to lead through <strong><p><strong>Next steps</strong></p></strong> None yet</div>

**Launch Plan**
* 🎯 QA Start - Jun 1
* 🎯 UAT Start - Jun 18
* 🎯 Beta Start - Jun 25
* 🎯 GA - Jul 9

### [Dynamic pages - Schema migration and duplicate prevention](https://app.asana.com/1/1123317448830974/project/1212560621975480) · Discovery
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Added AC for removing inline &quot;access&quot; section for People While reviewing Potts Family Foundation schemas, I found a number of real concerns <p><strong>Next steps</strong></p><ol><li>Planning with Russell, Bisoye, Feyi, and Yi</li></ol></div>

**Launch Plan**
* 🎯 QA Start - Jun 29
* 🎯 UAT Start - Jul 16
* 🎯 GA - Jul 23

### [Portal - Client Dashboard](https://app.asana.com/1/1123317448830974/project/1213506659163435) · Discovery
[tw:not set]
PRD: https://casecommons.atlassian.net/wiki/x/AgCrBQE

**Launch Plan**
* 🎯 QA Start - May 11
* 🎯 UAT Start - Jun 11
* 🎯 Beta Start - Jun 11
* GA [tw:not set]

#### Study

### [Assignment-based task notifications study](https://app.asana.com/1/1123317448830974/project/1209189001499701) · Study
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Nylas Upgrade - UX Improvements](https://app.asana.com/1/1123317448830974/project/1208822133040792) · Study
[status:on_hold:On Hold]
<!-- raw --><div class='status-body'>Completed a review of v3 diff and existing Nylas features that we have not leveraged <a href="https://developer.nylas.com/docs/v2/upgrade-to-v3/diff-view/#terminology-changes-in-v3">https://developer.nylas.com/docs/v2/upgrade-to-v3/diff-view/#terminology-changes-in-v3</a> A few interesting new features which would require additional dev: <strong>Email</strong> <ul><li>New webhook event for emails message.opened could be used to indicate that an internal user had seen a message</li></ul> <strong>Calendars</strong> <ul><li>Check a calendar for free/busy status</li><li>Each grant can now have up to 10 virtual calendars + Added the option to specify a primary calendar</li><li>”You can now send drafts” - save?</li><li>You can schedule a send time for a message, and edit or delete scheduled send times. - The new message.send_success and message.send_failed notifications allow you to track the results of a scheduled send</li><li>The new message.bounce_detected notification is available to check for message bounces from Google, Microsoft Graph, iCloud, and Yahoo.</li><li>You can now soft-delete messages and threads</li></ul> Also discussed Nylas’ scheduling tools which could address some user requests - after chatting with @Jordan Jan and Allie, it seems that this integration would be a heavy lift and wouldn’t qualify for low-hanging fruit <ul><li><a href="https://developer.nylas.com/docs/v3/calendar/group-booking/">https://developer.nylas.com/docs/v3/calendar/group-booking/</a></li></ul></div>

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

#### Backlog

### [Data import - Bulk import for Notes](https://app.asana.com/1/1123317448830974/project/1210860550580423) · Backlog
[status:on_track:On Track]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Nothin' doin' at the moment but will be prioritized later this quarter, likely with Duc and Tuan to lead through <p><strong>Next steps</strong></p>None yet</div>
PRD: https://casecommons.atlassian.net/wiki/x/CgBGZ

**Launch Plan**
* 🎯 QA Start - Jun 11
* 🎯 UAT Start - Jul 2
* 🎯 GA - Jul 13

### [Data import - Clearer IDs](https://app.asana.com/1/1123317448830974/project/1210860550580376) · Backlog
[status:on_hold:On Hold]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Sorting out next steps re: Tuan's priorities</div>
PRD: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/1682309130

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Forms - Long-term strategy](https://app.asana.com/1/1123317448830974/project/1209067717586483) · Backlog
[status:on_hold:On Hold]
<!-- raw --><div class='status-body'><strong>Temporarily de-prioritized based on 2025 planning</strong></div>

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Internal Admin - Activate/inactivate tenants from Chargebee](https://app.asana.com/1/1123317448830974/project/1210615331914095) · Backlog
[status:on_hold:On Hold]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>On hold; not in Q4 scope as of now.</div>

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Notes - Optional People in Service Notes](https://app.asana.com/1/1123317448830974/project/1213685097670612) · Backlog
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Services - Multiple rosters for enrollments and notes](https://app.asana.com/1/1123317448830974/project/1210452458408269) · Backlog
[status:at_risk:At Risk]
<!-- raw --><div class='status-body'><p><strong>Summary</strong></p>Currently showing risk for completion within Q1, will re-evaluate as other blocking work is completed</div>
PRD: https://casecommons.atlassian.net/wiki/x/BQBN2w

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Test Automation Suite for Endpoint Security](https://app.asana.com/1/1123317448830974/project/1210874981107020) · Backlog
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Text messaging - Phone number selection/onboarding](https://app.asana.com/1/1123317448830974/project/1210615331914089) · Backlog
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

#### N/A

### [Automation & Deflection 2026](https://app.asana.com/1/1123317448830974/project/1211796849380964) · None
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [MDM Upgrade & Implementation](https://app.asana.com/1/1123317448830974/project/1211002139187115) · None
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Notes - Anonymous service notes](https://app.asana.com/1/1123317448830974/project/1213022940723417) · None
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Services - Service groups for notes](https://app.asana.com/1/1123317448830974/project/1211708145580080) · None
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Services - Service note resource linking](https://app.asana.com/1/1123317448830974/project/1210154179999344) · None
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

### [Small wins - May](https://app.asana.com/1/1123317448830974/project/1209742093504572) · None
[tw:not set]

**Launch Plan**
* QA Start [tw:not set]
* UAT Start [tw:not set]
* GA [tw:not set]

## ⚙️ Data Quality
**Estimates:** 19/38 in-progress (50%)
**Actuals:** 6/28 in QA (21%)

| Engineer | Estimates | Actuals |
|---|---|---|
| Bisoye | 4/14 (28%) | 👀 2/12 (16%) |
| Blessing | 6/11 (54%) | 👀 0/10 (0%) |
| Russell | 5/7 (71%) | 👏 3/4 (75%) |
| Tuan | 4/5 (80%) | 1/2 (50%) |
| Uday | 👀 0/1 (0%) | — |

**Unprioritized:** 8 of 38 in-progress issues have no fix version set (21%)

| Project | Unprioritized |
|---|---|
| Notes - Bulk Service Notes | 4/18 (22%) |
| Notes - Notes datagrid | 2/7 (28%) |
| Services - Service plan datagrid with bulk actions | 1/9 (11%) |
| Services WLV - Bulk actions | 👀 1/1 (100%) |

