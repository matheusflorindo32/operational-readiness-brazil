"""Build a transparent, non-scientific access-priority queue for the non-PMC FT2 set."""
from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'batch10_4b'/'scientific'/'FULL_TEXT_SATURATION_MASTER.csv'
OUT=ROOT/'batch10_4b'/'ft2'
PMC=ROOT/'batch10_4b'/'ft1'/'artifacts'/'PMC100_PROVISIONAL_DECISIONS.csv'

def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name, rows, fields=None):
    OUT.mkdir(parents=True,exist_ok=True)
    fields=fields or list(rows[0])
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    source=read(SRC); remaining=[r for r in source if r['Full_Text_Status']!='LAWFUL_PMC_XML']
    if len(remaining)!=185 or len({r['Evidence_ID'] for r in remaining})!=185: raise SystemExit('remaining-185 identity mismatch')
    pmc=read(PMC); pmc_domains=Counter(r.get('Provisional_Decision','') for r in pmc)
    rows=[]
    for r in remaining:
        title=r['Title']; design=(r['Study_Design']+' '+r['Publication_Types']).lower(); domain=r['Domain']; notes=[]; score=0
        contrad=r['Evidence_ID'] in {'EV-0052','EV-0140','EV-1066'} or r['Contradictory_Flag']=='YES'
        repl=r['Replace_Existing_Flag']=='YES'
        p0='P0' in r['LOOP3X_Priority']
        brazil=('brazil' in title.lower() or 'brazil' in domain.lower() or r['Country'].lower()=='brazil')
        strong=any(x in design for x in ('systematic','meta-analysis','guideline','consensus','randomized','cohort'))
        direct=any(x in (title+' '+domain).lower() for x in ('police','military','firefighter','first responder','tactical','security'))
        if contrad: score+=50;notes.append('contradictory candidate')
        if repl: score+=35;notes.append('unresolved replacement candidate')
        if p0: score+=25;notes.append('P0 critical')
        if brazil: score+=18;notes.append('Brazil-specific relevance')
        if strong: score+=12;notes.append('potentially high-value design')
        if direct: score+=10;notes.append('direct tactical/occupational population')
        if r['LOOP3X_Final_Class'] in {'FULL_TEXT_REVIEW','REPLACE_EXISTING_CANDIDATE','CONTRADICTORY_CANDIDATE'}: score+=8
        cls='HIGH_IMPACT_ACCESS_REQUIRED' if score>=35 else ('MEDIUM_IMPACT_ACCESS_REQUIRED' if score>=18 else 'LOW_INCREMENTAL_VALUE_ACCESS_PENDING')
        route='Publisher OA / PubMed LinkOut / institutional or government repository; record version provenance before use'
        rows.append({'Evidence_ID':r['Evidence_ID'],'Title':title,'DOI':r['DOI'],'PMID':r['PMID'],'PMCID':r['PMCID'],'Year':r['Year'],'Study_Design':r['Study_Design'],'Population':r['Population'],'Domain':domain,'LOOP3X_Class':r['LOOP3X_Final_Class'],'Priority_Previous':r['LOOP3X_Priority'],'Claim_Relevance':'HIGH' if direct else 'MODERATE','Gap_Closure_Potential':'HIGH' if (contrad or repl or p0) else 'MODERATE','Replacement_Potential':'YES' if repl else 'NO','Contradictory_Potential':'YES' if contrad else 'NO','Population_Directness':'DIRECT' if direct else 'INDIRECT_OR_UNRESOLVED','Brazil_Relevance':'HIGH' if brazil else 'NOT_IDENTIFIED','International_Relevance':'HIGH' if direct else 'MODERATE','Study_Design_Value':'HIGH' if strong else 'UNRESOLVED_UNTIL_FULL_TEXT','Incremental_Value':'HIGH' if cls.startswith('HIGH') else ('MODERATE' if cls.startswith('MEDIUM') else 'LOW'),'Integrity_Status':r['Integrity_Status'],'Known_Access_Status':r['Full_Text_Status'],'Access_Priority_Score':str(score),'Access_Priority_Class':cls,'Access_Rationale':'; '.join(notes) or 'No structural signal of material claim, certainty, or reference-selection impact in available metadata.','Preferred_Access_Route':route,'Full_Text_Recovery_Status':'NOT_ATTEMPTED_IN_FT2','Next_Action':'Attempt lawful route only if queued by class; do not appraise in FT2.'})
    rows.sort(key=lambda x:(-int(x['Access_Priority_Score']),x['Evidence_ID']))
    fields=list(rows[0]);write('REMAINING185_ACCESS_PRIORITY_MASTER.csv',rows,fields)
    for cls,name in [('HIGH_IMPACT_ACCESS_REQUIRED','HIGH_IMPACT_ACCESS_REQUIRED.csv'),('MEDIUM_IMPACT_ACCESS_REQUIRED','MEDIUM_IMPACT_ACCESS_REQUIRED.csv'),('LOW_INCREMENTAL_VALUE_ACCESS_PENDING','LOW_INCREMENTAL_VALUE_ACCESS_PENDING.csv')]:write(name,[r for r in rows if r['Access_Priority_Class']==cls],fields)
    write('REMAINING185_DOMAIN_PRIORITY.csv',[{'Domain':d,'Remaining185':sum(x['Domain']==d for x in rows),'High':sum(x['Domain']==d and x['Access_Priority_Class'].startswith('HIGH') for x in rows),'PMC100_Decision_Context':'PMC100 has provisional-only coverage; no domain is declared saturated.'} for d in sorted({x['Domain'] for x in rows})])
    write('REMAINING185_REPLACEMENT_PRIORITY.csv',[r for r in rows if r['Replacement_Potential']=='YES'],fields)
    write('REMAINING185_CONTRADICTORY_PRIORITY.csv',[r for r in rows if r['Contradictory_Potential']=='YES'],fields)
    write('REMAINING185_ACCESS_ROUTE_PLAN.csv',[{'Evidence_ID':r['Evidence_ID'],'Access_Priority_Class':r['Access_Priority_Class'],'Preferred_Access_Route':r['Preferred_Access_Route'],'Recovery_Status':r['Full_Text_Recovery_Status'],'Next_Action':r['Next_Action']} for r in rows])
    gaps=[{'Gap':'No final Claim-Ready evidence','Status':'PERSISTS','Basis':'PMC100 remains AI-provisional; human confirmation is zero.'},{'Gap':'Brazil-direct evidence','Status':'PERSISTS','Basis':'Prioritize remaining Brazil-relevant records; no final synthesis.'},{'Gap':'Contradictory evidence appraisal','Status':'PERSISTS','Basis':'EV-0052, EV-0140 and EV-1066 remain high-priority access targets.'}]
    write('PMC100_GAP_UPDATE.csv',gaps)
    counts=Counter(r['Access_Priority_Class'] for r in rows)
    (OUT/'REMAINING185_PRIORITY_METHOD.md').write_text('# FT2 method\n\nThis is an access-ordering aid, not a scientific decision. Score = contradictory 50 + replacement 35 + P0 25 + Brazil relevance 18 + potentially high-value design 12 + direct population 10 + full-text-review class 8. HIGH is >=35, MEDIUM 18-34, LOW <18. Availability is deliberately not a score component.\n',encoding='utf-8')
    (OUT/'BATCH10_4B_FT2_MANIFEST.json').write_text(json.dumps({'phase':'BATCH 10.4B-FT2','state':'REMAINING185_ACCESS_PRIORITIZATION_COMPLETE','remaining_universe':185,'prioritized':len(rows),'classes':counts,'cef_v1_changed':False,'manuscript_changed':False,'reference_saturation':False,'ev_1379':'FAIL_CLOSED'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'BATCH10_4B_FT2_REPORT.md').write_text(f'# Batch 10.4B-FT2\n\nAll 185 non-PMC records were access-prioritized: HIGH {counts["HIGH_IMPACT_ACCESS_REQUIRED"]}, MEDIUM {counts["MEDIUM_IMPACT_ACCESS_REQUIRED"]}, LOW {counts["LOW_INCREMENTAL_VALUE_ACCESS_PENDING"]}. This does not appraise, include, exclude, or recover full texts. The next permitted action is FT3 lawful recovery for HIGH only.\n',encoding='utf-8')
    print(json.dumps({'total':len(rows),'classes':counts},ensure_ascii=False))
if __name__=='__main__':main()
