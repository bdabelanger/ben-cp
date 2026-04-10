# Initiative: Elevate Notes to a First-Class Experience — Index

> **Period:** Q2 2026
> Focus on making the Notes feature a central, reliable part of the Platform experience.

---

## 📋 KR Status Dashboard

| KR | Status | Baseline | Target | SOP |
| :--- | :--- | :--- | :--- | :--- |
| **Notes WLV Adoption** | 🛑 Blocked | Pending launch | Proxy Comp | *(pending)* |
| **Notes Quick Entry** | ✅ Confirmed | ~32% (GA) | 40% | [SOP](../planning-services-at-scale/notes_quick_entry.md) |
| **Locked / Signed Notes** | 🟡 Proxy | High-conf proxy | TBD | *(pending)* |
| **Bulk Import for Notes** | 🟡 Partial | Blocked (CX ops) | 🛑 Blocked | *(pending)* |

---

## 🛠️ Detailed Metadata & Next Steps

### 1. Notes WLV Adoption
- **Sources:** GA, ChurnZero (post-launch)
- **Next steps:**
  - Confirm GA events fire with tenant ID on launch (Beta 6/25, GA 7/27)
  - Pull Services WLV baseline as directional comp
  - Create KR measurement SOP at launch

### 2. Notes Quick Entry (Outside UOW)
- **Sources:** Google Analytics
- **Next steps:**
  - Confirm `EngageWLVAddNote` UOW vs. non-UOW context via dev tools
  - Discover additional live entry point events via dev tools
  - Set Q3 additive target once Notes WLV ships (Beta 7/13, GA 8/10)

### 3. Locked / Signed Notes (High-Confidentiality Tenants)
- **Sources:** ChurnZero, SQL (via Data team)
- **Next steps:**
  - Pull proxy baseline — locked note data for high-conf tenants in Reveal BI
  - Validate high-conf tenant segment with Margaux's sheet
  - Wait for Signed Notes launch (Beta 7/27, GA 8/24)

### 4. Bulk Import for Notes (New Tenants)
- **Sources:** CX ops (Cierra), GA / ChurnZero post-launch
- **Next steps:**
  - Check with Cierra on current paid migration volume for Notes
  - Move measurement window to Q3
