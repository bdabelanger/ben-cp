---
title: Schema Source-to-Intelligence Extraction
type: intelligence
domain: skills/pipelines/intelligence/schemas
---

# Schema: Source-to-Intelligence Extraction

You are an expert Intelligence Analyst. Your task is to extract structured information from a raw source document (PDF, TXT, or Confluence Markdown) and produce a standard Vault Intelligence Record.

## Frontmatter

Every intelligence record MUST begin with YAML frontmatter using the following structure. Source systems are alphabetized (`asana`, `confluence`, `google_drive`, `jira`). Each system contains a list of source entries. Only include systems that are actually referenced.

```yaml
---
title: [Title]
status: 🟡 Draft
date_ingested: YYYY-MM-DD
sources:
  asana:
    - type: project         # project | task | portfolio
      gid: "1208693459152259"
      last_fetched: YYYY-MM-DD
  confluence:
    - type: prd             # prd | launch_plan | spec | doc
      url: https://casecommons.atlassian.net/wiki/...
      last_fetched: YYYY-MM-DD
    - type: launch_plan
      url: https://casecommons.atlassian.net/wiki/...
      last_fetched: YYYY-MM-DD
  google_drive:
    - type: doc             # doc | sheet | slide | folder
      url: https://docs.google.com/...
      last_fetched: YYYY-MM-DD
  jira:
    - type: epic            # epic | story | bug | task
      key: CBP-XXXX
      last_fetched: YYYY-MM-DD
---
```

**Rules:**
- Always include `asana` if the record maps to an Asana project (use the project GID)
- Always include `confluence` entries for any PRD or Launch Plan links found in the source
- Always include `jira` if a CBP-* epic key is referenced
- `last_fetched` should be set to today's date on initial ingestion
- Do NOT include a system block if no sources of that type exist

## Extraction Fields

1. **Title**: A clear, descriptive title based on the project or topic name.
2. **Summary**: A 2-3 sentence overview of the core intent or purpose of the content.
3. **Key Capabilities**: A bulleted list of specific features, deliverables, or technical unlocks mentioned.
4. **Strategic Alignment**: (If applicable) Which OKR or roadmap theme does this support?
5. **Metrics & Targets**: Any specific dates, GIDs, or quantitative goals mentioned.
6. **Customer Context**: Any quotes or specific customer pain points mentioned.
7. **Open Questions**: List any ambiguities or "TODO" items identified in the source.

## Output Format (Markdown)

```markdown
---
title: [Title]
status: 🟡 Draft
date_ingested: YYYY-MM-DD
sources:
  confluence:
    - type: prd
      url: https://...
      last_fetched: YYYY-MM-DD
---

## Overview
[2-3 sentence summary]

## Key Capabilities
- [Capability 1]
- [Capability 2]

## Tactical Metadata
- **Strategic Theme:** [Theme]
- **Target Date:** [Date]
- **Customer Quote:** "[Quote]"

## Analysis & Open Questions
- [Question 1]
```

## Refresh behavior

The `sources` frontmatter is the authoritative list of what to re-fetch during harvest. The harvest script (`01_harvest.py`) walks all intelligence records, reads `sources`, and refreshes any entry where `last_fetched` is older than the staleness threshold (default: 7 days) or when `--force` is passed. After re-fetching, `last_fetched` is updated in the frontmatter.
