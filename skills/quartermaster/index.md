# Skill: Quartermaster

> **PURPOSE:** Upfront session planning and dependency tracking.
> Replaces the use of changelogs for "intent" logging.

---

## The Quartermaster Convention

The Quartermaster is an ephemeral planning document created at the start of a work-active session. It serves as the "load-out" for the agent, ensuring all dependencies are identified before the first write.

### Rules of Engagement

1. **Location:** `quartermaster.md` files are created in the specific `skills/` subdirectory where work is taking place.
2. **Timing:** Create at session start (after context loading). Delete immediately after the final `write_changelog_entry` of the session.
3. **Format:** Use `skills/quartermaster/quartermaster_template.md`.
4. **Visibility:** As a "living document," it is editable throughout the session.

---

## When to Use

- When starting a complex task with multiple file touches.
- When dependencies or prerequisites need to be verified (e.g., "Must read X before writing Y").
- When a session has significant risk of being interrupted (it preserves the "mental model").

---

## Audit (Lumberjack)

Lumberjack audits for "Lingering Quartermaster Files." Any `quartermaster.md` file found without active session commits for that same date is flagged as a "Lingering Plan" for deletion.

---

## Procedure

1. **Load Context:** Read `AGENTS.md` and role file.
2. **Draft Plan:** If writes are intended, create `quartermaster.md` in the target directory.
3. **Execute:** Perform the work, updating the plan if it evolves.
4. **Wrap-Up:** 
   - Write Subcommittee Changelog.
   - Write Root Changelog.
   - **Delete** the `quartermaster.md` file.
