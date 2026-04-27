# Intelligence/Governance Changelog

## [Unreleased]

## 2026-04-27 — Complete three handoffs (Link Standardization, Large File Convention, JSON Archive Retention) and improve Dream Sensor health.Scan

**Files changed:**
- `intelligence/` — Standardized link headers to `## Links` across 11 `index.md` files in the vault.Scan DONE
- `skills/dream/sensors/context.py` — Introduced the large file flag convention `_(SIZE)_` and an `IGNORE_LIST` in `context.py`. Applied the convention to Q2 Shareout source index.Scan DONE
- `skills/pipelines/status/scripts/update_manifest.py` — Created `retention_policy.md` enforcing a 7-day TTL on JSON archives. Implemented `cleanup_old_archives` in `update_manifest.py` and purged >50 expired JSON files.Scan DONE
- `skills/dream/sensors/links.py` — Fixed links sensor parsing to handle URL decoding and angle brackets cleanly, eliminating false-positive ghost links.Scan DONE

**Next:** Review remaining ghost links and broken index files if any.Scan

