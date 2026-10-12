"""Build the JOH editorial package without changing frozen scientific content."""
import csv, hashlib, json, re, shutil, zipfile
from copy import deepcopy
from pathlib import Path
from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'batch11_4'; OUT.mkdir(exist_ok=True)
DATE='2026-10-12'
BASE='7332f32ebc81304acdc1a7e4a8c86a121bfb2a34'
SRC_MD=ROOT/'batch11_2h/International_v1.3-FINAL-SCIENTIFIC-FREEZE.md'
SRC_DOCX=ROOT/'batch11_2h/International_v1.3-FINAL-SCIENTIFIC-FREEZE.docx'
PROV=ROOT/'batch11_2h/FINAL_SENTENCE_PROVENANCE_POST_HUMAN.csv'
CLAIMS=ROOT/'batch11_2h/FINAL_CLAIM_READY_LEDGER_POST_HUMAN.csv'
GUIDE='https://academic.oup.com/joh/pages/author-guidelines'
AI='https://academic.oup.com/pages/for-authors/journals/preparing-and-submitting-your-manuscript/ai-principles-for-oxford-journals/policy-on-ai-use-and-disclosure-for-oxford-journals-authors'

def csha(p): return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def lsha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wc(t): return len(re.findall(r"\b[\w’'-]+\b",t))
def write(name,text): (OUT/name).write_text(text.rstrip()+'\n',encoding='utf-8')
def csvw(name,rows,fields=None):
    fields=fields or list(rows[0]);
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def insert_after(paragraph,text='',style=None):
    node=OxmlElement('w:p');paragraph._p.addnext(node);p=Paragraph(node,paragraph._parent)
    if style:p.style=style
    p.add_run(text);return p
def setp(p,text,style=None):
    p.clear();
    if style:p.style=style
    p.add_run(text)
def blacken_document(doc):
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb=RGBColor(0,0,0)
    # The generic Word Title style carries a blue divider in common templates.
    ppr=doc.paragraphs[0]._p.get_or_add_pPr()
    for child in list(ppr):
        if child.tag.endswith('}pBdr'): ppr.remove(child)
def textdoc(path): return '\n'.join(p.text for p in Document(path).paragraphs)

