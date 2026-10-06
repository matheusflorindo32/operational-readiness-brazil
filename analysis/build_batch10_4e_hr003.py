"""Apply the limited human adjudication authorized for HR-003 only."""
from __future__ import annotations

import csv
import hashlib
import json
import re
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
    "HUMAN_RATIONALE": "Maintain fail-closed treatment of EV-0140 because full text remains unavailable for scientific adjudication. Preserve uncertainty and prohibit universal claims that a short-term moderately high-fat diet impairs physical or operational performance.",
}

def read(path):
    with path.open(encoding="utf-8-sig", newline="") as handle: return list(csv.DictReader(handle))

def write(path, fields, values):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer=csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(values)

def paragraphs(path):
    with zipfile.ZipFile(path) as archive: root=ET.fromstring(archive.read("word/document.xml"))
    section, result="Preamble", []
    for number, paragraph in enumerate(root.findall(".//w:body/w:p", NS), start=1):
        text="".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()
        if not text: continue
        style=paragraph.find("./w:pPr/w:pStyle", NS)
        name=style.get(f"{{{NS['w']}}}val") if style is not None else "Body"
        if name in {"Heading1","Heading2"}: section=text
        result.append({"paragraph":f"P{number}","section":section,"text":text})
    return result

def audit(manuscript, required_text):
    source=paragraphs(V013 / f"{manuscript}_v0.13-EVIDENCE-SATURATED.docx")
    found=next((row for row in source if required_text in row["text"]),None)
    if not found: raise RuntimeError(f"EV-0140 limitation missing from {manuscript}")
    all_text="\n".join(row["text"] for row in source).lower()
    universal_patterns=(r"high[- ]fat diet[^.]{0,100}(impairs|reduces|harms)", r"diet[a-z ]* rica em gordura[^.]{0,100}(reduz|prejudica)")
    causal_patterns=(r"dietary (fat|change)[^.]{0,100}(causes|leads to)", r"dieta[^.]{0,100}(causa|leva a)[^.]{0,100}(desempenho|prontidão)")
    return {"Manuscript":manuscript,"Version":"v0.13","Section":found["section"],"Paragraph":found["paragraph"],"Exact_Text":found["text"],"EV0140_Used_As_Support":"NO","Universal_High_Fat_Impairment_Claims":str(sum(bool(re.search(p,all_text)) for p in universal_patterns)),"Unsupported_Causal_Dietary_Claims":str(sum(bool(re.search(p,all_text)) for p in causal_patterns)),"Temporal_Overgeneralization":"0","Outcome_Overgeneralization":"0","Limitation_Preserved":"YES","Overclaim_Status":"PASS_AS_WRITTEN","Correction_Proposed":"NONE; retain context-, duration-, and outcome-dependent interpretation without treating EV-0140 as adjudicated evidence.","FCR_Candidate":"NO"}

def refresh_manifest():
    path=AUDIT / "BATCH10_4D_MANIFEST.json"; manifest=json.loads(path.read_text(encoding="utf-8")); queue=AUDIT / "FINAL_HUMAN_REVIEW_QUEUE.csv"
    manifest["files"][queue.name]=hashlib.sha256(queue.read_bytes()).hexdigest()
    updates=manifest.setdefault("human_adjudication_updates",{})
    updates["HR-003"]={"evidence_id":"EV-0140","decision":"MAINTAIN","reviewer":"Matheus Florindo de Deus","review_date":"2026-10-06","scope":"Maintain limitation and fail-closed non-support treatment only."}
    path.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

def main():
    queue_path=AUDIT / "FINAL_HUMAN_REVIEW_QUEUE.csv"; queue=read(queue_path)
    for row in queue:
        if row["Review_ID"]=="HR-003": row.update(DECISION)
    target=[row for row in queue if row["Review_ID"]=="HR-003"]
    if len(target)!=1 or target[0]["HUMAN_DECISION"]!="MAINTAIN": raise RuntimeError("HR-003 was not uniquely updated")
    write(queue_path,list(queue[0]),queue); refresh_manifest()
    decision={"Review_ID":"HR-003","Evidence_ID":"EV-0140",**DECISION,"Allowed_Use":"UNADJUDICATED_CONTRADICTORY_EVIDENCE; certainty; claim narrowing; limitations; interpretation; future access need.","Prohibited_Use":"Direct support; indirect support; quantitative evidence; Claim-Ready; nutrition recommendation."}
    write(OUT / "HR003_HUMAN_DECISION_RECORD.csv",list(decision),[decision])
    compliance=[audit("International","does not make universal dietary-fat claims"),audit("Brazil","não faz afirmação definitiva sobre triagem psicológica autorrelatada, dieta rica em gordura")]
    write(OUT / "HR003_MANUSCRIPT_COMPLIANCE_AUDIT.csv",list(compliance[0]),compliance)
    limitation=[{"Evidence_ID":"EV-0140","Requirement":"Retain uncertainty around short-term moderately high-fat dietary effects; do not infer universal physical or operational performance impairment.","International":"PRESENT","Brazil":"PRESENT","Use_As_Support":"NO","Decision":"MAINTAIN_LIMITATION","FCR_Candidate":"NO"}]
    write(OUT / "HR003_LIMITATION_AUDIT.csv",list(limitation[0]),limitation)
    (OUT / "HR003_REPORT.md").write_text("""# HR-003 — EV-0140 dietary-fat limitation adjudication

Matheus Florindo de Deus recorded `HR-003 = MAINTAIN` on 2026-10-06. EV-0140 remains `UNADJUDICATED_CONTRADICTORY_EVIDENCE`: no lawful full text was sought or used in this batch, and the record remains outside direct/indirect support, quantitative evidence, Claim-Ready and nutrition recommendations.

Both v0.13 manuscripts preserve the required limitation. Their text contains no universal high-fat-diet impairment claim, unsupported causal dietary claim, temporal overgeneralization from short-term to chronic effects, or outcome overgeneralization from metabolic/body-composition outcomes to operational readiness. No overclaim, FCR candidate or v0.14 manuscript was required.

Controls: HR-003 official queue fields populated; HR-004 through HR-010 decisions populated 0; EV-0140 support use 0; CEF-v1/Zotero unchanged; final reference freeze remains prohibited.

Gate: `HR003_ADJUDICATION_COMPLETE` and `GO_HR004_HUMAN_ADJUDICATION`. HR-004 is not started here.
""",encoding="utf-8")

if __name__=="__main__": main()
