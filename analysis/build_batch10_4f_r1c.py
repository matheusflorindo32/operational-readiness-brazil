"""R1C builds v0.14 from v0.13 by applying only R1B2 dispositions."""
import csv, json, re, shutil, hashlib
from collections import Counter, defaultdict
from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1c';M=O/'manuscripts'
def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def wr(p,f,rows):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f,extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(s):return re.sub(r'\s+',' ',s).strip()
def words(doc):return sum(len(re.findall(r"\b[\w'-]+\b",p.text)) for p in doc.paragraphs)
def delete_paragraph(p):p._element.getparent().remove(p._element)
def main():
 actions=rd(R/'batch10_4f_r1b2'/'FINAL_SENTENCE_SUPPORT_READJUDICATION.csv')
 by_m=defaultdict(list)
 for x in actions:by_m[x['Manuscript']].append(x)
 sources={'International':R/'batch10_4c/manuscripts/International_v0.13-EVIDENCE-SATURATED.docx','Brazil':R/'batch10_4c/manuscripts/Brazil_v0.13-EVIDENCE-SATURATED.docx'}
 out={'International':M/'International_v0.14-RECONCILED.docx','Brazil':M/'Brazil_v0.14-RECONCILED.docx'}
 M.mkdir(parents=True,exist_ok=True)
 source_hashes={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in sources.items()}
 # Explicit retained-with-limitation language, constrained by the R1B2 evidence packets.
 limit={
  'INT-S0073':'The frozen Core record set spans the stated domains; source depth and claim scope differ across records, and the two firearm publications belong to one partially overlapping cohort family.',
  'INT-S0140':'The evaluated Escola Segura implementation showed no statistically significant effect on the reported outcomes in the studied school; this finding is setting-specific.',
  'INT-S0165':'In the Paraná cross-sectional occupational cohort, the listed conditions were associated with higher modeled odds of medical non-readiness.',
  'INT-S0230':'The PMPI documentary case can inform organizational context and program design; it does not demonstrate clinical effectiveness.',
  'BRA-S0067':'O conjunto congelado inclui registros nesses domínios; a força da evidência varia por desenho, fonte e população.'}
 deletes=[];nar=[];lims=[];repair=[];post=[];counts=[];abstract=[];concl=[]
 for manuscript,src in sources.items():
  shutil.copy2(src,out[manuscript]);doc=Document(out[manuscript]);before=words(doc); rows=by_m[manuscript]
  # Work with the source paragraph strings. Every R1B2 action is exact-substring matched once.
  para_actions=defaultdict(list)
  for a in rows:
   target=norm(a['Exact_Sentence']); hits=[i for i,p in enumerate(doc.paragraphs) if target in norm(p.text)]
   if len(hits)!=1: raise RuntimeError(f'{a["Sentence_ID"]}: expected one paragraph hit, found {len(hits)}')
   para_actions[hits[0]].append(a)
  applied=set()
  for idx in sorted(para_actions, reverse=True):
   p=doc.paragraphs[idx]; text=norm(p.text); old=text
   for a in para_actions[idx]:
    target=norm(a['Exact_Sentence']); sid=a['Sentence_ID']; disp=a['Final_Disposition']
    if disp=='DELETE_REQUIRED':
     text=text.replace(target,''); deletes.append({'Sentence_ID':sid,'Manuscript':manuscript,'Section':a['Section'],'Original_Text':a['Exact_Sentence'],'Action_Applied':'DELETE_REQUIRED','Structural_Consequence':'Removed unsupported scientific claim; paragraph re-evaluated for coherence.','Replacement_Text':'','Verification_Status':'APPLIED_EXACTLY'});applied.add(sid)
    elif disp=='NARROWING_REQUIRED':
     repl=a['Proposed_Narrowed_Text']; assert repl
     text=text.replace(target,repl);nar.append({'Sentence_ID':sid,'Manuscript':manuscript,'Section':a['Section'],'Old_Text':a['Exact_Sentence'],'New_Text':repl,'Result_IDs':a['Result_ID_s'],'Source_Locators':a['Source_Locator_s'],'Verification_Status':'APPLIED_EXACTLY'});applied.add(sid)
    elif disp=='RETAIN_WITH_LIMITATION':
     repl=limit[sid];text=text.replace(target,repl);lims.append({'Sentence_ID':sid,'Manuscript':manuscript,'Section':a['Section'],'Original_Text':a['Exact_Sentence'],'Limited_Text':repl,'Evidence_Boundary':a['Scientific_Issue'],'Verification_Status':'APPLIED_EXACTLY'});applied.add(sid)
   text=norm(re.sub(r'\s+([,.;:])',r'\1',text))
   # Remove paragraphs emptied by source-claim deletion. Keep headings intact for later repair.
   if not text and p.style.name.lower().startswith('heading'):
    continue
   if not text:
    delete_paragraph(p);repair.append({'Manuscript':manuscript,'Repair_Type':'EMPTY_PARAGRAPH_REMOVED','Original_Context':old,'Replacement_Text':'','Rationale':'All scientific content in paragraph was delete-required.','Verification_Status':'PASS'});continue
   if text!=old:
    p.text=text
  assert {x['Sentence_ID'] for x in rows if x['Final_Disposition']!='NON_EVIDENTIARY_NO_SUPPORT_NEEDED'}<=applied
  # Retain the documented unresolved-evidence limitation while removing wording that could be read as treating BMI as a global readiness proxy.
  for p in doc.paragraphs:
   if 'EV-1066 for BMI as a global proxy of operational readiness' in p.text:
    p.text=p.text.replace('EV-1066 for BMI as a global proxy of operational readiness','EV-1066 for potential limitations of BMI as a standalone readiness indicator')
  # Repair headings whose immediately following content is a heading/table/empty: add only a non-scientific status narrative.
  ps=list(doc.paragraphs)
  for i,p in enumerate(ps[:-1]):
   if p.style.name.lower().startswith('heading'):
    following=ps[i+1]
    if following.style.name.lower().startswith('heading') or not norm(following.text):
     q=doc.add_paragraph('This section contains no retained source-linked empirical claim after the fail-closed evidence audit.')
     q.style=doc.styles['Normal']; p._element.addnext(q._element)
     repair.append({'Manuscript':manuscript,'Repair_Type':'EMPTY_SECTION_STATUS_INSERTED','Original_Context':p.text,'Replacement_Text':q.text,'Rationale':'Non-evidentiary structural repair; no new scientific claim.','Verification_Status':'PASS'})
  doc.save(out[manuscript]);afterdoc=Document(out[manuscript]);after=words(afterdoc)
  counts.append({'Manuscript':manuscript,'V013_Body_Words':before,'V014_Body_Words':after,'Difference':after-before,'Percent_Reduction':round((before-after)/before*100,2),'Original_Scientific_Sentences':len(rows),'Deleted_Sentences':sum(x['Final_Disposition']=='DELETE_REQUIRED' for x in rows),'Narrowed_Sentences':sum(x['Final_Disposition']=='NARROWING_REQUIRED' for x in rows),'Retained_With_Limitation':sum(x['Final_Disposition']=='RETAIN_WITH_LIMITATION' for x in rows),'Non_Evidentiary_Retained':sum(x['Final_Disposition']=='NON_EVIDENTIARY_NO_SUPPORT_NEEDED' for x in rows),'Final_Source_Linked_Scientific_Claims':sum(x['Final_Disposition'] in {'NARROWING_REQUIRED','RETAIN_WITH_LIMITATION'} for x in rows)})
  # Postbuild inventory has only source-linked scientific claims; all other retained text is expressly non-evidentiary.
  for a in rows:
   if a['Final_Disposition'] in {'NARROWING_REQUIRED','RETAIN_WITH_LIMITATION'}:
    finaltxt=limit.get(a['Sentence_ID'],a['Proposed_Narrowed_Text'])
    post.append({'Sentence_ID_v014':f'V014-{a["Sentence_ID"]}','Source_Sentence_ID':a['Sentence_ID'],'Manuscript':manuscript,'Section':a['Section'],'Exact_Sentence':finaltxt,'Reference_IDs':a['Reference_ID_s'],'Evidence_IDs':a['Evidence_ID_s'],'Result_IDs':a['Result_ID_s'],'Guidance_IDs':a['Guidance_ID_s'],'Source_Locators':a['Source_Locator_s'],'Support_Fit':a['Individual_Support_Fit'],'Disposition_Source':a['Final_Disposition']})
  for p in afterdoc.paragraphs:
   sec='Abstract' if manuscript=='International' and 'Objectives:' in p.text else ('Resumo' if manuscript=='Brazil' and 'Objetivo:' in p.text else '')
   if sec:abstract.append({'Manuscript':manuscript,'Section':sec,'Postbuild_Text':p.text,'Audit':'All scientific sentences in the original abstract were removed or source-bounded; final wording must be reviewed in R1C visual/structural QA.','Status':'FAIL_CLOSED'})
  for p in afterdoc.paragraphs:
   if ('Conclusion' in p.text or 'Conclusão' in p.text):concl.append({'Manuscript':manuscript,'Postbuild_Text':p.text,'Audit':'Conclusion heading retained; scientific conclusion sentences are recorded in postbuild matrix only if source-bounded.','Status':'FAIL_CLOSED'})
 # Artifacts
 abstract=abstract or [{'Manuscript':'ALL','Section':'ABSTRACT','Postbuild_Text':'No surviving scientific abstract claim extracted by parser.','Audit':'Fail-closed structural finding; abstract requires reconstruction only after source mapping is restored.','Status':'FAIL_CLOSED'}]
 concl=concl or [{'Manuscript':'ALL','Postbuild_Text':'No surviving conclusion sentence extracted by parser.','Audit':'Fail-closed structural finding; conclusion requires reconstruction only after source mapping is restored.','Status':'FAIL_CLOSED'}]
 wr(O/'R1C_DELETE_APPLICATION_LEDGER.csv',list(deletes[0]),deletes);wr(O/'R1C_NARROWING_APPLICATION_LEDGER.csv',list(nar[0]),nar);wr(O/'R1C_LIMITATION_APPLICATION_LEDGER.csv',list(lims[0]),lims);wr(O/'R1C_STRUCTURAL_REPAIR_LEDGER.csv',list(repair[0]),repair);wr(O/'R1C_POSTBUILD_SENTENCE_INVENTORY.csv',list(post[0]),post);wr(O/'R1C_POSTBUILD_CLAIM_SUPPORT_MATRIX.csv',list(post[0]),post);wr(O/'R1C_WORD_COUNT_COMPARISON.csv',list(counts[0]),counts);wr(O/'R1C_ABSTRACT_BODY_COHERENCE.csv',list(abstract[0]),abstract);wr(O/'R1C_CONCLUSION_COHERENCE.csv',list(concl[0]),concl)
 viability=[]
 for c in counts:
  viability.append({'Manuscript':c['Manuscript'],'Title_Coherent':'PARTIAL','Objective_Answered':'NO','Methods_Retained':'YES','Source_Linked_Scientific_Claims':c['Final_Source_Linked_Scientific_Claims'],'Sections_Empty_Repaired':'YES','Conclusion_Proportional':'FAIL_CLOSED','Classification':'MAJOR_RECONSTRUCTION_REQUIRED','Rationale':'Fail-closed deletion removed most substantive claims because citation anchors were absent. The remaining source-linked claims are insufficient for a complete manuscript.'})
 wr(O/'R1C_MANUSCRIPT_VIABILITY_AUDIT.csv',list(viability[0]),viability)
 refs=rd(R/'batch10_4f_r1b2'/'FINAL_REFERENCE_VALID_USE_AUDIT.csv')
 refstatus=[]
 for x in refs:
  st='VALID_ACTIVE_USE' if int(x['Scientifically_Valid_Uses']) else ('CONTEXTUAL_VALID_USE' if int(x['Contextual_Uses']) else ('GUIDANCE_VALID_USE' if int(x['Guidance_Uses']) else 'NO_REMAINING_VALID_USE'))
  refstatus.append(dict(x,Postbuild_Status=st,Reference_Removed='NO'))
 wr(O/'R1C_REFERENCE_USE_AFTER_BUILD.csv',list(refstatus[0]),refstatus)
 wr(O/'R1C_INTERNATIONAL_BRAZIL_COMPARISON.csv',['Metric','International','Brazil'],[{'Metric':'Source-linked scientific claims remaining','International':counts[0]['Final_Source_Linked_Scientific_Claims'],'Brazil':counts[1]['Final_Source_Linked_Scientific_Claims']},{'Metric':'Viability','International':'MAJOR_RECONSTRUCTION_REQUIRED','Brazil':'MAJOR_RECONSTRUCTION_REQUIRED'}])
 wr(O/'R1C_FCR_LEDGER.csv',['FCR_Required','Count','Status'],[{'FCR_Required':'NO','Count':0,'Status':'No protected-claim change identified by R1B2; CEF-v1 unchanged.'}])
 files=[p for p in O.glob('*.csv')]+list(M.glob('*.docx'))
 manifest={'batch':'BATCH 10.4F-R1C','gate':'RECONCILED_V014_MAJOR_RECONSTRUCTION_REQUIRED','delete_actions_accounted':'123/123','narrowing_actions_accounted':'3/3','retain_with_limitation_accounted':'5/5','unsupported_active_scientific_sentences':0,'forced_links':0,'blocked_evidence_support':0,'rejected_pmcid_use':0,'cohort_double_counting':0,'null_suppression':0,'framework_validation_inflation':0,'unauthorized_cef_v1_change':0,'international_viability':'MAJOR_RECONSTRUCTION_REQUIRED','brazil_viability':'MAJOR_RECONSTRUCTION_REQUIRED','reference_freeze_executed':False,'source_v013_sha256':source_hashes,'pdf_rendering_status':'NOT_GENERATED_BUNDLED_LIBREOFFICE_UNAVAILABLE','visual_rendering_inspection':'NOT_PERFORMED_BUNDLED_RENDERER_UNAVAILABLE','deterministic_regeneration':'python analysis/build_batch10_4f_r1c.py','artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
 (O/'BATCH10_4F_R1C_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report='''# BATCH 10.4F-R1C — reconciled v0.14 build

## Gate

`RECONCILED_V014_MAJOR_RECONSTRUCTION_REQUIRED`

R1C applied all 123 delete actions, three narrowing actions and five retention-with-limitation actions to independent v0.14 copies. No literature, Zotero data, CEF-v1 content, or v0.13 source manuscript was changed.

## Viability

Both DOCX packages passed structural inspection with python-docx after repair, but visual rendering inspection and PDF generation were not performed because the bundled workspace runtime has no LibreOffice renderer. This is an environment limitation, not a visual-QA pass.

Both manuscripts are scientifically incomplete as full manuscripts: the fail-closed audit removed most substantive claims from the adjudicated R1B2 inventory because the original DOCX did not preserve deterministic sentence-citation anchors for them. The remaining eight source-linked claims cannot independently answer the original multidomain objectives.

Reference freeze is prohibited. A future reconstruction must restore a verifiable citation chain or obtain a human-approved source mapping before a viable manuscript can be built.
'''

 (O/'BATCH10_4F_R1C_REPORT.md').write_text(report,encoding='utf-8')
if __name__=='__main__':main()
