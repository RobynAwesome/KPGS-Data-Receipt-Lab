# KPGS Data Receipt Lab

A governed data-engineering POC that preserves raw evidence, performs deterministic cleaning under partial knowledge, and emits verifiable KPGS receipts for every transformation.

## POC-001 — RAW → CLEAN → RECEIPT

```text
Stats SA QLFS Q2 2026
        ↓
RAW EVIDENCE
        ↓
DETERMINISTIC SCRUB
        ↓
RAW ↔ CLEAN DIFF
        ↓
PKA QUALITY STATE
KNOWN | PARTIAL | UNKNOWN | CONFLICTING
        ↓
HASH-LINKED KPGS RECEIPT
```

The first dataset is Statistics South Africa's **Quarterly Labour Force Survey (QLFS), Q2 2026**, published on 11 August 2026.

Official source surfaces:
- https://www.statssa.gov.za/?PPN=P0211&page_id=1854
- https://isibaloweb.statssa.gov.za/pages/surveys/pss/qlfs/2026/qlfs2026.php

The official Q2 2026 unemployment rate is **33.6%**. This project does not hard-code that number as proof; the point is to build a pipeline that can preserve evidence, transform data transparently, and state what the data can and cannot support.

## Governance laws

- `CRUD != truth`
- `selected data != trusted data`
- `cleaned data != raw evidence`
- `convergence != proof`
- `implemented != validated`
- `tests authored != tests passed`
- no transformation may silently overwrite raw evidence
- uncertainty must remain explicit

## Repository map

```text
contracts/   source and transformation contracts
src/         ingest, scrub, classify, receipt, pipeline
schemas/     machine-readable receipt schema
data/raw/    immutable local source captures
data/cleaned deterministic outputs
receipts/    machine-readable proof artifacts
tests/       executable POC checks
NOW.md       current bounded state
```

Large raw/cleaned datasets are intentionally not committed by default. Their SHA-256 hashes and source provenance belong in receipts.

## Run locally

```bash
python -m src.pipeline path/to/qlfs-q2-2026.csv \
  --source-url "https://isibaloweb.statssa.gov.za/pages/surveys/pss/qlfs/2026/qlfs2026.php"

python -m unittest discover -s tests -v
```

No third-party Python dependencies are required for POC-001.

## Proof state

`POC_BUILDING` — source surfaces verified; executable pipeline being implemented; real QLFS ingestion and test evidence still required before `POC_PROVEN`.

See [Issue #1](../../issues/1) for the acceptance contract.
