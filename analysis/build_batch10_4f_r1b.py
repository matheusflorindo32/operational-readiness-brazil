"""Adjudicate v0.13 scientific sentences conservatively from DOCX citation runs.

This is a traceability audit, not a semantic literature review.  It only treats a
number as linked when its superscript run is structurally attached to the same
sentence.  Because the versioned authorities do not contain sentence-to-result
evidence mappings, every active scientific claim remains an explicit corrective
action rather than receiving an inferred support rating.
"""
import csv, hashlib, json, re, zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4f_r1b"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def write_csv(path, fields, rows):
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def norm(value):
    return re.sub(r"\s+", " ", value or "").strip()

def parse_numbers(value):
    numbers=[]
    for token in re.findall(r"\d+(?:[–-]\d+)?", value or ""):
        ends=token.replace("–", "-").split("-")
        numbers.extend(range(int(ends[0]), int(ends[-1])+1))
    return numbers

def anchored_sentences(name):
    """Return paragraph/sentence text with only anchors inside its sentence span."""
    path=ROOT/"batch10_4c"/"manuscripts"/f"{name}_v0.13-EVIDENCE-SATURATED.docx"
    root=E.fromstring(zipfile.ZipFile(path).read("word/document.xml")); out=[]
    for pi, paragraph in enumerate(root.findall(".//w:body/w:p", NS), 1):
        pieces=[]; anchors=[]; cursor=0
        for run in paragraph.findall("./w:r", NS):
            text="".join(t.text or "" for t in run.findall(".//w:t", NS))
            vertical=run.find("./w:rPr/w:vertAlign", NS)
            is_super=vertical is not None and vertical.get("{"+NS["w"]+"}val")=="superscript"
            if is_super and re.fullmatch(r"[0-9,–\- ]+", text or ""):
                anchors.append((cursor, text))
            else:
                pieces.append(text); cursor += len(text)
        plain="".join(pieces).strip()
        if not plain: continue
        for match in re.finditer(r".*?(?:[.!?](?=\s|$)|$)", plain):
            sentence=match.group(0).strip()
            if not sentence: continue
            start=match.start()+len(match.group(0))-len(match.group(0).lstrip())
            end=match.start()+len(match.group(0).rstrip())
            # Word places a superscript immediately after terminal punctuation,
            # occasionally after a preserved space. Attach only that local run to
            # the preceding sentence; never broadcast a paragraph anchor.
            own=[text for pos,text in anchors if start <= pos <= end + 3]
            out.append((f"P{pi}", norm(sentence), ";".join(own), ";".join(map(str, sum((parse_numbers(x) for x in own), [])))))
    return out

def is_protected(text):
    low=text.lower()
    return any(term in low for term in [
        "body mass index", "bmi", "índice de massa corporal", "psychological self-report",
        "autorrelat", "high-fat", "rica em gordura", "caffeine", "cafeína", "validat",
        "score", "causal", "causally", "causalmente"
    ])

