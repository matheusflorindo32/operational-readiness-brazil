"""Record the two user-supplied, final human article-strategy decisions."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "batch10_4i"
OUT = ROOT / "batch10_4j"
REVIEWER = "Matheus Florindo de Deus"
REVIEW_DATE = "2026-10-09"

DECISIONS = {
    "V015-INT-ARTICLE-STRATEGY": {
        "decision": "APPROVE_SHORT_FORM",
        "rationale": "Short-form strategy preserves evidence proportionality and avoids artificial expansion beyond the supported evidence density.",
    },
    "V015-BRA-ARTICLE-STRATEGY": {
        "decision": "APPROVE_SHORT_FORM",
        "rationale": "Short-form strategy is more proportional to the final B2 evidence density and avoids expanding contextual or bounded claims solely to maintain full-manuscript length.",
    },
}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fields, data):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    queue_path = AUDIT / "FINAL_V015_HUMAN_REVIEW_QUEUE.csv"
    queue = read_csv(queue_path)
    assert {row["Review_ID"] for row in queue} == set(DECISIONS)
    for row in queue:
        supplied = DECISIONS[row["Review_ID"]]
        existing = (row["HUMAN_DECISION"], row["HUMAN_RATIONALE"], row["HUMAN_REVIEWER"], row["HUMAN_REVIEW_DATE"])
        expected = (supplied["decision"], supplied["rationale"], REVIEWER, REVIEW_DATE)
        assert existing == ("", "", "", "") or existing == expected
        row["HUMAN_DECISION"] = supplied["decision"]
        row["HUMAN_RATIONALE"] = supplied["rationale"]
        row["HUMAN_REVIEWER"] = REVIEWER
        row["HUMAN_REVIEW_DATE"] = REVIEW_DATE
    write_csv(queue_path, list(queue[0]), queue)

    ledger = []
    for row in queue:
        ledger.append({
            "Review_ID": row["Review_ID"],
            "Manuscript": row["Manuscript"],
            "Material_Decision": row["Material_Decision"],
            "AI_Recommendation": row["AI_Recommendation"],
            "HUMAN_DECISION": row["HUMAN_DECISION"],
            "HUMAN_RATIONALE": row["HUMAN_RATIONALE"],
            "HUMAN_REVIEWER": row["HUMAN_REVIEWER"],
            "HUMAN_REVIEW_DATE": row["HUMAN_REVIEW_DATE"],
            "Scientific_Impact": "NONE",
            "Reference_Impact": "NONE",
            "Freeze_Impact": "Clears the final human manuscript-strategy prerequisite; does not execute a freeze.",
        })
    write_csv(OUT / "FINAL_HUMAN_ADJUDICATION_LEDGER.csv", list(ledger[0]), ledger)

    impacts = [
        {"Area": "Scientific impact", "Status": "NONE", "Evidence": "Article-form decisions do not modify any claim, result, locator or certainty."},
        {"Area": "Claim-set impact", "Status": "NONE", "Evidence": "10 retained claims unchanged; removed claims remain absent."},
        {"Area": "Evidence-role impact", "Status": "NONE", "Evidence": "No evidence role changed."},
        {"Area": "CEF-v1 impact", "Status": "NONE", "Evidence": "CEF-v1 unchanged."},
        {"Area": "Zotero impact", "Status": "NONE", "Evidence": "No Zotero operation executed."},
        {"Area": "Reference eligibility impact", "Status": "NONE", "Evidence": "Working reference eligibility unchanged; no freeze executed."},
        {"Area": "Manuscript strategy impact", "Status": "YES", "Evidence": "International and Brazil are both approved for a short-form strategy."},
    ]
    write_csv(OUT / "FINAL_HUMAN_DECISION_IMPACT_AUDIT.csv", list(impacts[0]), impacts)

    readiness = [
        {"Control": "Human decisions expected", "Observed": "2", "Status": "PASS"},
        {"Control": "Human decisions completed", "Observed": "2/2", "Status": "PASS"},
        {"Control": "Simulated human decisions", "Observed": "0", "Status": "PASS"},
        {"Control": "Unresolved material human decisions", "Observed": "0", "Status": "PASS"},
        {"Control": "Scientific claims changed", "Observed": "0", "Status": "PASS"},
        {"Control": "Result IDs changed", "Observed": "0", "Status": "PASS"},
        {"Control": "Evidence roles changed", "Observed": "0", "Status": "PASS"},
        {"Control": "Null findings changed", "Observed": "0", "Status": "PASS"},
        {"Control": "CEF-v1 changed", "Observed": "0", "Status": "PASS"},
        {"Control": "Zotero changed", "Observed": "0", "Status": "PASS"},
        {"Control": "References frozen", "Observed": "NO", "Status": "PASS"},
        {"Control": "Freeze readiness", "Observed": "READY_FOR_FINAL_REFERENCE_FREEZE", "Status": "PASS"},
    ]
    write_csv(OUT / "POST_HUMAN_FINAL_FREEZE_READINESS.csv", list(readiness[0]), readiness)

    report = """# BATCH 10.4J — final human adjudication\n\n`FINAL_HUMAN_ADJUDICATION_PASS`\n\nThe two material article-strategy decisions were supplied directly by Matheus Florindo de Deus and recorded verbatim in the official v0.15 queue and final adjudication ledger on 2026-10-09. International and Brazil are both approved for a short-form strategy.\n\nThe decisions affect article strategy only. Scientific claims, Result_IDs, source locators, evidence roles, certainty, null findings, cohort handling, CEF-v1, Zotero, and working-reference eligibility are unchanged. No reference freeze was executed.\n\nAll final human material decisions are complete. The package is `READY_FOR_FINAL_REFERENCE_FREEZE`.\n\nNext permitted gate: `GO_FINAL_REFERENCE_FREEZE`.\n"""
    (OUT / "BATCH10_4J_REPORT.md").write_text(report, encoding="utf-8")
    artifacts = sorted(OUT.glob("*.csv")) + [OUT / "BATCH10_4J_REPORT.md"]
    manifest = {
        "batch": "BATCH 10.4J",
        "base_commit": "25c473377048a7ebb40f3f085715e7f0d8d8cc84",
        "entry_gate": "V015_FINAL_SCIENTIFIC_AUDIT_PASS",
        "gate": "FINAL_HUMAN_ADJUDICATION_PASS",
        "next_gate": "GO_FINAL_REFERENCE_FREEZE",
        "human_decisions_expected": 2,
        "human_decisions_completed": 2,
        "simulated_human_decisions": 0,
        "unresolved_material_human_decisions": 0,
        "scientific_claims_changed": 0,
        "result_ids_changed": 0,
        "evidence_roles_changed": 0,
        "null_findings_changed": 0,
        "CEF_v1_changed": 0,
        "Zotero_changed": 0,
        "references_frozen": False,
        "freeze_readiness": "READY_FOR_FINAL_REFERENCE_FREEZE",
        "artifact_sha256": {path.name: digest(path) for path in artifacts},
    }
    (OUT / "BATCH10_4J_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
