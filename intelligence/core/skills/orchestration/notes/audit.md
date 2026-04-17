# Audit Procedure: Communication

> **Owner:** Joint Operating Environment (Peer Team)

## Requirements
- [ ] Universal Signature: Every entry must be signed: `[Agent Name — YYYY-MM-DD HH:MM]`.
- [ ] Append-Only Integrity: Previous entries must remain untouched.
- [ ] Ground Truth Priority: human user's entries supersede all inferred context.
- [ ] Correction Protocol: Substantive errors must be corrected with an inline `[Correction — ...]` tag.

## Operating Procedures

### 1. Collaborative Writing
1. **Signature:** Begin with the standard agent signature block.
2. **Clarity:** Deliver high-density context; avoid fluff or subordinates phrasing.
3. **Append:** Use `replace_file_content` or similar to ensure existing notes are preserved.

### 2. Context Ingestion
1. **Primary Scan:** Read `intelligence/core/skills/orchestration/notes/notes.md` (or the mapped primary channel).
2. **Local Scan:** Read the `notes.md` within the active skill directory.
3. **Synthesis:** Weight human user notes as 100% priority ground truth.

### 3. Identity Compliance
1. Use direct, active verbiage (e.g., "Confirmed," "I have adjusted...").
2. Align with the peer-level peer-to-peer relationship model.
