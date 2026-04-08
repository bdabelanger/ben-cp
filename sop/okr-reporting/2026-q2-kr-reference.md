# Q2 2026 Platform KR Baseline Reference

> [!NOTE]
> 📅 **PERIOD:** Q2 2026 (April 1 – June 30)
> **SOURCE:** Migrated from *Q2 2026 - OKR Reference* (Google Doc, last updated 2026-04-02)
> **STATUS:** Active — update in place as baselines and targets are confirmed.
> This file is the single source of truth for Q2 Platform KR baseline status.
> Archive at end of Q2; do not carry quarterly content into `procedure.md`.

---

## How to Use This File

- Each KR entry shows blocker status, acquisition path, confirmed values, and next steps
- As baselines are pulled and targets are set, update the relevant KR entry here
- KRs with a dedicated measurement SOP are linked — those files contain the full pull instructions
- Status icons: 🛑 Blocked · 🟡 Proxy/Partial · ✅ Confirmed · ⏳ Pending launch

---

## Elevate Notes to first-class experience

---

### KR: Notes WLV Adoption
> *X% of Tenants with at least one Note created within collection period have at
> least one user with usage in the Notes WLV*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — Notes WLV not yet live |
| **Target** | 🟡 Proxy — Services WLV quarterly usage × beta tenant count |
| **Sources** | GA, ChurnZero (post-launch) |
| **SOP** | *(pending — create once feature ships)* |

**Next steps:**
- [ ] Confirm GA events fire with tenant ID on launch (Beta 6/25, GA 7/27)
- [ ] Pull Services WLV baseline as directional comp
- [ ] Create KR measurement SOP at launch

---

### KR: Notes Quick Entry (Outside UOW)
> *X% of Users with at least one Note created within collection period have
> created a Note from a global entry point (outside UOW)*

| | |
| :--- | :--- |
| **Baseline** | ✅ **~32%** — pulled April 2026 from GA (85-tenant beta cohort) |
| **Target** | ✅ **40%** — Q2 target, live entry points only |
| **Sources** | Google Analytics |
| **SOP** | `notes_quick_entry.md` |

**Next steps:**
- [ ] Confirm `EngageWLVAddNote` UOW vs. non-UOW context via dev tools
- [ ] Discover additional live entry point events via dev tools
- [ ] Set Q3 additive target once Notes WLV ships (Beta 7/13, GA 8/10)

---

### KR: Locked / Signed Notes (High-Confidentiality Tenants)
> *X% of high-confidentiality Tenants with at least one Note have created a
> locked or signed note with Services data*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — Locked Notes among high-conf tenants (Signed Notes not live) |
| **Target** | ⏳ TBD — # of high-conf beta tenants with locked/signed Note |
| **Sources** | ChurnZero, SQL (via Data team) |
| **SOP** | *(pending)* |

**Next steps:**
- [ ] Pull proxy baseline — locked note data for high-conf tenants in Reveal BI
- [ ] Validate high-conf tenant segment with Margaux's sheet
- [ ] Wait for Signed Notes launch (Beta 7/27, GA 8/24)

---

### KR: Bulk Import for Notes (New Tenants)
> *X% of new Tenants (rolling 90 days) have imported Notes using bulk import*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Partially blocked — needs CX ops comp from Cierra |
| **Target** | 🛑 Blocked |
| **Sources** | CX ops (Cierra), GA / ChurnZero post-launch |
| **SOP** | *(pending — move to Q3, GA 7/13)* |

**Next steps:**
- [ ] Check with Cierra on current paid migration volume for Notes
- [ ] Move measurement window to Q3

---

## Planning/delivering services at scale

---

### KR: Service Notes — Roster Association (Q1 carryover)
> *Increase % of Service Notes created that are associated with a Rostered Service Offering*

| | |
| :--- | :--- |
| **Baseline** | ✅ Unblocked — queryable in Reveal BI today |
| **Target** | ⏳ Set after baseline pull |
| **Sources** | Casebook Admin Reporting / Reveal BI |
| **SOP** | *(pending — create after first pull)* |

