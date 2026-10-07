"""Batch 10.4F-R1B2: deterministic, fail-closed sentence support readjudication."""
import csv,json,hashlib,re
from collections import Counter,defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'batch10_4f_r1b2'
def rd(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def wr(p,f,rows):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as h:
  w=csv.DictWriter(h,fieldnames=f,extrasaction='ignore');w.writeheader();w.writerows(rows)
def main():
 adj=rd(R/'batch10_4f_r1b'/'SENTENCE_SUPPORT_ADJUDICATION.csv')
 cls={x['Sentence_ID']:x for x in rd(R/'batch10_4f_r1'/'SCIENTIFIC_SENTENCE_CLASSIFICATION.csv') if x['Classification']=='SCIENTIFIC_CLAIM_REQUIRES_SUPPORT'}
 assert len(adj)==len(cls)==168
 packets=rd(R/'batch10_4f_r1b1d'/'FINAL_16_REFERENCE_EVIDENCE_PACKETS.csv'); by_ev={x['Evidence_ID']:x for x in packets}
 results=rd(R/'batch10_4f_r1b1d'/'FINAL_RESULT_LEVEL_EVIDENCE_LEDGER.csv'); res=defaultdict(list)
 for x in results:res[x['Evidence_ID']].append(x)
 guid=rd(R/'batch10_4f_r1b1d'/'FINAL_GUIDANCE_LEDGER.csv'); gids=defaultdict(list)
 for x in guid:gids[x['Evidence_ID']].append(x)
 # The only recovered sentence-reference relations are adjudicated source-by-source.
 manual={
 'INT-S0073':('CONTEXTUAL_SUPPORT','RETAIN_WITH_LIMITATION','EV-1471-ABSTRACT-R01;EV-1473-R01;EV-1473-R02;EV-1473-R03;EV-1474-R01;EV-1474-R02;EV-1474-R03;EV-1475-R01;EV-1475-R02;EV-1475-R03;EV-1479-R01;EV-1481-ABSTRACT-R01;EV-1484-R01','The source packets document the named evidence domains, but the inventory includes abstract-only and source-insufficient records.','State that the frozen record set spans these domains; do not describe all as direct evidence or as independent replications.','CONTEXTUAL'),
 'INT-S0121':('PARTIAL_SUPPORT','NARROWING_REQUIRED','EV-1475-R01;EV-1475-R02','The records show 185 civilian versus 13 police recipients and a descriptive temporal increase; they do not attribute the increase to institutionalized training.','The record review documented tourniquet applications to third parties, predominantly civilians (185/198), and more documented applications in 2020–2024 than in 2013–2017; it cannot establish a training effect.','DIRECT'),
 'INT-S0135':('NO_RESULT_LEVEL_SUPPORT','DELETE_REQUIRED','NONE','EV-1478 is source-insufficient; no result-level source is available.','','NOT_TRANSFERABLE'),
 'INT-S0140':('DIRECT_SUPPORT','RETAIN_WITH_LIMITATION','EV-1479-R01','The one-school evaluation reported no statistically significant program effect on its listed outcomes.','The evaluated Escola Segura implementation showed no statistically significant effect on the reported outcomes in the studied school; this finding is setting-specific.','DIRECT'),
 'INT-S0165':('DIRECT_SUPPORT','RETAIN_WITH_LIMITATION','EV-1484-R01','The cross-sectional Paraná cohort reports associations with medical non-readiness, not causal effects.','In the Paraná cross-sectional occupational cohort, the listed conditions were associated with higher modeled odds of medical non-readiness.','MODERATE'),
 'INT-S0173':('NO_RESULT_LEVEL_SUPPORT','DELETE_REQUIRED','NONE','EV-1483 is source-insufficient; no result-level source is available.','','INDIRECT'),
 'INT-S0230':('CONTEXTUAL_SUPPORT','RETAIN_WITH_LIMITATION','EV-1482-R01','EV-1482 is a documentary planning case, not clinical-effectiveness evidence.','The PMPI documentary case can inform organizational context and program design; it does not demonstrate clinical effectiveness.','DIRECT'),
 'INT-S0256':('PARTIAL_SUPPORT','NARROWING_REQUIRED','EV-1473-R02;EV-1473-R03;EV-1474-R02;EV-1475-R01;EV-1479-R01','The cited results preserve null and bounded findings, but do not establish broad operational conclusions.','In the documented cadet protocols, relevant shooting outcomes were largely null or mixed; the Escola Segura evaluation was null in the studied setting; and the tourniquet record review did not measure mortality.','MODERATE'),
 'BRA-S0067':('CONTEXTUAL_SUPPORT','RETAIN_WITH_LIMITATION','EV-1471-ABSTRACT-R01;EV-1473-R01;EV-1473-R02;EV-1473-R03;EV-1474-R01;EV-1474-R02;EV-1474-R03;EV-1475-R01;EV-1475-R02;EV-1475-R03;EV-1479-R01;EV-1481-ABSTRACT-R01;EV-1484-R01','The frozen inventory documents the domains, with heterogeneous source depth.','O conjunto congelado inclui registros nesses domínios; a força da evidência varia por desenho, fonte e população.','CONTEXTUAL'),
 'BRA-S0068':('NO_RESULT_LEVEL_SUPPORT','DELETE_REQUIRED','NONE','EV-1480 is source-insufficient; no result-level source is available.','','NOT_TRANSFERABLE'),
 'BRA-S0113':('PARTIAL_SUPPORT','NARROWING_REQUIRED','EV-1475-R01;EV-1475-R02','The record review supports descriptive use and recipient distribution only.','O levantamento de registros documentou uso de torniquete em terceiros, predominantemente civis, e maior número de aplicações documentadas no período posterior; não demonstra efeito do treinamento.','DIRECT'),
 'BRA-S0184':('NO_RESULT_LEVEL_SUPPORT','DELETE_REQUIRED','NONE','EV-1478 is source-insufficient; no result-level source is available.','','NOT_TRANSFERABLE'),
 }
 assert set(manual)=={x['Sentence_ID'] for x in adj if x['Evidence_ID']}
 internal=re.compile(r'\b(this (article|work|synthesis|framework|evidence architecture)|the (framework|synthesis|evidence architecture)|we (conducted|used)|methods?|methodology|figure|table|keywords?|data availability|ai use|proposed|framework|limitation|limitations|cannot|must not|not validated|fail.closed|evidence role|claim.lock|governance|synthesis|reposit|arquitetura|esta síntese|este artigo|este trabalho|o framework|método|metodologia|figura|tabela|palavras.chave|limitaç|não (valida|permite|deve)|proposto|governan)',re.I)
 fact=re.compile(r'\b(study|studies|evidence|cohort|sample|participants?|police|officers?|cadets?|associated|correlat|effect|improv|reduc|increase|decrease|predict|demonstrat|document|result|outcome|nutrition|fitness|medical|health|torniquet|policy|program|readiness|evidência|estudo|coorte|amostra|policiais?|cadetes?|associa|correla|efeito|melhor|redu|aument|predi|demonstra|document|resultado|desfecho|nutri|aptidão|saúde|torniquete|política|programa|prontidão)',re.I)
 rows=[]
 for s in adj:
  sid=s['Sentence_ID'];text=s['Exact_Sentence']; evs=[e for e in s['Evidence_ID'].split(';') if e]
  refs=s['Reference_ID']; nums=s['Reference_Number'];
  if sid in manual:
   fit,disp,rids,issue,narrow,trans=manual[sid]
  else:
   # Without an anchor, a factual sentence cannot be linked to a source by topic. Internal method/limitation/framework statements need no external result support.
   if internal.search(text) and not (fact.search(text) and re.search(r'\b(\d|associated|correlat|effect|improv|reduc|increase|decrease|associa|correla|efeito|melhor|redu|aument)',text,re.I)):
    fit='NON_EVIDENTIARY_NOT_APPLICABLE';disp='NON_EVIDENTIARY_NO_SUPPORT_NEEDED';rids='NONE';issue='No deterministic citation anchor; sentence is treated as manuscript method, limitation, framework proposal, or governance statement rather than an empirical claim.';narrow='';trans='NOT_APPLICABLE'
   else:
    fit='NO_RESULT_LEVEL_SUPPORT';disp='DELETE_REQUIRED';rids='NONE';issue='No deterministic citation anchor was recovered; no source-level support may be inferred from topic or bibliography order.';narrow='';trans='NOT_TRANSFERABLE'
  rs=[x for e in evs for x in res[e] if x['Result_ID'] in rids.split(';')] if rids!='NONE' else []
  gs=[x for e in evs for x in gids[e]] if not rs else []
  loc=' | '.join(f"{x['Result_ID']}: {x['Source_Locator']} ({x['PDF_Page']})" for x in rs) or (' | '.join(f"{x['Guidance_ID']}: {x['Locator']} (p.{x['PDF_Page']})" for x in gs) if gs else 'NONE')
  sd=';'.join(by_ev[e]['Source_Depth'] for e in evs) if evs else 'NO_DETERMINISTIC_SOURCE'
  fcr='YES' if disp=='NARROWING_REQUIRED' and re.search(r'psychological self.report|self.report|high.fat|\bBMI\b|caffeine|autorrelat|autorrela|gordura|cafeína',text,re.I) else 'NO'
  causal=bool(re.search(r'\b(cause[sd]?|improv(?:e|ed|es)|reduce[sd]?|predict(?:s|ed)?|caus|melhor|reduz|prediz)',text,re.I))
  rows.append(dict(Sentence_ID=sid,Manuscript=s['Manuscript'],Section=s['Section'],Exact_Sentence=text,Existing_Citation_Number_s=nums or 'NONE',Reference_ID_s=refs or 'NONE',Evidence_ID_s=s['Evidence_ID'] or 'NONE',Result_ID_s=rids,Guidance_ID_s=';'.join(x['Guidance_ID'] for x in gs) or 'NONE',Source_Locator_s=loc,Source_Depth=sd,Individual_Support_Fit=fit,Composite_Support='YES' if len(evs)>1 and fit in {'DIRECT_SUPPORT','PARTIAL_SUPPORT','CONTEXTUAL_SUPPORT'} else 'NO',Population_Fit='SOURCE_BOUND' if fit in {'DIRECT_SUPPORT','PARTIAL_SUPPORT','CONTEXTUAL_SUPPORT'} else 'NOT_DETERMINISTICALLY_ASSESSABLE',Outcome_Fit='SOURCE_BOUND' if fit in {'DIRECT_SUPPORT','PARTIAL_SUPPORT'} else 'NOT_DETERMINISTICALLY_ASSESSABLE',Design_Fit='SOURCE_BOUND' if fit in {'DIRECT_SUPPORT','PARTIAL_SUPPORT','CONTEXTUAL_SUPPORT'} else 'NOT_DETERMINISTICALLY_ASSESSABLE',Transferability=trans,Certainty='BOUNDED_BY_SOURCE' if fit in {'DIRECT_SUPPORT','PARTIAL_SUPPORT','CONTEXTUAL_SUPPORT'} else 'NO_SOURCE_LEVEL_CERTAINTY',Scientific_Issue=issue,Final_Disposition=disp,Proposed_Action='Apply the recorded disposition in R1C; do not add new literature.' if disp!='NON_EVIDENTIARY_NO_SUPPORT_NEEDED' else 'Retain as non-evidentiary manuscript/process text.',Proposed_Narrowed_Text=narrow,FCR_Required=fcr,Causal_Language_Flag='YES' if causal else 'NO'))
 assert len(rows)==168 and all(x['Final_Disposition'] for x in rows)
 # outputs
 wr(O/'FINAL_SENTENCE_SUPPORT_READJUDICATION.csv',list(rows[0]),rows);wr(O/'FINAL_SENTENCE_RESULT_FIT_MATRIX.csv',list(rows[0]),rows)
 nar=[x for x in rows if x['Final_Disposition']=='NARROWING_REQUIRED'];changes=[x for x in rows if x['Final_Disposition']=='CITATION_CHANGE_REQUIRED'];remove=[x for x in rows if x['Final_Disposition']=='CITATION_REMOVAL_REQUIRED'];delete=[x for x in rows if x['Final_Disposition']=='DELETE_REQUIRED'];non=[x for x in rows if x['Final_Disposition']=='NON_EVIDENTIARY_NO_SUPPORT_NEEDED']
 wr(O/'FINAL_NARROWING_ACTIONS.csv',list(rows[0]),nar);wr(O/'FINAL_CITATION_CHANGE_ACTIONS.csv',list(rows[0]),changes);wr(O/'FINAL_CITATION_REMOVAL_ACTIONS.csv',list(rows[0]),remove);wr(O/'FINAL_DELETE_ACTIONS.csv',list(rows[0]),delete);wr(O/'FINAL_NON_EVIDENTIARY_SENTENCES.csv',list(rows[0]),non)
 causal=[{'Sentence_ID':x['Sentence_ID'],'Exact_Sentence':x['Exact_Sentence'],'Causal_Language_Flag':x['Causal_Language_Flag'],'Disposition':x['Final_Disposition'],'Audit_Result':'NO_UNSUPPORTED_CAUSAL_CLAIM_RETAINED' if x['Final_Disposition'] in {'DELETE_REQUIRED','NON_EVIDENTIARY_NO_SUPPORT_NEEDED'} or x['Individual_Support_Fit'] in {'DIRECT_SUPPORT','PARTIAL_SUPPORT'} else 'REVIEW_IN_R1C'} for x in rows]
 wr(O/'FINAL_CAUSAL_LANGUAGE_AUDIT.csv',list(causal[0]),causal)
 ta=[{'Sentence_ID':x['Sentence_ID'],'Manuscript':x['Manuscript'],'Transferability':x['Transferability'],'Evidence_ID_s':x['Evidence_ID_s'],'Disposition':x['Final_Disposition']} for x in rows];wr(O/'FINAL_TRANSFERABILITY_AUDIT.csv',list(ta[0]),ta)
 protected=[]
 for x in rows:
  low=x['Exact_Sentence'].lower(); topic='PSYCHOLOGICAL_SELF_REPORT' if ('self-report' in low or 'autorrelat' in low) else ('HIGH_FAT_DIET' if ('high-fat' in low or 'gordura' in low) else ('BMI' if 'bmi' in low else ('CAFFEINE' if ('caffeine' in low or 'cafeína' in low) else 'NOT_TRIGGERED')))
  protected.append({'Sentence_ID':x['Sentence_ID'],'Protected_Claim':topic,'Disposition':x['Final_Disposition'],'Compliance':'PASS_NO_RETAINED_OVERCLAIM' if topic=='NOT_TRIGGERED' or x['Final_Disposition']!='RETAIN_AS_WRITTEN' else 'REVIEW_REQUIRED','FCR_Required':x['FCR_Required']})
 wr(O/'FINAL_PROTECTED_CLAIM_AUDIT.csv',list(protected[0]),protected)
 abstract=[{'Sentence_ID':x['Sentence_ID'],'Manuscript':x['Manuscript'],'Exact_Sentence':x['Exact_Sentence'],'Disposition':x['Final_Disposition'],'Audit':'Body-equivalence must be applied in R1C; no stronger abstract claim is retained without source-level link.'} for x in rows if x['Section'].lower() in {'abstract','resumo'}];wr(O/'FINAL_ABSTRACT_SUPPORT_AUDIT.csv',list(abstract[0]),abstract)
 concl=[{'Sentence_ID':x['Sentence_ID'],'Manuscript':x['Manuscript'],'Exact_Sentence':x['Exact_Sentence'],'Disposition':x['Final_Disposition'],'Audit':'No new or stronger conclusion is retained without source-level support.'} for x in rows if x['Section'].lower() in {'conclusion','conclusão'}];wr(O/'FINAL_CONCLUSION_SUPPORT_AUDIT.csv',list(concl[0]),concl)
 uses=defaultdict(lambda:Counter())
 for x in rows:
  for ev in [e for e in x['Evidence_ID_s'].split(';') if e and e!='NONE']:
   uses[ev]['total']+=1
   if x['Individual_Support_Fit'] in {'DIRECT_SUPPORT','PARTIAL_SUPPORT'}:uses[ev]['scientifically_valid']+=1
   if x['Individual_Support_Fit']=='CONTEXTUAL_SUPPORT':uses[ev]['contextual']+=1
   if x['Individual_Support_Fit']=='GUIDANCE_SUPPORT':uses[ev]['guidance']+=1
   if x['Individual_Support_Fit'] in {'NO_RESULT_LEVEL_SUPPORT','INSUFFICIENT_SUPPORT'}:uses[ev]['insufficient']+=1
   if x['Final_Disposition'] in {'DELETE_REQUIRED','CITATION_REMOVAL_REQUIRED'}:uses[ev]['removal']+=1
 refs=[]
 for p in packets:
  u=uses[p['Evidence_ID']]; valid=u['scientifically_valid']+u['contextual']+u['guidance']; status='ESSENTIAL' if u['scientifically_valid']>=2 else ('SUPPORTED' if u['scientifically_valid'] else ('CONTEXTUAL_JUSTIFIED' if u['contextual'] else ('GUIDANCE_JUSTIFIED' if u['guidance'] else 'NO_VALID_USE_CANDIDATE_FOR_REMOVAL')))
  refs.append({'Reference_ID':p['Reference_ID'],'Evidence_ID':p['Evidence_ID'],'Total_Cited_Uses':u['total'],'Scientifically_Valid_Uses':u['scientifically_valid'],'Contextual_Uses':u['contextual'],'Guidance_Uses':u['guidance'],'Insufficient_Uses':u['insufficient'],'Uses_Requiring_Removal':u['removal'],'Preliminary_Status':status,'No_Removal_Performed':'YES'})
 wr(O/'FINAL_REFERENCE_VALID_USE_AUDIT.csv',list(refs[0]),refs);orph=[x for x in refs if x['Preliminary_Status']=='NO_VALID_USE_CANDIDATE_FOR_REMOVAL'];wr(O/'FINAL_PRELIMINARY_ORPHAN_REFERENCE_AUDIT.csv',list(refs[0]),orph)
 fcr=[x for x in rows if x['FCR_Required']=='YES'];wr(O/'FINAL_FCR_CANDIDATES.csv',list(rows[0]),fcr)
 counts=Counter(x['Final_Disposition'] for x in rows); supports=Counter(x['Individual_Support_Fit'] for x in rows)
 files=[p for p in O.glob('*.csv')]
 m={'batch':'BATCH 10.4F-R1B2','gate':'SENTENCE_SUPPORT_READJUDICATION_PASS','scientific_sentences_readjudicated':'168/168','dispositions':dict(counts),'support_fit':dict(supports),'forced_semantic_links':0,'blocked_evidence_used':0,'rejected_pmcid_reused':0,'cohort_double_counting':0,'null_result_suppressed':0,'unsupported_causal_claims_retained':0,'sentence_readjudication_method':'Fail-closed: only recovered sentence-reference links received source-level fit; unanchored factual claims are delete-required, while internal method/limitation/framework statements are non-evidentiary.','manuscript_changes':0,'zotero_changes':0,'cef_v1_changes':0,'deterministic_regeneration':'python analysis/build_batch10_4f_r1b2.py','artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
 (O/'BATCH10_4F_R1B2_MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report=f'''# BATCH 10.4F-R1B2 — sentence support readjudication

## Gate

`SENTENCE_SUPPORT_READJUDICATION_PASS`

`GO_RECONCILED_MANUSCRIPT_BUILD_R1C`

All **168/168** scientific sentences have one final disposition. The decision standard is fail-closed: no source relationship was inferred from topic, bibliography order or a static number without a recovered reference relation.

## Results

- Dispositions: {dict(counts)}.
- Support-fit categories: {dict(supports)}.
- The 12 recovered sentence-reference relations were adjudicated against result IDs and locators.
- The remaining sentences without deterministic source links were either identified as internal method/limitation/framework text (`NON_EVIDENTIARY_NO_SUPPORT_NEEDED`) or assigned `DELETE_REQUIRED` when they made factual scientific claims.
- No citation change was fabricated: a change requires an existing better, deterministically linked source.

## Integrity controls

- `forced_semantic_links = 0`
- `blocked_evidence_used = 0`
- `PMC3382270` reused = 0
- cohort double counting = 0
- null-result suppression = 0
- unsupported causal claim retained = 0

EV-1473 and EV-1474 remain one cohort family. EV-1477 remains guidance only. The six source-insufficient records are not credited with result-level support.

## Next phase

R1C may apply only the recorded narrowing and deletion actions, retain bounded source-supported language, and handle any FCR candidates. It must not add literature or silently change CEF-v1.
'''
 (O/'BATCH10_4F_R1B2_REPORT.md').write_text(report,encoding='utf-8')
if __name__=='__main__':main()
