"""Conservative, reproducible first-pass title/abstract screening."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "search/exports/2026-08-28/2026-08-28_pubmed_ABC_deduplicated_metadata.json"
)
IDENTITIES = ROOT / "reporting/preanalysis/2026-09-06/evidence-identity-map.csv"

TITLE_PAIRS = {"38280817", "36368814", "33721322", "11469036"}
RETRACTION_PMID = "26159007"
SCREEN_DATE = "2026-09-07"
MANUAL_OVERRIDES = {
    "42425810": (
        "INCLUDE_FULL_TEXT",
        "Military-derived prolonged field care in austere settings is explicitly relevant to operational APHT transferability; retain for full text.",
    ),
    "42088002": (
        "PENDING_ADJUDICATION",
        "The record is a correction concerning a military suicide-prevention implementation study; review the corrected source before relevance adjudication.",
    ),
    "37094289": (
        "PENDING_ADJUDICATION",
        "Austere operational clinical-priority methods may be contextually relevant, but applicability cannot be resolved from title/abstract alone.",
    ),
}

DIRECT = re.compile(
    r"\b(police|law enforcement|fire ?fighters?|fire service|first responders?|"
    r"emergency responders?|ems personnel|paramedics?|military personnel|soldiers?|"
    r"marine corps|marines|army|navy|air force|armed forces?|tactical|combat|"
    r"warfighters?|special operations?|public safety|correctional officers?|"
    r"prison officers?|border patrol|homeland security|gendarmerie|peacekeepers?)\b",
    re.IGNORECASE,
)
DOMAIN = re.compile(
    r"\b(readiness|fit for duty|fitness|physical performance|occupational performance|"
    r"task performance|aerobic|strength|power|endurance|body composition|fatigue|sleep|"
    r"recovery|cogniti\w*|stress|resilien\w*|mental health|posttraumatic|ptsd|injur\w*|"
    r"musculoskeletal|occupational health|cardiovascular|cardiometabolic|nutrition|"
    r"hydration|wearable\w*|monitoring|load carriage|training|exercise)\b",
    re.IGNORECASE,
)
APHT = re.compile(
    r"\b(tactical combat casualty|tactical emergency casualty|tactical emergency medical|"
    r"prehospital|pre-hospital|hemorrhage|tourniquet|casualty evacuation|medical readiness|"
    r"buddy care|combat medic|combat trauma|tccc|tecc|tems)\b",
    re.IGNORECASE,
)
IMPLEMENTATION_STRONG = re.compile(
    r"\b(implementation science|implementation research|consolidated framework for implementation|"
    r"cfir|expert recommendations for implementing change|eric strateg\w*|"
    r"proctor implementation outcomes?)\b",
    re.IGNORECASE,
)
IMPLEMENTATION_TERMS = re.compile(
    r"\b(implementation|adoption|fidelity|feasibility|acceptability|appropriateness|"
    r"penetration|sustainability|implementation outcome)\b",
    re.IGNORECASE,
)
NOISE = re.compile(
    r"\b(tokamak|photocatal\w*|thermoelectric|semiconductor|radioisotope|nanoparticle|"
    r"gene polymorphism|schizophrenia|tumou?r|cancer cell|mouse model|mice model|rat model|"
    r"marine ecosystem|fish species|soil bacteria|enzyme activity|protein expression)\b",
    re.IGNORECASE,
)


def matches(pattern, text):
    return sorted({m.group(0).lower() for m in pattern.finditer(text)})


def classify(record, source):
    content = f"{record['title']} {record['abstract']}"
    direct = matches(DIRECT, content)
    domain = matches(DOMAIN, content)
    apht = matches(APHT, content)
    implementation_strong = matches(IMPLEMENTATION_STRONG, content)
    implementation = matches(IMPLEMENTATION_TERMS, content)
    noise = matches(NOISE, content)
    families = source["families"]
    retracted = "Retracted Publication" in record["publication_types"] or any(
        c["ref_type"].startswith("Retraction") for c in record["corrections"]
    )
    if retracted:
        decision = "BLOCKED_INTEGRITY"
        rationale = "PubMed identifies the record as a retracted publication and links a retraction notice."
    elif (direct and domain) or ("B" in families and apht) or implementation_strong:
        decision = "INCLUDE_FULL_TEXT"
        if implementation_strong:
            basis = "an explicit implementation-science construct"
        elif "B" in families and apht:
            basis = "an explicit operational APHT/medical-readiness topic"
        else:
            basis = "an explicit tactical/public-safety context and readiness domain"
        rationale = f"Title/abstract identify {basis}; retain for full-text assessment."
    elif not record["abstract"]:
        decision = "PENDING_ADJUDICATION"
        rationale = "No abstract is available in the current PubMed record; title alone is insufficient for exclusion."
    elif noise and not (direct or apht or implementation_strong):
        decision = "EXCLUDE_TITLE_ABSTRACT"
        rationale = "Title/abstract describe a clearly unrelated biomedical, physical-science or engineering topic."
    elif direct or domain or apht or ("C" in families and implementation):
        decision = "PENDING_ADJUDICATION"
        rationale = "A potentially relevant concept is present, but direct applicability is ambiguous at title/abstract level."
    else:
        decision = "EXCLUDE_TITLE_ABSTRACT"
        rationale = "No tactical/public-safety context, readiness domain, operational APHT link or explicit implementation-science role is evident in title/abstract."
    if record["pmid"] in MANUAL_OVERRIDES:
        decision, rationale = MANUAL_OVERRIDES[record["pmid"]]
    return (
        decision,
        rationale,
        {
            "direct_context": direct,
            "readiness_domain": domain,
            "apht": apht,
            "implementation_strong": implementation_strong,
            "implementation_terms": implementation,
            "unrelated_signal": noise,
        },
    )


def integrity(record):
    ref_types = {x["ref_type"] for x in record["corrections"]}
    if "Retracted Publication" in record["publication_types"] or any(
        x.startswith("Retraction") for x in ref_types
    ):
        return "Retracted", "Retracted", "BLOCK"
    if any(x.startswith(("Erratum", "Update")) for x in ref_types):
        return "Correction", "Pending", "REVIEW_CORRECTION"
    return "Clear", "Verified — clear", "CLEAR"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_rows = json.loads(SOURCE.read_text(encoding="utf-8"))
    source = {x["pmid"]: x for x in source_rows}
    current_rows = json.loads(args.current.read_text(encoding="utf-8"))
    decisions = []
    for record in current_rows:
        old = source[record["pmid"]]
        decision, rationale, terms = classify(record, old)
        correction, integrity_status, integrity_action = integrity(record)
        metadata_verified = all(
            record[x]
            for x in ("title_match", "authors_match", "journal_match", "year_match")
        )
        identifiers_verified = record["doi_match"]
        absent_doi = not old["doi"]
        priority = (
            record["pmid"] == RETRACTION_PMID
            or absent_doi
            or record["pmid"] in TITLE_PAIRS
        )
        if decision == "BLOCKED_INTEGRITY":
            limitation = "This retracted article cannot support any scientific conclusion in this project."
        elif decision == "EXCLUDE_TITLE_ABSTRACT":
            limitation = "This title/abstract screening record does not support conclusions about Brazilian operational readiness or institutional practice."
        elif decision == "PENDING_ADJUDICATION":
            limitation = "Title/abstract information is insufficient for a substantive scientific, causal, transferability or institutional claim."
        else:
            limitation = "Title/abstract screening alone does not establish effectiveness, causality, methodological quality, transferability to Brazilian public safety or an institutional recommendation."
        decisions.append(
            {
                "pmid": record["pmid"],
                "decision": decision,
                "rationale": rationale,
                "reviewer": "OpenAI Codex — AI-assisted primary screen",
                "review_date": SCREEN_DATE,
                "source": f"{record['source_url']} — NCBI Entrez EFetch 2026-09-07",
                "abstract_available": bool(record["abstract"]),
                "priority": priority,
                "priority_reasons": [
                    reason
                    for condition, reason in (
                        (record["pmid"] == RETRACTION_PMID, "retraction"),
                        (absent_doi, "source DOI absent"),
                        (record["pmid"] in TITLE_PAIRS, "same-title candidate pair"),
                    )
                    if condition
                ],
                "metadata_verified": metadata_verified,
                "metadata_conflicts": [
                    name
                    for name in ("title", "authors", "journal", "year")
                    if not record[f"{name}_match"]
                ],
                "identifiers_verified": identifiers_verified,
                "source_doi_absence_confirmed": absent_doi and not record["doi"],
                "correction_retraction_status": correction,
                "integrity_status": integrity_status,
                "integrity_action": integrity_action,
                "integrity_source_url": (
                    f"https://pubmed.ncbi.nlm.nih.gov/{record['corrections'][0]['pmid']}/"
                    if record["corrections"] and record["corrections"][0]["pmid"]
                    else record["source_url"]
                ),
                "correction_links": record["corrections"],
                "limitation": limitation,
                "matched_terms": terms,
                "families": old["families"],
            }
        )
    counts = Counter(x["decision"] for x in decisions)
    summary = {
        "screened": len(decisions),
        "decision_counts": dict(sorted(counts.items())),
        "priority_screened": sum(x["priority"] for x in decisions),
        "source_doi_absent": sum(not source[x["pmid"]]["doi"] for x in decisions),
        "source_doi_absence_confirmed": sum(
            x["source_doi_absence_confirmed"] for x in decisions
        ),
        "metadata_verified": sum(x["metadata_verified"] for x in decisions),
        "identifiers_verified": sum(x["identifiers_verified"] for x in decisions),
        "correction_review_pending": sum(
            x["integrity_action"] == "REVIEW_CORRECTION" for x in decisions
        ),
        "integrity_blocked": sum(
            x["decision"] == "BLOCKED_INTEGRITY" for x in decisions
        ),
        "claim_ready": 0,
        "input_sha256": hashlib.sha256(args.current.read_bytes()).hexdigest(),
        "rubric": "docs/TITLE_ABSTRACT_SCREENING_RUBRIC_2026-09-07.md",
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "screening-decisions.json").write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output / "screening-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ledger_fields = [
        "pmid",
        "decision",
        "rationale",
        "reviewer",
        "review_date",
        "source",
        "abstract_available",
        "priority",
        "priority_reasons",
        "metadata_verified",
        "metadata_conflicts",
        "identifiers_verified",
        "source_doi_absence_confirmed",
        "correction_retraction_status",
        "integrity_status",
        "integrity_action",
        "integrity_source_url",
        "limitation",
    ]
    with (args.output / "screening-decision-ledger.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=ledger_fields)
        writer.writeheader()
        for item in decisions:
            row = {key: item[key] for key in ledger_fields}
            row["priority_reasons"] = "; ".join(row["priority_reasons"])
            row["metadata_conflicts"] = "; ".join(row["metadata_conflicts"])
            writer.writerow(row)

    exceptions = {
        "metadata_conflicts": [
            {"pmid": x["pmid"], "fields": x["metadata_conflicts"]}
            for x in decisions
            if x["metadata_conflicts"]
        ],
        "identifier_conflicts": [
            {"pmid": x["pmid"], "status": "DOI mismatch; human source review required"}
            for x in decisions
            if not x["identifiers_verified"]
        ],
        "correction_review_pending": [
            {
                "pmid": x["pmid"],
                "links": x["correction_links"],
                "source": x["integrity_source_url"],
            }
            for x in decisions
            if x["integrity_action"] == "REVIEW_CORRECTION"
        ],
        "integrity_blocked": [
            {
                "pmid": x["pmid"],
                "links": x["correction_links"],
                "source": x["integrity_source_url"],
            }
            for x in decisions
            if x["decision"] == "BLOCKED_INTEGRITY"
        ],
    }
    (args.output / "screening-exceptions.json").write_text(
        json.dumps(exceptions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
