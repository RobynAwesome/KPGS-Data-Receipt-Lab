from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .ingest import sha256_file

GENESIS_HASH = "0" * 64


def _canonical_json(data: Dict[str, Any]) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_json(data: Dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data)).hexdigest()


def build_receipt(
    *,
    raw_path: Path | str,
    cleaned_path: Path | str,
    ingest_manifest: Dict[str, Any],
    scrub_stats: Dict[str, Any],
    pka: Dict[str, Any],
    previous_receipt_hash: str = GENESIS_HASH,
    sequence_number: int = 1,
) -> Dict[str, Any]:
    raw_hash = sha256_file(raw_path)
    cleaned_hash = sha256_file(cleaned_path)

    content = {
        "source_url": ingest_manifest.get("source_url"),
        "raw_sha256": raw_hash,
        "cleaned_sha256": cleaned_hash,
        "transform": scrub_stats,
        "pka": pka,
    }
    content_hash = _sha256_json(content)
    idempotency_key = hashlib.sha256(
        f"{raw_hash}:{cleaned_hash}:{scrub_stats['transform_version']}".encode("utf-8")
    ).hexdigest()

    receipt_core = {
        "sequence_number": sequence_number,
        "previous_receipt_hash": previous_receipt_hash,
        "content_hash": content_hash,
        "idempotency_key": idempotency_key,
        "pka_verdict": pka["state"],
        "claim_type": "DATA_TRANSFORMATION",
        "evidence_refs": [
            ingest_manifest.get("source_url"),
            str(raw_path),
            str(cleaned_path),
        ],
    }
    receipt_hash = _sha256_json(receipt_core)
    receipt_id = f"kpgs-data-{receipt_hash[:20]}"

    return {
        "apiVersion": "kpgs.kopanolabs/v1alpha1",
        "kind": "DataTransformationReceipt",
        "receipt_id": receipt_id,
        **receipt_core,
        "receipt_hash": receipt_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "raw": {
            "path": str(raw_path),
            "sha256": raw_hash,
            "bytes": ingest_manifest["bytes"],
        },
        "cleaned": {
            "path": str(cleaned_path),
            "sha256": cleaned_hash,
        },
        "transformation": scrub_stats,
        "pka": pka,
        "proof_state": "EXECUTED_UNVALIDATED",
        "boundaries": [
            "receipt_emitted_is_not_poc_proven",
            "cleaned_data_is_not_raw_evidence",
            "database_persistence_is_not_truth",
        ],
    }


def write_receipt(receipt: Dict[str, Any], receipts_dir: Path | str) -> Path:
    directory = Path(receipts_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{receipt['receipt_id']}.json"
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
