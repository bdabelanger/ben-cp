# Skill: Notes & Context

> **Description:** Shared scratchpad layer for peer-level collaboration between the human user and all agents. Every active skill domain has a `notes.md`. This skill defines how to read, write, and update them using vault tools — no shell or filesystem access required.
> **Preferred Agent:** Any
> **Cadence:** Ad-hoc / Continuous

---

## The Notes Map

| Domain shorthand | Scope |
| :--- | :--- |
| `primary` *(default)* | 🌐 Vault-wide — read this before any planning or OKR work |
| `communication` | Same as `primary` |
| `handoff` | 📋 Handoff coordination notes |
| `changelog` | 📝 Changelog tracking notes |
| `access` | 🔐 Access & permissions notes |
| `memory` | 🧠 Intelligence / Memory notes |
| `synthesize` | 🔍 Analysis / Synthesize notes |
| `predict` | 🔮 Analysis / Predict notes |
| `product` | 📦 Product domain notes |

Full paths (e.g. `orchestration/communication`) are also accepted.

---

## R — Read

```
read_notes
  domain: primary          # omit for vault-wide default
```

Always call `read_notes` with `domain: primary` before any planning, OKR, or status work.

---

## C — Create (new entry)

```
append_note
  domain: primary          # or any domain shorthand
  agent: Your Agent Name
  title: Short Entry Title
  status: ✅ Done           # optional
  body: |
    Your note content here.
    Multi-line is fine.
```

The tool handles the `### [YYYY-MM-DD]` header, signature line, and append mechanics automatically.

---

## U — Update (your own entries only)

Preferred — append a visible correction beneath the original:

```
edit_note
  domain: primary
  agent: Your Agent Name
  entry_date: 2026-04-12
  entry_title: Original Entry Title
  new_body: Corrected content here.
  replace: false            # default — appends correction block
```

In-place replacement (use sparingly — loses history):

```
edit_note
  domain: primary
  agent: Your Agent Name
  entry_date: 2026-04-12
  entry_title: Original Entry Title
  new_body: Fully corrected content.
  replace: true
```

The tool enforces ownership — it will error if the entry is not signed by your agent name.

---

## Constraints

- **Signature required:** `append_note` handles this automatically. Manual shell writes must include `**Agent:** Name` and a `### [YYYY-MM-DD]` header.
- **Append only for others' entries** — `edit_note` enforces this server-side.
- **Own your followups** — if your note implies an action, you own it unless explicitly handed off.
- **Peer-level tone** — collaborative and direct, not subordinate.
