"""Fail-closed structural audit for the Batch 10.4B source-discovery ledger."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "scientific"


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    rows = read_csv("FULL_TEXT_SATURATION_MASTER.csv")
    appraisal = read_csv("FULL_TEXT_APPRAISAL_LEDGER.csv")
    contradictions = read_csv("CONTRADICTORY_EVIDENCE_FINAL_LEDGER.csv")
    replacements = read_csv("CURRENT_VS_REPLACEMENT_MATRIX.csv")
    domains = read_csv("DOMAIN_SATURATION_FINAL.csv")
    access_holds = read_csv("FINAL_EXCLUSION_LEDGER.csv")
    classes = Counter(row["LOOP3X_Final_Class"] for row in rows)
    text_status = Counter(row["Full_Text_Status"] for row in rows)
    checks = {
        "queue_rows": len(rows) == 285,
        "unique_evidence_ids": len({row["Evidence_ID"] for row in rows}) == 285,
        "expected_classes": classes == Counter({"FULL_TEXT_REVIEW": 266, "REPLACE_EXISTING_CANDIDATE": 16, "CONTRADICTORY_CANDIDATE": 3}),
        "source_status_complete": set(text_status) == {"LAWFUL_PMC_XML", "FULL_TEXT_UNAVAILABLE"} and sum(text_status.values()) == 285,
        "claim_ready_fail_closed": all(row["Claim_Ready"] == "NO" for row in rows),
        "human_review_pending": all(row["Human_Review_Status"] == "PENDING" for row in rows),
        "no_final_inclusion": all(row["Final_Decision_AI_Provisional"] != "FINAL_INCLUDE" for row in rows),
        "appraisal_is_not_fabricated": all(row["Appraisal_Status"] in {"PENDING_AI_FULL_TEXT_REVIEW", "NOT_POSSIBLE_WITHOUT_LAWFUL_FULL_TEXT"} for row in appraisal),
        "contradictory_queue_complete": len(contradictions) == 3 and {row["Evidence_ID"] for row in contradictions} == {"EV-0052", "EV-0140", "EV-1066"},
        "replacement_queue_complete": len(replacements) == 16,
        "domains_not_prematurely_saturated": all(row["Status"] == "UNRESOLVED" for row in domains),
        "ev1379_absent_from_queue": "EV-1379" not in {row["Evidence_ID"] for row in rows},
        "access_holds_not_scientific_exclusions": all(row["Status"] == "ACCESS_PENDING_NOT_SCIENTIFIC_EXCLUSION" for row in access_holds),
    }
    result = {
        "phase": "DEEP EVIDENCE BATCH 10.4B — SOURCE DISCOVERY AUDIT",
        "counts": {
            "queue": len(rows),
            "unique_evidence_ids": len({row["Evidence_ID"] for row in rows}),
            "lawful_pmc_xml": text_status["LAWFUL_PMC_XML"],
            "full_text_unavailable": text_status["FULL_TEXT_UNAVAILABLE"],
            "contradictory": len(contradictions),
            "replacement": len(replacements),
            "final_includes": 0,
        },
        "checks": checks,
        "gate": "PARTIAL_GO" if all(checks.values()) else "BLOCKED",
    }
    (OUT / "BATCH10_4B_SOURCE_DISCOVERY_AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
