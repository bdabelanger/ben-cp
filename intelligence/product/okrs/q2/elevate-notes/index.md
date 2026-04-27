---
title: 'Initiative: Elevate Notes to a First-Class Experience — Index'
type: index
domain: intelligence/product/okrs/q2/elevate-notes
---


# Initiative: Elevate Notes to a First-Class Experience — Index

> **Period:** Q2 2026
> **Objective:** Elevate Notes to first-class experience
> Last updated: 2026-04-26

---

## 📋 KR Status Dashboard

| KR | Status | Baseline | Target | Data Source |
| :--- | :--- | :--- | :--- | :--- |
| **Notes WLV Adoption** | Pending release | 0 | 5 tenants | ChurnZero, GA, HubSpot |
| **Global Entry for Notes** | Pending release | 48.5% | 50% | ChurnZero, GA, HubSpot |
| **Bulk Import Notes** | Pending release | 0 | 1 customer | ChurnZero, GA, HubSpot |
| **Locked and Signed Notes** | Pending release | 18** | To do | ChurnZero, SQL |

---

## 🛠️ KR Details

### 1. Notes WLV Adoption
**KR:** 5 tenants with at least one Note created within collection period have at least one user with usage in the Global Notes WLV to validate users are navigating to note content faster.
- **Usage definition:** Filter, sort, search
- **Projects:** Notes - Notes WLV (GA 7/9)
- **Next steps:** Confirm GA events fire with tenant ID at launch; pull Services WLV baseline as directional comp

### 2. Global Entry for Notes (Outside UOW)
**KR:** X% of users with at least one Note created within collection period have created a Note from a global entry point (outside UOW).
- **Baseline:** 48.5% (March 2026)
- **Target:** 50%
- **Entry points:** Dashboard, Notes WLV, Engage WLV, Intake WLV, Providers WLV, Services WLV
- **Projects:** Notes - Notes WLV (GA 5/14 bundle)
- **Next steps:** Pull April baseline from GA; confirm `EngageWLVAddNote` UOW vs. non-UOW context

### 3. Bulk Import Notes
**KR:** At least 1 customer uses Notes bulk import in Q2 to validate that fewer customers need to pay for import.
- **Baseline:** 0
- **Target:** 1 (any user, including internal Onboarding users)
- **Projects:** Bulk import - Notes (GA 5/14)
- **Next steps:** Check with Cierra on current paid migration volume for Notes

### 4. Locked and Signed Notes
**KR:** X% of high-confidentiality tenants with at least one Note have created a locked or signed note with Services data.
- **Baseline:** 18** (proxy — high-conf tenant count, pending Margaux's sheet validation)
- **Target:** To do (set once Locked Notes GA 5/14 and Signing GA 7/23)
- **High-conf definition:** Matches Margaux's tenant sheet
- **Projects:** Notes - New note writing experience
- **Next steps:** Pull proxy baseline in Reveal BI; validate high-conf segment with Margaux; set target after 5/14 GA

---

## 📝 Records (Vault Shadow Files)
- [Locked and Signed Notes](locked_and_signed_notes.md)

---

## 🔗 Constituent Projects
