"""Build transparent, fail-closed FT1 artifacts from reviewed lots only."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FT1 = ROOT / "batch10_4b" / "ft1"
LOTS = FT1 / "lots"
STAGING = FT1 / "staging"
OUT = FT1 / "artifacts"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    decision_files = sorted(LOTS.glob("FT1-LOT-*_APPRAISAL.csv"))
    if not decision_files:
        raise SystemExit("No reviewed FT1 lot exists")
    decisions = [row for path in decision_files for row in read_csv(path)]
    staged = []
    for path in decision_files:
        lot = path.name.removesuffix("_APPRAISAL.csv")
        staged.extend(json.loads((STAGING / f"{lot}_FULL_TEXT_DIGEST.json").read_text(encoding="utf-8")))
    by_id = {row["Evidence_ID"]: row for row in decisions}
    if len(decisions) != len(by_id) or {row["Evidence_ID"] for row in staged} != set(by_id):
        raise SystemExit("FT1 reviewed-lot identity mismatch")
    extraction = []
    for source in staged:
        decision = by_id[source["Evidence_ID"]]
        extraction.append({
            "Evidence_ID": source["Evidence_ID"], "Title": source["Title_Canonical"], "DOI": source["DOI"],
            "PMID": source["PMID"], "PMCID": source["PMCID"], "Year": "NR — NOT REPORTED",
            "Journal": "NR — NOT REPORTED", "Country": "NR — NOT REPORTED", "Population": "NR — NOT REPORTED",
            "Tactical_Population": "NR — NOT REPORTED", "Sample_Size": "NR — NOT REPORTED",
            "Study_Design": decision["Study_Design"], "Objective": source["Abstract"],
            "Exposure": "NR — NOT REPORTED", "Intervention": "NR — NOT REPORTED", "Comparator": "NR — NOT REPORTED",
            "Primary_Outcomes": "NR — NOT REPORTED", "Secondary_Outcomes": "NR — NOT REPORTED", "Instruments": "NR — NOT REPORTED",
            "Follow_Up": "NR — NOT REPORTED", "Main_Results": decision["Evidence_Result"],
            "Effect_Estimate": "NR — NOT REPORTED", "CI95": "NR — NOT REPORTED", "p_value": "NR — NOT REPORTED",
            "OR": "NR — NOT REPORTED", "RR": "NR — NOT REPORTED", "HR": "NR — NOT REPORTED",
            "Correlation": "NR — NOT REPORTED", "Regression": "NR — NOT REPORTED", "Other_Statistics": "NR — NOT REPORTED",
            "Author_Conclusion": source["Conclusion"], "Author_Limitations": source["Limitations"],
            "Project_Limitations": decision["Prohibited_Inference"], "Funding": source["Funding"], "COI": source["COI"],
            "Integrity_Status": decision["Integrity_Status"], "Full_Text_Source": source["Full_Text_Source"],
            "Relevant_Section": decision["Relevant_Location"], "Relevant_Table": " | ".join(source["Table_Captions"]),
            "Relevant_Result": decision["Evidence_Result"], "Full_Text_Reading_Status": decision["Full_Text_Reading_Status"],
            "Raw_XML_SHA256": source["Raw_XML_SHA256"], "Human_Confirmation": decision["HUMAN_CONFIRMATION"],
            "Claim_Ready_Provisional": decision["CLAIM_READY_PROVISIONAL"],
        })
    extraction_fields = list(extraction[0])
    write_csv("PMC100_FULL_TEXT_EXTRACTION.csv", extraction_fields, extraction)
    appraisal_fields = ["Evidence_ID", "Study_Design", "Appraisal_Instrument", "Appraisal_Overall_AI", "Appraisal_Rationale", "Full_Text_Reading_Status", "AI_Qualified", "HUMAN_CONFIRMATION"]
    write_csv("PMC100_APPRAISAL_LEDGER.csv", appraisal_fields, decisions)
    rob_fields = ["Evidence_ID", "Appraisal_Instrument", "Appraisal_Overall_AI", "Appraisal_Rationale", "Integrity_Status", "Red_Team_Status"]
    write_csv("PMC100_RISK_OF_BIAS_LEDGER.csv", rob_fields, decisions)
    claim_fields = ["Evidence_ID", "Claim_ID", "Manuscript_Layer", "Claim_Current_Wording", "Evidence_Result", "Citation_Fitness", "Relevant_Location", "Transferability", "Prohibited_Inference", "HUMAN_CONFIRMATION"]
    mapped = [row for row in decisions if row["Citation_Fitness"] not in {"UNRESOLVED", "DISCUSSION_ONLY"}]
    write_csv("PMC100_CLAIM_CITATION_MATRIX.csv", claim_fields, mapped)
    decision_fields = ["Evidence_ID", "Citation_Fitness", "Provisional_Decision", "AI_Qualified", "HUMAN_CONFIRMATION", "CLAIM_READY_PROVISIONAL", "Prohibited_Inference"]
    write_csv("PMC100_PROVISIONAL_DECISIONS.csv", decision_fields, decisions)
    repl = [row for row in decisions if row["Replacement_Comparison"] != "NOT_APPLICABLE"]
    repl_fields = ["Evidence_ID", "Provisional_Decision", "Replacement_Comparison", "Evidence_Result", "Appraisal_Overall_AI", "Integrity_Status", "HUMAN_CONFIRMATION"]
    write_csv("PMC100_REPLACEMENT_COMPARISON.csv", repl_fields, repl)
    contradiction = [{"Evidence_ID": evidence, "Status": "FULL_TEXT_UNAVAILABLE", "Decision": "NOT_ADJUDICATED_IN_FT1", "Reason": "No lawful full text identified in Batch 10.4B source discovery."} for evidence in ("EV-0052", "EV-0140", "EV-1066")]
    write_csv("PMC100_CONTRADICTORY_LEDGER.csv", list(contradiction[0]), contradiction)
    overlap = [{"Evidence_ID": row["Evidence_ID"], "Overlap_Status": row["Overlap_Status"], "Decision": "No final redundancy decision before whole-PMC comparison."} for row in decisions]
    write_csv("PMC100_COHORT_OVERLAP_LEDGER.csv", list(overlap[0]), overlap)
    integrity_fields = ["Evidence_ID", "Integrity_Status", "Integrity_Rationale", "Full_Text_Reading_Status", "HUMAN_CONFIRMATION"]
    write_csv("PMC100_INTEGRITY_LEDGER.csv", integrity_fields, decisions)
    write_csv("PMC100_FCR_CANDIDATES.csv", ["Evidence_ID", "FCR_CANDIDATE_FULL_TEXT_SUPPORTED", "Reason"], [])
    by_domain = Counter()
    for source in staged:
        by_domain[source["Domain"]] += 1
    coverage = [{"Domain": domain, "Reviewed_In_FT1": count, "Status": "PARTIAL_NOT_SATURATED", "Reason": "Only FT1 lot 01 has completed AI-provisional appraisal."} for domain, count in sorted(by_domain.items())]
    write_csv("PMC100_DOMAIN_COVERAGE.csv", list(coverage[0]), coverage)
    all_staged = []
    for digest in sorted(STAGING.glob("FT1-LOT-*_FULL_TEXT_DIGEST.json")):
        all_staged.extend(json.loads(digest.read_text(encoding="utf-8")))
    all_staged.sort(key=lambda row: int(row["Lot_Order"]))
    if len(all_staged) != 100 or len({row["Evidence_ID"] for row in all_staged}) != 100:
        raise SystemExit("FT1 staged-universe identity mismatch")
    reviewed_ids = set(by_id)
    next_evidence_id = next((row["Evidence_ID"] for row in all_staged if row["Evidence_ID"] not in reviewed_ids), "NONE_ALL_100_DOCUMENTED")
    checkpoint = []
    cumulative = []
    for path in decision_files:
        lot_rows = read_csv(path)
        cumulative.extend(lot_rows)
        c_count = len(cumulative)
        c_full_body = sum(row["Full_Text_Reading_Status"] not in {"XML_ABSTRACT_ONLY_NOT_FULL_TEXT", "FULL_TEXT_INSUFFICIENT"} for row in cumulative)
        c_decisions = Counter(row["Provisional_Decision"] for row in cumulative)
        c_ids = {row["Evidence_ID"] for row in cumulative}
        c_next = next((row["Evidence_ID"] for row in all_staged if row["Evidence_ID"] not in c_ids), "NONE_ALL_100_DOCUMENTED")
        checkpoint.append({"Lot": path.name.removesuffix("_APPRAISAL.csv"), "Evidence_IDs_Processed": "|".join(row["Evidence_ID"] for row in lot_rows), "Eligible_PMC_Universe": 100, "Reviewed": c_count, "Remaining": 100 - c_count, "Scientifically_Appraised": c_full_body, "Full_Text_Insufficient_or_Unresolved": c_count - c_full_body, "Provisional_Include": c_decisions["PROVISIONAL_INCLUDE"], "Provisional_Replacement": c_decisions["PROVISIONAL_REPLACE_CANDIDATE"], "Provisional_Contradictory": c_decisions["PROVISIONAL_CONTRADICTORY_INCLUDE"], "Discussion_Only": c_decisions["DISCUSSION_ONLY"], "Context_Only": c_decisions["CONTEXT_ONLY"], "Redundant_Exclude": c_decisions["REDUNDANT_EXCLUDE"], "Quality_Exclude": c_decisions["QUALITY_EXCLUDE"], "Misaligned_Exclude": c_decisions["MISALIGNED_EXCLUDE"], "Integrity_Blocks": c_decisions["INTEGRITY_BLOCK"], "Unresolved": c_decisions["UNRESOLVED"] + c_decisions["FULL_TEXT_INSUFFICIENT"], "FCR_Candidates": 0, "Progress_Percent": f"{c_count:.2f}", "LAST_REVIEWED_EV_ID": lot_rows[-1]["Evidence_ID"], "NEXT_UNREVIEWED_EV_ID": c_next, "Gate": "PARTIAL_GO"})
    write_csv("PMC100_CHECKPOINT_LEDGER.csv", list(checkpoint[0]), checkpoint)
    full_body = sum(row["Full_Text_Reading_Status"] not in {"XML_ABSTRACT_ONLY_NOT_FULL_TEXT", "FULL_TEXT_INSUFFICIENT"} for row in decisions)
    manifest = {"phase": "BATCH 10.4B-FT1", "state": "PARTIAL_GO", "eligible_pmc_xml": 100, "reviewed": len(decisions), "full_article_body_read": full_body, "xml_abstract_only": len(decisions) - full_body, "remaining": 100 - len(decisions), "claim_ready_provisional": 0, "human_confirmation": 0, "cef_v1_changed": False, "ev_1379": "FAIL_CLOSED", "next_evidence_id": next_evidence_id}
    (OUT / "BATCH10_4B_FT1_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
