# NOW — KPGS Data Receipt Lab

**Date:** 2026-09-11  
**State:** `POC_BUILDING`  
**Active issue:** #1 — RAW → CLEAN → RECEIPT

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
- POC-001 executable pipeline is under implementation.
- Real QLFS CSV has **not yet been ingested by this repository**.
- No generated receipt is POC proof until the pipeline is executed and tests pass.

## Active vertical slice

`RAW → CLEAN → PKA → RECEIPT`

## Proof state

```yaml
implementation: IN_PROGRESS
source_surface: VERIFIED
raw_ingestion: NOT_RUN
cleaning: NOT_RUN
pka_classification: NOT_RUN
receipt_generation: NOT_RUN
tests_authored: IN_PROGRESS
tests_executed: NOT_RUN
poc: NOT_YET_PROVEN
```

## Next gate

1. Land deterministic ingest/scrub/classify/receipt code.
2. Land unit tests.
3. Download QLFS Q2 2026 CSV from the official ISIbalo portal.
4. Run POC-001 against the real file.
5. Inspect emitted receipt and raw/clean hashes.
6. Run tests.
7. Only then promote proof state.

## Explicit hold

No dashboard, recommendation engine, database layer, RAG, vector search, or visualisation is authorized as POC completion yet.
