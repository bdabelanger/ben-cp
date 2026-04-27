---
title: Status Mapping Rules OKR Health Logic
type: task
domain: skills/status/schemas
---

# Status Mapping Rules: OKR Health Logic

> [!NOTE]
> 🧠 **PURPOSE:** This file defines the quantitative and qualitative rules used to map raw Key Result (KR) data into standardized health statuses (e.g., Green, Yellow, Red). These rules are reusable across all Skills.

---

## 📊 Metric-Based Status Logic

This logic applies when both 'Current Value' and 'Target Value' are present.

| Condition | Resulting Status | Corresponding Emoji (Reference: `styles/emoji_key.md`) |
| :--- | :--- | :--- |
| Current $\ge$ Target | Achieved | ✅ Done/Achieved |
| $0.8 <$ Progress $< 1.0$ | At Risk | ⚠️ At Risk/Needs Attention |
| Progress $\le 0.8$ | Missed | ❌ Missed/Failed |
| Current = Target (Exactly) | Achieved | ✅ Done/Achieved |

## ❓ Data Quality Logic

This logic applies when metrics are incomplete.

| Condition | Resulting Status | Corresponding Emoji (Reference: `styles/emoji_key.md`) |
| :--- | :--- | :--- |
| Current Value is Null/Missing | Needs Attention (Data) | 👀 Needs Attention (Data) |
| Target Value is Null/Missing | On Track / Unknown | 🎯 On Track/Action Required |

---

## ⚙️ Future Expansion Notes

*   **Weighting:** This logic can be expanded to handle weighted KRs where multiple metrics contribute to a single overall status.
*   **Trend Analysis:** We may add rules here later to incorporate trend data (e.g., if the last 3 reports show declining progress, flag as 'At Risk' even if current value is okay).