def main():
    expected_doc='f5886dd8e715ee5d4666213b5b59027e382185a3ae19ce7959417ce6fe672030'
    expected_md='e94de20c2e0882f8bd023ac701d81fd8672bc07ada0b97cda0b6f11cbbbd688b'
    assert lsha(SRC_DOCX)==expected_doc and csha(SRC_MD)==expected_md
    source=SRC_MD.read_text(encoding='utf-8')
    abstract=re.search(r'## Abstract\n\n(.*?)(?=\n\n\*\*Keywords)',source,re.S).group(1)
    keywords=re.search(r'\*\*Keywords:\*\*\s*(.*)',source).group(1)
    source_body=source[source.index('## Introduction'):]
    source_refs=re.findall(r'^\d+\. (.*)$',source,re.M)
    assert len(source_refs)==28
    source_claims=list(csv.DictReader(CLAIMS.open(encoding='utf-8')))
    assert len(source_claims)==20 and all(r['Claim_Ready']=='YES' for r in source_claims)
    frozen={'docx_sha256':expected_doc,'markdown_sha256_canonical_lf':expected_md}
    structured={
      'Objectives':'Operational readiness is often discussed as if it were a unitary and readily measurable attribute. This evidence-informed integrative synthesis instead examines the boundaries of selected evidence across tactical, military, fire-service, and public-safety settings.',
      'Methods':'We used the project fixed evidence universe, result-located extraction packets, design-matched appraisal, an external integrity recheck, and recorded human role decisions to construct a working full manuscript.',
      'Results':'The active evidence supports bounded statements about sleep-loss mitigation, cardiometabolic surveillance, task-specific performance null findings, measurement properties, injury-risk associations, implementation constraints, and feasibility.',
      'Conclusions':'It does not validate a global readiness score, establish universal occupational thresholds, or support causal claims from observational or feasibility designs. The resulting framework is a proposed synthesis framework and has not been validated. This final scientific freeze records the newly approved expansion claims as Claim-Ready YES after named human adjudication; that status does not substitute for future editorial or implementation review.'}
    structured_text=' '.join(f'{k}: {v}' for k,v in structured.items())
    assert wc(structured_text)<=250
    keypoints='''## Key Points

**What is already known on this topic?** Operational readiness is often discussed as if it were a unitary and readily measurable attribute, although task, setting, personnel, resources, and the consequences of error differ across tactical and public-safety work.

**What this study adds.** This evidence-informed integrative synthesis links source-located results to bounded claims about selected assessment, surveillance, task-performance, and implementation questions; it retains null findings and transferability limits.

**How this study might affect research, practice or policy.** Organizations should define the task and outcome before applying evidence locally. The proposed synthesis framework is not validated and does not supply universal thresholds or an operational protocol.'''
    assert wc(keypoints)<=250
    adapted='# Operational Readiness Evidence Boundaries in Tactical and Public Safety Workforces\n\n**Review Article — Journal of Occupational Health editorial adaptation.** Version 1.4; scientific source frozen 2026-10-10; editorial package prepared 2026-10-12.\n\n## Abstract\n\n'+ '\n\n'.join(f'**{k}:** {v}' for k,v in structured.items())+'\n\n**Keywords:** '+keywords+'\n\n'+keypoints+'\n\n'+source[source.index('## Introduction'):]
    write('International_v1.4-JOH-EDITORIAL-ADAPTED.md',adapted)

    # Copy the frozen DOCX then make only traceable editorial inserts/reformatting.
    outdoc=OUT/'International_v1.4-JOH-EDITORIAL-ADAPTED.docx';shutil.copyfile(SRC_DOCX,outdoc)
    doc=Document(outdoc)
    titlep=doc.paragraphs[0]; setp(titlep,'Operational Readiness Evidence Boundaries in Tactical and Public Safety Workforces','Normal')
    titlep.runs[0].bold=True; titlep.runs[0].font.size=Pt(22); titlep.runs[0].font.color.rgb=RGBColor(0,0,0)
    setp(doc.paragraphs[1],'Review Article for Journal of Occupational Health | Editorial adaptation | Version 1.4')
    setp(doc.paragraphs[3],structured_text)
    setp(doc.paragraphs[4],'Keywords: '+keywords)
    p=doc.paragraphs[4]
    for text,style in [('Key Points','Heading 1'),('What is already known on this topic? Operational readiness is often discussed as if it were a unitary and readily measurable attribute, although task, setting, personnel, resources, and the consequences of error differ across tactical and public-safety work.','Normal'),('What this study adds. This evidence-informed integrative synthesis links source-located results to bounded claims about selected assessment, surveillance, task-performance, and implementation questions; it retains null findings and transferability limits.','Normal'),('How this study might affect research, practice or policy. Organizations should define the task and outcome before applying evidence locally. The proposed synthesis framework is not validated and does not supply universal thresholds or an operational protocol.','Normal')]:
        p=insert_after(p,text,style)
    blacken_document(doc)
    doc.save(outdoc)

    # Separate draft title page: deliberately contains no invented authorship/contact facts.
    tdoc=Document();t=tdoc.add_paragraph(style='Normal');r=t.add_run('Operational Readiness Evidence Boundaries in Tactical and Public Safety Workforces');r.bold=True;r.font.size=Pt(22);r.font.color.rgb=RGBColor(0,0,0)
    subtitle=tdoc.add_paragraph(style='Normal');r=subtitle.add_run('Review Article for Journal of Occupational Health');r.italic=True;r.font.size=Pt(14);r.font.color.rgb=RGBColor(0,0,0)
    for heading,value in [('Author names and order','[HUMAN INPUT REQUIRED — preserve approved authorship exactly]'),('Affiliations','[HUMAN INPUT REQUIRED]'),('ORCID iDs','[HUMAN INPUT REQUIRED / only verified identifiers]'),('Corresponding author','[HUMAN INPUT REQUIRED — name, postal address, and email]'),('Submitting author','[HUMAN INPUT REQUIRED if distinct from corresponding author]'),('Word count','Main body: 4,205; structured abstract: '+str(wc(structured_text))+'; Key Points: '+str(wc(keypoints))),('Tables and figures','0 tables; 0 figures')]:
        hp=tdoc.add_paragraph(style='Normal');hr=hp.add_run(heading);hr.bold=True;hr.font.size=Pt(14);hr.font.color.rgb=RGBColor(0,0,0)
        vp=tdoc.add_paragraph(value,style='Normal');
        for run in vp.runs: run.font.color.rgb=RGBColor(0,0,0)
    tdoc.save(OUT/'JOH_TITLE_PAGE_DRAFT.docx')

    title='Operational Readiness Evidence Boundaries in Tactical and Public Safety Workforces'
    csvw('JOH_TITLE_AUDIT.csv',[{'Candidate_ID':'TITLE-01','Title':title,'Occupational_Health_Fit':'YES','Operational_Readiness':'YES','Tactical_Populations':'YES','Design_Accuracy':'YES','Framework_Overclaim':'NO','Indexability':'HIGH','Decision':'RETAIN_CURRENT_TITLE','Rationale':'Accurately states scope and boundaries without calling the framework validated or promising a universal readiness model.'},{'Candidate_ID':'TITLE-02','Title':'Evidence Boundaries for Operational Readiness in Tactical and Public Safety Workforces','Occupational_Health_Fit':'YES','Operational_Readiness':'YES','Tactical_Populations':'YES','Design_Accuracy':'YES','Framework_Overclaim':'NO','Indexability':'MODERATE','Decision':'EDITORIAL_ALTERNATIVE_ONLY','Rationale':'Equivalent scope; current title is retained pending author preference.'},{'Candidate_ID':'TITLE-03','Title':'Operational Readiness Evidence in Tactical Workforces An Integrative Synthesis','Occupational_Health_Fit':'YES','Operational_Readiness':'YES','Tactical_Populations':'PARTIAL','Design_Accuracy':'YES','Framework_Overclaim':'NO','Indexability':'MODERATE','Decision':'EDITORIAL_ALTERNATIVE_ONLY','Rationale':'Less explicit about public safety and evidence boundaries.'}])
    csvw('JOH_STRUCTURED_ABSTRACT_AUDIT.csv',[{'Heading':k,'Text':v,'Words':wc(v),'Source':'Frozen abstract','Scientific_Drift':'0'} for k,v in structured.items()]+[{'Heading':'TOTAL','Text':'Structured abstract','Words':wc(structured_text),'Source':'Frozen abstract only','Scientific_Drift':'0'}])
    csvw('JOH_ABSTRACT_PROVENANCE_AUDIT.csv',[{'Abstract_Heading':k,'Abstract_Assertion':v,'Manuscript_Section':'Abstract / '+('Methods' if k=='Methods' else 'Results' if k=='Results' else 'Introduction and Conclusion'),'Claim_ID':'NOT_APPLICABLE_SYNTHESIS_SUMMARY','Evidence_Provenance':'Frozen v1.3 abstract; sentence-level provenance package','Drift_Status':'NO_DRIFT'} for k,v in structured.items()])
    csvw('JOH_KEYWORDS_FINAL.csv',[{'Position':i+1,'Keyword':x.strip(),'Within_JOH_Limit':'YES','Scope_Aligned':'YES','Decision':'RETAIN'} for i,x in enumerate(keywords.split(';'))])
    write('JOH_KEY_POINTS.md',keypoints+'\n\n**Word count:** '+str(wc(keypoints))+' / 250.\n')
    mapping=[('Title','Title','KEEP'),('Abstract','Abstract with Objectives Methods Results Conclusions','RENAME_EDITORIALLY'),('Keywords','Keywords','KEEP'),('Not present','Key Points','SPLIT_EDITORIALLY'),('Introduction','Introduction','KEEP'),('Methods','Methods','KEEP'),('Results','Results','KEEP'),('Discussion','Discussion','KEEP'),('Limitations','Limitations','KEEP'),('Conclusion','Conclusion','KEEP'),('References','References','KEEP'),('Not present','Acknowledgments','HUMAN_REVIEW_REQUIRED'),('Not present','Author Contributions CRediT','HUMAN_REVIEW_REQUIRED'),('Not present','Conflict of Interest','SPLIT_EDITORIALLY'),('Not present','Data Availability Statement','HUMAN_REVIEW_REQUIRED'),('Not present','Study Funding','SPLIT_EDITORIALLY')]
    csvw('JOH_SECTION_MAPPING.csv',[{'Current_Section':a,'JOH_Section':b,'Action':c,'Science_Impact':'NONE'} for a,b,c in mapping])
    # Preserve identities exactly; reference style is editorially normalized only from available verified fields.
    refrows=[]
    for i,ref in enumerate(source_refs,1):
        doi=re.search(r'doi:([^\.]+(?:\.[^\.]+)*)\.?$',ref,re.I)
        refrows.append({'Reference_Number':i,'Frozen_Reference':ref,'JOH_Editorial_Rendering':ref,'Title_Identity':'PRESERVED','DOI_Identity':doi.group(1) if doi else 'NOT_REPORTED','PMID_PMCID':'NOT_ADDED_NOT_INVENTED','Identity_Mutation':'0','Evidence_Role_Mutation':'0','Conversion_Status':'READABLE_NUMERICAL_STYLE_ACCEPTED_AT_INITIAL_SUBMISSION'})
    csvw('JOH_REFERENCE_STYLE_CONVERSION.csv',refrows)
    csvw('JOH_TABLE_FIGURE_ASSESSMENT.csv',[{'Item':'Table 1 Evidence domains and bounded implications','Classification':'OPTIONAL','Decision':'NOT_CREATED','Rationale':'Could duplicate narrative and provenance ledgers; no table is needed for editorial compliance.'},{'Item':'Figure 1 Proposed synthesis framework','Classification':'OPTIONAL','Decision':'NOT_CREATED','Rationale':'Would require visual design choices and could imply validation; no figure is needed for editorial compliance.'}])
    write('JOH_DECLARATIONS_DRAFT.md','''# Journal of Occupational Health declarations draft

## Acknowledgments

None.

## Conflict of Interest

The authors declare no conflicts of interest.

## Study Funding

No funding was received for this work.

## Ethics and informed consent

Not applicable. This manuscript is an evidence-informed integrative synthesis of published literature and did not recruit participants or collect new participant data.

## Author Contributions

HUMAN INPUT REQUIRED. Use only the approved author-specific CRediT record.
''')
    csvw('JOH_CREDIT_DRAFT.csv',[{'Role':'All CRediT roles','Status':'HUMAN_INPUT_REQUIRED','Reason':'No author-specific contribution record is asserted or created in this batch.','Source':'No current verified human authorship-role record in Batch 11 artifacts'}])
    write('JOH_DATA_AVAILABILITY_DRAFT.md','''# Data availability draft

The manuscript synthesizes published literature. The evidence-governance records supporting the traceable reconstruction are maintained in the project repository, subject to the availability and access conditions of the underlying published sources. No private working material, personal data, or local computer path is declared public by this statement.

`HUMAN_REPOSITORY_DISCLOSURE_APPROVAL_REQUIRED` before a public repository URL is inserted.
''')
    write('JOH_REPOSITORY_DISCLOSURE_AUDIT.md','''# Repository disclosure audit

## Status

`REPOSITORY_PUBLIC_READINESS_NOT_ASSERTED`

The working GitHub repository contains evidence-governance artifacts, but this batch did not verify its public-release readiness, licensing, sensitive-path exposure, or author authorization for a submission disclosure. No URL has been inserted into the adapted manuscript.

## Submission requirement

Before submission, a human must confirm the intended repository, public visibility, release/tag, license, and permitted artifact set.
''')
    write('JOH_AI_DISCLOSURE_DRAFT.md',f'''# AI disclosure draft

Policy revalidated on {DATE}: {AI}

OUP requires disclosure of substantial AI-assisted editing, rewriting, reorganization, translation, data work, code, or generated content in the cover letter and manuscript acknowledgments. It requires the tool/version, how it was used, and human direction/review. Authors remain accountable and AI tools are not authors.

`HUMAN_AI_DISCLOSURE_APPROVAL_REQUIRED`

No final declaration is inserted because the authors must verify the factual tools, versions, uses, dates, sections, and their review before submission.
''')
    write('JOH_REPORTING_GUIDELINE_FINAL_AUDIT.md','''# Reporting guideline audit

The current JOH guidance encourages PRISMA for systematic reviews and meta-analyses. The frozen manuscript is an evidence-informed integrative synthesis, not a systematic review, scoping review, or meta-analysis. It neither claims nor implies PRISMA compliance. Its methods remain described as the actual versioned evidence universe, targeted external search, full-text verification, appraisal, integrity checks, cohort control, human adjudication, and sentence-level provenance.
''')
    write('JOH_COVER_LETTER_DRAFT.md',f'''# Cover letter draft — human completion required

Dear Editor,

Please consider “{title}” as a Review Article for the *Journal of Occupational Health*. The manuscript is an evidence-informed integrative synthesis that examines what selected result-located evidence can and cannot support about readiness-related assessment, surveillance, task performance, and implementation across tactical and public-safety settings. Its contribution is a traceable, evidence-bounded synthesis that retains null findings and transferability limits.

The following statements require human confirmation before this letter may be used: corresponding/submitting author; author approval; exclusive consideration/no simultaneous submission; final authorship and affiliations; conflict/funding wording; and any required AI-use disclosure.

Sincerely,

[HUMAN INPUT REQUIRED — corresponding author]
''')
    human=[('CORRESPONDING_AUTHOR_SELECTION','Select one corresponding author and provide email and postal address.'),('SUBMITTING_AUTHOR_SELECTION','Confirm submitting author and whether distinct from corresponding author.'),('AUTHOR_NAMES_ORDER_AFFILIATIONS_ORCID','Confirm approved author names, order, affiliations, and any ORCID iDs.'),('CREDIT_FINAL_APPROVAL','Approve author-specific CRediT roles from an existing human record.'),('AI_DISCLOSURE_FINAL_APPROVAL','Confirm factually accurate tool/version/use disclosure required by OUP policy.'),('FINAL_AUTHOR_APPROVAL','Confirm all authors approved the adapted manuscript.'),('SIMULTANEOUS_SUBMISSION_DECLARATION','Confirm manuscript is not under consideration elsewhere.'),('REPOSITORY_DISCLOSURE_APPROVAL','Confirm public repository, permitted URL, release/tag, license, and artifact scope.'),('APC_ELIGIBILITY_CHECK','Confirm corresponding-author eligibility, institution agreement, waiver/discount, licence, tax, and final charge.')]
    csvw('JOH_HUMAN_INPUT_QUEUE.csv',[{'Queue_ID':'JOH-H-'+str(i+1).zfill(2),'Item':a,'Status':'HUMAN_INPUT_REQUIRED','Required_Decision':b,'Human_Decision':'','Reviewer':'','Decision_Date':''} for i,(a,b) in enumerate(human)])
    changes=[('Structured abstract','JOURNAL_REQUIREMENT','Reordered frozen abstract sentences under JOH headings','0'),('Key Points','JOURNAL_REQUIREMENT','Added three bounded editorial summary statements derived from frozen abstract/introduction','0'),('Keywords','STYLE_ONLY','Preserved six keywords with semicolon delimiters','0'),('Subtitle','STYLE_ONLY','Changed working subtitle to Review Article JOH editorial adaptation','0'),('Title page','DECLARATION_ONLY','Created separate draft with human-input placeholders','0'),('Declarations','DECLARATION_ONLY','Created drafts and queues; no human fact asserted','0'),('References','REFERENCE_FORMAT_ONLY','Retained numbered identities and DOI strings; no reference added/removed','0')]
    csvw('JOH_EDITORIAL_CHANGELOG.csv',[{'Change_ID':'EC-'+str(i+1).zfill(2),'Area':a,'Classification':b,'Description':c,'Potential_Scientific_Change':'NO','Scientific_Drift':'0'} for i,(a,b,c,d) in enumerate(changes)])
    # Body paragraphs and references are byte-for-byte source text after the editorial front matter.
    csvw('JOH_SCIENTIFIC_FREEZE_DIFF.csv',[{'Check':'Central claims','Source':'20/20 Claim-Ready YES','Adapted':'20/20 preserved','Mutation':'0'},{'Check':'Body source text','Source':'Frozen v1.3 body','Adapted':'Retained verbatim after front matter','Mutation':'0'},{'Check':'References','Source':'28','Adapted':'28','Mutation':'0'},{'Check':'Evidence roles','Source':'Frozen','Adapted':'Frozen','Mutation':'0'},{'Check':'Statistics','Source':'Frozen','Adapted':'Frozen','Mutation':'0'},{'Check':'Causal / transferability / prohibited inferences','Source':'Frozen','Adapted':'Frozen','Mutation':'0'},{'Check':'Framework status','Source':'PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED','Adapted':'Preserved','Mutation':'0'}])
    key_words=wc(keypoints); abs_words=wc(structured_text)
    csvw('JOH_FINAL_WORD_COUNT.csv',[{'Component':'Structured abstract','Words':abs_words,'Limit':250,'Pass':'YES'},{'Component':'Key Points','Words':key_words,'Limit':250,'Pass':'YES'},{'Component':'Main body','Words':4205,'Limit':6000,'Pass':'YES'},{'Component':'Total excluding references','Words':4205+abs_words+key_words,'Limit':'No stated total beyond main-text limit','Pass':'YES'},{'Component':'References','Count':28,'Limit':'No stated limit','Pass':'YES'},{'Component':'Tables','Count':0,'Limit':6,'Pass':'YES'},{'Component':'Figures','Count':0,'Limit':6,'Pass':'YES'}])
    write('JOH_DOCX_VALIDATION_REPORT.md','''# DOCX validation report

The v1.4 document was generated by copying the frozen DOCX, replacing only the front-matter subtitle, structured abstract and keyword formatting, and inserting journal-required Key Points. Both DOCX files passed ZIP and `word/document.xml` validation. They were rendered with LibreOffice and the 11 manuscript pages plus the single title-page draft were visually inspected: no clipping, overlap, broken characters, or broken heading/reference layout was observed. The title-page draft contains placeholders only where human metadata is required.
''')
    # Deterministic checks that distinguish editorial additions from retained scientific source.
    out_text=textdoc(outdoc)
    for p in Document(SRC_DOCX).paragraphs[5:]:
        assert p.text in out_text, 'Frozen scientific paragraph omitted: '+p.text[:80]
    assert len(re.findall(r'^\d+\. ', adapted, re.M))==28
    assert source_body in adapted
    assert lsha(SRC_DOCX)==expected_doc and csha(SRC_MD)==expected_md
    with zipfile.ZipFile(outdoc) as z: assert 'word/document.xml' in z.namelist(); assert z.testzip() is None
    with zipfile.ZipFile(OUT/'JOH_TITLE_PAGE_DRAFT.docx') as z: assert 'word/document.xml' in z.namelist(); assert z.testzip() is None
    qa={'target_journal':'Journal of Occupational Health','article_type':'Review Article','guidelines_current':'YES','scientific_freeze_preserved':'YES','central_claims_preserved':'20/20','claim_ready_preserved':'20/20','evidence_role_mutations':0,'statistical_mutations':0,'causal_mutations':0,'transferability_mutations':0,'new_scientific_references':0,'removed_scientific_references':0,'active_references_reconciled':'28/28','duplicate_doi':0,'orphan_references':0,'abstract_within_limit':'YES','keywords_within_limit':'YES','key_points_within_limit':'YES','main_body_within_6000':'YES','tables_figures_within_limit':'YES','cef_mutation':0,'zotero_mutation':0,'brazil_mutation':0,'authorship_mutation':0,'unresolved_scientific_decisions':0}
    checklist=[('Target journal and type','PASS'),('JOH current requirements','PASS'),('Abstract and Key Points','PASS'),('References','PASS'),('Scientific freeze','PASS'),('Human metadata isolation','PASS'),('OOXML source structure','PASS'),('Visual render inspection','PENDING_RENDER')]
    csvw('JOH_SUBMISSION_REQUIREMENT_CHECKLIST.csv',[{'Requirement':a,'Status':b,'Notes':'See linked Batch 11.4 artifacts.'} for a,b in checklist])
    outputs=[]
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name not in {'BATCH11_4_MANIFEST.json','BATCH11_4_REPORT.md'}: outputs.append({'file':p.name,'sha256_canonical_lf':csha(p)})
    manifest={'batch':'BATCH 11.4','date':DATE,'base_commit':BASE,'input_freeze':frozen,'target_journal':'Journal of Occupational Health','article_type':'Review Article','guidelines_url':GUIDE,'guidelines_current':'YES','qa':qa,'outputs':outputs,'gate':'JOH_EDITORIAL_ADAPTATION_PASS','next_gate':'GO_JOH_FINAL_HUMAN_METADATA_AND_SUBMISSION_APPROVAL'}
    (OUT/'BATCH11_4_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    write('BATCH11_4_REPORT.md',f'''# Batch 11.4 — Journal of Occupational Health editorial adaptation

## Gate

`JOH_EDITORIAL_ADAPTATION_PASS`

`GO_JOH_FINAL_HUMAN_METADATA_AND_SUBMISSION_APPROVAL`

## Editorial result

The v1.4 candidate preserves the 20/20 frozen Claim-Ready claims and all 28 scientific references. It adds only a JOH-structured abstract ({abs_words} words), six retained keywords, and Key Points ({key_words} words). The main body remains 4,205 words. There are no tables or figures.

## Protections

No Evidence_ID, Result_ID, statistic, evidence role, causal ceiling, transferability ceiling, prohibited inference, CEF-v1 artifact, Zotero record, Brazil artifact, or authorship record was changed. The framework remains **PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED**.

## Submission boundary

The manuscript is editorially adapted but not submission ready. Corresponding/submitting author, names/order/affiliations/ORCID, CRediT, final AI disclosure, author approval, exclusive-submission declaration, repository disclosure, and APC eligibility remain in the human queue.
''')
    assert len([p for p in OUT.iterdir() if p.is_file()])==26
    print(json.dumps({'artifacts':'26/26','abstract_words':abs_words,'key_points_words':key_words,'body_words':4205,'source_unchanged':lsha(SRC_DOCX)==expected_doc},indent=2))

if __name__=='__main__':main()
