# Agent Permission and Behavior Refinement

> **Prepared by:** Antigravity (Initial Concept, 2026-04-10) — updated by Claude via Dispatch (2026-04-11, 2026-04-12)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1 — Process refinement and new agent definition
> **v1.3**
> **STATUS: ✅ COMPLETE — 2026-04-12**

Launched Roz (Access Auditor) and refined the synergy between her and Changelog Auditor. Implemented a mandatory Artifact-First Workflow policy in AGENTS.md to improve vault safety and human oversight. Verified Check 8 (Lingering Plans) with a successful decoy cleanup.

**Changelog:** (see root changelog.md)


---

## Context

This handoff covers two related concerns: (1) the original Strategic PM access scoping and session pattern refinement, and (2) the introduction of **Roz** — a new meta-agent whose role is access auditing for agents. Roz enforces least-privilege: she checks that each agent has the access it needs to function and no more. She works in tandem with Changelog Auditor and participates in nightly dream cycles.

---

## Core Principle: Defined Duties, Collaborative Execution

**Meta-agents do exactly their defined work and nothing more.** This is non-negotiable and must be encoded in `AGENTS.md` as a universal rule.

When an agent needs information or capability outside its defined scope, it does not acquire that access itself. Instead, it delegates to another agent whose defined scope covers that need. This applies in both directions:

- **Roz** cannot directly audit changelog accuracy — that is Changelog Auditor's domain. If Roz needs changelog context to understand an agent's activity pattern, she reads Changelog Auditor's output, not the changelogs themselves.
- **Changelog Auditor** cannot directly check current agent permission definitions — that is Roz's domain. If Changelog Auditor flags an out-of-scope file touch, it records the finding and yields to Roz for follow-up.
- **Vault Auditor** does not enforce access policy — that is Roz's domain. If Vault Auditor finds a vault integrity issue that implicates agent permissions, it surfaces the finding for Roz.
- **Robert** monitors `AGENTS.md` integrity only. He does not read agent skill directories or session logs. If he needs to verify that a rule is being followed in practice, he surfaces it as an open question for Changelog Auditor or Roz.

**Runners / mycelium layer** — still TBD as a concept, but the core idea is a stateless connective layer that moves structured outputs between agents without interpreting or deciding anything. Named agents define what to check and produce structured output; runners (or equivalent) transport it to where it needs to go. All judgment stays with named agents. This keeps lanes clean even as information flows between them. Design is human user's call — this is noted here for the receiving agent to confirm with human user before implementing.

This pattern enforces least-privilege at the agent level and prevents scope creep from compounding over time. Every inter-agent delegation must be explicit — define in each agent's `index.md` which agents it may call on and under what conditions.

---

## Execution Order

1. **Verify Infrastructure** — Check `skills/pmm/index.md` and `AGENTS.md` for existing rules
2. **Define Roz** — Confirm her role with Ben, then create her skill directory (see Task 5)
3. **Artifact Scoping Policy** — Define and document the access control policy (see Task 2)
4. **Encode Inter-Agent Delegation Rules** — Add delegation protocol to `AGENTS.md` (see Core Principle above)
5. **Audit Check** — Run Changelog Auditor with Check 8 to verify quartermaster.md detection
6. **Register Roz in `AGENTS.md`** — After her skill directory is created
7. **Changelog + Completion**

---

## Task 1: Verify Skill and Rules

Confirm the following files exist and match the intended convention:
- `skills/pmm/index.md`
- `skills/pmm/quartermaster_template.md`
- `AGENTS.md` (Check Step 3 and Step 6 of the Session Pattern)

---

## Task 2: Artifact Scoping and Access Control Policy

**Goal:** Restrict agent access to only necessary files while granting full read/write capability within `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`. Agents should primarily interact with designated artifact types (Tasks, Implementation Plans, Walkthroughs) when performing work. Human user maintains ultimate control via manual commits and merges as a safety net.

**Action:** Define and write this policy into `AGENTS.md` as a formal section. It should specify:
- Which artifact types agents may create and modify autonomously
- Which files and directories require human user's explicit approval before changes
- How agents signal when they are about to touch something outside their normal scope
- **How inter-agent delegation works** — when an agent needs something outside its scope, which agents it may request from, and how that request is structured

