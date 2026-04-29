---
title: Service Plan - Service Plan Datagrid with Bulk Actions — Demo Guide
type: demo
domain: product/projects/q2/services-service-plan-datagrid-with-bulk-actions
taxonomy: Service Plan
---

# Demo Guide: Service Plan — Bulk Enrollments + Datagrid

## Canonical Demo Case

**Huy Nguyen** — Valley Elder & Caregiver Alliance (VECA)

Huy (72) is a widowed Vietnamese-American man who recently moved in with his daughter Amy and her husband Eric Vuong after suffering a minor stroke. He has mobility issues and early signs of cognitive decline. Amy and Eric proactively reached out to VECA to avoid a caregiver burnout crisis. The goal is to keep Huy safely at home while wrapping him with the right services.

**Why this case works:** Huy has a natural enrollment progression — he enters the system with a single APS Safety Check and then gets layered with additional services as the picture gets clearer. This tells a real intake story rather than a static demo.

---

## QA Setup

- Huy Nguyen has an open case with one existing enrollment: **APS Initial Safety Check**
- Two services ready to add: **Meals on Wheels** and **In-Home Health Aide**
- Pad with 2–3 historical or ended services so the datagrid has enough rows to demonstrate sorting, filtering, and pinning
- Amy Vuong linked as emergency contact / family caregiver on the case

---

## Part 1 — Bulk Enrollments

Open Huy's case and navigate to the Service Plan. The APS Safety Check is already there.

*"Huy came to us through an APS referral. Now that we know his situation better, we're connecting him with two more resources."*

Open the enrollment dialog — add Meals on Wheels and In-Home Health Aide in a single pass.

Both now appear alongside the existing enrollment in the datagrid.

---

## Part 2 — The Service Plan Datagrid

*"Now let's look at what you can do with this view."*

Show 5 rows minimum visible — *"No more clicking 'View all' just to see what's active."*

Sort by service type to group health-related services together.

Quick filter — type "aide" to isolate the In-Home Health Aide instantly.

Bulk action — select Meals on Wheels and In-Home Health Aide — *"Check, check — add a coordination note to both at once."*

---

## Part 3 — Best Practices

*"A few things worth knowing as you get comfortable with datagrids."*

Hide the Provider column — *"If you only have one provider, you don't need that column taking up space. Hide it — you can always bring it back."*

Drag to reorder columns — put Service Type first — *"Set it up the way your team thinks, not the way it shipped."*

Pin the In-Home Health Aide row — *"Pin anything you want to keep in view while you scroll."*

Export — *"This exports everything across all pages, respects your filters, and drops to CSV — ready for Excel or a report."*

*"Any changes you make save to your account. Your colleague sees their own layout. You come back tomorrow on any device and it's exactly how you left it."*

**Admin note:** There is no admin-level default layout — if your organization wants staff to work from a consistent column setup, you'll need to train them to configure it themselves. The good news is it only takes a minute and sticks permanently.

---

## Key Talking Points

- "Built for speed — includes all the bells and whistles, exceeding Notes datagrid functionality."
- Arc of the Capital customer quote: *"Can I bulk add service enrollments? All five of them?"* — the answer is now yes.
- Developer came in under estimate with high data quality — positions well for a May drop.
- Strategic prerequisite: Single-Click Edits (GA 4.2) is the downstream dependency.

---

## Timeline

- Beta: May 18, 2026
- GA: June 15, 2026
- Demo environment: QA only until Beta

---

## Related

- [Overview](overview.md)
- [Launch Plan](launch_plan.md)
