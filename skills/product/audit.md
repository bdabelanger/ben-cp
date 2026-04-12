# Audit Procedure: Product Domain

> **Owner:** Strategic PM (Tony)

## Requirements
- [ ] KR Compliance: Every KR SOP must contain a `target_value` and `current_value`.
- [ ] Logic Mapping: Metrics must be cross-referenced against `knowledge/mapping/status_mapping.md`.
- [ ] Index Integrity: Q2 indices in `q2-2026/` must be explicitly linked in the product `index.md`.
- [ ] Hygiene: Reports older than 30 days must be moved to `outputs/product/archive/`.

## Operating Procedure

### 1. OKR Validation
1. Scan `skills/product/okr-reporting/` for all active SOPS.
2. Verify all status emojis correspond to the calculated metric health.
3. Flag any SOP missing a "next step" or valid baseline date.

### 2. Reporting Integrity
1. Check `outputs/product/` for current week's manifests.
2. Ensure every automated report has a signed executive summary from the Strategic PM.
3. Validate that data sources quoted in reports exist in `skills/product/shared/data_sources.md`.
