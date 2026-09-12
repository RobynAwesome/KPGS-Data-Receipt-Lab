# NOW — KPGS Data Receipt Lab

**Date:** 2026-09-11  
**State:** `POC_BUILDING`  
**Active issue:** #1 — RAW → CLEAN → RECEIPT  
**Active PR:** #2 — feat: implement POC-001 RAW → CLEAN → RECEIPT

## Current source

Statistics South Africa, Quarterly Labour Force Survey (QLFS), Q2 2026.

Official publication surface:
- https://www.statssa.gov.za/?PPN=P0211&page_id=1854

Official unit-record portal:
- https://isibaloweb.statssa.gov.za/pages/surveys/pss/qlfs/2026/qlfs2026.php

## Current truth

- Repo exists and is public.
- Apache-2.0 is active.
- Stats SA QLFS Q2 2026 source surfaces are verified.
- Issue #1 defines the POC acceptance contract.
- POC-001 code is implemented on PR #2.
- GitHub Actions POC-001 Proof Gate run #1 passed on the implementation commit.
- Real QLFS CSV has **not yet been ingested by this repository**.
- CI success proves the synthetic reproducibility/collision tests, not the real-world POC.

## Active vertical slice

`RAW → CLEAN → PKA → RECEIPT`

## Proof state

```yaml
implementation: CODED
source_surface: VERIFIED
raw_ingestion_real_qlfs: NOT_RUN
cleaning_real_qlfs: NOT_RUN
pka_classification_real_qlfs: NOT_RUN
receipt_generation_real_qlfs: NOT_RUN
tests_authored: true
ci_synthetic_tests: PASS
poc: NOT_YET_PROVEN
```

## Next gate

1. Capture the official QLFS Q2 2026 CSV from the Stats SA ISIbalo portal without editing or renaming its contents.
2. Run `python -m src.pipeline <csv> --source-url <official-portal-url>` against the real file.
3. Inspect the raw SHA-256, cleaned SHA-256, transformation counts, PKA state, idempotency key and receipt hash.
4. Re-run the same input and prove receipt/idempotency stability.
5. Preserve the generated receipt as evidence.
6. Review whether the real dataset exposes any scrub assumptions that need correction.
7. Only then promote POC-001 or revise it.

## Explicit hold

No dashboard, recommendation engine, database layer, RAG, vector search, or visualisation is authorized as POC completion yet.
