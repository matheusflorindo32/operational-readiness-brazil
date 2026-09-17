"""Build the first fail-closed full-text qualification pilot.

Raw PubMed and PMC XML remain outside Git.  This module verifies those inputs,
materializes compact audit ledgers, and enforces the Claim-Ready gate without
writing to Zotero or the canonical Master Evidence workbook.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = Path(
    r"C:\Users\mathe\Documents\Codex\2026-08-26\zotero-plugin-zotero-openai-curated-remote"
) / "outputs/full-text/2026-09-17-pilot-01"
DEFAULT_OUTPUT = ROOT / "reporting/full-text/2026-09-17/pilot-01"

SELECTED = [
    ("EV-0668", "36141388", "BHR9XD2I", "10.3390/healthcare10091777", "PMC9498760"),
    ("EV-0787", "33933923", "4AXW7YEU", "10.1016/j.drugpo.2021.103259", "PMC8530836"),
    ("EV-0758", "34622213", "CRYUZSIZ", "10.1007/s43477-021-00011-6", "PMC8116638"),
    ("EV-0753", "34665820", "NAFL5D8I", "10.1371/journal.pone.0258547", "PMC8525775"),
    ("EV-0727", "35076700", "H7XKJIDC", "10.1001/jamanetworkopen.2021.44955", "PMC8790663"),
    ("EV-0593", "37297641", "57HE5M3N", "10.3390/ijerph20116037", "PMC10252876"),
    ("EV-0523", "38115970", "45XR289H", "10.1136/tsaco-2023-001292", "PMC10729156"),
    ("EV-0503", "38322801", "7Q3Z785H", "10.1177/26334895231220259", "PMC10775732"),
    ("EV-0447", "39028235", "5H6N3ED3", "10.5811/westjem.18033", "PMC11254139"),
    ("EV-0425", "39205432", "96HF9IFT", "10.1111/dar.13926", "PMC12372593"),
]


CURATED = {
    "EV-0668": {
        "country_context": "Canada; public safety personnel and healthcare workers",
        "population": "No empirical sample; narrative review and program-development article",
        "design": "narrative review / program development",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Relevant conceptual and implementation source for occupational stress prevention, with no effectiveness evaluation.",
        "appraisal_tool": "SANRA",
        "tool_version": "2019 six-item scale",
        "appraisal_summary": "AI-assisted provisional SANRA 8/12; search methods absent and endpoint evidence incompletely presented.",
        "extraction": "STEADY combines social support, distress tracking, education, discussion and community-building; KTA and CFIR informed development.",
        "result": "The paper describes program components and planned implementation; it explicitly does not report a STEADY evaluation.",
        "exact_evidence_location": "The STEADY Program ¶1–2; Key Components ¶1–8; What Does STEADY Add? ¶10; Next Steps and Implications for Practice ¶1–2",
        "supported_claims": "The authors developed and described the five-component STEADY program and its proposed implementation basis.",
        "unsupported_claims": "The article does not establish STEADY effectiveness, causal mental-health benefit, long-term outcomes or superiority to other programs.",
        "transferability_limits": "Canadian program-development context; mixed PSP/healthcare target; no Brazilian implementation or outcome data.",
        "red_team_finding": "Program description could be misread as effectiveness evidence; retained only as conceptual/implementation evidence.",
    },
    "EV-0787": {
        "country_context": "Manchester, New Hampshire, United States; fire-department Safe Station",
        "population": "Safe Station clients (n=49), fire staff/leadership (n=29), ED staff (n=6), ambulance partner staff (n=4), recovery partner staff (n=6)",
        "design": "convergent parallel mixed-methods process evaluation",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Directly evaluates implementation determinants and metrics for a first-responder-linked access program.",
        "appraisal_tool": "MMAT",
        "tool_version": "2018",
        "appraisal_summary": "AI-assisted provisional appraisal: mixed-method rationale and integration are reported; quantitative samples are small and significance testing was not performed.",
        "extraction": "Observations, interviews and implementation measures were integrated using CFIR; stigma, funding, treatment availability, staffing and communication affected implementation.",
        "result": "Implementation scores were descriptive; small samples precluded significance testing, and staff adoption/acceptability appeared lower than client and leadership ratings.",
        "exact_evidence_location": "Methods—Design ¶1; Participants ¶1; Analysis Plan ¶1–2; Results—Participant Characteristics ¶1; Quantitative Metrics ¶1; Study Strengths and Limitations ¶1",
        "supported_claims": "In this local evaluation, participating stakeholder groups identified specific facilitators and barriers to Safe Station implementation.",
        "unsupported_claims": "The study does not prove program effectiveness, mortality reduction, causal benefit, sustainability or transportability to Brazil.",
        "transferability_limits": "Single US city, self-selected small stakeholder samples, local fire/health partnerships and no inferential testing.",
        "red_team_finding": "Effectiveness language in participant perceptions must not be converted into measured clinical effectiveness.",
    },
    "EV-0758": {
        "country_context": "United States; five implementation-practice examples",
        "population": "No formal study sample; illustrative applications across five organizations/projects",
        "design": "conceptual implementation tool with descriptive case illustrations",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Relevant conceptual source for organizational readiness during disruption; empirical utility remains unverified.",
        "appraisal_tool": "JBI Text and Opinion",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: argument and references are coherent, but utility evidence is anecdotal and formal validation is absent.",
        "extraction": "RRR extends R=MC² readiness thinking by considering an innovation and a disruption simultaneously; five applications are described.",
        "result": "Authors report preliminary user experience and explicitly state that structured qualitative and quantitative evaluation is still needed.",
        "exact_evidence_location": "Enhancing the Readiness Building System with RRR Tools and Approaches ¶1–5; RRR in Practice; Next Steps for RRR ¶1–5; Conclusions ¶1–4",
        "supported_claims": "The article describes the RRR tool, its conceptual basis and five early applications.",
        "unsupported_claims": "It does not validate the tool, establish psychometric properties, prove effectiveness or demonstrate generalizability.",
        "transferability_limits": "Heterogeneous US examples; no Brazilian public-safety application; authors characterize validity support as anecdotal.",
        "red_team_finding": "Early applications and author conclusions were bounded as descriptive; no effectiveness claim was retained.",
    },
    "EV-0753": {
        "country_context": "California, United States; firearm policy implementation",
        "population": "21 interviews with 27 judges, law-enforcement officers, attorneys, policy experts, advocates and a researcher",
        "design": "qualitative grounded-theory/CFIR evaluation",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Direct implementation study involving law enforcement and policy actors.",
        "appraisal_tool": "JBI Qualitative Research",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: sampling, analysis, triangulation, voices and ethics are reported; researcher positioning and influence are not fully addressed.",
        "extraction": "Informants described funding, planning, interagency coordination, training, local ideology and organizational culture as implementation determinants.",
        "result": "Perceived effectiveness was favorable but informants and authors stated that outcome evidence remained incomplete.",
        "exact_evidence_location": "Materials and methods—Study sample ¶1–2; Analytic approach ¶2–3; Results ¶1; Implementation sections; Evidence strength and quality ¶1–4; Limitations ¶1–2",
        "supported_claims": "Interviewed California stakeholders identified barriers, facilitators and perceived outcomes of GVRO implementation.",
        "unsupported_claims": "The interviews do not establish that GVROs reduce violence or suicide, quantify causal effects, or resolve equity impacts.",
        "transferability_limits": "California law and institutions differ from Brazil; participating counties had used GVROs and informants may have been more supportive.",
        "red_team_finding": "Perceived effectiveness was separated from actual outcome effectiveness and causal inference.",
    },
    "EV-0727": {
        "country_context": "Six emergency departments in the United States",
        "population": "31 adults with untreated opioid use disorder in six focus groups",
        "design": "multisite qualitative focus-group study",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Implementation-relevant patient perspectives on emergency care and treatment access.",
        "appraisal_tool": "JBI Qualitative Research",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: sampling, analysis, audit trail, participant voices and ethics are reported; researcher influence remains partly unclear.",
        "extraction": "Themes included stigma, pain minimization, lack of OUD treatment expectations, time-sensitive readiness, on-demand treatment and staff training.",
        "result": "The study reports participant experiences and implementation needs; it did not test an intervention effect.",
        "exact_evidence_location": "Methods—Selection of Participants ¶1; Data Collection ¶1; Data Analysis ¶1; Results—Participant Characteristics ¶1; Themes ¶1; Discussion—Limitations ¶1; Conclusions ¶1",
        "supported_claims": "Participants in these focus groups reported stigma and identified opportunities to improve ED care and treatment linkage.",
        "unsupported_claims": "The study does not quantify prevalence, prove intervention effectiveness, establish causality or represent all people with OUD.",
        "transferability_limits": "US ED and addiction-care context; selected English-speaking participants; no Brazilian public-safety workforce sample.",
        "red_team_finding": "Patient reports were preserved as qualitative findings, not prevalence estimates or causal effects.",
    },
    "EV-0593": {
        "country_context": "Urban Alberta, Canada; emergency and critical-care nurses",
        "population": "19 questionnaire respondents; 12 focus-group participants, all women",
        "design": "embedded mixed-methods implementation study",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Relevant implementation evidence for workplace reintegration, with indirect occupational transferability.",
        "appraisal_tool": "MMAT",
        "tool_version": "2018",
        "appraisal_summary": "AI-assisted provisional appraisal: mixed-method design and triangulation are explicit; small self-selected sample and narrow readiness assessment limit confidence.",
        "extraction": "Participants reported traumatic exposure and implementation needs including education, buy-in, resources, support and adaptation of a reintegration program.",
        "result": "Among 19 respondents, 89% reported psychological distress, 63% sought mental health care and 42% required time away; findings are descriptive and self-reported.",
        "exact_evidence_location": "Materials and Methods—Study Design ¶1–3; Participants ¶1; Data Collection ¶1–4; Data Analysis ¶1–2; Results—Questionnaire ¶1 and Thematic Analysis ¶1; Limitations ¶1",
        "supported_claims": "This small sample identified perceived needs and contextual barriers for a nurse workplace-reintegration program.",
        "unsupported_claims": "The study does not establish program effectiveness, population prevalence, causal benefit or direct applicability to police in Brazil.",
        "transferability_limits": "Canadian nurses, all-women sample, one health system, small self-selected groups and no implemented intervention outcome.",
        "red_team_finding": "Percentages were tied to denominator 19 and not generalized to nurses or public-safety personnel.",
    },
    "EV-0523": {
        "country_context": "Commentary on a national first-responder training initiative in Pakistan",
        "population": "No original sample or data",
        "design": "editorial commentary",
        "ai_full_text_decision": "HUMAN_REVIEW_REQUIRED",
        "decision_reason": "Full text is commentary without original methods or outcomes; a human must decide contextual-source eligibility.",
        "appraisal_tool": "JBI Text and Opinion",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: author and argument are identifiable and referenced, but the commentary supplies no independently appraisable empirical data.",
        "extraction": "The author comments that EPIS structured reporting of a large CPR/bleeding-control initiative and highlights sustainability planning.",
        "result": "No original effectiveness, training-target attainment or lives-saved result is reported.",
        "exact_evidence_location": "Body ¶1–3",
        "supported_claims": "The commentary describes the author's interpretation of another implementation report and its use of EPIS.",
        "unsupported_claims": "It cannot establish training effectiveness, lives saved, fidelity, sustainability or national generalizability.",
        "transferability_limits": "Opinion about a Pakistan initiative; no original data; different institutions, curriculum and health-system context.",
        "red_team_finding": "PMC article type is article-commentary; the queue's generic Journal Article label must not imply an empirical study.",
    },
    "EV-0503": {
        "country_context": "Queensland, Australia; police mental-health co-responder program",
        "population": "6 clinicians, 2 clinician managers, 15 police officers and 7 station officers in charge",
        "design": "qualitative service evaluation using post hoc CFIR analysis",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Direct police implementation study with clearly bounded qualitative outcomes.",
        "appraisal_tool": "JBI Qualitative Research",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: participant groups, analysis, ethics and findings are clear; post hoc framework use, researcher positioning and unknown police denominator limit confidence.",
        "extraction": "Data sharing, leadership, complementary skills and learning culture enabled implementation; staffing, governance, legislation and interagency differences constrained it.",
        "result": "Participants perceived the program favorably; no cost-benefit, consumer outcome or causal effectiveness evaluation was conducted.",
        "exact_evidence_location": "Method—Design ¶1; Participants ¶1; Interviews ¶1–2; Analysis ¶1; Results—Participants ¶1–2 and Overall Findings ¶1–4; Strengths and Limitations ¶1–2",
        "supported_claims": "Participating Queensland police and mental-health staff identified contextual barriers and enablers to this co-responder model.",
        "unsupported_claims": "The study does not prove clinical effectiveness, cost-effectiveness, reduced detention or transport, or success in other jurisdictions.",
        "transferability_limits": "Queensland legal/data-sharing context, post hoc evaluation and uncertain police participation denominator differ from Brazil.",
        "red_team_finding": "Perceived better outcomes were not treated as measured consumer outcomes or cost-effectiveness.",
    },
    "EV-0447": {
        "country_context": "King County, Washington, United States; first responders and mobile health staff",
        "population": "32 first responders, mobile medical clinicians and EMS leaders",
        "design": "community-engaged qualitative interview study",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Direct implementation study of first-responder overdose interventions.",
        "appraisal_tool": "JBI Qualitative Research",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: reflexivity, dual coding, saturation, voices and ethics are reported; convenience/snowball sampling and low demographic diversity remain concerns.",
        "extraction": "Participants perceived leave-behind naloxone as most compatible; field buprenorphine raised workflow concerns; HIV/HCV testing was often considered unsuitable for rapid response.",
        "result": "The study identifies perceived facilitators and barriers; it does not evaluate patient health impact.",
        "exact_evidence_location": "Methods—Study Design ¶1; Reflexivity ¶1; Recruitment ¶1; Data Collection ¶1; Thematic Analysis ¶1–2; Results—Participant Demographics ¶1 and Qualitative Results; Limitations ¶1",
        "supported_claims": "Interviewed first responders and leaders identified local implementation barriers and facilitators for three overdose interventions.",
        "unsupported_claims": "The study does not demonstrate intervention efficacy, safety, cost-effectiveness, adoption rates or patient outcomes.",
        "transferability_limits": "Single US county, convenience/snowball sample, limited racial/ethnic diversity and opioid-policy context unlike Brazil.",
        "red_team_finding": "Participant endorsement was retained as perception and not upgraded to effectiveness evidence.",
    },
    "EV-0425": {
        "country_context": "King County, Washington, United States; people who use drugs",
        "population": "13 adults with opioid-use experience and a recent EMS encounter",
        "design": "community-engaged qualitative interview study",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT",
        "decision_reason": "Implementation-relevant service-user perspectives for field overdose care.",
        "appraisal_tool": "JBI Qualitative Research",
        "tool_version": "2017",
        "appraisal_summary": "AI-assisted provisional appraisal: community partnership, reflexivity, double coding, voices and analysis are explicit; convenience sampling and regionality limit transferability.",
        "extraction": "Participants generally favored leave-behind naloxone and field buprenorphine, were less interested in field HIV/HCV testing, and emphasized compassionate care and reduced police visibility.",
        "result": "Findings describe preferences and experiences, not clinical or implementation effectiveness.",
        "exact_evidence_location": "Methods—Community-engaged approach ¶1; Recruitment ¶1; Data Collection ¶1; Analysis ¶1; Results ¶1–3 and thematic sections; Limitations ¶1",
        "supported_claims": "These 13 participants described preferences and concerns about post-overdose interventions in their local EMS context.",
        "unsupported_claims": "The study does not establish population-wide acceptability, intervention effectiveness, safety, treatment uptake or causal outcomes.",
        "transferability_limits": "Small convenience sample from service-connected Seattle locations; highly regional overdose and policing context.",
        "red_team_finding": "Preferences were not converted into evidence that the interventions improve health or implementation outcomes.",
    },
}


SANRA = [
    ("importance justified", "2"), ("aims stated", "2"),
    ("literature search described", "0"), ("referencing", "2"),
    ("scientific reasoning", "1"), ("endpoint data", "1"),
]
JBI_QUAL = {
    "EV-0753": ["UNCLEAR", "YES", "YES", "YES", "YES", "UNCLEAR", "UNCLEAR", "YES", "YES", "YES"],
    "EV-0727": ["UNCLEAR", "YES", "YES", "YES", "YES", "UNCLEAR", "UNCLEAR", "YES", "YES", "YES"],
    "EV-0503": ["UNCLEAR", "YES", "YES", "YES", "YES", "UNCLEAR", "UNCLEAR", "YES", "YES", "YES"],
    "EV-0447": ["YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES"],
    "EV-0425": ["YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES"],
}
JBI_QUAL_DOMAINS = [
    "methodology/philosophical perspective congruity", "methodology/research question congruity",
    "methodology/data collection congruity", "methodology/data representation/analysis congruity",
    "methodology/interpretation congruity", "researcher culturally/theoretically located",
    "researcher influence addressed", "participants and voices represented",
    "ethics approval", "conclusions flow from analysis",
]


def text(element: ET.Element | None) -> str:
    return " ".join("".join(element.itertext()).split()) if element is not None else ""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_pmc(path: Path) -> dict[str, str]:
    root = ET.parse(path).getroot()
    article = root.find(".//article") if root.tag != "article" else root
    assert article is not None
    ids = {node.get("pub-id-type", ""): text(node) for node in article.findall(".//article-meta/article-id")}
    authors = []
    for contrib in article.findall(".//article-meta/contrib-group/contrib"):
        if contrib.get("contrib-type") != "author":
            continue
        name = contrib.find("./name")
        if name is not None:
            authors.append(f"{text(name.find('./given-names'))} {text(name.find('./surname'))}".strip())
        elif contrib.find("./collab") is not None:
            authors.append(text(contrib.find("./collab")))
    license_node = article.find(".//permissions/license")
    return {
        "title": text(article.find(".//article-meta/title-group/article-title")),
        "journal": text(article.find(".//journal-meta/journal-title-group/journal-title")),
        "year": text(article.find(".//article-meta/pub-date/year")),
        "volume": text(article.find(".//article-meta/volume")),
        "issue": text(article.find(".//article-meta/issue")),
        "pages": text(article.find(".//article-meta/elocation-id")) or text(article.find(".//article-meta/fpage")),
        "doi": ids.get("doi", ""), "pmid": ids.get("pmid", ""), "pmcid": ids.get("pmcid", ""),
        "article_type": article.get("article-type", ""), "authors": "; ".join(authors),
        "license": text(license_node), "manuscript_id": ids.get("manuscript-id", ""),
    }


def parse_pubmed_integrity(path: Path) -> tuple[str, str]:
    root = ET.parse(path).getroot()
    relations = []
    for node in root.findall(".//CommentsCorrections"):
        relations.append(f"{node.get('RefType', '')}:{text(node.find('./PMID'))}")
    publication_types = [text(node) for node in root.findall(".//PublicationType")]
    if any("Retracted Publication" == item for item in publication_types):
        return "BLOCKED_INTEGRITY", "; ".join(relations)
    integrity_relations = [
        item for item in relations
        if item.split(":", 1)[0] in {
            "ErratumFor", "ErratumIn", "ExpressionOfConcernFor", "ExpressionOfConcernIn",
            "RetractionOf", "RetractionIn", "UpdateOf", "UpdateIn",
        }
    ]
    if integrity_relations:
        return "INTEGRITY_REVIEW_REQUIRED", "; ".join(relations)
    if relations:
        return "INTEGRITY_CLEAR", "; ".join(relations) + "; non-integrity editorial relation retained"
    return "INTEGRITY_CLEAR", "No correction/retraction relation found in the current PubMed record; this is not proof of absolute absence."


def claim_ready_allowed(row: dict[str, str]) -> bool:
    required = {
        "full_text_obtained": "YES", "identity_status": "MATCH_CONFIRMED",
        "ai_full_text_decision": "INCLUDE_FULL_TEXT", "extraction_complete": "YES",
        "appraisal_complete_ai": "YES", "integrity_status": "INTEGRITY_CLEAR",
        "exact_location_complete": "YES", "boundary_complete": "YES",
        "transferability_complete": "YES", "human_confirmation": "YES",
    }
    return all(row.get(key) == value for key, value in required.items()) and row.get("editorial_hold") != "YES"


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def build(raw_root: Path = DEFAULT_RAW, output: Path = DEFAULT_OUTPUT) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    queue_path = ROOT / "reporting/nonblocking/2026-09-16/full-text-priority-queue.csv"
    with queue_path.open(encoding="utf-8-sig", newline="") as handle:
        queue = {r["evidence_id"]: r for r in csv.DictReader(handle)}
    records, provenance, red_team = [], [], []
    for evidence_id, pmid, zotero_key, doi, pmcid in SELECTED:
        assert evidence_id in queue and zotero_key != "FXC7ZY9R" and pmid != "26159007"
        pmc_path = raw_root / "raw/pmc" / f"{pmcid}.xml"
        pubmed_path = raw_root / "raw/pubmed" / f"{pmid}.xml"
        if not pmc_path.exists() or not pubmed_path.exists():
            raise FileNotFoundError(f"Missing audited raw full text for {evidence_id}")
        meta = parse_pmc(pmc_path)
        if (meta["pmid"], meta["doi"].lower(), meta["pmcid"]) != (pmid, doi.lower(), pmcid):
            raise ValueError(f"Identity mismatch for {evidence_id}")
        integrity, relations = parse_pubmed_integrity(pubmed_path)
        curated = CURATED[evidence_id]
        version = "AUTHOR_ACCEPTED_MANUSCRIPT" if meta["manuscript_id"] else "VERSION_OF_RECORD"
        row = {
            "evidence_id": evidence_id, "pmid": pmid, "doi": doi, "pmcid": pmcid,
            "zotero_key": zotero_key, "title": meta["title"], "authors": meta["authors"],
            "journal": meta["journal"], "year": meta["year"], "volume": meta["volume"],
            "issue": meta["issue"], "pages_or_elocation": meta["pages"],
            "full_text_source": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/",
            "access_type": "PMC", "lawful_access": "YES", "discovered_on": "2026-09-17",
            "full_text_obtained": "YES", "identity_status": "MATCH_CONFIRMED",
            "version_status": version, "article_type_jats": meta["article_type"],
            "integrity_status": integrity, "integrity_detail": relations,
            **curated,
            "extraction_complete": "YES", "appraisal_complete_ai": "YES",
            "exact_location_complete": "YES", "boundary_complete": "YES",
            "transferability_complete": "YES", "editorial_hold": "NO",
            "human_reviewer": "", "human_review_date": "", "human_decision": "",
            "human_justification": "", "human_confirmation": "",
            "claim_ready": "NO", "record_status": "HUMAN_REVIEW_REQUIRED",
        }
        assert not claim_ready_allowed(row)
        records.append(row)
        pubmed_locator = f"external://full-text/2026-09-17-pilot-01/raw/pubmed/{pmid}.xml"
        pmc_locator = f"external://full-text/2026-09-17-pilot-01/raw/pmc/{pmcid}.xml"
        provenance.extend([
            {"evidence_id": evidence_id, "stage": "RAW_PUBMED", "source": "NCBI Entrez EFetch", "path_external": pubmed_locator, "sha256": sha256(pubmed_path), "timestamp": "2026-09-17", "tool": "ncbi_entrez.py", "transformation": "none"},
            {"evidence_id": evidence_id, "stage": "FULL_TEXT", "source": "NCBI PMC EFetch JATS XML", "path_external": pmc_locator, "sha256": sha256(pmc_path), "timestamp": "2026-09-17", "tool": "ncbi_entrez.py", "transformation": "parsed metadata and section locations"},
            {"evidence_id": evidence_id, "stage": "EXTRACTION_APPRAISAL", "source": "audited JATS full text", "path_external": "", "sha256": "", "timestamp": "2026-09-17", "tool": "build_full_text_pilot.py", "transformation": "AI-assisted provisional extraction and design-specific appraisal; human fields unchanged"},
        ])
        red_team.append({
            "evidence_id": evidence_id, "identity": "PASS", "doi": "PASS", "supplement_confusion": "PASS",
            "editorial_relation": "PASS" if integrity == "INTEGRITY_CLEAR" else "ATTENTION",
            "retraction": "PASS" if integrity != "BLOCKED_INTEGRITY" else "BLOCKED",
            "duplicate": "PASS", "design": "ATTENTION" if evidence_id in {"EV-0668", "EV-0758", "EV-0523"} else "PASS",
            "appraisal_compatibility": "PASS", "result_extraction": "PASS", "denominator": "PASS",
            "table_interpretation": "PASS", "primary_secondary_outcome": "PASS",
            "adjusted_unadjusted": "PASS", "causal_overreach": "PASS", "population_generalization": "PASS",
            "claim_boundary": "PASS", "finding_and_correction": curated["red_team_finding"],
        })

    appraisal = []
    for domain, judgment in SANRA:
        appraisal.append({"evidence_id": "EV-0668", "tool": "SANRA", "domain": domain, "judgment": judgment, "basis": CURATED["EV-0668"]["exact_evidence_location"], "human_confirmed": ""})
    for eid, judgments in JBI_QUAL.items():
        for domain, judgment in zip(JBI_QUAL_DOMAINS, judgments):
            appraisal.append({"evidence_id": eid, "tool": "JBI Qualitative Research", "domain": domain, "judgment": judgment, "basis": CURATED[eid]["exact_evidence_location"], "human_confirmed": ""})
    for eid in ("EV-0787", "EV-0593"):
        for domain, judgment in [
            ("clear research questions", "YES"), ("data address research questions", "YES"),
            ("rationale for mixed methods", "YES"), ("components effectively integrated", "YES"),
            ("integrated outputs interpreted", "YES"), ("divergence/inconsistency addressed", "UNCLEAR"),
            ("component quality adequate", "UNCLEAR"),
        ]:
            appraisal.append({"evidence_id": eid, "tool": "MMAT 2018", "domain": domain, "judgment": judgment, "basis": CURATED[eid]["exact_evidence_location"], "human_confirmed": ""})
    for eid in ("EV-0758", "EV-0523"):
        judgments = ["YES", "YES", "UNCLEAR", "YES", "YES", "UNCLEAR" if eid == "EV-0758" else "NOT_APPLICABLE"]
        for domain, judgment in zip(["source identified", "expertise/standing", "interests central to population", "logical basis", "reference to extant literature", "incongruence defended"], judgments):
            appraisal.append({"evidence_id": eid, "tool": "JBI Text and Opinion", "domain": domain, "judgment": judgment, "basis": CURATED[eid]["exact_evidence_location"], "human_confirmed": ""})

    write_csv(output / "pilot-records.csv", records)
    write_csv(output / "appraisal-domain-ledger.csv", appraisal)
    write_csv(output / "red-team-ledger.csv", red_team)
    write_csv(output / "provenance-ledger.csv", provenance)
    summary = {
        "generated_on": datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat(),
        "policy": "FAIL_CLOSED_NONBLOCKING_FULL_TEXT_V1",
        "pilot_size": len(records), "full_text_obtained": sum(r["full_text_obtained"] == "YES" for r in records),
        "identity_match_confirmed": sum(r["identity_status"] == "MATCH_CONFIRMED" for r in records),
        "version_of_record": sum(r["version_status"] == "VERSION_OF_RECORD" for r in records),
        "author_accepted_manuscript": sum(r["version_status"] == "AUTHOR_ACCEPTED_MANUSCRIPT" for r in records),
        "integrity_clear": sum(r["integrity_status"] == "INTEGRITY_CLEAR" for r in records),
        "ai_include_full_text": sum(r["ai_full_text_decision"] == "INCLUDE_FULL_TEXT" for r in records),
        "ai_human_review_required": sum(r["ai_full_text_decision"] == "HUMAN_REVIEW_REQUIRED" for r in records),
        "appraisal_completed_ai_provisional": len(records), "human_decisions": 0, "claim_ready": 0,
        "control_item_present": any(r["zotero_key"] == "FXC7ZY9R" for r in records),
        "retracted_pmid_present": any(r["pmid"] == "26159007" for r in records),
        "scientific_pass": "PROHIBITED", "decision": "GO_NONBLOCKING_HUMAN_REVIEW_REQUIRED",
    }
    (output / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {p.name: {"sha256": sha256(p), "bytes": p.stat().st_size} for p in sorted(output.iterdir()) if p.is_file() and p.name != "manifest.json"}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.raw_root, args.output), ensure_ascii=False, indent=2))
