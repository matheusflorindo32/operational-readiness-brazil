"""FT6: gap-led selection of MEDIUM records; no access recovery or appraisal."""
from __future__ import annotations

import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "ft6"; OUT.mkdir(parents=True, exist_ok=True)
MEDIUM = ROOT / "batch10_4b" / "ft2" / "MEDIUM_IMPACT_ACCESS_REQUIRED.csv"
FT1 = ROOT / "batch10_4b" / "ft1" / "artifacts" / "PMC100_DOMAIN_COVERAGE.csv"
HIGH = ROOT / "batch10_4b" / "ft5" / "HIGH22_ACCESS_REMEDIATION_MASTER.csv"
CLAIMS = ROOT / "batch10_4b" / "ft1" / "artifacts" / "PMC100_CLAIM_CITATION_MATRIX.csv"

DOMAINS = [
    ("Operational / occupational readiness", "CRITICAL_GAP", "No direct FT1 domain ledger; operational outcomes remain fragmented."),
    ("Physical / academy readiness", "UNRESOLVED_DUE_TO_ACCESS", "22 FT1 records; two contradictory HIGH and replacement HIGH remain inaccessible."),
    ("Nutrition", "UNRESOLVED_DUE_TO_ACCESS", "Nutrition/shift FT1 records exist, but a contradictory HIGH and replacement candidates remain inaccessible."),
    ("Shift work", "IMPORTANT_GAP", "Current coverage is grouped with nutrition; direct shift-work evidence is not separately established."),
    ("Sleep / fatigue / recovery", "PARTIALLY_COVERED", "Nine FT1 records plus bounded HIGH3 caffeine synthesis; transferability remains limited."),
    ("Mental health / stress", "IMPORTANT_GAP", "Nine FT1 records, but direct operational-readiness and implementation implications remain incomplete."),
    ("Cognition", "UNRESOLVED_DUE_TO_ACCESS", "Cognition/firearm coverage exists, but two HIGH replacement candidates remain inaccessible."),
    ("Firearm / operational performance", "IMPORTANT_GAP", "Eight FT1 cognition/firearm records; direct operational outcome support remains incomplete."),
    ("Medical / cardiovascular readiness", "PARTIALLY_COVERED", "Six FT1 records and one direct but bounded PMDF HIGH3 study."),
    ("Musculoskeletal injury", "PARTIALLY_COVERED", "Nineteen FT1 records and direct Brazil context, but causal/prevention support remains bounded."),
    ("Tactical medicine", "UNRESOLVED_DUE_TO_ACCESS", "P0 HIGH records remain inaccessible."),
    ("TCCC / TECC / APH", "UNRESOLVED_DUE_TO_ACCESS", "P0 HIGH records remain inaccessible."),
    ("Implementation science", "IMPORTANT_GAP", "Six FT1 records; institutional/public-safety implementation directness remains incomplete."),
    ("Organizational / policy readiness", "CRITICAL_GAP", "No separately completed FT1 coverage category."),
    ("Hydration / heat", "PARTIALLY_COVERED", "Two FT1 records; P0 hydration HIGH remains inaccessible."),
    ("Monitoring / wearables", "IMPORTANT_GAP", "No separately completed FT1 coverage category."),
    ("Brazil-specific evidence", "IMPORTANT_GAP", "Only bounded HIGH3 Brazil evidence documented; cross-institutional transferability unknown."),
    ("International transferability", "IMPORTANT_GAP", "Evidence is heterogeneous across military, police and first-responder contexts."),
]

