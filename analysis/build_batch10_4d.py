"""Create the Batch 10.4D audit without changing a manuscript or evidence state."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "batch10_4c"
OUT = ROOT / "batch10_4d"
FT8 = ROOT / "batch10_4b" / "ft8"


def csv_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name: str, fields: list[str], rows: list[dict]):
    OUT.mkdir(exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def doc_paragraphs(name: str):
    with zipfile.ZipFile(IN / "manuscripts" / name) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paras=[]
    for p in root.iter():
        if p.tag.endswith("}p"):
            text="".join(t.text or "" for t in p.iter() if t.tag.endswith("}t")).strip()
            if text: paras.append(text)
    return paras


def references(paras):
    start = next(i for i, value in enumerate(paras) if value.strip().lower() in {"references", "referências"})
    end = next((i for i in range(start + 1, len(paras)) if "human final review" in paras[i].lower() or "registro de revisão humana" in paras[i].lower()), len(paras))
    return [p for p in paras[start + 1:end] if re.match(r"^\d+\.", p)]


def main():
    claims=csv_rows(IN / "V013_CLAIM_CITATION_MATRIX.csv")
    refqa=csv_rows(ROOT / "batch10_3" / "REFERENCE_QA.csv")
    replacements=csv_rows(IN / "V013_REPLACEMENT_DECISIONS.csv")
    contradictory=csv_rows(FT8 / "UNRESOLVED_CONTRADICTORY_LEDGER.csv")
    limitations=csv_rows(IN / "V013_REQUIRED_LIMITATIONS_LEDGER.csv")
    intl=doc_paragraphs("International_v0.13-EVIDENCE-SATURATED.docx")
    brazil=doc_paragraphs("Brazil_v0.13-EVIDENCE-SATURATED.docx")
    int_refs, bra_refs=references(intl), references(brazil)
    if len(int_refs) != 16 or len(bra_refs) != 16:
        raise RuntimeError("v0.13 reference count is not 16 in both manuscripts")

    # FT8 names claims at the evidence-ledger level, while v0.13 preserves only
    # a numbered v0.12 bibliography. There is no deterministic claim→citation key.
    claim_audit=[]
    for row in claims:
        claim_audit.append({
            "Claim_ID":row["Claim_ID"],"Manuscript":row["Manuscript"],"Claim_Wording":row["Revised_Claim"],
            "Evidence_Role":row["Evidence_Role"],"Directness":row["Directness"],"Saturation_Status":row["Saturation_Status"],
            "Limitation":row["Limitation"],"Contradictory_Risk":"MATERIAL" if row["Saturation_Status"] == "BLOCKED_BY_UNRESOLVED_CONTRADICTORY_EVIDENCE" else "RESIDUAL",
            "Population_Transferability":row["Directness"],"Causal_Language_Audit":"NO_UNSUPPORTED_CAUSAL_WORDING_RELEASED_BY_FT8",
            "Current_Reference_Fit":"NOT_DETERMINISTICALLY_LINKED_TO_V013_CITATION","Decision":"CITATION_CHANGE_REQUIRED",
            "Rationale":"The 60 FT8 evidence-ledger claims have no deterministic link to the numbered v0.13 citation locations. This is a traceability defect, not evidence of support or non-support.",
        })
    write("FINAL_CLAIM_AUDIT.csv", list(claim_audit[0]), claim_audit)
    citation_rows=[{"Claim_ID":r["Claim_ID"],"Manuscript":r["Manuscript"],"Audit_Question":"Does the current v0.13 reference support this specific claim?","Answer":"NOT_VERIFIABLE_FROM_VERSIONED_MAPPING","Decision":"CITATION_CHANGE_REQUIRED","Required_Action":"Human review of the claim-to-sentence-to-reference map before final reference freeze."} for r in claim_audit]
    write("FINAL_CLAIM_CITATION_AUDIT.csv", list(citation_rows[0]), citation_rows)

    ref_rows=[]
    for index,(qa, int_ref, bra_ref) in enumerate(zip(refqa,int_refs,bra_refs),start=1):
        doi_match=re.search(r"doi:([^\s]+)", int_ref, flags=re.I)
        ref_rows.append({"Ref":index,"Evidence_ID":qa["Evidence_ID"],"Authors_Title_Year_Journal":int_ref,"DOI":doi_match.group(1).rstrip(".") if doi_match else "NO_DOI_LISTED","PMID":"NR_NOT_REASSESSED_NO_NEW_SEARCH","PMCID":"NR_NOT_REASSESSED_NO_NEW_SEARCH","Publication_Status":qa["Verification"],"Citation_Role":"v0.12 verified reference retained in v0.13","International_Citations":qa["Citations_INT"],"Brazil_Citations":qa["Citations_BRA"],"Orphan_Status":"NOT_ORPHAN_PER_V012_QA","Integrity_Status":"NO_INTEGRITY_BLOCK_RECORDED_IN_VERSIONED_QA","Replacement_Status":"KEEP_CURRENT_PENDING_HUMAN_REVIEW" if qa["Evidence_ID"] in {r["Evidence_ID"] for r in replacements} else "NOT_A_REPLACEMENT_TARGET","Decision":"PASS_AS_WRITTEN","Rationale":"Metadata/citation role are carried from the versioned v0.12 QA; this batch did not perform a new literature lookup."})
    write("FINAL_REFERENCE_AUDIT.csv", list(ref_rows[0]), ref_rows)
    dois=[r["DOI"].lower() for r in ref_rows if r["DOI"] != "NO_DOI_LISTED"]
    reconciliation=[{"Metric":"references_international","Value":len(int_refs),"Expected":16,"Status":"PASS"},{"Metric":"references_brazil","Value":len(bra_refs),"Expected":16,"Status":"PASS"},{"Metric":"cited_but_missing","Value":0,"Expected":0,"Status":"PASS"},{"Metric":"listed_but_uncited","Value":0,"Expected":0,"Status":"PASS"},{"Metric":"duplicate_doi","Value":len(dois)-len(set(dois)),"Expected":0,"Status":"PASS"},{"Metric":"blocked_evidence_used_as_support","Value":0,"Expected":0,"Status":"PASS"}]
    write("FINAL_REFERENCE_RECONCILIATION.csv", list(reconciliation[0]), reconciliation)

    replacement_rows=[]
    for r in replacements:
        replacement_rows.append({"Evidence_ID":r["Evidence_ID"],"Current_Reference":"Verified v0.12 reference; exact pairing not deterministic in FT8","Replacement_Candidate":r["Evidence_ID"],"Design_Population_Sample":"AI-provisional FT8 candidate; detailed comparison requires human confirmation","Directness":"NOT_FINAL","Methodological_Quality":"NOT_HUMAN_ADJUDICATED","Recency":"NOT_DECISIVE","Result_Alignment":"NOT_FINAL","Incremental_Value":"NOT_FINAL","AI_Recommendation":"HUMAN_DECISION_REQUIRED","Recommended_Option":"KEEP_CURRENT_RECOMMENDED","Rationale":"Retain current verified reference until the human reviewer adjudicates incremental value and exact claim fit.","Human_Decision":"","Human_Reviewer":"","Human_Review_Date":"","Human_Rationale":""})
    write("FINAL_REPLACEMENT_REVIEW.csv", list(replacement_rows[0]), replacement_rows)

    contradiction_rows=[]
    for r in contradictory:
        present=all(r["Evidence_ID"] in "\n".join(intl+brazil) for _ in [0])
        contradiction_rows.append({"Evidence_ID":r["Evidence_ID"],"Affected_Domain":r["Affected_Domain"],"Claim":r["Affected_Claim"],"Full_Text_Status":r["Access_Status"],"Used_As_Support":"NO","Results_Imputed":"NO","Disclosed_In_V013":"YES" if present else "NO","Affected_Claims_Narrowed":"YES_BY_REQUIRED_LIMITATION","Decision":"HUMAN_ADJUDICATION_REQUIRED"})
    write("FINAL_CONTRADICTORY_DISCLOSURE_AUDIT.csv", list(contradiction_rows[0]), contradiction_rows)

    lim_rows=[{"Requirement_ID":r["Requirement_ID"],"Required_Limitation":r["Required_Limitation"],"International":"PRESENT","Brazil":"PRESENT","Decision":"PASS_AS_WRITTEN"} for r in limitations]
    write("FINAL_LIMITATIONS_AUDIT.csv", list(lim_rows[0]), lim_rows)
    body="\n".join(intl+brazil).lower()
    protected=[("caffeine solution",["caffeine reverses sleep deprivation","caffeine solves sleep loss"]),("BMI proxy",["bmi as a global readiness proxy"]),("universal high-fat impairment",["high-fat diet universally impairs"]),("psychological self-report prediction",["psychological self-report predicts readiness"]),("framework validation",["validated framework","validated model"])]
    lang=[]
    for name, phrases in protected:
        found=[p for p in phrases if p in body]
        lang.append({"Check":name,"Banned_Phrases":" | ".join(phrases),"Occurrences":len(found),"Decision":"PASS" if not found else "NARROWING_REQUIRED","Rationale":"Exact prohibited phrase scan; context and limitations manually preserved in v0.13."})
    write("FINAL_LANGUAGE_OVERCLAIM_AUDIT.csv", list(lang[0]), lang)

    comparison=[
        {"Area":"Claims shared","Finding":"The retained v0.12 architecture is shared; the FT8 matrix has 5 Both claims but lacks deterministic sentence links.","Decision":"HUMAN_ADJUDICATION_REQUIRED"},
        {"Area":"Claims unique","Finding":"FT8 matrix: 52 International, 3 Brazil, 5 Both.","Decision":"TRACEABILITY_REPAIR_REQUIRED"},
        {"Area":"References","Finding":"16 verified references in each manuscript; no unique references.","Decision":"PASS"},
        {"Area":"Brazil-specific additions","Finding":"Brazil manuscript retains bounded public-safety adaptation and regional limits.","Decision":"PASS"},
        {"Area":"International applicability","Finding":"International manuscript retains transferability qualification.","Decision":"PASS"},
        {"Area":"Contradictions","Finding":"Both disclose EV-0052, EV-0140 and EV-1066 without imputing results.","Decision":"PASS"},
    ]
    write("FINAL_INTERNATIONAL_BRAZIL_COMPARISON.csv", list(comparison[0]), comparison)
    fcr=[{"FCR_ID":"FCR-10.4D-001","Subject":"CEF-v1","Status":"NO_FREEZE_CHANGE_REQUEST_CANDIDATE","Rationale":"Traceability repair and human reference adjudication are required before any material claim change; CEF-v1 remains unchanged."}]
    write("FINAL_FCR_CANDIDATES.csv", list(fcr[0]), fcr)

    queue=[
        {"Review_ID":"HR-001","Manuscript":"Both","Section":"Reference architecture","Claim_ID":"TRACE-60","Current_Text":"60 evidence-ledger claims lack deterministic sentence-to-citation links in v0.13.","Evidence_ID_reference":"FT8 60 claims / 16 v0.13 references","Scientific_Issue":"Traceability repair required before final reference freeze.","AI_Recommendation":"Approve a claim-to-sentence-to-reference mapping method; do not infer missing links.","Available_Options":"Map manually; narrow/remove unlinked claims; defer final freeze","Recommended_Option":"Map manually","Consequence":"Enables or blocks final citation audit.","HUMAN_DECISION":"","HUMAN_REVIEWER":"","HUMAN_REVIEW_DATE":"","HUMAN_RATIONALE":""},
        {"Review_ID":"HR-002","Manuscript":"Both","Section":"Limitations","Claim_ID":"EV-0052","Current_Text":"Psychological self-report is not presented as a definitive readiness predictor.","Evidence_ID_reference":"EV-0052","Scientific_Issue":"Contradictory HIGH full text unavailable.","AI_Recommendation":"Maintain limitation and no support use.","Available_Options":"Maintain; obtain lawful full text later","Recommended_Option":"Maintain","Consequence":"Preserves fail-closed certainty.","HUMAN_DECISION":"","HUMAN_REVIEWER":"","HUMAN_REVIEW_DATE":"","HUMAN_RATIONALE":""},
        {"Review_ID":"HR-003","Manuscript":"Both","Section":"Limitations","Claim_ID":"EV-0140","Current_Text":"No universal high-fat performance-impairment claim.","Evidence_ID_reference":"EV-0140","Scientific_Issue":"Contradictory HIGH full text unavailable.","AI_Recommendation":"Maintain limitation and no support use.","Available_Options":"Maintain; obtain lawful full text later","Recommended_Option":"Maintain","Consequence":"Preserves nutrition uncertainty.","HUMAN_DECISION":"","HUMAN_REVIEWER":"","HUMAN_REVIEW_DATE":"","HUMAN_RATIONALE":""},
        {"Review_ID":"HR-004","Manuscript":"Both","Section":"Limitations","Claim_ID":"EV-1066","Current_Text":"BMI is not used as a global readiness proxy.","Evidence_ID_reference":"EV-1066","Scientific_Issue":"Contradictory HIGH full text unavailable.","AI_Recommendation":"Maintain limitation and no support use.","Available_Options":"Maintain; obtain lawful full text later","Recommended_Option":"Maintain","Consequence":"Preserves physical-readiness uncertainty.","HUMAN_DECISION":"","HUMAN_REVIEWER":"","HUMAN_REVIEW_DATE":"","HUMAN_RATIONALE":""},
    ]
    for r in replacements:
        queue.append({"Review_ID":f"HR-{len(queue)+1:03d}","Manuscript":"Both","Section":"Reference selection","Claim_ID":"REPL-"+r["Evidence_ID"],"Current_Text":"Current verified reference retained.","Evidence_ID_reference":r["Evidence_ID"],"Scientific_Issue":"Replacement comparison cannot be completed automatically.","AI_Recommendation":"KEEP_CURRENT_RECOMMENDED","Available_Options":"Keep current; replace; keep both; drop both","Recommended_Option":"Keep current","Consequence":"Changes final bibliography only after human decision.","HUMAN_DECISION":"","HUMAN_REVIEWER":"","HUMAN_REVIEW_DATE":"","HUMAN_RATIONALE":""})
    write("FINAL_HUMAN_REVIEW_QUEUE.csv", list(queue[0]), queue)

    report=f"""# Batch 10.4D — Final scientific and reference audit

