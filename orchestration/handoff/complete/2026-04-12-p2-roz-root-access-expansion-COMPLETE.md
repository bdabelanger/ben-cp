# Implementation Plan: roz-root-access-expansion

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude (Cowork) / Claude Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.1**
> **STATUS**: ✅ COMPLETE

Established a sealed proxy bucket using symlinks to map hidden local files (`~/.claude/` and `~/.gemini/`) natively into the `skills/access/agent-roots/` vault paths. To safeguard GitHub token leakage, deployed a high-priority `.gitignore` file masking the buckets entirely. Finally, updated Changelog Auditor to actively scan these files so Roz can successfully triangulate over-privileged tool sets or stale paths.

**Changelog:** (see root changelog.md)


---

## Context
Roz was recently launched as the Access Auditor for the `ben-cp` vault. Human user requested that Roz's access and auditing scope be expanded beyond the immediate vault directory to include the local configuration roots for the agents themselves.

## The Antigravity Perspective
For Antigravity, our contextual memory and app settings are natively stored inside `~/.gemini/antigravity/` (specifically, knowledge, persistent `task.md`/`implementation_plan.md` artifacts, and persistent system logs are found in `~/.gemini/antigravity/brain/`). Exposing this root to Roz allows her to formally audit *exactly* what Antigravity remembers, cross-referencing my persistent knowledge with actual vault state. Roz can identify cases where I am holding stale context and recommend cache-clearing procedures.

## The Claude Perspective
> **Injected by:** Claude (Cowork) (2026-04-12)

For Claude, the most relevant config artifacts that Roz should audit fall into two directories:

**`~/.claude/`**
- `settings.json` — global Claude Code settings including permissions, `allowedTools`, and hook configurations. Staleness here means Claude may be operating with outdated tool grants or disallowed patterns that no longer reflect current vault/project state.
- `projects/` — per-project `.mcp.json` and settings overrides. Worth auditing for orphaned project configs pointing to directories that no longer exist or have changed ownership.
- `statsig/` / cache files — local feature flag and telemetry cache. Low risk but worth flagging if stale.

**`~/.anthropic/`**
- API key or credential files — Roz should confirm these exist and have appropriately restrictive file permissions (600 or tighter), but should **not** audit the contents or log values.
- Any local config overrides for model defaults or rate limits.

**What Roz should flag:**
1. MCP server entries in `settings.json` pointing to paths that no longer exist on disk.
2. Tool permission grants (`allowedTools` / `deniedTools`) that are overly broad (e.g. `Bash(*)` without restrictions).
3. Orphaned project entries referencing deleted or archived repos.
4. Any config files that are world-readable (permissions wider than 600).

**What Roz should NOT do:**
- Read or log actual credential/token values.
- Modify any Claude config files directly — flag and recommend only.

## Execution
1. [Claude] ✅ Inject your perspective into the section above. *(Done 2026-04-12)*
2. [Claude Code] Determine how Roz can safely read from these hidden user-level directories without granting overarching root system access (e.g. symlinking specific dotfiles vs passing explicit MCP filesystem parameters).
3. Update `skills/access/procedure.md` to analyze agent-level settings, ensuring they are kept clean and trimmed (least privilege).
4. Update `AGENTS.md` and `skills/access/SKILL.md` to reflect this expanded boundary.
