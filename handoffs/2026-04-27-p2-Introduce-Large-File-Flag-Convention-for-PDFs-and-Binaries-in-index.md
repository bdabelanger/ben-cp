---
title: Introduce Large File Flag Convention and Context Sensor Ignore List
type: handoff
domain: handoffs
---

# Introduce Large File Flag Convention and Context Sensor Ignore List

## Context

The context sensor red-flags files over 750KB. Some of these (e.g. `intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.pdf` at 7.2MB) are intentional and should be kept — they are source materials, not pipeline artifacts.

Ben's decision: large binaries (PDFs, source files) should be maintained in the vault, but we need two complementary mechanisms:
1. A convention to call out file size explicitly in `index.md` and any markdown links referencing them, so readers know what they're linking to
2. An `ignore` list in the context sensor config so that explicitly-flagged large files are skipped during scanning — consistent with the `ignore` pattern being adopted across all sensors

## Logic

Define and implement the large-file flag convention. Add an `ignore` config to the context sensor. Update affected files. Keep the sensor catching genuinely unexpected large files.

## Execution Steps

1. [ ] **Define the convention.** Proposed approach — annotate large file links in `index.md` with a size callout:
   - `- [Q2 2026 Product Shareout](source/Q2 2026 Product Shareout.pdf) _(7.4MB)_`
   - Document this convention in `intelligence/governance/` (can be a section in the retention policy doc or a separate style guide entry)

2. [ ] **Add `ignore` to the context sensor config.** Following the same pattern being standardized across all sensors, add an `ignore` list to the context sensor configuration. Files or glob patterns in the ignore list are excluded from red/yellow flag reporting entirely.

3. [ ] **Populate the ignore list** with currently-known intentional large files:
   - `intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.pdf`
   - Add any other known source/binary files that are intentionally large

4. [ ] **Update affected index.md files.** Apply the size callout convention to:
   - `intelligence/product/shareout/q2/index.md` (or whichever index references the PDF)
   - Any other markdown files that link directly to the PDF

5. [ ] Re-run `generate_report(skill='dream')` and confirm the PDF no longer appears as a red flag, while non-ignored large files still do.

## Verification Checklist

- [ ] Context sensor config has an `ignore` key (consistent with other sensors)
- [ ] Known intentional large files are in the ignore list
- [ ] `intelligence/product/shareout/q2/` index.md includes the size callout
- [ ] Convention is documented in `intelligence/governance/`
- [ ] `get_report('dream/context.json')` shows no red/yellow flags for ignored files
- [ ] Unannotated large files (true unknowns) are still caught by the sensor
