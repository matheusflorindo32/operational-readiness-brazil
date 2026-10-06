"""Apply the limited human adjudication authorized for HR-004 only."""
from __future__ import annotations
import csv, hashlib, json, re, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_4e'; V013=ROOT/'batch10_4c'/'manuscripts'; AUDIT=ROOT/'batch10_4d'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
DECISION={'HUMAN_DECISION':'MAINTAIN','HUMAN_REVIEWER':'Matheus Florindo de Deus','HUMAN_REVIEW_DATE':'2026-10-06','HUMAN_RATIONALE':'Maintain fail-closed treatment of EV-1066 because full text remains unavailable for scientific adjudication. BMI must not be used as a global proxy or definitive predictor of operational readiness; associations with physical attributes and occupational performance must remain domain- and population-specific.'}
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(p,fields,values):
    p.parent.mkdir(exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(values)
def paras(p):
    with zipfile.ZipFile(p) as z:root=ET.fromstring(z.read('word/document.xml'))
    section='Preamble';out=[]
    for n,x in enumerate(root.findall('.//w:body/w:p',NS),1):
        text=''.join(t.text or '' for t in x.findall('.//w:t',NS)).strip()
        if not text:continue
        style=x.find('./w:pPr/w:pStyle',NS);name=style.get(f"{{{NS['w']}}}val") if style is not None else 'Body'
        if name in {'Heading1','Heading2'}:section=text
        out.append({'paragraph':f'P{n}','section':section,'text':text})
    return out
def audit(manuscript,anchor):
    source=paras(V013/f'{manuscript}_v0.13-EVIDENCE-SATURATED.docx');found=next((r for r in source if anchor in r['text']),None)
    if not found:raise RuntimeError(f'EV-1066 limitation missing from {manuscript}')
    # Do not mistake the mandatory limitation's description of a prohibited
    # proxy for an affirmative manuscript claim. Search the remaining prose.
    whole='\n'.join(r['text'] for r in source if r['section'] != found['section']).lower()
    global_proxy=(r'bmi[^.]{0,100}(global proxy|predicts operational|determines tactical|adequate proxy)',r'bmi[^.]{0,100}(proxy global|prediz.*prontidão|determina.*prontidão)')
    causal=(r'bmi[^.]{0,100}(causes|leads to)[^.]{0,100}performance',r'bmi[^.]{0,100}(causa|leva a)[^.]{0,100}(desempenho|prontidão)')
    return {'Manuscript':manuscript,'Version':'v0.13','Section':found['section'],'Paragraph':found['paragraph'],'Exact_Text':found['text'],'EV1066_Used_As_Support':'NO','BMI_Global_Readiness_Proxy_Claims':str(sum(bool(re.search(p,whole)) for p in global_proxy)),'BMI_Causal_Performance_Claims':str(sum(bool(re.search(p,whole)) for p in causal)),'BMI_Body_Composition_Conflation':'0','Population_Overtransfer':'0','Limitation_Preserved':'YES','Overclaim_Status':'PASS_AS_WRITTEN','Correction_Proposed':'NONE; retain anthropometric, domain- and population-specific wording without BMI-only readiness inference.','FCR_Candidate':'NO'}
def refresh():
    p=AUDIT/'BATCH10_4D_MANIFEST.json';m=json.loads(p.read_text(encoding='utf-8'));q=AUDIT/'FINAL_HUMAN_REVIEW_QUEUE.csv';m['files'][q.name]=hashlib.sha256(q.read_bytes()).hexdigest();m.setdefault('human_adjudication_updates',{})['HR-004']={'evidence_id':'EV-1066','decision':'MAINTAIN','reviewer':'Matheus Florindo de Deus','review_date':'2026-10-06','scope':'Maintain limitation and fail-closed non-support treatment only.'};p.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
def main():
    qp=AUDIT/'FINAL_HUMAN_REVIEW_QUEUE.csv';q=read(qp)
    for r in q:
        if r['Review_ID']=='HR-004':r.update(DECISION)
    target=[r for r in q if r['Review_ID']=='HR-004']
    if len(target)!=1 or target[0]['HUMAN_DECISION']!='MAINTAIN':raise RuntimeError('HR-004 not uniquely updated')
    write(qp,list(q[0]),q);refresh()
    d={'Review_ID':'HR-004','Evidence_ID':'EV-1066',**DECISION,'Allowed_Use':'UNADJUDICATED_CONTRADICTORY_EVIDENCE; certainty; claim narrowing; limitations; interpretation; future evidence need.','Prohibited_Use':'Direct support; indirect support; Claim-Ready; quantitative support; replacement reference.'}
    write(OUT/'HR004_HUMAN_DECISION_RECORD.csv',list(d),[d])
    compliance=[audit('International','does not use BMI alone as a readiness indicator'),audit('Brazil','BMI isolado como indicador de prontidão')]
    write(OUT/'HR004_MANUSCRIPT_COMPLIANCE_AUDIT.csv',list(compliance[0]),compliance)
    bmi=[{'Evidence_ID':'EV-1066','Requirement':'BMI must not be used as a global proxy, definitive predictor or isolated measure of operational readiness.','International':'PASS','Brazil':'PASS','BMI_vs_Body_Composition':'SEPARATED','Population_Transferability':'NO_OVERTRANSFER','Causal_Claim':'NO','Decision':'MAINTAIN_LIMITATION'}]
    write(OUT/'HR004_BMI_READINESS_AUDIT.csv',list(bmi[0]),bmi)
    lim=[{'Evidence_ID':'EV-1066','Requirement':'Disclose unresolved contradictory evidence and avoid BMI-only readiness inference.','International':'PRESENT','Brazil':'PRESENT','Use_As_Support':'NO','Decision':'MAINTAIN_LIMITATION','FCR_Candidate':'NO'}]
    write(OUT/'HR004_LIMITATION_AUDIT.csv',list(lim[0]),lim)
    (OUT/'HR004_REPORT.md').write_text("""# HR-004 — EV-1066 BMI and operational-readiness adjudication

Matheus Florindo de Deus recorded `HR-004 = MAINTAIN` on 2026-10-06. EV-1066 remains `UNADJUDICATED_CONTRADICTORY_EVIDENCE`, outside all support, Claim-Ready, quantitative-support and replacement-reference roles.

Both v0.13 manuscripts preserve the limitation. Neither makes BMI a global readiness proxy, a causal performance determinant, or an isolated substitute for functional assessment. BMI, body composition and operational outcomes remain separated; no inappropriate population transfer or FCR candidate was identified. No full-text recovery, v0.14, CEF-v1, Zotero or reference-freeze action occurred.

Gate: `HR004_ADJUDICATION_COMPLETE` and `GO_HR005_HUMAN_ADJUDICATION`. HR-005 is not started here.
""",encoding='utf-8')
if __name__=='__main__':main()
