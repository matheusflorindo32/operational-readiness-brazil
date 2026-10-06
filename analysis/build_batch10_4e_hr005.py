"""Build the constrained HR-005 replacement adjudication record.

This writes only the authorized HR-005 human decision after the documented
comparison establishes that EV-0386 must not replace the two retained,
claim-specific references.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4e"
AUDIT = ROOT / "batch10_4d"
DECISION = {
    "HUMAN_DECISION": "KEEP_CURRENT",
    "HUMAN_REVIEWER": "Matheus Florindo de Deus",
    "HUMAN_REVIEW_DATE": "2026-10-06",
    "HUMAN_RATIONALE": "After final comparative review of the current verified reference and EV-0386, the current reference was retained because it provides equal or superior claim alignment, directness, methodological suitability, or incremental citation value for the manuscript.",
}


def read(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, fields, rows):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def refresh_manifest():
    path = AUDIT / "BATCH10_4D_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    queue = AUDIT / "FINAL_HUMAN_REVIEW_QUEUE.csv"
    manifest["files"][queue.name] = hashlib.sha256(queue.read_bytes()).hexdigest()
    manifest.setdefault("human_adjudication_updates", {})["HR-005"] = {
        "evidence_id": "EV-0386",
        "decision": "KEEP_CURRENT",
        "reviewer": "Matheus Florindo de Deus",
        "review_date": "2026-10-06",
        "scope": "Retain EV-1484 and EV-1483 for their distinct, existing v0.13 claims; do not promote EV-0386 as a replacement or supporting citation.",
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main():
    comparison = []
    dimensions = [
        ("claim alignment", "EV-1484/EV-1483 support existing medical-readiness and patrol-context citations in v0.13.", "Only partially supports INT-MED-CAUTIOUS-SUPPLEMENT, a claim not present as supporting text in v0.13.", "CURRENT", "HR001 mapping; v0.13 reference audit; PMC100 claim matrix"),
        ("population directness", "Brazilian police/firefighter records and Brazilian peacekeepers.", "15 male career firefighters from one station.", "CURRENT", "Canonical master; PMC100 extraction"),
        ("occupational/tactical relevance", "Directly contextualize the retained occupational medical and patrol-readiness content.", "Fire-ground task is relevant, but only to a short astaxanthin intervention.", "CURRENT", "v0.13 roles; PMC100 extraction"),
        ("study design", "Cross-sectional medical-record study plus repeated-measures field observation; suited to their descriptive contexts.", "Randomized double-blind placebo-controlled crossover trial.", "NO AUTOMATIC WIN", "Canonical master; FT1 appraisal"),
        ("sample", "EV-1484: 6,621 police officers and 1,347 firefighters; EV-1483: 20 peacekeepers.", "15 firefighters.", "CURRENT", "Canonical master; PMC100 extraction"),
        ("outcome alignment", "Health-status and hydration/autonomic context match current citations.", "No statistically or clinically significant cardiometabolic or fire-ground performance effect after four weeks.", "CURRENT", "FT1 extraction and claim matrix"),
        ("methodological quality", "Verified retained references are bounded to their existing descriptive roles.", "RoB 2: SOME_CONCERNS; small sample and unresolved crossover/reporting issues.", "CURRENT", "FINAL_REFERENCE_AUDIT; FT1 appraisal"),
        ("risk of bias", "No integrity block in versioned QA; no new causal role assigned.", "SOME_CONCERNS, including randomization, carryover and selective-reporting questions.", "CURRENT", "FINAL_REFERENCE_AUDIT; FT1 risk-of-bias ledger"),
        ("statistical informativeness", "Current citations are not used to make the astaxanthin claim.", "Most apparent biomarker changes were within-group; between-group operational/cardiometabolic effects were null.", "CURRENT", "PMC100 extraction"),
        ("recency", "2015 and 2022.", "2024.", "EV-0386 ONLY", "Canonical master"),
        ("generalizability", "EV-1484 has a large regional Brazilian service population; both records retain stated limits.", "Single-station male sample; moderate transferability only.", "CURRENT", "Canonical master; FT1 appraisal"),
        ("Brazil relevance", "Direct Brazilian populations and context.", "No Brazilian public-safety inference permitted.", "CURRENT", "Canonical master; FT1 prohibited inference"),
        ("international relevance", "Existing citations already serve their bounded contexts.", "Relevant firefighter setting, but intervention-specific and not tied to an active claim.", "CURRENT", "v0.13/HR001 mapping; FT1 appraisal"),
        ("incremental value", "Retains existing, cited content without reference inflation.", "No material incremental value because its proposed supplement claim is absent and results do not demonstrate performance benefit.", "CURRENT", "HR001 mapping; FT1 extraction"),
        ("overlap/redundancy", "Two current records have distinct roles and populations.", "No cohort overlap identified, but adding it would create an uncited claim pathway.", "CURRENT", "PMC100 cohort-overlap ledger; HR001 mapping"),
        ("integrity", "No integrity block recorded in versioned QA.", "INTEGRITY_CLEAR_AS_OF_2026-10-03, date-bounded.", "TIE", "FINAL_REFERENCE_AUDIT; FT1 integrity ledger"),
        ("citation fitness", "Cited in v0.13 with 2/2 and 3/2 International/Brazil occurrences respectively.", "PARTIAL_SUPPORT and HUMAN_REVIEW_PENDING; no manuscript citation.", "CURRENT", "FINAL_REFERENCE_AUDIT; PMC100 claim matrix"),
        ("suitability for exact manuscript wording", "Matches existing bounded wording; no change required.", "Would require creating/narrowing a supplement-specific sentence and cannot support a performance-improvement claim.", "CURRENT", "HR001 map; FT1 prohibited inference"),
    ]
    for number, (dimension, current, candidate, favors, source) in enumerate(dimensions, 1):
        comparison.append({
            "Comparison_ID": "HR005-REPL-EV-0386",
            "Dimension_Number": number,
            "Dimension": dimension,
            "Current_Reference_Set": "EV-1484 (Ref 14) + EV-1483 (Ref 15)",
            "Current_Evidence": current,
            "EV0386_Evidence": candidate,
            "Finding_Favors": favors,
            "Source": source,
            "Final_Classification": "KEEP_CURRENT",
        })
    write(OUT / "HR005_REPLACEMENT_COMPARISON.csv", list(comparison[0]), comparison)

    impact = [
        {"Claim_ID": "BR-CLM-011", "Manuscript": "Both", "Current_Wording": "Bounded health-status context for police officers and firefighters in Paraná.", "Current_Reference": "EV-1484 / Ref 14", "EV0386_Role": "Does not assess this claim.", "Effect_If_Current_Kept": "Retains the direct, regional descriptive context.", "Effect_If_Replaced": "Loses the current claim's population and outcome alignment.", "Effect_If_Both": "Adds an unneeded supplement study to a different claim.", "Wording_Change_Required": "NO", "Decision": "KEEP_CURRENT"},
        {"Claim_ID": "BR-CLM-010", "Manuscript": "Both", "Current_Wording": "Military patrol strain as context only.", "Current_Reference": "EV-1483 / Ref 15", "EV0386_Role": "Does not assess patrol hydration or autonomic modulation.", "Effect_If_Current_Kept": "Retains the bounded operational context.", "Effect_If_Replaced": "Removes a distinct context without claim-equivalent evidence.", "Effect_If_Both": "Inflates references without a sentence-level role for EV-0386.", "Wording_Change_Required": "NO", "Decision": "KEEP_CURRENT"},
        {"Claim_ID": "INT-MED-CAUTIOUS-SUPPLEMENT", "Manuscript": "Both", "Current_Wording": "NOT PRESENT AS A SUPPORTING CLAIM IN V0.13.", "Current_Reference": "No assigned v0.13 citation", "EV0386_Role": "PARTIAL_SUPPORT only; four-week astaxanthin intervention had no statistically or clinically significant cardiometabolic or fire-ground performance effect.", "Effect_If_Current_Kept": "No manuscript change; avoids unsupported promotion.", "Effect_If_Replaced": "Would require a new narrowed sentence and human-approved citation path.", "Effect_If_Both": "Would still require a new sentence and adds reference inflation.", "Wording_Change_Required": "YES IF EV-0386 WERE EVER CITED; NOT AUTHORIZED HERE", "Decision": "KEEP_CURRENT"},
    ]
    write(OUT / "HR005_CLAIM_IMPACT.csv", list(impact[0]), impact)

    record = {"Review_ID": "HR-005", "Evidence_ID": "EV-0386", "Replacement_Relationship": "DETERMINISTIC: EV-1484; EV-1483", "Final_Classification": "KEEP_CURRENT", **DECISION, "Current_References_Retained": "EV-1484 (Ref 14); EV-1483 (Ref 15)", "EV0386_Use": "Not promoted as support or replacement; no manuscript change.", "Final_Reference_Freeze": "NO"}
    write(OUT / "HR005_HUMAN_DECISION_RECORD.csv", list(record), [record])

    queue_path = AUDIT / "FINAL_HUMAN_REVIEW_QUEUE.csv"
    queue = read(queue_path)
    for row in queue:
        if row["Review_ID"] == "HR-005":
            row.update(DECISION)
    target = [row for row in queue if row["Review_ID"] == "HR-005"]
    if len(target) != 1 or target[0]["HUMAN_DECISION"] != "KEEP_CURRENT":
        raise RuntimeError("HR-005 was not uniquely updated")
    write(queue_path, list(queue[0]), queue)
    refresh_manifest()

    (OUT / "HR005_REPORT.md").write_text("""# HR-005 — EV-0386 final reference decision

