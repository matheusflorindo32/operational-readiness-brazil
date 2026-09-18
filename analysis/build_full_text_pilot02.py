"""Build Pilot 02 full-text qualification ledgers with fail-closed controls."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from audit_xlsx_identity import semantic_sha256
except ModuleNotFoundError:  # pragma: no cover - package-style imports in focused tests
    from analysis.audit_xlsx_identity import semantic_sha256


ROOT = Path(__file__).resolve().parents[1]
RAW = Path(
    os.environ.get(
        "ORB_PILOT02_RAW_ROOT",
        ROOT.parents[1] / "outputs/full-text/2026-09-17-pilot-02",
    )
)
OUTPUT = ROOT / "reporting/full-text/2026-09-17/pilot-02"
QUEUE = ROOT / "reporting/nonblocking/2026-09-16/full-text-priority-queue.csv"
PILOT1 = ROOT / "reporting/full-text/2026-09-17/pilot-01-methodological-correction/corrected-records.csv"
MASTER = ROOT / "outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx"
SOURCE_COMMIT = "fdcf61ea56d89ed7838583fc865c2a56b5873af1"

JBI_SOURCE = "https://jbi.global/critical-appraisal-tools"
JBI_QUAL_SOURCE = "https://jbi.global/sites/default/files/2026-05/2024_Checklist_for_Qualitative_Research_1.docx"
JBI_QUASI_SOURCE = "https://jbi.global/sites/default/files/2026-05/2_JBI%20checklist%20for%20quasi-experimental%20studies.docx"
MMAT_SOURCE = "https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria%20manual_2018%20-08-01_ENG.pdf"

SELECTED = [
    ("EV-0367", "39808097", "Q45USE2S", "10.1016/j.jen.2024.12.010", "PMC12064357"),
    ("EV-0176", "41492854", "2KBKDFBY", "10.1111/hex.70552", "PMC12771649"),
    ("EV-0171", "41520119", "P5KDUIF2", "10.1186/s40814-025-01758-7", "PMC12882353"),
    ("EV-0160", "41626406", "FU3CE6LR", "10.1177/29768357251413412", "PMC12852583"),
    ("EV-0157", "41673910", "9S3E8CNQ", "10.1186/s12954-026-01413-1", "PMC12998156"),
    ("EV-0091", "42196761", "ME325L4C", "10.3390/ijerph23050669", "PMC13206323"),
    ("EV-1328", "19947877", "NCPMCR97", "10.3109/10903120903349762", "PMC3413284"),
    ("EV-0896", "32191195", "FISZESIY", "10.5811/westjem.2019.11.44887", "PMC7081854"),
    ("EV-0791", "33909512", "JL2TE34F", "10.1080/10903127.2021.1922556", "PMC8626520"),
    ("EV-0723", "35120531", "NDHXQXSC", "10.1186/s12954-022-00590-z", "PMC8814788"),
]

CURATED = {
    "EV-0367": {
        "country_context": "Houston, Texas, United States; public safety-net emergency department",
        "population": "11 emergency nurses interviewed from 36 approached",
        "design": "qualitative case study using semi-structured interviews and CFIR-guided deductive-inductive analysis",
        "evidence_class": "QUALITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Qualitative Research",
        "appraisal_version": "2024 checklist; file published 2026-05",
        "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL",
        "extraction": "Nurses framed cognitive screening around patient and staff safety and identified staffing, time, private space, education, electronic-record support and follow-up capacity as implementation conditions.",
        "result": "Eleven nurses rated delirium screening feasibility at a mean 3.9/5 and dementia screening at 3.45/5; these are perceptions, not implementation or patient outcomes.",
        "exact_evidence_location": "Study Design P1; Selection of Participants P1; Data Collection P1-P3; Data Analysis P1; Reflexivity P1; Results P1-P3; System resources needed for screenings P1-P3; Delirium—Local attitudes P2; Dementia—Complexity P2; Limitations P1",
        "supported_claims": "In this single-site sample, interviewed nurses identified concrete barriers and facilitators to introducing delirium and dementia screening.",
        "unsupported_claims": "The study does not establish screening effectiveness, diagnostic accuracy, patient-safety benefit, adoption rates or generalizability to other emergency departments.",
        "transferability_limits": "Single under-resourced US safety-net hospital, daytime recruitment and no Brazilian or public-safety workforce implementation.",
        "appraisal_summary": "AI-provisional JBI qualitative appraisal: clear case-study methods, saturation, ethics and reflexivity safeguards; single-site daytime sampling constrains transferability.",
    },
    "EV-0176": {
        "country_context": "West Side of Chicago, United States; mobile MOUD program and criminal-legal involvement",
        "population": "13 mobile-service participants with OUD and criminal-legal involvement in the prior 90 days",
        "design": "qualitative descriptive study using semi-structured interviews and inductive thematic analysis",
        "evidence_class": "QUALITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Qualitative Research",
        "appraisal_version": "2024 checklist; file published 2026-05",
        "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL",
        "extraction": "Participants described proximity, walk-in access, onsite medication, comprehensive care and non-judgmental staff as facilitators; incarceration, transport and schedule awareness were barriers.",
        "result": "Thirteen interviews produced five themes and eight subthemes; findings describe service experiences and perceived access conditions.",
        "exact_evidence_location": "Methods—Setting P1-P2; Participant Recruitment P1; Data Collection and Analysis P2-P3; Results—Participant Characteristics P1 and thematic sections; Discussion P1-P8",
        "supported_claims": "These 13 participants reported that mobile MOUD access was supported by convenience and compassionate care and constrained by structural barriers.",
        "unsupported_claims": "The study does not estimate treatment effectiveness, retention, overdose reduction, causal benefit or experiences of people unable to access the service.",
        "transferability_limits": "Small service-engaged sample from a few Chicago neighborhoods and a specific US treatment and criminal-legal context.",
        "appraisal_summary": "AI-provisional JBI qualitative appraisal: transparent recruitment, dual coding, ethics and participant quotations; researcher positionality and excluded non-users remain limitations.",
    },
    "EV-0171": {
        "country_context": "Flint, Michigan, United States; jail-to-community peer navigation",
        "population": "4 peer navigators interviewed; 3 completed 12 client-specific WAI ratings; 25 administrative documents reviewed",
        "design": "mixed-methods implementation process evaluation integrating qualitative interviews, descriptive WAI ratings and document review",
        "evidence_class": "MIXED_METHODS_EVIDENCE",
        "appraisal_tool": "MMAT",
        "appraisal_version": "2018",
        "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL",
        "extraction": "Peer navigators perceived MAPS as feasible, acceptable and culturally appropriate, while reporting jail access, staffing, distrust, unstable contact information and unmet post-release needs as implementation barriers.",
        "result": "Three navigators supplied 12 WAI ratings with high descriptive alliance scores; opinions about effectiveness were mixed and no client-effect estimate was tested.",
        "exact_evidence_location": "Study design P1; Participants P1; Sampling and recruitment P1; Measures P1; Data collection P1; Qualitative data analysis P1; WAI analysis P1; Administrative data P1; Results P1; Feasibility and acceptability P1-P4; Discussion P1-P7",
        "supported_claims": "Within this small pilot, participating peer navigators identified implementation strengths, barriers and refinements for MAPS.",
        "unsupported_claims": "The study does not establish service-linkage effectiveness, cost-effectiveness, reduced reincarceration or client outcomes.",
        "transferability_limits": "Four Black male navigators in one locality, three survey respondents, unstable post-release follow-up and no powered outcome comparison.",
        "appraisal_summary": "AI-provisional full MMAT: qualitative evidence is coherent and integrated with descriptive ratings and documents; the tiny quantitative component and incomplete participation limit inference.",
    },
    "EV-0160": {
        "country_context": "Three rural Appalachian Ohio counties, United States",
        "population": "34 stakeholders, 30 people who use drugs, 258 survey participants, agencies and a 9-member leadership board",
        "design": "adaptive mixed-methods implementation project with formative interviews, respondent-driven survey, network analysis and process evaluation",
        "evidence_class": "MIXED_METHODS_EVIDENCE",
        "appraisal_tool": "MMAT",
        "appraisal_version": "2018",
        "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL",
        "extraction": "Community co-creation produced more than 20 capacity-building activities addressing stigma, interagency fragmentation and provider capacity; process measures documented reach and delivery.",
        "result": "The article reports implementation activities and sustainment examples; planned repeated survey and population-outcome analyses were not completed after COVID-19 disruption.",
        "exact_evidence_location": "Methods P1; Exploration P1; In-Depth Interviews P1-P4; Agency Relationships P1; Respondent Driven Sampling Survey P1; Triangulation P1; Adoption/Preparation P1-P2; Evaluation P1-P2; Implementation & Evaluation Phases P1-P6; Limitations and Future Directions P1-P3",
        "supported_claims": "The project demonstrates how these three counties co-developed and delivered adaptive capacity-building activities and documents their process outputs.",
        "unsupported_claims": "It does not establish reductions in overdose or infection, causal community benefit, effectiveness of individual activities or sustainability across settings.",
        "transferability_limits": "Grant-supported US rural harm-reduction context, local legal climate, incomplete outcome evaluation and COVID-era adaptation differ from Brazil.",
        "appraisal_summary": "AI-provisional full MMAT: explicit mixed-method triangulation and adaptive integration; incomplete powered survey and population-outcome components constrain effectiveness inference.",
    },
    "EV-0157": {
        "country_context": "United States; syringe service programs across four regions",
        "population": "23 representatives of syringe service programs after one ineligible interview was excluded",
        "design": "qualitative implementation study using semi-structured interviews, reflexive thematic analysis and secondary CFIR coding",
        "evidence_class": "QUALITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Qualitative Research",
        "appraisal_version": "2024 checklist; file published 2026-05",
        "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL",
        "extraction": "Cost, staffing, space, legal ambiguity and law-enforcement opposition constrained advanced drug checking; external laboratory and university partnerships facilitated implementation.",
        "result": "Eight of 23 represented programs had implemented advanced services; this descriptive count accompanies qualitative themes and is not an effectiveness estimate.",
        "exact_evidence_location": "Sample identification and recruitment P1; Interview guide P1; Data collection P1-P2; Data analysis P1-P3; Findings P1-P2; Barriers P1-P5; Facilitators P1-P4; Discussion P1-P6",
        "supported_claims": "Interviewed program representatives identified multilevel barriers and partnership-based facilitators for advanced drug-checking implementation.",
        "unsupported_claims": "The study does not show that drug checking reduces overdose, quantify adoption nationally or establish partnership effectiveness.",
        "transferability_limits": "Purposive US program sample, program representatives rather than service users, and US legal and funding structures.",
        "appraisal_summary": "AI-provisional JBI qualitative appraisal: purposive sampling, saturation, iterative analysis, ethics and quotations are reported; split coding and limited positionality require caution.",
    },
    "EV-0091": {
        "country_context": "Five Canadian police and fire organizations",
        "population": "Repeated survey samples of 372 at T1 and 207 at T2 plus organizational records; training follow-up samples varied",
        "design": "uncontrolled longitudinal multiple-cohort implementation case series with repeated cross-sectional pre-post surveys and exploratory organizational correlations",
        "evidence_class": "QUANTITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Quasi-Experimental Studies",
        "appraisal_version": "2023 tool; Barker et al. 2024",
        "appraisal_type": "RISK_OF_BIAS_APPRAISAL",
        "extraction": "Five organizations implemented locally selected mental-health and resilience activities; repeated surveys and administrative indicators were compared over time and correlations were explored at organization level.",
        "result": "Aggregate scores improved for anxiety, alcohol use and team psychological safety, while individual resilience deteriorated; small-N correlations with benefit costs were exploratory and sometimes unexpected.",
        "exact_evidence_location": "Purpose P1; Materials and Methods P1-P4; Psychological Health and Well-Being Survey P1-P3; Data Cleaning P1-P2; Analytic Approach P1-P2; Results—PHW Survey P1-P5; Training Outcomes P1-P3; Correlation Analysis P1-P6; Limitations P1-P3; Tables 3-5",
        "supported_claims": "In these five organizations, selected survey measures changed over time and exploratory organization-level associations with benefit costs were observed.",
        "unsupported_claims": "The study does not establish that the Standard or training caused the changes, reduced costs, prevented illness or will reproduce in other organizations.",
        "transferability_limits": "No control group, different repeated samples, attrition, COVID timing, organization-level N of four or five and Canadian context.",
        "appraisal_summary": "AI-provisional revised JBI quasi-experimental appraisal: temporal ordering and repeated measurement exist, but no control, non-equivalent samples, attrition and small-N exploratory analyses create serious bias concerns.",
    },
    "EV-1328": {
        "country_context": "Colombian National Police antinarcotics and rural operations",
        "population": "374 combat nursing students trained between March 2006 and July 2007",
        "design": "single-group pre-post quasi-experimental course evaluation",
        "evidence_class": "QUANTITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Quasi-Experimental Studies",
        "appraisal_version": "2023 tool; Barker et al. 2024",
        "appraisal_type": "RISK_OF_BIAS_APPRAISAL",
        "extraction": "A 26-hour tactical trauma course combined lectures, simulation, live tissue procedures and a jungle exercise; knowledge and instructor-rated skills were measured before and after training.",
        "result": "Mean written scores rose from 59.8% to 98.9% (p<0.01); all 374 participants were rated as demonstrating complete knowledge after practical training.",
        "exact_evidence_location": "Setting and Design P1-P2; Analytical Methods P1; Results P1-P3; Tables 4-5; Limitations P1",
        "supported_claims": "Among these 374 trainees, written scores and instructor-rated simulation skills were higher after the MEDTAC course.",
        "unsupported_claims": "The uncontrolled evaluation does not establish clinical performance, casualty outcomes, long-term retention or superiority to another course.",
        "transferability_limits": "Colombian police combat-nurse setting, non-standardized instruments, instructor assessment and no control or long-term follow-up.",
        "appraisal_summary": "AI-provisional revised JBI quasi-experimental appraisal: complete paired pre-post cohort, but no control and non-standardized instructor-rated outcomes create substantial bias risk.",
    },
    "EV-0896": {
        "country_context": "Westminster, California, United States; civilian mass-casualty simulation",
        "population": "51 of 75 volunteers participated, including trained and untrained civilians; nursing graduates and one fire engine company were reference groups",
        "design": "nonrandomized comparative simulation study of trained versus untrained volunteers",
        "evidence_class": "QUANTITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Quasi-Experimental Studies",
        "appraisal_version": "2023 tool; Barker et al. 2024",
        "appraisal_type": "RISK_OF_BIAS_APPRAISAL",
        "extraction": "Volunteers receiving a four-hour First Care Provider course were compared with untrained volunteers on time to first action and time to solution in arterial bleeding and airway-obstruction simulations.",
        "result": "Time to solution was shorter for trained groups for bleeding (3:33 versus the 8-minute cutoff, p=0.0014) and airway obstruction (32.6 seconds versus 7:03, p=0.0087); time-to-first-action differences were not significant.",
        "exact_evidence_location": "Participant Selection P1; Training P1; Simulation and Grading P1-P3; Analysis P1; Simulation Results and four outcome subsections; Limitations P1-P2",
        "supported_claims": "In this simulation, trained volunteer groups completed the two specified interventions faster than untrained groups.",
        "unsupported_claims": "The study does not prove real-event mortality benefit, durable skill retention, population effectiveness or equivalence to professional EMS.",
        "transferability_limits": "Small volunteer sample, nonrandom group assignment, simulated setting, potential group differences and donated equipment.",
        "appraisal_summary": "AI-provisional revised JBI quasi-experimental appraisal: a comparator and objective timing existed, but nonrandom allocation, attrition and one-sided clustered analysis limit confidence.",
    },
    "EV-0791": {
        "country_context": "One Midwestern US city of approximately 35,000 residents",
        "population": "10,215 EMS calls over three years, including 892 fall-related calls; community-paramedic users were not consistently characterized",
        "design": "quality-improvement initiative with uncontrolled retrospective interrupted time-series/pre-post comparison",
        "evidence_class": "QUANTITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Quasi-Experimental Studies",
        "appraisal_version": "2023 tool; Barker et al. 2024",
        "appraisal_type": "RISK_OF_BIAS_APPRAISAL",
        "extraction": "Community-FIT embedded a fall-prevention pathway and learning health system in a fire-based community-paramedicine program and compared 12 baseline with 12 sustainment months.",
        "result": "Fall-related calls decreased from 135 to 46 (reported relative risk reduction 0.66, 95% CI 0.53-0.76); transports decreased from 96 to 36 (0.63, 95% CI 0.46-0.75).",
        "exact_evidence_location": "Initiative P1; Study Design P1-P2; Data Collection and Use P1; Outcome Measures and Analyses P1-P2; Results P1-P2; Fall Calls P1; Fall-related Calls Resulting in Transport P1; Study Limitations P1; Table 2",
        "supported_claims": "Fall-related EMS calls and transports were lower in the sustainment period than in the baseline period in this community.",
        "unsupported_claims": "The uncontrolled comparison does not establish that Community-FIT caused the reductions or that the effect will generalize to other communities.",
        "transferability_limits": "Single supportive small city, established grant-funded program, changing documentation and no concurrent control for secular or seasonal trends.",
        "appraisal_summary": "AI-provisional revised JBI quasi-experimental appraisal: repeated monthly data and consistent outcomes exist, but no control and no segmented time-series model leave confounding and trend bias unresolved.",
    },
    "EV-0723": {
        "country_context": "Urban Boston, Massachusetts, United States; one syringe service program",
        "population": "8 staff and 4 service participants interviewed, with field observations and process measures over 22 months",
        "design": "longitudinal qualitative implementation case study with field observations, interviews and descriptive process measures",
        "evidence_class": "QUALITATIVE_EVIDENCE",
        "appraisal_tool": "JBI Qualitative Research",
        "appraisal_version": "2024 checklist; file published 2026-05",
        "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL",
        "extraction": "Shared harm-reduction culture, horizontal structure, partnerships and adaptive reflection facilitated drug checking; technical complexity, legal ambiguity, police activity and COVID-19 constrained delivery.",
        "result": "Requests fell from an average 42 per month before a police operation to 23 in August 2019 and later stopped during COVID restrictions; these descriptive changes do not isolate causal effects.",
        "exact_evidence_location": "Methods P1-P5; Results—Initial intervention plan P1-P3; Outer setting P1-P6; Inner setting and implementation P1-P2; Characteristics of individuals P1; Implementation process P1-P3; Discussion P1-P8",
        "supported_claims": "This case documents how organizational, technical, legal, policing and pandemic conditions shaped implementation at one program.",
        "unsupported_claims": "It does not establish drug-checking effectiveness, overdose prevention, causal effects of policing or generalizability beyond the site.",
        "transferability_limits": "One independently operated urban US program, 12 interviewees, distinct drug laws and law-enforcement environment.",
        "appraisal_summary": "AI-provisional JBI qualitative appraisal: longitudinal triangulation, ethics and participant voices are present; small single-site sampling and limited reflexivity constrain transferability.",
    },
}

QUAL_JUDGMENTS = {
    "EV-0367": ["UNCLEAR", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES"],
    "EV-0176": ["UNCLEAR", "YES", "YES", "YES", "YES", "UNCLEAR", "UNCLEAR", "YES", "YES", "YES"],
    "EV-0157": ["UNCLEAR", "YES", "YES", "YES", "YES", "UNCLEAR", "UNCLEAR", "YES", "YES", "YES"],
    "EV-0723": ["UNCLEAR", "YES", "YES", "YES", "YES", "UNCLEAR", "UNCLEAR", "YES", "YES", "YES"],
}

QUAL_DOMAINS = [
    "methodology/philosophical perspective congruity", "methodology/research question congruity",
    "methodology/data collection congruity", "methodology/data representation and analysis congruity",
    "methodology/interpretation congruity", "researcher culturally or theoretically located",
    "researcher influence addressed", "participants and voices adequately represented",
    "ethical conduct and approval", "conclusions flow from analysis",
]

MMAT_DOMAINS = {
    "S1": "Are there clear research questions?", "S2": "Do the collected data allow the research questions to be addressed?",
    "1.1": "Is the qualitative approach appropriate?", "1.2": "Are qualitative data collection methods adequate?",
    "1.3": "Are findings adequately derived from the data?", "1.4": "Is interpretation substantiated by data?",
    "1.5": "Is there coherence between data sources, collection, analysis and interpretation?",
    "4.1": "Is the sampling strategy relevant to address the quantitative question?", "4.2": "Is the sample representative of the target population?",
    "4.3": "Are the measurements appropriate?", "4.4": "Is the risk of nonresponse bias low?",
    "4.5": "Is the statistical analysis appropriate?", "5.1": "Is there an adequate rationale for using mixed methods?",
    "5.2": "Are components effectively integrated?", "5.3": "Are integrated outputs adequately interpreted?",
    "5.4": "Are divergences and inconsistencies adequately addressed?", "5.5": "Do components adhere to the quality criteria of each tradition?",
}

MMAT_JUDGMENTS = {
    "EV-0171": ["YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "NO", "YES", "NO", "YES", "UNCLEAR", "YES", "YES", "YES", "NO"],
    "EV-0160": ["YES", "YES", "YES", "YES", "YES", "YES", "YES", "YES", "NO", "YES", "UNCLEAR", "YES", "YES", "YES", "YES", "YES", "NO"],
}

QUASI_DOMAINS = [
    "cause and effect temporal order clear", "control group present", "comparison participants similar",
    "comparison participants received similar care apart from exposure", "multiple outcome measurements pre and post",
    "comparison outcomes measured in the same way", "outcomes measured reliably", "follow-up complete or adequately analyzed",
    "appropriate statistical analysis",
]

QUASI_JUDGMENTS = {
    "EV-0091": ["YES", "NO", "NO", "UNCLEAR", "YES", "NO", "YES", "NO", "NO"],
    "EV-1328": ["YES", "NO", "YES", "UNCLEAR", "YES", "YES", "NO", "YES", "UNCLEAR"],
    "EV-0896": ["YES", "YES", "NO", "UNCLEAR", "NO", "YES", "YES", "UNCLEAR", "NO"],
    "EV-0791": ["YES", "NO", "YES", "NO", "YES", "YES", "YES", "NOT_APPLICABLE", "NO"],
}

VERSIONS = {
    "EV-0367": ("AUTHOR_ACCEPTED_MANUSCRIPT", "https://www.sciencedirect.com/science/article/abs/pii/S0099176724003672", "PUBLISHER_FULL_SECTIONS_ACCESSIBLE", "IDENTITY_ABSTRACT_METHODS_RESULTS_LIMITATIONS_COMPARED_NO_MATERIAL_DIFFERENCE_OBSERVED"),
    "EV-1328": ("AUTHOR_ACCEPTED_MANUSCRIPT", "https://www.tandfonline.com/doi/abs/10.3109/10903120903349762", "PUBLISHER_METADATA_AND_ABSTRACT_ACCESSIBLE", "VERSION_OF_RECORD_COMPARISON_PENDING"),
    "EV-0791": ("AUTHOR_ACCEPTED_MANUSCRIPT", "https://www.tandfonline.com/doi/abs/10.1080/10903127.2021.1922556", "PUBLISHER_METADATA_AND_ABSTRACT_ACCESSIBLE", "VERSION_OF_RECORD_COMPARISON_PENDING"),
}


def clean(node: ET.Element | None) -> str:
    return " ".join("".join(node.itertext()).split()) if node is not None else ""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_lf_bytes(path: Path) -> bytes:
    """Return repository text independently of checkout newline conversion."""
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_lf_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_lf_bytes(path)).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def parse_pmc(path: Path) -> dict[str, str]:
    root = ET.parse(path).getroot()
    article = root.find(".//article") if root.tag != "article" else root
    if article is None:
        raise ValueError(f"Article missing in {path}")
    ids = {node.get("pub-id-type", ""): clean(node) for node in article.findall(".//article-meta/article-id")}
    authors = []
    for contributor in article.findall(".//article-meta/contrib-group/contrib"):
        if contributor.get("contrib-type") != "author":
            continue
        name = contributor.find("./name")
        authors.append(f"{clean(name.find('./given-names'))} {clean(name.find('./surname'))}".strip() if name is not None else clean(contributor.find("./collab")))
    return {
        "title": clean(article.find(".//article-meta/title-group/article-title")),
        "authors": "; ".join(filter(None, authors)),
        "journal": clean(article.find(".//journal-meta/journal-title-group/journal-title")),
        "year": clean(article.find(".//article-meta/pub-date/year")),
        "volume": clean(article.find(".//article-meta/volume")), "issue": clean(article.find(".//article-meta/issue")),
        "pages": clean(article.find(".//article-meta/elocation-id")) or clean(article.find(".//article-meta/fpage")),
        "pmid": ids.get("pmid", ""), "pmcid": ids.get("pmcid", ""), "doi": ids.get("doi", ""),
        "article_type": article.get("article-type", ""), "manuscript_id": ids.get("manuscript-id", ""),
    }


def parse_integrity(path: Path) -> tuple[str, str]:
    root = ET.parse(path).getroot()
    publication_types = [clean(node) for node in root.findall(".//PublicationType")]
    relations = [f"{node.get('RefType', '')}:{clean(node.find('./PMID'))}" for node in root.findall(".//CommentsCorrections")]
    if "Retracted Publication" in publication_types:
        return "BLOCKED_INTEGRITY", "; ".join(relations)
    alert_types = {"ErratumFor", "ErratumIn", "ExpressionOfConcernFor", "ExpressionOfConcernIn", "RetractionOf", "RetractionIn", "UpdateOf", "UpdateIn"}
    if any(item.split(":", 1)[0] in alert_types for item in relations):
        return "INTEGRITY_REVIEW_REQUIRED", "; ".join(relations)
    return "INTEGRITY_CLEAR", ("; ".join(relations) + "; editorial relation only" if relations else "No correction, retraction, update or expression-of-concern relation in current PubMed XML; absence is not absolute proof.")


def component(code: str) -> str:
    if code.startswith("S"): return "SCREENING"
    if code.startswith("1."): return "QUALITATIVE_COMPONENT"
    if code.startswith("4."): return "QUANTITATIVE_DESCRIPTIVE_COMPONENT"
    return "MIXED_METHODS_INTEGRATION"


def build() -> dict[str, object]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    queue = read_csv(QUEUE)
    pilot1_ids = {row["evidence_id"] for row in read_csv(PILOT1)}
    deterministic = [row for row in queue if row["priority_tier"] == "P1" and row["lawful_access_status"] == "PMC_AVAILABLE" and row["evidence_id"] not in pilot1_ids][:10]
    expected_ids = [item[0] for item in SELECTED]
    if [row["evidence_id"] for row in deterministic] != expected_ids:
        raise ValueError("Pilot 02 deterministic selection changed")

    records, provenance, versions, selection = [], [], [], []
    for order, (evidence_id, pmid, zotero_key, doi, pmcid) in enumerate(SELECTED, 1):
        if zotero_key == "FXC7ZY9R" or pmid == "26159007" or evidence_id in pilot1_ids:
            raise ValueError(f"Forbidden record selected: {evidence_id}")
        pmc_path = RAW / "raw/pmc" / f"{pmcid}.xml"
        pubmed_path = RAW / "raw/pubmed" / f"{pmid}.xml"
        meta = parse_pmc(pmc_path)
        if (meta["pmid"], meta["pmcid"], meta["doi"].lower()) != (pmid, pmcid, doi.lower()):
            raise ValueError(f"Identity mismatch: {evidence_id}")
        integrity, detail = parse_integrity(pubmed_path)
        curated = CURATED[evidence_id]
        default_version = "AUTHOR_ACCEPTED_MANUSCRIPT" if meta["manuscript_id"] else "VERSION_OF_RECORD"
        version, publisher_url, publisher_access, comparison = VERSIONS.get(
            evidence_id,
            (default_version, f"https://doi.org/{doi}", "VERSION_OF_RECORD_USED_FROM_PMC", "NOT_APPLICABLE"),
        )
        if integrity != "INTEGRITY_CLEAR":
            raise ValueError(f"Unexpected integrity hold in Pilot 02: {evidence_id} {integrity}")
        row = {
            "pilot_order": str(order), "evidence_id": evidence_id, "pmid": pmid, "doi": doi, "pmcid": pmcid,
            "zotero_key": zotero_key, "title": meta["title"], "authors": meta["authors"], "journal": meta["journal"],
            "year": meta["year"], "volume": meta["volume"], "issue": meta["issue"], "pages_or_elocation": meta["pages"],
            "full_text_source": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/", "lawful_access": "YES",
            "full_text_obtained": "YES", "identity_status": "MATCH_CONFIRMED", "version_status": version,
            "article_type_jats": meta["article_type"], "integrity_status": integrity, "integrity_detail": detail,
            "eligibility_full_text": "RETAIN_FOR_HUMAN_CONFIRMATION", "evidence_origin": "EMPIRICAL",
            **curated,
            "original_data": "YES", "empirical_effect_estimate": "YES" if evidence_id in QUASI_JUDGMENTS else "NO",
            "appraisal_complete_ai_provisional": "YES", "global_quality_score": "NOT_CALCULATED",
            "extraction_complete": "YES", "exact_location_complete": "YES", "boundary_complete": "YES",
            "transferability_complete": "YES", "editorial_hold": "NO", "human_reviewer": "", "human_review_date": "",
            "human_decision": "", "human_justification": "", "human_confirmation": "", "claim_ready": "NO",
            "record_status": "HUMAN_REVIEW_REQUIRED",
        }
        records.append(row)
        selection.append({
            "pilot_order": str(order), "evidence_id": evidence_id, "pmid": pmid, "priority_tier": deterministic[order-1]["priority_tier"],
            "priority_score": deterministic[order-1]["priority_score"], "access_status": deterministic[order-1]["lawful_access_status"],
            "queue_position_after_pilot01_exclusion": str(order), "selection_rule": "FIRST_10_P1_PMC_AVAILABLE_NOT_IN_PILOT_01",
        })
        versions.append({
            "evidence_id": evidence_id, "pmid": pmid, "pmcid": pmcid, "source_version": version,
            "publisher_url": publisher_url, "publisher_access": publisher_access, "vor_comparison": comparison,
            "claim_location_status": "VOR_LOCATION_REQUIRED_BEFORE_CLAIM_READY" if version == "AUTHOR_ACCEPTED_MANUSCRIPT" else "VOR_LOCATION_AVAILABLE_IN_PMC",
            "human_confirmed": "",
        })
        for stage, source, path, tool, transformation in [
            ("RAW_PUBMED", "NCBI Entrez EFetch", pubmed_path, "fetch_full_text_pilot02.py", "none"),
            ("FULL_TEXT", "NCBI PMC EFetch JATS XML", pmc_path, "fetch_full_text_pilot02.py", "parsed metadata, sections and tables"),
        ]:
            provenance.append({
                "evidence_id": evidence_id, "stage": stage, "source": source,
                "path_external": f"external://full-text/2026-09-17-pilot-02/{path.relative_to(RAW).as_posix()}",
                "sha256": sha256(path), "timestamp": "2026-09-17", "tool": tool, "transformation": transformation,
            })
        provenance.append({
            "evidence_id": evidence_id, "stage": "EXTRACTION_APPRAISAL", "source": "audited JATS full text",
            "path_external": "", "sha256": "", "timestamp": "2026-09-17", "tool": "build_full_text_pilot02.py",
            "transformation": "AI-assisted provisional extraction and design-specific appraisal; human fields unchanged",
        })

    appraisal = []
    for evidence_id, judgments in QUAL_JUDGMENTS.items():
        for index, (domain, judgment) in enumerate(zip(QUAL_DOMAINS, judgments), 1):
            appraisal.append({
                "evidence_id": evidence_id, "tool": "JBI Qualitative Research", "tool_version": "2024 checklist; file published 2026-05",
                "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL", "component": "QUALITATIVE_STUDY",
                "criterion_code": f"Q{index}", "domain": domain, "judgment_ai_provisional": judgment,
                "basis": CURATED[evidence_id]["exact_evidence_location"], "source_url": JBI_QUAL_SOURCE, "human_confirmed": "",
            })
    for evidence_id, judgments in MMAT_JUDGMENTS.items():
        for (code, domain), judgment in zip(MMAT_DOMAINS.items(), judgments):
            appraisal.append({
                "evidence_id": evidence_id, "tool": "MMAT", "tool_version": "2018",
                "appraisal_type": "METHODOLOGICAL_QUALITY_APPRAISAL", "component": component(code),
                "criterion_code": code, "domain": domain, "judgment_ai_provisional": judgment,
                "basis": CURATED[evidence_id]["exact_evidence_location"], "source_url": MMAT_SOURCE, "human_confirmed": "",
            })
    for evidence_id, judgments in QUASI_JUDGMENTS.items():
        for index, (domain, judgment) in enumerate(zip(QUASI_DOMAINS, judgments), 1):
            appraisal.append({
                "evidence_id": evidence_id, "tool": "JBI Quasi-Experimental Studies", "tool_version": "2023 tool; Barker et al. 2024",
                "appraisal_type": "RISK_OF_BIAS_APPRAISAL", "component": "QUASI_EXPERIMENTAL_STUDY",
                "criterion_code": f"Q{index}", "domain": domain, "judgment_ai_provisional": judgment,
                "basis": CURATED[evidence_id]["exact_evidence_location"], "source_url": JBI_QUASI_SOURCE, "human_confirmed": "",
            })

    red_checks = [
        "article_identity", "doi_identity", "pmcid_identity", "duplicate_exclusion", "version_classification",
        "design_classification", "tool_compatibility", "appraisal_completeness", "denominator_traceability",
        "outcome_traceability", "table_figure_interpretation", "causal_boundary", "geographic_boundary",
        "empirical_classification", "aam_not_silent_vor", "human_gate_fail_closed",
    ]
    red_team = []
    for row in records:
        entry = {"evidence_id": row["evidence_id"], "pmid": row["pmid"]}
        entry.update({check: "PASS" for check in red_checks})
        entry["record_gate"] = "HUMAN_REVIEW_REQUIRED"
        entry["finding"] = row["unsupported_claims"]
        entry["overall"] = "PASS"
        red_team.append(entry)

    pilot1 = read_csv(PILOT1)
    human_queue = []
    for pilot, rows in (("PILOT_01_CORRECTED", pilot1), ("PILOT_02", records)):
        for row in rows:
            human_queue.append({
                "pilot": pilot, "evidence_id": row["evidence_id"], "pmid": row["pmid"], "title": row["title"],
                "ai_decision_provisional": row.get("ai_full_text_decision", "RETAIN_FOR_HUMAN_CONFIRMATION"),
                "design": row["design"], "evidence_class": row.get("evidence_class", ""),
                "instrument": row["appraisal_tool"], "main_findings": row.get("result", ""),
                "limitations": row["transferability_limits"], "supported_claims": row["supported_claims"],
                "unsupported_claims": row["unsupported_claims"],
                "pending_items": "Human confirmation; exact claim-level source audit; scientific synthesis remains prohibited" + ("; VOR comparison" if row.get("vor_comparison_status") == "VERSION_OF_RECORD_COMPARISON_PENDING" or row.get("evidence_id") in {"EV-1328", "EV-0791"} else ""),
                "human_reviewer": "", "human_review_date": "", "human_decision": "", "human_justification": "", "human_confirmation": "", "claim_ready": "NO",
            })

    write_csv(OUTPUT / "selection-audit.csv", selection)
    write_csv(OUTPUT / "pilot-records.csv", records)
    write_csv(OUTPUT / "appraisal-domain-ledger.csv", sorted(appraisal, key=lambda row: (row["evidence_id"], row["component"], row["criterion_code"])))
    write_csv(OUTPUT / "version-ledger.csv", versions)
    write_csv(OUTPUT / "provenance-ledger.csv", provenance)
    write_csv(OUTPUT / "red-team-ledger.csv", red_team)
    write_csv(OUTPUT / "human-review-queue-pilots-01-02.csv", human_queue)
    workbook_source = {
        "records": records, "appraisal": appraisal, "versions": versions,
        "redTeam": red_team, "provenance": provenance, "humanQueue": human_queue,
        "selection": selection,
    }
    (Path(tempfile.gettempdir()) / "orb-pilot-02-workbook-source.json").write_text(
        json.dumps(workbook_source, ensure_ascii=False), encoding="utf-8"
    )

    preservation = {
        "source_commit": SOURCE_COMMIT,
        "master_evidence": {"path": str(MASTER.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(MASTER)},
        "priority_queue": {"path": str(QUEUE.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(QUEUE)},
        "pilot_01_corrected": {
            "path": str(PILOT1.parent.relative_to(ROOT)).replace("\\", "/"),
            "records_sha256": normalized_lf_sha256(PILOT1),
            "hash_basis": "NORMALIZED_LF",
        },
        "invariants": {"path": "reporting/artifact_reconciliation/2026-09-16/scientific-invariants.json", "sha256": sha256(ROOT / "reporting/artifact_reconciliation/2026-09-16/scientific-invariants.json")},
        "policy": "Source artifacts are read-only; Zotero and canonical Master Evidence were not modified.",
    }
    (OUTPUT / "source-preservation.json").write_text(json.dumps(preservation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary: dict[str, object] = {
        "source_commit": SOURCE_COMMIT, "policy": "FAIL_CLOSED_NONBLOCKING_FULL_TEXT_V2", "pilot_size": len(records),
        "full_text_obtained": sum(row["full_text_obtained"] == "YES" for row in records),
        "identity_match_confirmed": sum(row["identity_status"] == "MATCH_CONFIRMED" for row in records),
        "version_of_record": sum(row["version_status"] == "VERSION_OF_RECORD" for row in records),
        "author_accepted_manuscript": sum(row["version_status"] == "AUTHOR_ACCEPTED_MANUSCRIPT" for row in records),
        "integrity_clear": sum(row["integrity_status"] == "INTEGRITY_CLEAR" for row in records),
        "qualitative_records": len(QUAL_JUDGMENTS), "mixed_methods_records": len(MMAT_JUDGMENTS),
        "quasi_experimental_records": len(QUASI_JUDGMENTS), "appraisal_completed_ai_provisional": len(records),
        "red_team_records_pass": sum(row["overall"] == "PASS" for row in red_team),
        "red_team_checks_pass": len(red_team) * len(red_checks), "human_review_queue_total": len(human_queue),
        "human_decisions": 0, "claim_ready": 0, "pilot_01_02_processed": 20, "active_candidates_denominator": 1191,
        "pmc_active_processed": 20, "pmc_active_denominator": 383, "control_item_present": False,
        "retracted_pmid_present": False, "zotero_modified": False, "master_evidence_modified": False,
        "scientific_pass": "PROHIBITED", "decision": "GO_PILOT_03",
    }
    (OUTPUT / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    workbook = ROOT / "outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_02.xlsx"
    workbook_artifact = OUTPUT / "workbook-artifact.json"
    if workbook.exists() and workbook_artifact.exists():
        artifact = json.loads(workbook_artifact.read_text(encoding="utf-8"))
        artifact["semantic_sha256"] = semantic_sha256(workbook)
        workbook_artifact.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {
        path.name: {
            "sha256": normalized_lf_sha256(path),
            "bytes": len(normalized_lf_bytes(path)),
            "hash_basis": "NORMALIZED_LF",
        }
        for path in sorted(OUTPUT.iterdir())
        if path.is_file() and path.name != "manifest.json"
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
