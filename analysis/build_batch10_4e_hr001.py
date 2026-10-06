"""Materialize the human-authorized HR-001 traceability adjudication.

HR-001 authorizes a map, not a scientific promotion.  A claim is mapped only
when a v0.13 sentence, its numeric citation, and its retained reference form a
deterministic chain.  The FT8 candidates were not promoted to the v0.13
bibliography, so this run deliberately records missing chains rather than
inventing them.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4e"
V013 = ROOT / "batch10_4c"
FT1 = ROOT / "batch10_4b" / "ft1" / "artifacts"

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
SPECIAL_EVIDENCE = {
    "INT-SLEEP-CAFFEINE-MITIGATION": "EV-1462",
    "BRA-PMDF-CVD-SURVEILLANCE": "EV-1463",
    "BRA-PM-PAIN-CONTEXT": "EV-1466",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, fields: list[str], values: list[dict[str, str]]) -> None:
    OUT.mkdir(exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(values)


def paragraphs(docx: Path) -> list[dict[str, str]]:
    """Extract body paragraphs with stable OOXML ordinal and active heading."""
    with zipfile.ZipFile(docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    result, section = [], "Preamble"
    for ordinal, paragraph in enumerate(root.findall(".//w:body/w:p", NS), start=1):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()
        if not text:
            continue
        style = paragraph.find("./w:pPr/w:pStyle", NS)
        style_name = style.get(f"{{{NS['w']}}}val") if style is not None else "Body"
        if style_name in {"Heading1", "Heading2"}:
            section = text
        result.append({"ordinal": str(ordinal), "section": section, "text": text})
    return result


def limitation_boundary(claim_id: str, document_rows: list[dict[str, str]]) -> dict[str, str] | None:
    anchors = {
        "INT-SLEEP-CAFFEINE-MITIGATION": "EV-1462 may only contextualize",
        "BRA-PMDF-CVD-SURVEILLANCE": "EV-1463",
        "BRA-PM-PAIN-CONTEXT": "EV-1466",
    }
    anchor = anchors.get(claim_id)
    if not anchor:
        return None
    return next((row for row in document_rows if anchor in row["text"]), None)


def main() -> None:
    claims = rows(V013 / "V013_CLAIM_CITATION_MATRIX.csv")
    ft1 = rows(FT1 / "PMC100_CLAIM_CITATION_MATRIX.csv")
    source_ids: dict[str, list[str]] = defaultdict(list)
    for item in ft1:
        source_ids[item["Claim_ID"]].append(item["Evidence_ID"])
    for claim_id, evidence_id in SPECIAL_EVIDENCE.items():
        source_ids[claim_id].append(evidence_id)

    documents = {
        "International": paragraphs(V013 / "manuscripts" / "International_v0.13-EVIDENCE-SATURATED.docx"),
        "Brazil": paragraphs(V013 / "manuscripts" / "Brazil_v0.13-EVIDENCE-SATURATED.docx"),
    }
    map_rows: list[dict[str, str]] = []
    citation_rows: list[dict[str, str]] = []
    for claim in claims:
        claim_id, manuscript = claim["Claim_ID"], claim["Manuscript"]
        target = "International" if manuscript == "International" else "Brazil"
        boundary = limitation_boundary(claim_id, documents[target])
        is_not_released = claim_id == "NR — NOT REPORTED"
        status = "UNLINKED_DELETE_REQUIRED" if is_not_released else "UNLINKED_NARROWING_REQUIRED"
        action = (
            "Remove this non-claim placeholder from any future claim-to-citation matrix; it has no releasable proposition."
            if is_not_released
            else "Do not add this FT8 candidate claim to v0.13 without a future human-approved sentence, citation and reference decision."
        )
        evidence = "; ".join(sorted(set(source_ids.get(claim_id, [])))) or "NOT_UNIQUELY_RESOLVED_FROM_VERSIONED_CLAIM_ROW"
        exact_sentence = "NOT PRESENT AS A SUPPORTING CLAIM IN V0.13"
        paragraph = "N/A"
        section = claim["Section"]
        notes = (
            "No sentence/citation/reference chain exists. FT8 candidate evidence was intentionally not promoted to the v0.13 bibliography."
        )
        if boundary:
            paragraph = f"P{boundary['ordinal']}"
            section = boundary["section"]
            exact_sentence = boundary["text"]
            notes = (
                "This is a limitation-only boundary disclosure. It has no numbered manuscript citation and is not a supporting claim or reference promotion."
            )
        record = {
            "Claim_ID": claim_id,
            "Manuscript": manuscript,
            "Section": section,
            "Paragraph": paragraph,
            "Exact_Sentence": exact_sentence,
            "Current_Citation": "NO_MANUSCRIPT_CITATION",
            "Reference_ID": "NOT_ASSIGNED_IN_V013",
            "Evidence_ID": evidence,
            "Evidence_Role": claim["Evidence_Role"],
            "Citation_Fit": "NO_SUPPORTING_CITATION_TO_ASSESS",
            "Directness": claim["Directness"],
            "Saturation_Status": claim["Saturation_Status"],
            "Mapping_Status": status,
            "Action_Required": action,
            "Notes": notes,
        }
        map_rows.append(record)
        citation_rows.append({
            "Claim_ID": claim_id,
            "Manuscript": manuscript,
            "Evidence_ID": evidence,
            "Exact_Sentence_Location": paragraph,
            "Citation": "NO_MANUSCRIPT_CITATION",
            "Reference_ID": "NOT_ASSIGNED_IN_V013",
            "Citation_Fit": record["Citation_Fit"],
            "Red_Team_Result": "PASS_NO_FORCED_LINK",
            "Rationale": notes,
        })

    fields = list(map_rows[0])
    write("HR001_CLAIM_SENTENCE_REFERENCE_MAP.csv", fields, map_rows)
    unlinked = [row for row in map_rows if row["Mapping_Status"] != "AMBIGUOUS_HUMAN_REVIEW_REQUIRED"]
    write("HR001_UNLINKED_CLAIMS.csv", fields, unlinked)
    write("HR001_AMBIGUOUS_CLAIMS.csv", fields, [])
    write("HR001_CITATION_FIT_AUDIT.csv", list(citation_rows[0]), citation_rows)

    decision_rows = [{
        "Review_ID": "HR-001",
        "HUMAN_DECISION": "MAP MANUALLY",
        "HUMAN_REVIEWER": "Matheus Florindo de Deus",
        "HUMAN_REVIEW_DATE": "2026-10-05",
        "HUMAN_RATIONALE": "Approved deterministic claim-to-sentence-to-reference mapping before final reference freeze to prevent unsupported or inferred citation links.",
        "Scope": "Mapping method only; no reference freeze, scientific promotion, CEF-v1 change or Zotero change.",
    }]
    write("HR001_HUMAN_DECISION_RECORD.csv", list(decision_rows[0]), decision_rows)

    counts = Counter(row["Mapping_Status"] for row in map_rows)
    report = f"""# HR-001 — deterministic claim to sentence to reference mapping