DOMAIN_ALIASES = {
    "Nutrition / shift work": ["Nutrition", "Shift work"],
    "Physical / academy readiness": ["Physical / academy readiness", "Operational / occupational readiness"],
    "Cognition / firearm performance": ["Cognition", "Firearm / operational performance"],
    "Medical / cardiovascular readiness": ["Medical / cardiovascular readiness"],
    "Musculoskeletal injury": ["Musculoskeletal injury"],
    "Sleep / fatigue / recovery": ["Sleep / fatigue / recovery"],
    "Mental health / stress": ["Mental health / stress"],
    "Tactical medicine / TCCC / TECC / APH": ["Tactical medicine", "TCCC / TECC / APH"],
    "Hydration / heat / thermoregulation": ["Hydration / heat"],
    "Implementation science": ["Implementation science", "Organizational / policy readiness"],
}
CLAIM_TERMS = {
    "Operational / occupational readiness": ("operational", "occupational readiness"),
    "Physical / academy readiness": ("physical", "fitness", "academy", "bodycomposition"),
    "Nutrition": ("nutrition", "diet", "supplement", "caffeine"),
    "Shift work": ("shift", "schedule", "workload"),
    "Sleep / fatigue / recovery": ("sleep", "fatigue", "recovery"),
    "Mental health / stress": ("mental", "stress", "psychological", "ptsd"),
    "Cognition": ("cognition", "cognitive"),
    "Firearm / operational performance": ("firearm", "shoot", "marksmanship"),
    "Medical / cardiovascular readiness": ("cardiovascular", "medical", "cvd"),
    "Musculoskeletal injury": ("musculoskeletal", "injury", "msk"),
    "Tactical medicine": ("tacmed", "tactical medicine", "hemorrhage"),
    "TCCC / TECC / APH": ("tccc", "tecc", "aph", "prehospital"),
    "Implementation science": ("implementation", "acceptability", "barriers"),
    "Organizational / policy readiness": ("organizational", "policy", "portfolio"),
    "Hydration / heat": ("hydration", "heat", "thermoregulation"),
    "Monitoring / wearables": ("monitoring", "wearable", "telehealth"),
    "Brazil-specific evidence": ("brazil", "brazilian", "police"),
    "International transferability": ("transferability", "international"),
}

def read(path):
    with path.open(encoding="utf-8", newline="") as f: return list(csv.DictReader(f))
def write(name, rows):
    with (OUT/name).open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["Evidence_ID"]); w.writeheader(); w.writerows(rows)
def points(value, weights): return weights.get(value, 0)

