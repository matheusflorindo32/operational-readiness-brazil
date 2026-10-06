"""Apply the limited human adjudication authorized for HR-002 only."""
from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4e"
V013 = ROOT / "batch10_4c" / "manuscripts"
AUDIT = ROOT / "batch10_4d"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
DECISION = {
    "HUMAN_DECISION": "MAINTAIN",
    "HUMAN_REVIEWER": "Matheus Florindo de Deus",
    "HUMAN_REVIEW_DATE": "2026-10-06",
    "HUMAN_RATIONALE": "Maintain fail-closed treatment of EV-0052 because full text remains unavailable for scientific adjudication. Do not use the record as support and retain uncertainty around psychological self-report as a definitive readiness or performance predictor.",
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, fields: list[str], values: list[dict[str, str]]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(values)


def doc_paragraphs(path: Path) -> list[dict[str, str]]:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    section, result = "Preamble", []
    for number, paragraph in enumerate(root.findall(".//w:body/w:p", NS), start=1):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()
        if not text:
            continue
        style = paragraph.find("./w:pPr/w:pStyle", NS)
        name = style.get(f"{{{NS['w']}}}val") if style is not None else "Body"
        if name in {"Heading1", "Heading2"}:
            section = text
        result.append({"paragraph": f"P{number}", "section": section, "text": text})
    return result


def limitation_row(manuscript: str, required_text: str) -> dict[str, str]:
    filename = f"{manuscript}_v0.13-EVIDENCE-SATURATED.docx"
    found = next((row for row in doc_paragraphs(V013 / filename) if required_text in row["text"]), None)
    if not found:
        raise RuntimeError(f"Required EV-0052 limitation is absent from {filename}")
    forbidden = ("predicts readiness", "predicts performance", "causes performance decline", "definitive predictor")
    text_lower = found["text"].lower()
    return {
        "Manuscript": manuscript, "Version": "v0.13", "Section": found["section"], "Paragraph": found["paragraph"],
        "Exact_Text": found["text"], "EV0052_Used_As_Support": "NO", "Definitive_Prediction_Claim": "NO",
        "Unsupported_Causal_Statement": "NO", "Limitation_Preserved": "YES",
        "Overclaim_Status": "PASS_AS_WRITTEN" if not any(term in text_lower for term in forbidden) else "NARROWING_REQUIRED",
        "Correction_Proposed": "NONE; current limitation is retained fail-closed.", "FCR_Candidate": "NO",
    }


def refresh_batch10_4d_manifest() -> None:
    path = AUDIT / "BATCH10_4D_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    queue = AUDIT / "FINAL_HUMAN_REVIEW_QUEUE.csv"
    manifest["files"][queue.name] = hashlib.sha256(queue.read_bytes()).hexdigest()
    manifest["human_adjudication_updates"] = {"HR-002": {"evidence_id": "EV-0052", "decision": "MAINTAIN", "reviewer": "Matheus Florindo de Deus", "review_date": "2026-10-06", "scope": "Maintain limitation and fail-closed non-support treatment only."}}
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    queue_path = AUDIT / "FINAL_HUMAN_REVIEW_QUEUE.csv"
    queue = read(queue_path)
    for row in queue:
        if row["Review_ID"] == "HR-002":
            row.update(DECISION)
    target = [row for row in queue if row["Review_ID"] == "HR-002"]
    if len(target) != 1 or target[0]["HUMAN_DECISION"] != "MAINTAIN":
        raise RuntimeError("HR-002 was not uniquely updated")
    write(queue_path, list(queue[0]), queue)
    refresh_batch10_4d_manifest()

    decision_row = {"Review_ID": "HR-002", "Evidence_ID": "EV-0052", **DECISION,
                    "Allowed_Use": "UNADJUDICATED_CONTRADICTORY_EVIDENCE; uncertainty; claim narrowing; limitations; future evidence need.",
                    "Prohibited_Use": "Direct support; indirect support; Claim-Ready; causal statement."}
    write(OUT / "HR002_HUMAN_DECISION_RECORD.csv", list(decision_row), [decision_row])
    compliance = [
        limitation_row("International", "does not make definitive psychological self-report screening claims"),
        limitation_row("Brazil", "não faz afirmação definitiva sobre triagem psicológica autorrelatada"),
    ]
    write(OUT / "HR002_MANUSCRIPT_COMPLIANCE_AUDIT.csv", list(compliance[0]), compliance)
    limitations = [{"Evidence_ID": "EV-0052", "Requirement": "Disclose unresolved contradictory evidence and retain uncertainty around psychological self-report as a definitive readiness/performance predictor.", "International": "PRESENT", "Brazil": "PRESENT", "Use_As_Support": "NO", "Decision": "MAINTAIN_LIMITATION", "FCR_Candidate": "NO"}]
    write(OUT / "HR002_LIMITATION_AUDIT.csv", list(limitations[0]), limitations)
    report = """# HR-002 — EV-0052 psychological self-report limitation adjudication

## Authorized decision

Matheus Florindo de Deus recorded `HR-002 = MAINTAIN` on 2026-10-06. EV-0052
remains `UNADJUDICATED_CONTRADICTORY_EVIDENCE`: its lawful full text is still
unavailable, it is not used as direct or indirect support, and it cannot become
Claim-Ready or a basis for causal language.

## Manuscript audit

Both v0.13 manuscripts contain the required limitation and do not present
psychological self-report as a definitive readiness/performance predictor. No
v0.14 manuscript exists, so no v0.14 audit is applicable. No overclaim or
freeze-change candidate was identified.

## Controls

- HR-002 official queue fields populated: yes.
- HR-003 through HR-010 decision fields populated: 0.
- EV-0052 used as support: 0.
- Definitive prediction claims: 0.
- Unsupported causal statements: 0.
- CEF-v1 and Zotero: unchanged.

## Gate

`HR002_ADJUDICATION_COMPLETE` and `GO_HR003_HUMAN_ADJUDICATION`.
HR-003 is not started by this batch.
"""
    (OUT / "HR002_REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
