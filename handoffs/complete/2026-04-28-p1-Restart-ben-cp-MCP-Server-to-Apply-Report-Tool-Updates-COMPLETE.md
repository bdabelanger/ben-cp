# Implementation Plan: Restart ben-cp MCP Server to Apply Report Tool Updates

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Ben
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-28

MCP server restarted. Both get_report and generate_report now show correct skill parameter in tool definitions.

---

## Context

Two source code changes were made to `src/ben-cp.ts` and built successfully (`npm run build` clean), but the MCP server has not been restarted. Until it is, all agents still see the old tool definitions:

- `get_report` still shows `path` as the parameter (old)
- `generate_report` still shows `"e.g. 'platform', 'dream'"` in its description (old, `platform` still present)

## Required Action — Ben Only

Restart the ben-cp MCP server. In Claude Cowork desktop app:
1. Open Settings → MCP Servers
2. Find `ben-cp` and restart it

Or via terminal:
```
cd "/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp" && npm run build
```
Then restart the MCP server.

## Expected Result After Restart

- `get_report(skill="status")` — works, no path needed
- `get_report(skill="dream")` — works
- `generate_report(skill="status")` — description no longer mentions `platform`
- `generate_report(skill="platform")` — correctly fails with valid options listed