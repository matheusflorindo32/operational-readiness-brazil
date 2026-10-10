import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'batch10_5a_h'; AUDIT=ROOT/'batch10_5a'; FREEZE=ROOT/'batch10_4k'
def rows(p):
 with (p).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def test_two_authorized_human_selections_and_scientific_immutability():
 m=json.loads((OUT/'BATCH10_5A_H_MANIFEST.json').read_text(encoding='utf-8'));assert m['gate']=='TARGET_JOURNAL_HUMAN_SELECTION_PASS' and m['journal_decisions_completed']=='2/2';assert all(m[k]==0 for k in ['scientific_changes','claim_changes','reference_changes','result_id_changes','cef_v1_changes','zotero_changes','frozen_docx_changes'])
 q=rows(AUDIT/'TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv');assert [(r['Decision_ID'],r['Selected_Target'],r['Selected_Article_Type']) for r in q]==[('INT-TARGET-SELECTION','Frontiers in Sports and Active Living','Mini Review'),('BRA-TARGET-SELECTION','Revista Brasileira de Saúde Ocupacional','Ensaio')];assert all(r['HUMAN_DECISION']=='APPROVE_PRIMARY_TARGET' and r['HUMAN_REVIEWER']=='Matheus Florindo de Deus' and r['HUMAN_REVIEW_DATE']=='2026-10-09' for r in q)
def test_docx_hashes_and_artifact_hashes_remain_valid():
 assert hashlib.sha256((FREEZE/'International_v0.16-B2-SCIENTIFIC-FROZEN.docx').read_bytes()).hexdigest()=='0abe30789f6f395a7b67d8f2b87ae893befb4b3eed810c5b252492ae0753cfd2';assert hashlib.sha256((FREEZE/'Brazil_v0.16-B2-SCIENTIFIC-FROZEN.docx').read_bytes()).hexdigest()=='bcedc42658c3c624e40747c623652500280ce45f1ad1000d22fdb30438e2f486'
 m=json.loads((OUT/'BATCH10_5A_H_MANIFEST.json').read_text(encoding='utf-8'));assert all(hashlib.sha256((OUT/n).read_bytes()).hexdigest()==v for n,v in m['artifact_sha256'].items())