The replacement relationship is deterministic: EV-0386 was proposed against the retained set EV-1484 (reference 14) and EV-1483 (reference 15). The comparison covers all 18 required dimensions. These references support distinct existing, bounded claims in v0.13: Brazilian police/firefighter health-status context and Brazilian peacekeeper patrol context. EV-0386 is a 2024 randomized, double-blind, placebo-controlled crossover trial in 15 male career firefighters, but its four-week astaxanthin intervention showed no statistically or clinically significant cardiometabolic or fire-ground performance effect. It is only `PARTIAL_SUPPORT` for `INT-MED-CAUTIOUS-SUPPLEMENT`, which has no supporting sentence or citation in v0.13.

The final classification is `KEEP_CURRENT`. Matheus Florindo de Deus recorded the conditionally authorized decision on 2026-10-06. This does not promote EV-0386 to support, does not change either manuscript, does not freeze references, and does not modify CEF-v1, Zotero, or Claim-Ready status.

Red Team found no recency, design-prestige, citation-count, population/outcome mismatch, or reference-inflation basis to replace the current set. Gate: `HR005_ADJUDICATION_COMPLETE`; next authorized item: `GO_HR006_HUMAN_ADJUDICATION`.
""", encoding="utf-8")


if __name__ == "__main__":
    main()
