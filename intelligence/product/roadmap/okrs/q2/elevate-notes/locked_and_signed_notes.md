# KR Measurement SOP: Locked and Signed Notes (High-Confidentiality)

> [!NOTE]
> ⚙️ **STATUS:** Proxy Baseline — v1.0 (2026-04-10)
> KR Owner: Platform Team
> Period: Q2 2026
> Last updated: 2026-04-10

---

## 🎯 KR Definition

> *X% of high-confidentiality Tenants with at least one Note have created a locked or
> signed a note with Services data to validate that customers can secure their notes
> according to their security/compliance requirements*

---

## 📐 Measurement Definition

### Denominator
**High-confidentiality Tenants with at least one Note**

| Field | Value |
| :--- | :--- |
| Segment | "High-Confidentiality" (as defined in Margaux's mapping sheet) |
| Activity | At least one Note created in Casebook |
| Window | Q2 2026 (April 1 – June 30) |

### Numerator
**High-confidentiality Tenants who have locked or signed at least one Note containing Services data**

| Field | Value |
| :--- | :--- |
| Actions | Note Locked OR Note Signed |
| Context | Services data (Services Track or specific Services entity) |

---

## 🛠️ Data Sources & Tools

- **Segmentation**: ChurnZero + Margaux's Master Tenant Sheet (Google Sheet: https://docs.google.com/spreadsheets/d/1Lh0linGLJO9Oz_qBpJCZuOeV4RNtb_-AvkXWORSRJMw/edit?gid=1186385427#gid=1186385427).
- **Proxy Baseline**: Reveal BI (Platform Dashboard → Notes Tab → Locked Notes) AND Margaux's Sheet for validation.
- **Exact Pull**: SQL Query (Data Team request) for signed + locked cross-segmentation.

---

## 📊 Baseline Approach

Because "Signed Notes" is a late-Q2/Q3 launch (Beta 7/27, GA 8/24), the current measurement uses **Locked Notes** as a proxy for the security behavior.

| Pull date | Metric type | Baseline value |
| :--- | :--- | :--- |
| March 2026 | Proxy (Locked only) | 18 Tenants |

---

## 🗺️ How to Pull the Metric

### Path A: Proxy via Reveal BI
1. Open Reveal BI → Platform Weekly Dashboard.
2. Filter by Tenant Segment: **High-Confidentiality**.
3. Navigate to **Notes** tab.
4. Observe "% of Note-active Tenants with Locked Notes".

### Path B: Validating High-Conf Segment
1. Access **Margaux's High-Conf Tenant Sheet**.
2. Cross-reference the tenant list against the ChurnZero **Note-Active** segment.
3. Use the intersection as the refined Denominator.

---

## 🎯 Target Setting

- **Q2 Target**: Directional growth in Locked Note adoption for the High-Conf segment.
- **Q3/Q4 Target**: 25%+ adoption once "Signed Notes" ships and is bundled into the compliance protocol.

---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| Signed Notes not yet live | Numerator tracks intent via Lock only | Transition to mixed Numerator (Signed + Locked) in Q3 |
| High-Conf segment manual sync | Baseline may drift if sheet is stale | Re-validate segment membership with Account Management monthly |

---

## 🔗 Constituent Projects

The following initiatives contribute to this KR:
- [**Notes - Locked Notes**](../../projects/q2/notes-locked-notes-(1211786365522017).md)
- [**Notes - Signing / Service Note Locking**](../../projects/q2/notes-signing-service-note-locking-(1213685097670626).md)

---

## 🔗 References

- Parent procedure: `../../procedure.md`
- Elevate Notes Index: `./index.md`
- Status logic: `../../../skill-builder/mappings/status_mapping.md`
- Visual standards: `../../../skill-builder/styles/emoji_key.md`
