## Objective
Automate the extraction of structured intelligence records from the raw files (PDFs, TXT, Meeting Notes, and Confluence Pages) staged in various `source/` subdirectories.

## Context
We currently have a backlog of raw source materials (e.g., in `intelligence/product/tasks/q2-shareout/source/`). Agents like Gemma are manually parsing these one by one. Specifically, PRDs stored in Confluence are critical sources of truth that need to be harvested into the vault.

## Proposed Pipeline
1. **Pipeline Home:** `orchestration/pipelines/intelligence/ingestion/`
2. **Logic:**
   - **Harvester:** Expand to pull directly from Confluence (PRDs, Technical Specs) and Stage them in `source/`.
   - **Scanner:** Identify files in any `source/` directory that do not have a corresponding `.md` record in the parent directory.
   - **Parser:** Use a dedicated ingestion script (with LLM synthesis) to extract key themes, metrics, and narratives.
   - **Generator:** Create the initial `.md` record using the `add_intelligence` tool pattern.
3. **Drafting Protocol:**
   - New records should be tagged with `Status: 🟡 Draft` or `Source: Auto-Ingested`.
   - Human/Gemma then reviews and "promotes" the record via `edit_intelligence`.

## Next Steps
- Research Confluence API for exporting pages to Markdown or HTML.
- Implement a basic directory scanner that looks for "orphaned" source files.
- Design a "Source-to-Intelligence" prompt template for the parser.
- Test with the Q2 Product Shareout source materials and a sample PRD.
