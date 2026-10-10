"""Record the two user-authorized Batch 10.5A-H editorial selections."""
import csv, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; AUDIT=ROOT/'batch10_5a'; OUT=ROOT/'batch10_5a_h'; FREEZE=ROOT/'batch10_4k'
DATE='2026-10-09'; BASE='c4df9a07d7f26fdc2069ca7d25e5b598c544e8e0'
SELECTIONS={
 'INT-TARGET-SELECTION':{'Selected_Target':'Frontiers in Sports and Active Living','Selected_Article_Type':'Mini Review','Target_Code':'FRONTIERS_SPORTS_ACTIVE_LIVING__MINI_REVIEW','HUMAN_RATIONALE':'Approved by Matheus Florindo de Deus: 46/50 editorial fit; 1,627-word short form fits the 3,000-word Mini Review ceiling; focused synthesis matches tactical/human-performance audience without a systematic-review conversion, new search or claims.'},
 'BRA-TARGET-SELECTION':{'Selected_Target':'Revista Brasileira de Saúde Ocupacional','Selected_Article_Type':'Ensaio','Target_Code':'RBSO__ENSAIO','HUMAN_RATIONALE':'Approved by Matheus Florindo de Deus: 47/50 editorial fit; Ensaio supports the focal occupational-health reflection without converting the internal evidence-informed integrative synthesis into a systematic review.'},
}
BACKUPS=[
 ('International','PRIMARY_TARGET','Frontiers in Sports and Active Living','Mini Review'),('International','BACKUP_TARGET_1','Journal of Occupational Health','Review Article'),('International','BACKUP_TARGET_2','Frontiers in Public Health','Mini Review'),
 ('Brazil','PRIMARY_TARGET','Revista Brasileira de Saúde Ocupacional','Ensaio'),('Brazil','BACKUP_TARGET_1','Cadernos de Saúde Pública','Ensaio'),('Brazil','BACKUP_TARGET_2','Revista Brasileira de Medicina do Trabalho','Artigo de Revisão')]
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def write(p,fields,rows):
 with p.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 OUT.mkdir(exist_ok=True)
 assert json.loads((AUDIT/'BATCH10_5A_MANIFEST.json').read_text(encoding='utf-8'))['gate']=='TARGET_JOURNAL_FIT_AUDIT_PASS'
 for n,x in {'International_v0.16-B2-SCIENTIFIC-FROZEN.docx':'0abe30789f6f395a7b67d8f2b87ae893befb4b3eed810c5b252492ae0753cfd2','Brazil_v0.16-B2-SCIENTIFIC-FROZEN.docx':'bcedc42658c3c624e40747c623652500280ce45f1ad1000d22fdb30438e2f486'}.items():assert sha(FREEZE/n)==x
 queue=read(AUDIT/'TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv'); assert {r['Decision_ID'] for r in queue}==set(SELECTIONS)
 fields=list(queue[0]); fields += [x for x in ['Selected_Target','Selected_Article_Type','Target_Code'] if x not in fields]
 for r in queue:
  s=SELECTIONS[r['Decision_ID']]; r.update(s);r['HUMAN_DECISION']='APPROVE_PRIMARY_TARGET';r['HUMAN_REVIEWER']='Matheus Florindo de Deus';r['HUMAN_REVIEW_DATE']=DATE;r['Decision_Status']='HUMAN_DECISION_RECORDED'
 write(AUDIT/'TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv',fields,queue)
 audit_manifest_path=AUDIT/'BATCH10_5A_MANIFEST.json';audit_manifest=json.loads(audit_manifest_path.read_text(encoding='utf-8'));audit_manifest['human_decisions_populated']=2;audit_manifest['human_selection_state']='RECORDED_IN_BATCH10_5A_H';audit_manifest['artifact_sha256']['TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv']=sha(AUDIT/'TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv');audit_manifest_path.write_text(json.dumps(audit_manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 finalfields=['Decision_ID','Manuscript','Scientific_Type_Internal','Journal_Article_Type','Target_Code','HUMAN_DECISION','HUMAN_REVIEWER','HUMAN_REVIEW_DATE','HUMAN_RATIONALE','Backups_Preserved','Status']
 final=[]
 for r in queue:final.append(dict(Decision_ID=r['Decision_ID'],Manuscript=r['Manuscript'],Scientific_Type_Internal='Evidence-informed integrative synthesis',Journal_Article_Type=r['Selected_Article_Type'],Target_Code=r['Target_Code'],HUMAN_DECISION=r['HUMAN_DECISION'],HUMAN_REVIEWER=r['HUMAN_REVIEWER'],HUMAN_REVIEW_DATE=r['HUMAN_REVIEW_DATE'],HUMAN_RATIONALE=r['HUMAN_RATIONALE'],Backups_Preserved='YES',Status='PASS'))
 write(OUT/'FINAL_TARGET_JOURNAL_HUMAN_SELECTION.csv',finalfields,final)
 bf=['Manuscript','Target_Role','Journal','Journal_Article_Type','Selection_Status'];write(OUT/'TARGET_AND_BACKUP_JOURNALS.csv',bf,[dict(Manuscript=m,Target_Role=role,Journal=j,Journal_Article_Type=t,Selection_Status='SELECTED_PRIMARY' if role=='PRIMARY_TARGET' else 'PRESERVED_BACKUP') for m,role,j,t in BACKUPS])
 impacts=[('scientific changes',0),('claim changes',0),('reference changes',0),('Result_ID changes',0),('CEF-v1 changes',0),('Zotero changes',0),('scientific frozen DOCX changes',0),('journal decisions completed','2/2')]
 write(OUT/'TARGET_SELECTION_IMPACT_AUDIT.csv',['Control','Observed','Status'],[dict(Control=k,Observed=v,Status='PASS') for k,v in impacts])
 rationale='''# Target-selection rationale\n\n## International\n\n- **Scientific type:** `Evidence-informed integrative synthesis`\n- **Journal submission type:** `Mini Review`\n- **Selected target:** Frontiers in Sports and Active Living\n- **Human decision:** Matheus Florindo de Deus, 2026-10-09, `APPROVE_PRIMARY_TARGET`.\n\nThe selection retains the 1,627-word short form and its frozen evidence-boundary focus. It does not convert the manuscript to a systematic review or authorize new science. Journal of Occupational Health and Frontiers in Public Health remain backups.\n\n## Brazil\n\n- **Scientific type:** `Evidence-informed integrative synthesis`\n- **Journal submission type:** `Ensaio`\n- **Selected target:** Revista Brasileira de Saúde Ocupacional\n- **Human decision:** Matheus Florindo de Deus, 2026-10-09, `APPROVE_PRIMARY_TARGET`.\n\n`Ensaio` is solely the journal submission type. It does not replace the project’s internal scientific classification. Cadernos de Saúde Pública and Revista Brasileira de Medicina do Trabalho remain backups.\n'''
 (OUT/'TARGET_SELECTION_RATIONALE.md').write_text(rationale,encoding='utf-8')
 report='''# BATCH 10.5A-H — final target journal human selection\n\n`TARGET_JOURNAL_HUMAN_SELECTION_PASS`\n\n`GO_TARGET_SPECIFIC_EDITORIAL_FORMATTING`\n\nTwo explicit human editorial decisions were recorded exactly as authorized by Matheus Florindo de Deus on 2026-10-09. International selected Frontiers in Sports and Active Living as a Mini Review. Brazil selected Revista Brasileira de Saúde Ocupacional as an Ensaio. The internal scientific type remains `Evidence-informed integrative synthesis` for both.\n\nThe four backup routes remain recorded. This is a journal-selection record only: no frozen manuscript, claim, reference, Result_ID, source locator, evidence role, certainty, CEF-v1 or Zotero record changed. Batch 10.5B is the next permitted phase.\n'''
 (OUT/'BATCH10_5A_H_REPORT.md').write_text(report,encoding='utf-8')
 files=sorted(p for p in OUT.iterdir() if p.is_file() and p.name!='BATCH10_5A_H_MANIFEST.json')
 manifest={'batch':'BATCH 10.5A-H','base_commit':BASE,'gate':'TARGET_JOURNAL_HUMAN_SELECTION_PASS','next_gate':'GO_TARGET_SPECIFIC_EDITORIAL_FORMATTING','human_reviewer':'Matheus Florindo de Deus','human_review_date':DATE,'journal_decisions_completed':'2/2','scientific_changes':0,'claim_changes':0,'reference_changes':0,'result_id_changes':0,'cef_v1_changes':0,'zotero_changes':0,'frozen_docx_changes':0,'artifact_sha256':{p.name:sha(p) for p in files}}
 (OUT/'BATCH10_5A_H_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
