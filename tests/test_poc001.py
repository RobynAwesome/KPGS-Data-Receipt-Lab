from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.ingest import sha256_file
from src.pipeline import run_pipeline


class Poc001Tests(unittest.TestCase):
    def test_raw_clean_receipt_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sample.csv"
            source.write_text(
                "name,age,status\n"
                " Alice ,25,Employed\n"
                "Bob, ,Unemployed\n"
                "Alice,25,Employed\n",
                encoding="utf-8",
            )
            original_hash = sha256_file(source)

            first = run_pipeline(
                source,
                source_url="https://example.invalid/official-source",
                root=root / "run",
            )
            second = run_pipeline(
                source,
                source_url="https://example.invalid/official-source",
                root=root / "run",
            )

            raw_path = Path(first["ingest"]["raw_path"])
            cleaned_path = Path(first["cleaned_path"])
            receipt_path = Path(first["receipt_path"])

            self.assertEqual(sha256_file(raw_path), original_hash)
            self.assertTrue(cleaned_path.exists())
            self.assertTrue(receipt_path.exists())

            self.assertEqual(first["scrub"]["input_rows"], 3)
            self.assertEqual(first["scrub"]["output_rows"], 2)
            self.assertEqual(first["scrub"]["duplicate_rows_removed"], 1)
            self.assertEqual(first["scrub"]["rows_with_missing"], 1)
            self.assertEqual(first["pka"]["state"], "PARTIAL")

            self.assertEqual(first["receipt"]["receipt_hash"], second["receipt"]["receipt_hash"])
            self.assertEqual(first["receipt"]["idempotency_key"], second["receipt"]["idempotency_key"])
            self.assertEqual(first["receipt"]["raw"]["sha256"], original_hash)
            self.assertEqual(len(first["receipt"]["cleaned"]["sha256"]), 64)

            emitted = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(emitted["receipt_hash"], first["receipt"]["receipt_hash"])
            self.assertEqual(emitted["proof_state"], "EXECUTED_UNVALIDATED")

    def test_raw_collision_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sample.csv"
            source.write_text("a,b\n1,2\n", encoding="utf-8")
            run_root = root / "run"
            run_pipeline(source, root=run_root)

            source.write_text("a,b\n9,9\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                run_pipeline(source, root=run_root)


if __name__ == "__main__":
    unittest.main()