def main():
    medium = read(MEDIUM); assert len(medium)==109 and len({r['Evidence_ID'] for r in medium})==109
    ft1 = {r['Domain']:r for r in read(FT1)}; high = read(HIGH); claim_rows=read(CLAIMS)
    claim_by_domain = {}
    for claim in claim_rows:
        cid=claim.get('Claim_ID',''); wording=claim.get('Claim_Current_Wording','')
        hay=(cid+' '+wording).lower()
        for domain, terms in CLAIM_TERMS.items():
            if any(term in hay for term in terms): claim_by_domain.setdefault(domain, []).append((cid, wording))
    high_by_domain={}
    for r in high:
        for d in DOMAIN_ALIASES.get(r['Domain'],[]): high_by_domain.setdefault(d,[]).append(r)
    coverage=[]
    for domain,status,reason in DOMAINS:
        ft1_match = next((row for key,row in ft1.items() if domain in DOMAIN_ALIASES.get(key,[])), None)
        h=high_by_domain.get(domain,[])
        coverage.append({"Domain":domain,"Gap_Status":status,"Rationale":reason,"PMC100_Reviewed":ft1_match['Reviewed_In_FT1'] if ft1_match else "0 — not separately categorized","PMC100_Status":ft1_match['Status'] if ft1_match else "NOT_SEPARATELY_CATEGORIZED","HIGH_Unresolved":str(len(h)),"Unresolved_HIGH_Exists":"YES" if h else "NO","Contradictory_Access_Gap_Persists":"YES" if any(x['Contradictory_Flag']=='YES' for x in h) else "NO","HIGH3_Contribution":"EV-1462 bounded sleep-loss caffeine" if domain=="Sleep / fatigue / recovery" else ("EV-1463 bounded PMDF surveillance" if domain=="Medical / cardiovascular readiness" else ("EV-1466 context-only Bahia pain" if domain=="Musculoskeletal injury" else "None documented")),"Current_Claim_Examples":" | ".join(cid for cid,_ in claim_by_domain.get(domain,[])[:3]) or "NR — no claim mapped in FT1 matrix"})
    write("DOMAIN_GAP_ANALYSIS_MASTER.csv",coverage); write("DOMAIN_COVERAGE_COMBINED_PMC100_HIGH3.csv",coverage)
    claim_gap=[]
    for domain,status,_ in DOMAINS:
        mapped=claim_by_domain.get(domain,[]) or [(f"GAP-{domain.upper().replace(' / ','-').replace(' ','-')}","No explicitly mapped current claim in the reviewed ledger; domain-gap placeholder only.")]
        for cid, wording in mapped:
            h=high_by_domain.get(domain,[])
            claim_gap.append({"Claim_ID":cid,"Current_Wording":wording,"Domain":domain,"Evidence_Strength":"AI-provisional only; Claim-Ready 0","Directness":"Heterogeneous/claim-specific","Current_Problems":"No final human-confirmed synthesis; access and transferability constraints.","Missing_Population":"Brazilian public-safety validation where applicable","Missing_Outcome":"Operationally meaningful outcome or implementation outcome where not directly observed","Missing_Design":"Design-specific appraisal pending","Contradictory_Evidence":"YES — access unresolved" if any(x['Contradictory_Flag']=='YES' for x in h) else "No unresolved HIGH contradictory flag mapped","Replacement_Need":"YES" if any(x['Replacement_Flag']=='YES' for x in h) else "NO documented HIGH replacement flag","Brazil_Gap":"YES" if domain in {"Brazil-specific evidence","Medical / cardiovascular readiness","Musculoskeletal injury"} else "POSSIBLE","International_Gap":"YES" if status in {"CRITICAL_GAP","IMPORTANT_GAP","UNRESOLVED_DUE_TO_ACCESS"} else "POSSIBLE","MEDIUM_Candidate_Need":"YES" if status in {"CRITICAL_GAP","IMPORTANT_GAP","UNRESOLVED_DUE_TO_ACCESS"} else "NO"})
    write("CLAIM_LEVEL_GAP_ANALYSIS.csv",claim_gap)
    write("UNRESOLVED_HIGH_IMPACT_MAP.csv",[{"Evidence_ID":r['Evidence_ID'],"Title":r['Title'],"Domain":r['Domain'],"Contradictory":r['Contradictory_Flag'],"Replacement":r['Replacement_Flag'],"P0":r['P0_Flag'],"Access_Status":r['Final_Access_Status'],"Appraisal_Ready":r['Appraisal_Ready'],"Gap_Visibility":"PRESERVED"} for r in high])
    gap_status={d:s for d,s,_ in DOMAINS}
    decisions=[]
    for r in medium:
        applicable=DOMAIN_ALIASES.get(r['Domain'],[r['Domain']]); severity=next((gap_status[d] for d in applicable if d in gap_status),"IMPORTANT_GAP")
        score=(points(r['Claim_Relevance'],{'HIGH':2,'MODERATE':1})+points(r['Gap_Closure_Potential'],{'HIGH':3,'MODERATE':1})+points(r['Population_Directness'],{'DIRECT':2,'INDIRECT_OR_UNRESOLVED':0})+points(r['Brazil_Relevance'],{'HIGH':2,'MODERATE':1})+points(r['International_Relevance'],{'HIGH':1,'MODERATE':1})+points(r['Replacement_Potential'],{'YES':2})+points(r['Contradictory_Potential'],{'YES':2})+points(r['Study_Design_Value'],{'HIGH':2,'MODERATE':1})+points(r['Incremental_Value'],{'HIGH':2,'MODERATE':1})+ (2 if severity=='CRITICAL_GAP' else 1 if severity in {'IMPORTANT_GAP','UNRESOLVED_DUE_TO_ACCESS'} else 0))
        selected = score >= 9 and (severity in {'CRITICAL_GAP','IMPORTANT_GAP','UNRESOLVED_DUE_TO_ACCESS'} or r['Brazil_Relevance']=='HIGH' or r['Contradictory_Potential']=='YES')
        low = score <= 3
        decision='MEDIUM_TARGETED_REVIEW_REQUIRED' if selected else ('MEDIUM_LOW_INCREMENTAL_VALUE_AFTER_GAP_ANALYSIS' if low else 'MEDIUM_DEFER')
        priority='M1 — CRITICAL' if selected and (severity=='CRITICAL_GAP' or r['Contradictory_Potential']=='YES') else ('M2 — HIGH' if selected and score>=12 else ('M3 — MODERATE' if selected else 'NOT_SELECTED'))
        claim_id=next((x['Claim_ID'] for x in claim_gap if x['Domain'] in applicable and not x['Claim_ID'].startswith('GAP-')),f"GAP-{applicable[0].upper().replace(' / ','-').replace(' ','-')}")
        decisions.append({**r,"Gap_Type":applicable[0],"Gap_Severity":severity,"Claim_ID":claim_id,"Targeted_Medium_Priority":priority,"Selection_Decision":decision,"Selection_Score":str(score),"Selection_Rationale":"Metadata-only, gap-linked prioritization; no full-text or quality appraisal inferred.","Expected_Contribution":"Test whether this record closes the named gap or improves directness; otherwise retain defer status.","Next_Action":"FT7 lawful full-text access only" if selected else "Do not recover in FT7; retain in queue."})
    assert len(decisions)==109 and len({r['Evidence_ID'] for r in decisions})==109
    write("MEDIUM109_INCREMENTAL_VALUE_SCREEN.csv",decisions)
    selected=[r for r in decisions if r['Selection_Decision']=='MEDIUM_TARGETED_REVIEW_REQUIRED']; deferred=[r for r in decisions if r['Selection_Decision']!='MEDIUM_TARGETED_REVIEW_REQUIRED']
    queue_headers=['Evidence_ID','Title','DOI','PMID','Year','Study_Design','Population','Domain','Claim_ID','Gap_Type','Gap_Severity','Population_Directness','Brazil_Relevance','International_Relevance','Replacement_Potential','Contradictory_Potential','Incremental_Value','Known_Access_Status','Targeted_Medium_Priority','Selection_Rationale','Expected_Contribution','Next_Action']
    write("TARGETED_MEDIUM_REVIEW_QUEUE.csv",[{key:r.get(key,'') for key in queue_headers} for r in selected])
    write("TARGETED_MEDIUM_PRIORITY.csv",[{"Evidence_ID":r['Evidence_ID'],"Targeted_Medium_Priority":r['Targeted_Medium_Priority'],"Selection_Score":r['Selection_Score'],"Gap_Severity":r['Gap_Severity'],"Rationale":r['Selection_Rationale']} for r in selected])
    write("MEDIUM_DEFER_LEDGER.csv",[r for r in deferred if r['Selection_Decision']=='MEDIUM_DEFER'])
    write("MEDIUM_REDUNDANCY_LEDGER.csv",[r for r in deferred if r['Selection_Decision']=='MEDIUM_LOW_INCREMENTAL_VALUE_AFTER_GAP_ANALYSIS'])
    write("TARGETED_MEDIUM_ACCESS_PLAN.csv",[{"Evidence_ID":r['Evidence_ID'],"Priority":r['Targeted_Medium_Priority'],"Preferred_Access_Route":r['Preferred_Access_Route'],"Known_Access_Status":r['Known_Access_Status'],"Scope_Boundary":"FT7 access/identity/provenance only; no appraisal."} for r in selected])
    counts={k:sum(r['Selection_Decision']==k for r in decisions) for k in ['MEDIUM_TARGETED_REVIEW_REQUIRED','MEDIUM_DEFER','MEDIUM_LOW_INCREMENTAL_VALUE_AFTER_GAP_ANALYSIS']}
    pri={k:sum(r['Targeted_Medium_Priority']==k for r in selected) for k in ['M1 — CRITICAL','M2 — HIGH','M3 — MODERATE']}
    report=f"""# Batch 10.4B-FT6 — domain-gap analysis and targeted MEDIUM selection\n\nFT6 assessed all 109/109 MEDIUM metadata records against the documented PMC100, HIGH3 and unresolved-HIGH state. It performed no full-text retrieval, appraisal, manuscript/CEF/Zotero change or final reference decision.\n\n- Targeted review required: {counts['MEDIUM_TARGETED_REVIEW_REQUIRED']}/109\n- Deferred: {counts['MEDIUM_DEFER']}/109\n- Low incremental value: {counts['MEDIUM_LOW_INCREMENTAL_VALUE_AFTER_GAP_ANALYSIS']}/109\n- Selected priorities: {json.dumps(pri)}\n- Unresolved HIGH contradictories retained: EV-0052, EV-0140, EV-1066\n\nThe selection is metadata-only and reversible. It does not treat accessibility, recency, systematic-review label, positive findings or Brazilian setting as sufficient for evidence inclusion. Every selected MEDIUM is linked to a domain gap and provisional claim identifier.\n\n## Gate\n\n`TARGETED_MEDIUM_QUEUE_READY`: {len(selected)} records are eligible for **FT7 lawful access and identity remediation only**. No appraisal should start automatically.\n"""
    (OUT/'BATCH10_4B_FT6_REPORT.md').write_text(report,encoding='utf-8')
    files=sorted(p for p in OUT.iterdir() if p.name!='BATCH10_4B_FT6_MANIFEST.json')
    manifest={"batch":"BATCH10_4B_FT6","gate":"TARGETED_MEDIUM_QUEUE_READY","medium_assessed":109,"selected":len(selected),"deferred":len(deferred),"priorities":pri,"cef_v1":"UNCHANGED","zotero":"UNCHANGED","manuscript":"UNCHANGED","files":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (OUT/'BATCH10_4B_FT6_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+"\n",encoding='utf-8')

if __name__=='__main__': main()