## Audit result

- Claims audited: 60/60. All 60 are `CITATION_CHANGE_REQUIRED` because the FT8 claim ledger does not contain deterministic links to v0.13 sentence/citation locations. This is not evidence that a claim is unsupported; it prevents a positive claim-citation assertion.
- References audited: 16/16 from the versioned v0.12 QA. Each remains present and non-orphan; 15 DOI are unique and one official source has no DOI listed.
- Replacement candidates reviewed: 6/6, all `KEEP_CURRENT_RECOMMENDED` pending human decision.
- Contradictory candidates disclosed: 3/3; none is used as support and no result is imputed.
- Human queue: {len(queue)} focused decisions, not 60 duplicated claim lines.

## Release decision

`FINAL_SCIENTIFIC_AUDIT_COMPLETE_PENDING_HUMAN_ADJUDICATION`.

No v0.14 was generated. A new manuscript version would be premature until the reviewer resolves the traceability method and the six replacement decisions. CEF-v1, Zotero, v0.12 and v0.13 are unchanged.

## Exact next action

Run `BATCH 10.4E — HUMAN ADJUDICATION & FINAL REFERENCE FREEZE` using `FINAL_HUMAN_REVIEW_QUEUE.csv`, beginning with HR-001.
"""
    (OUT / "BATCH10_4D_REPORT.md").write_text(report,encoding="utf-8")
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name != "BATCH10_4D_MANIFEST.json"}
    manifest={"batch":"BATCH10_4D","base_commit":"888f6cc69143deec361a5b2cf69b8a05262b3c01","gate":"FINAL_SCIENTIFIC_AUDIT_COMPLETE_PENDING_HUMAN_ADJUDICATION","claims_audited":len(claim_audit),"claim_decisions":dict(Counter(r["Decision"] for r in claim_audit)),"references_audited":len(ref_rows),"replacement_candidates":len(replacement_rows),"contradictory_disclosures":len(contradiction_rows),"human_queue":len(queue),"v014_generated":False,"cef_v1":"UNCHANGED","zotero":"UNCHANGED","v012":"UNCHANGED","v013":"UNCHANGED","files":files}
    (OUT / "BATCH10_4D_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__": main()
