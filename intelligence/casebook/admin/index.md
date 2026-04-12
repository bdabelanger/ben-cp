# Skill: Casebook Admin MCP

> **Repo:** `/Users/benbelanger/GitHub/casebook-admin-mcp`
> **Package name:** `casebook-admin-mcp`
> **MCP server name:** `casebook-admin-mcp`
> **Server:** SSE/Express on port `3002`
> **Entry point:** `src/casebook-mcp.ts`
> Last updated: 2026-04-08

---

## What It Does

Provides CRUD access to the Casebook Admin API across six resource domains, plus application form configuration management. Uses OAuth 2.0 client credentials for auth — token is obtained once per session via `authenticate`, then passed as `bearerToken` to all subsequent calls.

---

## Auth

| Env var | Purpose |
| :--- | :--- |
| `CASEBOOK_BASE_URL` | Base URL for the Casebook instance |
| `CASEBOOK_CLIENT_ID` | OAuth 2.0 client ID |
| `CASEBOOK_CLIENT_SECRET` | OAuth 2.0 client secret |

**Session pattern:** call `authenticate` → get token → call `initialize_endpoints` → use token for all resource ops.

---

## APIs (resource domains)

`attachments` · `cases` · `intake` · `people` · `providers` · `services`

Pass as the `api` param on every resource tool call.

---

## MCP Tools

### Core CRUD

| Tool | Method | Description |
| :--- | :--- | :--- |
| `authenticate` | POST `/oauth2/token` | OAuth 2.0 client credentials flow — returns bearer token |
| `initialize_endpoints` | GET `/{api}` × all APIs | Discovers available endpoints dynamically; sets session base URL |
| `create_resource` | POST `/{api}/{endpoint}` | Create a new resource |
| `search_resources` | GET `/{api}/{endpoint}?filter=...` | Fuzzy filter search — requires `params.filter` |
| `list_resources` | GET `/{api}/{endpoint}` | Paginated list with optional filtering, sorting, sparse fieldsets |
| `fetch_resource` | GET `/{api}/{endpoint}/{id}` | Fetch a single resource by ID |
| `bulk_operation` | POST `/{api}/operations` | Atomic batch of POST / PATCH / DELETE operations |

### Form Configurations (admin namespace)

| Tool | Method | Description |
| :--- | :--- | :--- |
| `list_form_configurations` | GET `/admin/application_form_configurations` | List all tenant application form configurations |
| `get_form_configuration` | GET `/admin/application_form_configurations/:id` | Fetch a single config by ID |
| `update_form_configuration` | PATCH `/admin/application_form_configurations/:id` | Update `custom_schema` on a config |

---

## Key Files

| File | Purpose |
| :--- | :--- |
| `src/casebook-mcp.ts` | MCP server, tool definitions, request handlers |
| `src/casebook-api.ts` | API layer — CRUD functions + form config helpers |

---

## SOPs

_None yet — add procedure files here as workflows are documented._
