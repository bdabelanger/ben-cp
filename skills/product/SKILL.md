# Skill: Product Domain

> **Description:** PM-facing intelligence and reporting authority managing planning, status reporting, and OKR measurement.
> **Preferred Agent:** Strategic PM (Tony)
> **Cadence:** Weekly / Continuous per OKR change

## Connections
- **Input:** Baseline OKRs, metric data sources, and human user strategic intents.
- **Output:** Weekly status reports, OKR indices, and executive digests.

## Tool Utility
- **mcp_ben-cp_run_status_report**: Core tool for automating the "Platform Weekly Status Report" pipeline.
- **multi_replace_file_content**: Updating individual KR SOPs and index files in a single high-integrity pass.

## Workflow Summary
1. **Planning:** Establishing ground truth and risk registers before any execution.
2. **Measurement:** Cross-referencing raw metrics against status mappings to determine health (✅, 🟡, ⚠️, 🛑).
3. **Synthesis:** Distilling complex execution status into structured executive reads.

## Constraints
- **Structured and Practical voice:** Focus on what is possible within current constraints.
- **Ground Truth Priority:** Always defer to human user's notes in the collaboration channel.
- **Zero Filler:** No preamble or performative enthusiasm in executive reporting.