This policy is the foundation for Roz's audit work (see Task 5).

---

## Task 3: Audit Check

Run the Changelog Auditor procedure (including Check 8) on a directory with a decoy `quartermaster.md` to confirm it is flagged as a lingering file.

---

## Task 4: Changelog Auditor and Roz Coordination

Roz and Changelog Auditor are complementary but distinct:
- **Changelog Auditor** audits what agents *did* — changelog accuracy, completeness, cross-references
- **Roz** audits what agents *can do* — access scope, permission compliance, least-privilege

In the dream cycle, Changelog Auditor runs before Roz. Roz may reference Changelog Auditor's **output** when flagging agents that touched files outside their defined scope — she reads Changelog Auditor's report, not the changelogs directly.

**Delegation protocol:** If Changelog Auditor flags an out-of-scope file touch, the finding is written to Changelog Auditor's output in a structured format Roz can consume. Roz reads it in her phase and decides whether to escalate. Neither agent modifies the other's reports. Document this handoff format in both agents' `index.md` files once Roz exists.

---

## Task 5: Define and Create Roz

**Roz's role:** Access auditor for agents. She ensures each agent in the vault has the access needed for its functions and not more. She is not a gatekeeper in real-time — she audits after the fact and flags violations in her dream cycle segment.

**Confirmed character details from Ben:**
- Reports in short log format
- Skips successful access checks
- Focuses on outliers: agents touching files outside their defined scope, unexpected permission patterns, or access that has expanded without a corresponding AGENTS.md update
- Works in tandem with Changelog Auditor (reads Changelog Auditor's output; does not re-audit changelogs directly)
- Participates in nightly dream cycles
- If Roz needs something checked that falls outside her defined access, she delegates to a runner or to Changelog Auditor/Vault Auditor based on their predefined access and output requirements — she does not expand her own access

**What to create:**

```
skills/access/
  index.md          — purpose, scope, checks, output format, delegation rules (what Roz may request from other agents and how)
  character.md      — Roz's voice and dream cycle segment format (see below)
  procedure.md      — step-by-step audit procedure
  reports/          — generated reports
  changelog.md
```

**Roz's dream cycle segment format** — short access log, outliers only:

```
ROZ — 2026-04-12 02:14
[02:14:03] robert: accessed skills/okr-reporting/ — outside defined scope (monitors AGENTS.md only)
[02:14:07] lumberjack: no out-of-scope access detected
[02:14:11] crypt-keeper: no out-of-scope access detected
END
```

No narrative. No "all clear" lines for clean agents. Timestamp, agent name, anomaly. If nothing to flag, Roz does not appear in the dream report.

**Register Roz in `AGENTS.md`** after creating her skill directory. Include her phase in the dream cycle (Phase 4, after Vault Auditor).

**Also create `character.md` files for existing agents** as part of this work — this is a new convention introduced with dream cycles. Create them for: Robert, Changelog Auditor, Vault Auditor, and Roz. Each file defines voice, tone, and dream cycle segment format.

---

## Task 6: Changelog + Completion

Write changelog entries (subdirectory first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent

- Roz is new and not yet in `AGENTS.md` or the vault. Do not assume she exists — create her from scratch using the description in Task 5.
- Confirm Roz's exact check list with human user before writing her `procedure.md`. The access log format is confirmed but the specific checks she runs (which files, which agents, what counts as out-of-scope) need to be defined collaboratively.
- **The inter-agent collaboration model is a first-class rule, not a suggestion.** When encoding it in `AGENTS.md`, treat it as a constraint equal in weight to the artifact scoping policy. Every agent's `index.md` should include a section called "Delegation" that names which agents it may request from and for what.
- Strategic PM is intended to eventually become an MCP-level tool. For now it is a manual documentation convention.
- Always delete `quartermaster.md` after the changelog is written but before ending the session.
- Cross-reference `handoff/2026-04-12-p1-dream-cycles.md` — Roz must be defined before the dream cycle agent roster is finalized.
- The standalone `handoff/2026-04-12-p1-roz-agent-definition.md` is superseded by this file. Move it to `handoff/complete/` or delete it at the start of this session.
