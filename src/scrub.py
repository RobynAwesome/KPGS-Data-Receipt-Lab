from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List

NULL_TOKENS = {"n/a", "null", "none"}


def _normalise_cell(value: str) -> tuple[str, bool, bool]:
    stripped = value.strip()
    trimmed = stripped != value
    null_normalised = stripped.lower() in NULL_TOKENS
    if null_normalised:
        stripped = ""
    return stripped, trimmed, null_normalised


def scrub_csv(raw_path: Path | str, cleaned_path: Path | str) -> Dict[str, Any]:
    """Deterministically trim cells, normalise explicit null tokens, and remove exact duplicates.

    Structurally malformed rows are rejected rather than silently repaired.
    """
    raw = Path(raw_path)
    cleaned = Path(cleaned_path)
    cleaned.parent.mkdir(parents=True, exist_ok=True)

    rows: List[List[str]] = []
    input_rows = 0
    cells_trimmed = 0
    nulls_normalised = 0
    duplicate_rows_removed = 0
    rows_with_missing = 0

    with raw.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError("CSV is empty")

        normalised_headers = [header.strip() for header in headers]
        if not normalised_headers or any(not header for header in normalised_headers):
            raise ValueError("CSV contains blank column names")
        if len(set(normalised_headers)) != len(normalised_headers):
            raise ValueError("CSV contains duplicate column names after normalisation")

        seen: set[tuple[str, ...]] = set()
        for line_number, row in enumerate(reader, start=2):
            input_rows += 1
            if len(row) != len(normalised_headers):
                raise ValueError(
                    f"Malformed row at line {line_number}: expected {len(normalised_headers)} cells, got {len(row)}"
                )

            cleaned_row: List[str] = []
            for value in row:
                normalised, trimmed, null_normalised = _normalise_cell(value)
                cleaned_row.append(normalised)
                cells_trimmed += int(trimmed)
                nulls_normalised += int(null_normalised)

            key = tuple(cleaned_row)
            if key in seen:
                duplicate_rows_removed += 1
                continue
            seen.add(key)

            if any(value == "" for value in cleaned_row):
                rows_with_missing += 1
            rows.append(cleaned_row)

    with cleaned.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(normalised_headers)
        writer.writerows(rows)

    return {
        "transform_version": "scrub-v1",
        "columns": len(normalised_headers),
        "input_rows": input_rows,
        "output_rows": len(rows),
        "duplicate_rows_removed": duplicate_rows_removed,
        "cells_trimmed": cells_trimmed,
        "nulls_normalised": nulls_normalised,
        "rows_with_missing": rows_with_missing,
    }