def main():
    source=read_csv(ROOT/"batch10_4f_r1"/"SCIENTIFIC_SENTENCE_CLASSIFICATION.csv")
    scientific=[r for r in source if r["Classification"]=="SCIENTIFIC_CLAIM_REQUIRES_SUPPORT"]
    refs=read_csv(ROOT/"batch10_4d"/"FINAL_REFERENCE_AUDIT.csv")
    by_ref={r["Ref"]:r for r in refs}
    # Pair sentence positions within each Word paragraph.  The original R1 inventory
    # includes superscript glyphs in its visible text while this parser strips those
    # glyphs into anchors, so text equality would be a false negative.
    recovered=defaultdict(dict)
    for manuscript in ("International", "Brazil"):
        parsed=defaultdict(list)
        for pid, text, rendered, nums in anchored_sentences(manuscript):
            parsed[pid].append({"rendered":rendered,"numbers":nums})
        positions=defaultdict(int)
        for source_row in [x for x in source if x["Manuscript"]==manuscript]:
            pid=source_row["Paragraph_ID"]
            pos=positions[pid]; positions[pid] += 1
            recovered[manuscript][source_row["Sentence_ID"]] = parsed[pid][pos] if pos < len(parsed[pid]) else {"rendered":"","numbers":""}

    fields=["Sentence_ID","Manuscript","Section","Paragraph_ID","Exact_Sentence","Rendered_Citation","Reference_Number","Reference_ID","Evidence_ID","Evidence_Role","Support_Fit","Population_Fit","Exposure_Fit","Outcome_Fit","Design_Fit","Certainty","Composite_Support","Scientific_Issue","Final_Disposition","Proposed_Action","Proposed_Narrowed_Text"]
    adjudications=[]; fit_rows=[]; narrowing=[]; citation_actions=[]; deletes=[]; protected=[]
    for row in scientific:
        found=recovered[row["Manuscript"]].get(row["Sentence_ID"], {"rendered":"","numbers":""})
        nums=[x for x in found["numbers"].split(";") if x]
        evs=[by_ref.get(n,{}).get("Evidence_ID", "") for n in nums]
        refids=[n for n in nums]
        # The current authoritative audit expressly reports that exact claim-to-reference support was not verified.
        if nums:
            support="INSUFFICIENT_SUPPORT"
            issue="Anchor and bibliography identity recovered; no versioned result-level sentence-to-evidence support mapping exists."
        else:
            support="INSUFFICIENT_SUPPORT"
            issue="No structurally attached rendered citation anchor was recovered for this scientific claim."
        disposition="CITATION_CHANGE_REQUIRED"
        action="Perform source-level human scientific review; retain only after a reference-specific result, location, and fit are documented."
        proposed=""
        if is_protected(row["Exact_Sentence"]):
            disposition="NARROWING_REQUIRED"
            action="Apply protected-claim limitation before retention; do not use unresolved contradictory evidence as support."
            proposed="Use bounded, non-causal, population-specific wording and retain the documented limitation."
            narrowing.append(dict(row, Rendered_Citation=found["rendered"], Proposed_Action=action, Proposed_Narrowed_Text=proposed))
            protected.append({"Sentence_ID":row["Sentence_ID"],"Exact_Sentence":row["Exact_Sentence"],"Protected_Rule":"Protected claim / causal or validation language review","Finding":"NARROWING_REQUIRED","Action":action})
        elif not nums:
            citation_actions.append(dict(row, Rendered_Citation="", Reference_Number="", Evidence_ID="", Issue=issue, Action=action))
        record={
            "Sentence_ID":row["Sentence_ID"],"Manuscript":row["Manuscript"],"Section":row["Section"],"Paragraph_ID":row["Paragraph_ID"],"Exact_Sentence":row["Exact_Sentence"],
            "Rendered_Citation":found["rendered"],"Reference_Number":";".join(refids),"Reference_ID":";".join(refids),"Evidence_ID":";".join(evs),"Evidence_Role":"VERSIONED_V013_REFERENCE_ONLY",
            "Support_Fit":support,"Population_Fit":"NOT_VERIFIABLE_WITHOUT_SOURCE_LEVEL_REVIEW","Exposure_Fit":"NOT_VERIFIABLE_WITHOUT_SOURCE_LEVEL_REVIEW","Outcome_Fit":"NOT_VERIFIABLE_WITHOUT_SOURCE_LEVEL_REVIEW","Design_Fit":"NOT_VERIFIABLE_WITHOUT_SOURCE_LEVEL_REVIEW","Certainty":"NOT_REASSESSED_AT_SENTENCE_LEVEL","Composite_Support":"YES" if len(nums)>1 else "NO","Scientific_Issue":issue,"Final_Disposition":disposition,"Proposed_Action":action,"Proposed_Narrowed_Text":proposed}
        adjudications.append(record)
        for n,e in zip(refids,evs): fit_rows.append({"Sentence_ID":row["Sentence_ID"],"Manuscript":row["Manuscript"],"Exact_Sentence":row["Exact_Sentence"],"Reference_Number":n,"Evidence_ID":e,"Support_Fit":support,"Fit_Rationale":issue,"Forced_Link":"NO"})

    ref_use=[]
    for r in refs:
        uses=[x for x in fit_rows if x["Reference_Number"]==r["Ref"]]
        ref_use.append({"Reference_Number":r["Ref"],"Evidence_ID":r["Evidence_ID"],"Reference":r["Authors_Title_Year_Journal"],"Actual_Sentence_Uses":len(uses),"Defensible_Support_Uses":0,"Use_Class":"UNUSED" if not uses else "ALL_USES_REQUIRE_REVIEW","Rationale":"No source-level sentence support was inferred from bibliographic identity alone."})
    orphan=[dict(x, Preliminary_Orphan="YES" if x["Actual_Sentence_Uses"]=="0" else "PENDING_SOURCE_LEVEL_REVIEW") for x in ref_use]
    non_evid=[r for r in source if r["Classification"] in {"METHOD_STATEMENT","LIMITATION_STATEMENT","FRAMEWORK_PROPOSAL"}]
    abstract=[dict(r, Audit="SCIENTIFIC_SENTENCE_REQUIRES_SAME_OR_STRONGER_BODY_SUPPORT", Result="CITATION_CHANGE_REQUIRED" if r["Final_Disposition"]=="CITATION_CHANGE_REQUIRED" else r["Final_Disposition"]) for r in adjudications if r["Section"].lower()=="abstract"]
    conclusion=[dict(r, Audit="CONCLUSION_CANNOT_EXCEED_BODY_SUPPORT", Result="CITATION_CHANGE_REQUIRED" if r["Final_Disposition"]=="CITATION_CHANGE_REQUIRED" else r["Final_Disposition"]) for r in adjudications if r["Section"].lower() in {"conclusion","conclusão"}]
    causal=[{"Sentence_ID":r["Sentence_ID"],"Exact_Sentence":r["Exact_Sentence"],"Finding":"REQUIRES_SOURCE_LEVEL_REVIEW","Action":r["Proposed_Action"]} for r in adjudications if re.search(r"\b(caus|predict|preven|improv|reduz|increase|decrease)\w*",r["Exact_Sentence"],re.I)]
    transfer=[{"Sentence_ID":r["Sentence_ID"],"Manuscript":r["Manuscript"],"Exact_Sentence":r["Exact_Sentence"],"Finding":"POPULATION_TRANSFERABILITY_NOT_VERIFIED","Action":r["Proposed_Action"]} for r in adjudications]
    fcr=[]
    write_csv(OUT/"SENTENCE_SUPPORT_ADJUDICATION.csv",fields,adjudications)
    write_csv(OUT/"SENTENCE_REFERENCE_FIT_MATRIX.csv",["Sentence_ID","Manuscript","Exact_Sentence","Reference_Number","Evidence_ID","Support_Fit","Fit_Rationale","Forced_Link"],fit_rows)
    write_csv(OUT/"NARROWING_ACTIONS.csv",["Sentence_ID","Manuscript","Section","Paragraph_ID","Exact_Sentence","Rendered_Citation","Proposed_Action","Proposed_Narrowed_Text"],narrowing)
    write_csv(OUT/"CITATION_CHANGE_ACTIONS.csv",["Sentence_ID","Manuscript","Section","Paragraph_ID","Exact_Sentence","Rendered_Citation","Reference_Number","Evidence_ID","Issue","Action"],citation_actions)
    write_csv(OUT/"DELETE_ACTIONS.csv",["Sentence_ID","Exact_Sentence","Reason"],deletes)
    write_csv(OUT/"NON_EVIDENTIARY_SENTENCES.csv",list(non_evid[0]) if non_evid else ["Sentence_ID"],non_evid)
    write_csv(OUT/"REFERENCE_USE_CLASSIFICATION.csv",list(ref_use[0]),ref_use)
    write_csv(OUT/"PRELIMINARY_ORPHAN_REFERENCE_AUDIT.csv",list(orphan[0]),orphan)
    write_csv(OUT/"ABSTRACT_SUPPORT_AUDIT.csv",list(abstract[0]) if abstract else fields+["Audit","Result"],abstract)
    write_csv(OUT/"CONCLUSION_SUPPORT_AUDIT.csv",list(conclusion[0]) if conclusion else fields+["Audit","Result"],conclusion)
    write_csv(OUT/"CAUSAL_LANGUAGE_AUDIT.csv",["Sentence_ID","Exact_Sentence","Finding","Action"],causal)
    write_csv(OUT/"TRANSFERABILITY_AUDIT.csv",["Sentence_ID","Manuscript","Exact_Sentence","Finding","Action"],transfer)
    write_csv(OUT/"PROTECTED_CLAIM_AUDIT.csv",["Sentence_ID","Exact_Sentence","Protected_Rule","Finding","Action"],protected)
    write_csv(OUT/"FCR_CANDIDATES.csv",["Sentence_ID","Status","Rationale"],fcr)
    counts=Counter(r["Final_Disposition"] for r in adjudications)
    support=Counter(r["Support_Fit"] for r in adjudications)
    manifest={"gate":"SENTENCE_SUPPORT_ADJUDICATION_BLOCKED","scientific_sentences_expected":168,"scientific_sentences_adjudicated":len(adjudications),"citation_anchors_structurally_attached":sum(bool(r["Reference_Number"]) for r in adjudications),"forced_links":0,"blocked_evidence_used_as_support":0,"cohort_double_counting":0,"cef_v1_changed":False,"zotero_changed":False,"manuscripts_changed":False,"dispositions":dict(counts),"support_fit":dict(support),"reason":"Versioned authorities recover bibliography identity but do not provide source-result-level sentence support; no thematic inference performed."}
    (OUT/"BATCH10_4F_R1B_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    report=f"""# Batch 10.4F-R1B — sentence support adjudication

## Gate

`SENTENCE_SUPPORT_ADJUDICATION_BLOCKED`

All **{len(adjudications)}/168** scientific sentences were dispositioned without forced links. The DOCX run structure deterministically identifies its static superscript numbers and bibliography entries, but the available versioned authorities do **not** document a result-level sentence-to-reference support relation. Bibliographic identity is therefore not treated as scientific support.

## Counts

- Citation change required: {counts['CITATION_CHANGE_REQUIRED']}
- Narrowing required: {counts['NARROWING_REQUIRED']}
- Source-level direct/partial/contextual support asserted: 0
- Forced links: 0
- Blocked evidence used as support: 0
- CEF-v1/Zotero/manuscripts changed: no/no/no

## Exact blocking condition

Each row in `SENTENCE_SUPPORT_ADJUDICATION.csv` needs a lawful source-level review that records the relevant result, its location, and population/exposure/outcome/design fit. The recovery artifacts provide a deterministic navigation path; they do not supply that appraisal. No reference freeze or manuscript revision is permitted yet.
"""
    (OUT/"BATCH10_4F_R1B_REPORT.md").write_text(report,encoding="utf-8")

if __name__=="__main__": main()
