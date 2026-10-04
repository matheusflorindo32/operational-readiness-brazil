"""Assemble source-discovery lots into transparent, non-promotional Batch 10.4B ledgers."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "batch10_4b"
LOTS = BASE / "scientific" / "lots"
OUT = BASE / "scientific"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    files = sorted(LOTS.glob("LOT-*_SOURCE_DISCOVERY.csv"))
    rows = [row for path in files for row in read_csv(path)]
    rows.sort(key=lambda row: int(row["Batch_Order"]))
    if len(rows) != 285 or len({row["Evidence_ID"] for row in rows}) != 285:
        raise SystemExit(f"Expected 285 unique records, found {len(rows)} rows / {len({row['Evidence_ID'] for row in rows})} IDs")
    write_csv(OUT / "FULL_TEXT_SATURATION_MASTER.csv", list(rows[0]), rows)
    appraisal_fields = ["Evidence_ID", "Title", "Study_Design", "Publication_Types", "Appraisal_Instrument", "Appraisal_Status", "Full_Text_Status", "Human_Review_Status", "Claim_Ready"]
    write_csv(OUT / "FULL_TEXT_APPRAISAL_LEDGER.csv", appraisal_fields, rows)
    integrity_fields = ["Evidence_ID", "PMID", "DOI", "Primary_Metadata_Source", "Integrity_Status", "Integrity_Notices", "Full_Text_Status", "Full_Text_URL", "Retrieval_Error"]
    write_csv(OUT / "INTEGRITY_FINAL_LEDGER.csv", integrity_fields, rows)
    contradictory = [row for row in rows if row["LOOP3X_Final_Class"] == "CONTRADICTORY_CANDIDATE"]
    contradiction_rows = []
    impacts = {"EV-0052": "MINOR_QUALIFICATION", "EV-0140": "MINOR_QUALIFICATION", "EV-1066": "CLAIM_NARROWING"}
    for row in contradictory:
        contradiction_rows.append({"Evidence_ID": row["Evidence_ID"], "Title": row["Title"], "PMID": row["PMID"], "DOI": row["DOI"], "Primary_Source": row["Primary_Metadata_Source"], "Full_Text_Status": row["Full_Text_Status"], "Observed_Abstract_Boundary": row["Abstract"], "AI_Provisional_Impact": impacts[row["Evidence_ID"]], "Decision": row["Final_Decision_AI_Provisional"], "Human_Review_Status": "PENDING", "Notes": "No final contradictory inclusion without lawful full text and design-specific appraisal."})
    write_csv(OUT / "CONTRADICTORY_EVIDENCE_FINAL_LEDGER.csv", list(contradiction_rows[0]), contradiction_rows)
    current_by_section = {
        "Physical and Academy Readiness / Aptidao e academia": "EV-1481; EV-1480",
        "Medical and Cardiovascular Readiness / Saude e prontidao medica": "EV-1484; EV-1483",
        "Nutrition and Schedule Load / Nutricao e jornadas": "EV-1471; EV-1472",
        "Cognition and Firearm-Task Performance / Cognicao e tiro": "EV-1473; EV-1474",
    }
    replacements = [row for row in rows if row["LOOP3X_Final_Class"] == "REPLACE_EXISTING_CANDIDATE"]
    replacement_rows = [{"Candidate_Evidence_ID": row["Evidence_ID"], "Candidate_Title": row["Title"], "Current_Related_Evidence": current_by_section.get(row["Section"], "SECTION_MAPPING_REQUIRED"), "Section": row["Section"], "Candidate_Design": row["Study_Design"] or row["Publication_Types"], "Full_Text_Status": row["Full_Text_Status"], "Comparison_Decision_AI_Provisional": "UNRESOLVED", "Reason": "No replacement is permitted before full-text appraisal, claim-level comparison and human confirmation."} for row in replacements]
    write_csv(OUT / "CURRENT_VS_REPLACEMENT_MATRIX.csv", list(replacement_rows[0]), replacement_rows)
    no_rows = []
    for filename, fields in {
        "FINAL_CLAIM_CITATION_MATRIX.csv": ["Evidence_ID", "Manuscript", "Section", "Claim", "Exact_Result", "Location", "Status"],
        "FINAL_INCLUDE_REFERENCES_INTERNATIONAL.csv": ["Evidence_ID", "Title", "DOI", "PMID", "Claim", "Status"],
        "FINAL_INCLUDE_REFERENCES_BRAZIL.csv": ["Evidence_ID", "Title", "DOI", "PMID", "Claim", "Status"],
        "REDUNDANCY_FINAL_LEDGER.csv": ["Evidence_ID", "Comparison_Group", "Status", "Reason"],
        "MANUSCRIPT_CHANGE_REQUIREMENTS.csv": ["Claim_ID", "Requirement", "Evidence_ID", "Status"],
        "FREEZE_CHANGE_ADJUDICATION.csv": ["Evidence_ID", "Candidate", "Reason", "Decision", "Human_Review_Status"],
    }.items():
        write_csv(OUT / filename, fields, no_rows)
    # The requested filename is retained for downstream compatibility, but an
    # unavailable lawful full text is an access-status hold, never a scientific
    # exclusion.  Calling these records excluded would silently overstate what
    # this bounded source-discovery phase established.
    exclusions = [{"Evidence_ID": row["Evidence_ID"], "Title": row["Title"], "Status": "ACCESS_PENDING_NOT_SCIENTIFIC_EXCLUSION", "Decision": row["Final_Decision_AI_Provisional"], "Reason": row["Decision_Rationale"], "Full_Text_Status": row["Full_Text_Status"]} for row in rows if row["Final_Decision_AI_Provisional"] == "FULL_TEXT_UNAVAILABLE"]
    write_csv(OUT / "FINAL_EXCLUSION_LEDGER.csv", list(exclusions[0]), exclusions)
    domains = defaultdict(list)
    for row in rows:
        domains[row["Domain"]].append(row)
    domain_rows = [{"Domain": domain, "Candidates": len(group), "Source_Discovery_Complete": len(group), "Lawful_Full_Text": sum(item["Full_Text_Status"] == "LAWFUL_PMC_XML" for item in group), "Final_Included": 0, "Unresolved": sum(item["Final_Decision_AI_Provisional"] == "UNRESOLVED" for item in group), "Status": "UNRESOLVED", "Saturation_Stop_Reason": "No domain may be declared saturated before full-text appraisal and claim-level review."} for domain, group in sorted(domains.items())]
    write_csv(OUT / "DOMAIN_SATURATION_FINAL.csv", list(domain_rows[0]), domain_rows)
    checkpoint = {"queue": 285, "source_discovery_complete": len(rows), "lawful_pmc_xml": sum(row["Full_Text_Status"] == "LAWFUL_PMC_XML" for row in rows), "full_text_unavailable": len(exclusions), "unresolved": sum(row["Final_Decision_AI_Provisional"] == "UNRESOLVED" for row in rows), "final_include": 0, "gate": "PARTIAL_GO", "next_unreviewed_ev_id": next((row["Evidence_ID"] for row in rows if row["Final_Decision_AI_Provisional"] == "UNRESOLVED"), None)}
    (OUT / "BATCH10_4B_SOURCE_DISCOVERY_MANIFEST.json").write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checkpoint, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
