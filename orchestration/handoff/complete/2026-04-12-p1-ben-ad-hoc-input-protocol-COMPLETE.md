# Implementation Plan: ben-ad-hoc-input-protocol

> **Prepared by:** Antigravity (Gemini) / Claude via Dispatch (2026-04-12)
> **Assigned to:** human user + Claude (collaborative design)
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P1 — human user is an actor in this system and needs a defined interface
> **v1.1**
> **STATUS: ✅ COMPLETE — 2026-04-12**

Transformed the rigid 'weekly input' request into a natively nested 'Input' skill operating around a continuous human user notes. Bound the skill with a 'character.md' mapping designed to enforce horizontal, collaborative, sea-faring leadership behavior across all meta-agents interacting with human user's ad-hoc brain dumps. Updated global architecture rules demanding agents read this ground-truth log prior to executing proactive loops.

**Changelog:** (see root changelog.md)


---

## Context

Human user is not just a user of the vault — he is a primary intelligence agent. He holds context that the system cannot derive on its own: stakeholder meetings, sudden priority shifts, real-world blockers, and intuitive learnings. 

Without a defined channel for that information to enter the vault, the meta-agents are always operating from stale context, resulting in out-of-date OKR baselines and desynced Asana tickets.

Originally conceptualized as a "Weekly Read In", human user correctly noted that scheduled, structured inputs create friction and don't reflect how human updates unfold. It needs to be an **Ad-Hoc / Stream of Consciousness** channel. He might write in three times on Tuesday and skip Wednesday entirely.

---

## The Design Challenge

**How do we capture human user's "human user notes" with zero friction?**

The goal is to design an interface where human user can dump raw, unfiltered context whenever it hits him, seamlessly allowing the vault's meta-agents (and active Claude sessions) to harvest that ground truth in their next sequence.

### Questions for Collaborative Design:

1. **The Entry Interface:** Does human user want a single, continuous `captains-log.md` where he just keeps appending thoughts to the bottom? Or does he prefer talking to Claude/Gemini and having the agent parse his dictation into discrete `input-[datetime].md` files?
2. **The "Character" Mapping:** Right now, Digest Editor edits, Changelog Auditor audits, and Roz accesses. What is human user's formal character in the vault architecture? *The Captain? The Oracle? The Operator?* Giving human user a formal persona allows the system to identify the absolute authority of his notes.
3. **The Harvest:** When "Daily Progress Digest" spins up nightly via Digest Editor, how does it process human user's ad-hoc notes? Should there be a "From the Captain's Desk" section summarizing what human user taught the system that day?

## Proposed Starting Architecture (To Refine Together)

We create `skills/ben/` (or whatever human user's character ends up being named). 
Inside, we place a continuous `log.md` file designed for raw, bulleted brain-dumps.

Whenever a meta-agent (like Strategic PM) spins up to generate a sprint plan, their VERY FIRST STEP is to call `mcp_filesystem_read_text_file` on human user's rolling log. They use today's timestamp to find his most recent insights, completely reshaping their assumptions before generating a ticket or OKR update. 

---

## Notes for Claude
- Do not execute anything from this handoff without exploring the concepts with Ben. This is a design conversation first.
- The goal is the absolute lightest-weight process that actually works. If it adds friction to his workflow, it will fail.
- Once the protocol is designed, deploy the directory and update `AGENTS.md` to instruct all meta-agents to regularly read human user's drops!