from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

from .classify import classify_dataset
from .ingest import ingest_file
from .receipt import GENESIS_HASH, build_receipt, write_receipt
from .scrub import scrub_csv


def run_pipeline(
    input_path: Path | str,
    *,
    source_url: str | None = None,
    root: Path | str = ".",
    previous_receipt_hash: str = GENESIS_HASH,
    sequence_number: int = 1,
) -> Dict[str, Any]:
    root_path = Path(root)
    ingest_manifest = ingest_file(input_path, root_path / "data" / "raw", source_url=source_url)

    raw_path = Path(ingest_manifest["raw_path"])
    cleaned_path = root_path / "data" / "cleaned" / f"{raw_path.stem}.clean.csv"

    scrub_stats = scrub_csv(raw_path, cleaned_path)
    pka = classify_dataset(scrub_stats)
    receipt = build_receipt(
        raw_path=raw_path,
        cleaned_path=cleaned_path,
        ingest_manifest=ingest_manifest,
        scrub_stats=scrub_stats,
        pka=pka,
        previous_receipt_hash=previous_receipt_hash,
        sequence_number=sequence_number,
    )
    receipt_path = write_receipt(receipt, root_path / "receipts")

    return {
        "ingest": ingest_manifest,
        "cleaned_path": str(cleaned_path),
        "scrub": scrub_stats,
        "pka": pka,
        "receipt": receipt,
        "receipt_path": str(receipt_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run KPGS POC-001 RAW → CLEAN → RECEIPT")
    parser.add_argument("input", help="Path to the source CSV downloaded from an official source")
    parser.add_argument("--source-url", default=None, help="Evidence URL for source provenance")
    parser.add_argument("--root", default=".", help="Repository/output root")
    args = parser.parse_args()

    result = run_pipeline(args.input, source_url=args.source_url, root=args.root)
    print(result["receipt_path"])
    print(result["receipt"]["receipt_hash"])
    print(result["pka"]["state"])


if __name__ == "__main__":
    main()
