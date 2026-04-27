---
title: Skill Casebook Subscriptions MCP
type: index
domain: intelligence/casebook/subscriptions
---

# Skill: Casebook Subscriptions MCP

> **Repo:** `/Users/benbelanger/GitHub/casebook-billing-mcp` _(dir name is legacy — repo should be renamed to `casebook-subscriptions-mcp` on GitHub)_
> **Package name:** `casebook-subscriptions-mcp`
> **MCP server name:** `casebook-subscriptions-mcp`
> **Server:** SSE/Express on port `3003`
> **Entry point:** `src/casebook-mcp.ts`
> Last updated: 2026-04-08

---

## What It Does

Chargebee billing data — fetch usage records, enrich with company names, generate pivot tables, and update subscription plan items. All reads auto-paginate. Write ops are exposed but scoped to subscription item updates only.

---

## Auth

| Env var | Purpose |
| :--- | :--- |
| `CHARGEBEE_API_KEY` | Chargebee API key (Basic auth, key as username, empty password) |

Can also be passed per-call as `chargebeeApiKey`.

---

## MCP Tools

| Tool | Description |
| :--- | :--- |
| `fetch_chargebee_usages` | Fetch all usage records for a date range (auto-paginated). Returns: `subscription_id`, `month` (YYYY-MM), `quantity`. Dates accept `YYYY-MM-DD` or `MM/DD/YYYY`. Optional `includeCompanyNames` bool. |
| `fetch_subscription_companies` | Enrich a list of subscription IDs with company names. Batched 10 at a time. Returns `{ subscription_id: company_name }`. |
| `update_subscription_items` | Update a subscription's plan item. Requires `subscriptionId`, `itemPriceId`, `site` (Chargebee subdomain). Write op. |
| `generate_usage_pivot_table` | Generate a markdown pivot table from transformed usage data. Rows = subscriptions, columns = months. Pass `data` from `fetch_chargebee_usages`. Optional `companyNames` map adds a Company column. |

---

## Key Files

| File | Purpose |
| :--- | :--- |
| `src/casebook-mcp.ts` | MCP server, tool definitions, request handlers |
| `src/casebook-api.ts` | Chargebee API layer — fetch, paginate, transform, pivot |

---

## SOPs

_None yet — add procedure files here as workflows are documented._
