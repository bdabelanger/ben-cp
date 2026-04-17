# Skill: Report Publishing (Pouch Protocol)

- **agent:** Antigravity
- **status:** 🟡 Proposed
- **type:** Architecture / Skill

# Skill: Report Publishing

> **Description:** Procedural standard for exposing physical pipeline outputs to authorized agentic observers (Gemma/Local).
> **Domain:** Orchestration / Reporting

## The Problem
Agents restricted to the **MCP Layer** (Gemma/Local) cannot access the `orchestration/pipelines/outputs/` directory. This creates a "Data Silo" where high-fidelity status reports are unreachable for cross-domain synthesis.

## The Standard
Every pipeline execution MUST conclude by "Publishing" its Markdown report to a standardized intelligence path.

### 📍 Standard Publishing Paths
Output agents MUST copy their final `.md` report to:
- **Project Roadmap**: `intelligence/product/reports/latest-roadmap-status.md`
- **Platform GA**: `intelligence/product/reports/latest-platform-status.md`
- **Dream Cycle**: `intelligence/dream/reports/latest-dream-synthesis.md`

### 🔧 Integration Pattern
Pipelines should include a "Step 7" (or final step) that executes:
```python
shutil.copy2(OUTPUT_PATH, os.path.join(VAULT_ROOT, "intelligence/[domain]/reports/latest-[report-name].md"))
```

## Agent Retrieval Logic
Restricted agents can fetch any "Latest" report by calling:
`get_intelligence(path='[domain]/reports/latest-[report-name].md')`

## Audit Rule
The Intelligence Access auditor will flag any pipeline report in `outputs/` that has been modified without a corresponding timestamp update in the `intelligence/` archive.