**Next steps:**
- [ ] Pull baseline in Reveal BI — join `cbp_service_notes` + `cbp_services` on `service_id`, filter `rostering = true`; disengaged filter via `cbp_active_users` on `tenant_id`
- [ ] Set target once baseline is in hand

---

### KR: Notes Datagrid — Navigation Shortcuts
> *X% of Tenants who have ever used the Notes datagrid have at least one user
> who has used at least one new navigation shortcut in the Notes datagrid*

| | |
| :--- | :--- |
| **Baseline** | ⏳ Pending first full-month GA pull (GA live 4/9) |
| **Target** | ⏳ Set after April baseline pull |
| **Sources** | Google Analytics (tenant_id confirmed available) |
| **SOP** | `notes_datagrid_shortcuts.md` |

**Next steps:**
- [ ] Pull April baseline from GA — see `notes_datagrid_shortcuts.md` for full instructions
- [ ] Flag `NotesWLVSort` gap to Engineering
- [ ] Set target after first pull

---

### KR: Service Plan Datagrid — Navigation Shortcuts
> *X% of Tenants who have ever used the Service Plan datagrid have at least one
> user who has used at least one new navigation shortcut*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — feature not yet launched |
| **Target** | 🛑 Blocked — Notes datagrid as comp once available |
| **Sources** | TBD — GA / ChurnZero at launch (GA 5/28) |
| **SOP** | *(pending — create at launch)* |

---

### KR: Service Notes — All Data Entry Shortcuts
> *X% of Tenants with at least one Service Note created have at least one user
> who used at least one data entry shortcut*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Partial — some shortcuts live; prod baseline pullable |
| **Target** | 🟡 Estimated — comp to be identified |
| **Sources** | GA, ChurnZero |
| **SOP** | *(pending)* |

**Next steps:**
- [ ] Pull prod baseline for currently-live shortcuts
- [ ] Identify comp feature for target

---

### KR: Enrollments — All Data Entry Shortcuts
> *X% of Tenants with at least one Enrollment created have at least one user
> who used at least one data entry shortcut*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Partial — some shortcuts live; Casebook Admin Reporting pullable |
| **Target** | 🟡 Estimated — Service Notes shortcuts as comp |
| **Sources** | Casebook Admin Reporting, GA / ChurnZero |
| **SOP** | *(pending)* |

**Next steps:**
- [ ] Pull prod baseline from Casebook Admin Reporting
- [ ] Use Service Notes shortcuts as comp for target

---

## Reduce admin burden — Third-party data entry channels

---

### KR: Zapier — Custom Fields
> *# of entitled Tenants with at least one Incoming Integration have created/
> updated a record via Zapier including at least one new field or line item*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — Zapier Insights exploration needed |
| **Target** | 🛑 Blocked — no meaningful comp yet |
| **Sources** | Zapier Insights, Super Admin (API Access flag) |
| **SOP** | *(pending — Engineering input needed)* |

**Next steps:**
- [ ] Explore Zapier Insights with Engineering
- [ ] Verify "API Access" flag in Super Admin tenants table

---

### KR: Portal — Invitations Sent
> *# of entitled BETA Tenants have sent at least one portal invitation to a (non-Provider) Person*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — Portal data model unstable |
| **Target** | 🛑 Blocked |
| **Sources** | DB (`external_user_invitations` — pending model confirmation) |
| **SOP** | *(pending — all 3 Portal KRs unblock together)* |

---

### KR: Portal — Invitation Acceptance
> *# of entitled BETA Tenants where a (non-Provider) Person logged in to the Portal*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — data model unstable |
| **Target** | 🛑 Blocked |
| **Sources** | GA `/portal` page view (proxy), DB session data |
| **SOP** | *(pending — unblocks with Portal data model)* |

---

### KR: Portal — Person Profile Updates
> *# of entitled BETA Tenants where a (non-Provider) Person updated their profile via the Portal*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — external Task completion as directional comp |
| **Target** | 🛑 Blocked — non-Provider distinction unresolved |
| **Sources** | DB / GA |
| **SOP** | *(pending — unblocks with Portal data model)* |

**Notes:** All three Portal KRs share the same architectural blocker — they unblock together once the data model is confirmed.