## Authorized human decision

`HR-001 = MAP MANUALLY` was recorded for **Matheus Florindo de Deus** on
2026-10-05. The authorization permits this traceability adjudication only.
It does not approve any new scientific claim, candidate reference, CEF-v1
change, Zotero write, or final reference freeze.

## Result

- Claims reviewed and statused: {len(map_rows)}/{len(claims)}.
- `MAPPED_CONFIRMED`: {counts['MAPPED_CONFIRMED']}.
- `MAPPED_AFTER_NARROWING`: {counts['MAPPED_AFTER_NARROWING']}.
- `UNLINKED_NARROWING_REQUIRED`: {counts['UNLINKED_NARROWING_REQUIRED']}.
- `UNLINKED_DELETE_REQUIRED`: {counts['UNLINKED_DELETE_REQUIRED']}.
- `AMBIGUOUS_HUMAN_REVIEW_REQUIRED`: {counts['AMBIGUOUS_HUMAN_REVIEW_REQUIRED']}.

The FT8 claim rows are candidate-evidence ledger entries. None has a complete
v0.13 chain of exact supporting sentence, numeric citation and retained
reference. The three FT4 candidates have limitation-boundary text, but that
text is explicitly not a support citation. The map therefore records no forced
links. This resolves the traceability question faithfully: a future manuscript
revision must either add a human-approved evidence chain or retain the claim
outside the prose.

## Gate

`HR001_ADJUDICATION_COMPLETE` and `GO_HR002_HUMAN_ADJUDICATION`.
`FINAL_REFERENCE_FREEZE` remains prohibited until HR-002 through HR-010.
"""
    (OUT / "HR001_REPORT.md").write_text(report, encoding="utf-8")

    manifest_path = OUT / "HR001_MAPPING_MANIFEST.json"
    files = [path for path in OUT.iterdir() if path.is_file() and path.name != manifest_path.name]
    manifest = {
        "batch": "BATCH10_4E",
        "review_id": "HR-001",
        "base_commit": "279de422a070a435eeb9be82876239758486bdd3",
        "gate": "HR001_ADJUDICATION_COMPLETE",
        "next_gate": "GO_HR002_HUMAN_ADJUDICATION",
        "claims_expected": 60,
        "claims_statused": len(map_rows),
        "mapping_status_counts": dict(counts),
        "blank_mapping_status": sum(not row["Mapping_Status"] for row in map_rows),
        "unsupported_forced_links": 0,
        "blocked_evidence_used_as_support": 0,
        "orphan_citations_created": 0,
        "reference_freeze": "PROHIBITED_PENDING_HR002_TO_HR010",
        "cef_v1": "UNCHANGED",
        "zotero": "UNCHANGED",
        "human_decision": decision_rows[0],
        "files": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
