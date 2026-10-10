import csv, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_5a'; FREEZE=ROOT/'batch10_4k'
def rows(n):
 with (OUT/n).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_non_scientific_audit_and_empty_human_queue():
 m=json.loads((OUT/'BATCH10_5A_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='TARGET_JOURNAL_FIT_AUDIT_PASS'
 assert all(m[k]==0 for k in ['v016_manuscripts_changed','cef_v1_changed','zotero_changed','scientific_claims_changed','result_ids_changed','references_changed'])
 q=rows('TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv'); assert [r['Decision_ID'] for r in q]==['INT-TARGET-SELECTION','BRA-TARGET-SELECTION']; assert all(r['Decision_Status'] in {'PENDING_HUMAN_SELECTION','HUMAN_DECISION_RECORDED'} for r in q)
def test_mandated_candidates_shortlists_and_hard_exclusions():
 i=rows('INTERNATIONAL_JOURNAL_CANDIDATES.csv'); b=rows('BRAZIL_JOURNAL_CANDIDATES.csv')
 assert {r['Journal'] for r in i}>={'Frontiers in Public Health','Frontiers in Sports and Active Living'} and len(i)>=7
 assert {r['Journal'] for r in b}>={'Revista Brasileira de Segurança Pública','Revista Brasileira de Saúde Ocupacional','Revista Brasileira de Medicina do Trabalho'} and len(b)>=8
 assert len(rows('INTERNATIONAL_JOURNAL_RANKING.csv'))==len(rows('BRAZIL_JOURNAL_RANKING.csv'))==3
 assert all(r['Fit_Status']!='HARD_EXCLUDE' for n in ['INTERNATIONAL_JOURNAL_RANKING.csv','BRAZIL_JOURNAL_RANKING.csv'] for r in rows(n))
 rbsp=next(r for r in b if r['Candidate_ID']=='BRA-05'); assert rbsp['Submission_Status']=='CURRENTLY_NOT_SUBMITTABLE' and rbsp['Hard_Exclusion']=='YES'
def test_provenance_hashes_and_frozen_docs():
 required={'INTERNATIONAL_JOURNAL_CANDIDATES.csv','BRAZIL_JOURNAL_CANDIDATES.csv','JOURNAL_CURRENT_GUIDELINE_EVIDENCE.csv','JOURNAL_ARTICLE_TYPE_COMPATIBILITY.csv','JOURNAL_WORD_LIMIT_COMPATIBILITY.csv','JOURNAL_APC_AND_ACCESS.csv','JOURNAL_INDEXING_AUDIT.csv','JOURNAL_SUBMISSION_STATUS.csv','JOURNAL_EDITORIAL_RED_FLAGS.csv','JOURNAL_EDITORIAL_INTEGRITY_AUDIT.csv','INTERNATIONAL_JOURNAL_RANKING.csv','BRAZIL_JOURNAL_RANKING.csv','PRIMARY_AND_BACKUP_TARGETS.csv','TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv','BATCH10_5A_MANIFEST.json','BATCH10_5A_REPORT.md'}
 assert required <= {p.name for p in OUT.iterdir()}
 allowed=('frontiersin.org','academic.oup.com','scielo.br','forumseguranca.org.br','militaryhealth.bmj.com','brjp.org.br','rbafs.org.br')
 assert all(r['Official_URL'].startswith('https://') and any(host in r['Official_URL'] for host in allowed) for r in rows('JOURNAL_CURRENT_GUIDELINE_EVIDENCE.csv'))
 m=json.loads((OUT/'BATCH10_5A_MANIFEST.json').read_text(encoding='utf-8'))
 assert all(hashlib.sha256((OUT/n).read_bytes()).hexdigest()==x for n,x in m['artifact_sha256'].items())
 assert hashlib.sha256((FREEZE/'International_v0.16-B2-SCIENTIFIC-FROZEN.docx').read_bytes()).hexdigest()=='0abe30789f6f395a7b67d8f2b87ae893befb4b3eed810c5b252492ae0753cfd2'
 assert hashlib.sha256((FREEZE/'Brazil_v0.16-B2-SCIENTIFIC-FROZEN.docx').read_bytes()).hexdigest()=='bcedc42658c3c624e40747c623652500280ce45f1ad1000d22fdb30438e2f486'
