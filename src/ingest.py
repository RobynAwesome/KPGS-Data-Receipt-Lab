from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path | str) -> str:
    return sha256_bytes(Path(path).read_bytes())


def ingest_file(source_path: Path | str, raw_dir: Path | str, source_url: str | None = None) -> Dict[str, Any]:
    """Copy a local source file into immutable raw storage without silent overwrite."""
    source = Path(source_path)
    if not source.is_file():
        raise FileNotFoundError(source)

    data = source.read_bytes()
    source_hash = sha256_bytes(data)

    raw = Path(raw_dir)
    raw.mkdir(parents=True, exist_ok=True)
    destination = raw / source.name

    if destination.exists():
        existing_hash = sha256_file(destination)
        if existing_hash != source_hash:
            raise FileExistsError(
                f"Raw evidence collision: {destination} already exists with a different SHA-256"
            )
    else:
        destination.write_bytes(data)

    return {
        "source_path": str(source),
        "raw_path": str(destination),
        "source_url": source_url,
        "sha256": source_hash,
        "bytes": len(data),
    }
