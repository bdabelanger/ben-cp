# Initiative: Reduce Admin Burden — Third-Party Data Entry — Index

> **Period:** Q2 2026
> Focus on streamlining data entry via integrations and external portal access.

---

## 📋 KR Status Dashboard

| KR | Status | Baseline | Target | SOP |
| :--- | :--- | :--- | :--- | :--- |
| **Zapier — Custom Fields** | 🟡 Proxy | Insights needed | 🛑 Blocked | *(pending)* |
| **Portal — Invitations Sent** | 🛑 Blocked | Model unstable | 🛑 Blocked | *(pending)* |
| **Portal — Acceptances** | 🛑 Blocked | Model unstable | 🛑 Blocked | *(pending)* |
| **Portal — Profile Updates** | 🟡 Proxy | Task completion comp | 🛑 Blocked | *(pending)* |

---

## 🛠️ Detailed Metadata & Next Steps

### 1. Zapier — Custom Fields
- **Sources:** Zapier Insights, Super Admin (API Access flag)
- **Next steps:**
  - Explore Zapier Insights with Engineering
  - Verify "API Access" flag in Super Admin tenants table

### 2. Portal KRs (Invitations, Acceptance, Profile Updates)
- **Sources:** DB (`external_user_invitations`), GA `/portal` page view, DB session data
- **Note:** All three Portal KRs share the same architectural blocker — they unblock together once the data model is confirmed.
