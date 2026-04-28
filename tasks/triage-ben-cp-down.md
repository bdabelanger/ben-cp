# Triage: ben-cp MCP Server Down

- **priority:** P2
- **status:** IN_PROGRESS

# Triage: ben-cp MCP Server Down After Restart

## Context
The user reports that `ben-cp` is down after a restart. Initial triage reveals multiple instances of `ben-cp` and related MCP servers running from different paths (`GitHub` vs `My Drive`), which may be causing conflicts or confusion in the MCP client.

## Proposed Logic
1. **Clear Zombie Processes**: Multiple instances of `node dist/ben-cp.js` are currently running. Some are pointing to `/Users/benbelanger/GitHub/ben-cp` and others to `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`. These must be cleared to ensure a fresh start.
2. **Standardize Path**: The repo recently underwent a "Great Flattening" restructuring. We should standardize on the `My Drive` path as it appears to be the most active and recently modified.
3. **Rebuild & Verify**: Ensure the `dist/ben-cp.js` is up to date and that environment variables in `.env` are correct.
4. **Client Config**: The user should verify that Claude Desktop's `config.json` points to the correct `dist/ben-cp.js` path.

## Execution Steps
- [x] Triage running processes (`ps aux | grep ben-cp`)
- [x] Verify build integrity (`npm run build`)
- [ ] Kill all stale MCP processes:
  - `pkill -f ben-cp`
  - `pkill -f mcp-shell`
- [ ] Verify Claude Desktop `config.json` paths (User Action)
- [ ] Restart Claude Desktop

