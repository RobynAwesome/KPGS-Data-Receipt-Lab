from __future__ import annotations

from typing import Any, Dict

PKA_STATES = {"KNOWN", "PARTIAL", "UNKNOWN", "CONFLICTING"}


def classify_dataset(scrub_stats: Dict[str, Any]) -> Dict[str, Any]:
    """Classify the cleaned dataset's current epistemic quality state.

    KNOWN       -> rows exist and no missing/duplicate-cleanup signal remains.
    PARTIAL     -> rows exist but missing values or duplicate evidence exists.
    UNKNOWN     -> no data rows exist.
    CONFLICTING -> reserved for explicit contradictory evidence; never inferred casually.
    """
    if scrub_stats["output_rows"] == 0:
        state = "UNKNOWN"
        reasons = ["no_data_rows"]
    elif scrub_stats["rows_with_missing"] > 0 or scrub_stats["duplicate_rows_removed"] > 0:
        state = "PARTIAL"
        reasons = []
        if scrub_stats["rows_with_missing"] > 0:
            reasons.append("missing_values_present")
        if scrub_stats["duplicate_rows_removed"] > 0:
            reasons.append("duplicate_rows_detected")
    else:
        state = "KNOWN"
        reasons = ["structurally_complete_after_scrub"]

    return {
        "state": state,
        "reasons": reasons,
        "conflicting_claims": [],
        "boundary": "CONFLICTING requires explicit contradictory evidence and is not auto-inferred.",
    }
