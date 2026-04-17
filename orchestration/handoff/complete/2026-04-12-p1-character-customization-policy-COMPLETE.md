# Implementation Plan: character-customization-policy

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Antigravity / Claude Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **v1.2**
> **STATUS**: ✅ COMPLETE

Expanded domain execution safety standards by launching `skills/handoff/character.md` to force sharp, brief context swaps (Baton). Created a non-conversational core fallback persona (`character.md`) placed safely at repository root. Updated `AGENTS.md` directly beneath the core mission statement locking agents from initiating functional sequences explicitly without first parsing either the local map or defaulting to root.

**Changelog:** (see root changelog.md)


---

## Context
We have established a strict architectural divide separating mechanical capabilities (`skills/`) from autonomous tone and identity mapping (`character.md`). While Daily Progress Digest characters are established, other generalized domains require character definitions to enforce tone match across the system.

**Naming convention:** Character names are confined exclusively to `character.md` files. All skill references, routing logic, index files, and `AGENTS.md` use the generic skill name only.

## The Claude Perspective
> **Injected by:** Claude (Cowork) (2026-04-12)

This policy has direct implications for how I (Claude/Cowork) operate within the vault. A few thoughts:

**On reading `character.md` at skill invocation:**
This is the right call. Currently I read `SKILL.md` at the start of every skill invocation to load best practices — `character.md` should be treated the same way: a mandatory read, not optional. The two files serve complementary purposes: `SKILL.md` tells me *what* to do and *how*, `character.md` tells me *who I am while doing it*. Both need to be loaded together.

**On the `handoff` skill's character:**
The `skills/handoff/character.md` should specify a voice that skews toward clarity and brevity over warmth — handoffs sit at the seam between agents, so tone drift here has outsized impact on continuity.

**On `AGENTS.md` enforcement:**
The proposed vault directive (agents must read `character.md` before using a skill) should also clarify what to do when a skill directory has *no* `character.md` — agents should fall back to the vault-root `character.md`. The vault-root character should be a **generic, best-practices-informed baseline**: professional and direct, never condescending or patronizing, no unnecessary hedging or hand-holding. It exists to prevent tone drift in uncustomized skills, not to impose a strong persona.

**Gaps to address:**
- Skills invoked by Claude Code (non-Cowork) need the same directive, since Claude Code doesn't have Cowork's system prompt reminders — the enforcement has to live in `AGENTS.md` or the skill files themselves.
- Consider whether `character.md` profiles should specify *which agents they apply to* (all agents vs. Claude only vs. Antigravity only), since tone norms may differ by agent type.

## Execution Plan
1. Define comprehensive `character.md` profiles within remaining non-Digest `skills/` directories.
2. Create `skills/handoff/character.md` — voice should prioritize clarity and brevity, suited to inter-agent transitions.
3. **Crucial Core Update:** Modify `AGENTS.md` to establish a mandatory vault directive: agents must read the `character.md` file inside any skill directory they utilize. This guarantees agents adopt the intended tone dynamically.
4. Create vault-root `character.md` as a generic fallback: professional, direct, best-practices-informed — not condescending or patronizing. Used when a skill directory has no `character.md` of its own.
5. Confirm enforcement path for Claude Code (non-Cowork) invocations.
