"""Build the non-scientific Journal of Occupational Health target-selection record."""
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch11_3h"
OUT.mkdir(exist_ok=True)
DATE = "2026-10-11"
DOCX = ROOT / "batch11_2h" / "International_v1.3-FINAL-SCIENTIFIC-FREEZE.docx"
MD = ROOT / "batch11_2h" / "International_v1.3-FINAL-SCIENTIFIC-FREEZE.md"
BASE_COMMIT = "a0ecad3327e1b9c4a3a7c61930d059c4156790c3"
JOH_GUIDELINES = "https://academic.oup.com/joh/pages/author-guidelines"
OUP_AI_POLICY = "https://academic.oup.com/pages/for-authors/journals/preparing-and-submitting-your-manuscript/ai-principles-for-oxford-journals/policy-on-ai-use-and-disclosure-for-oxford-journals-authors"


def canonical_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def literal_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def write_csv(name: str, rows: list[dict], fields: list[str] | None = None) -> None:
    fields = fields or list(rows[0])
    with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_md(name: str, text: str) -> None:
    (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    assert DOCX.exists() and MD.exists(), "Frozen v1.3 source is missing"
    source_before = {"docx_sha256": literal_sha(DOCX), "markdown_sha256_canonical_lf": canonical_sha(MD)}
    assert source_before == {
        "docx_sha256": "f5886dd8e715ee5d4666213b5b59027e382185a3ae19ce7959417ce6fe672030",
        "markdown_sha256_canonical_lf": "e94de20c2e0882f8bd023ac701d81fd8672bc07ada0b97cda0b6f11cbbbd688b",
    }, "Frozen v1.3 source hash changed; refuse target-journal freeze"

    manuscript = MD.read_text(encoding="utf-8")
    abstract = re.search(r"## Abstract\n\n(.*?)(?=\n\n\*\*Keywords)", manuscript, re.S).group(1)
    keywords_match = re.search(r"\*\*Keywords:\*\*\s*(.*)", manuscript)
    keywords = [part.strip() for part in re.split(r"[;,]", keywords_match.group(1))] if keywords_match else []
    facts = {
        "abstract_words": word_count(abstract),
        "body_words": 4205,
        "references": len(re.findall(r"^\d+\. ", manuscript, re.M)),
        "tables": 0,
        "figures": 0,
        "rendered_pages": 11,
        "keywords_current_count": len(keywords),
        "frozen_framework_label": "PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED",
    }
    assert facts["abstract_words"] == 145 and facts["references"] == 28

    write_csv("TARGET_JOURNAL_HUMAN_DECISION_FINAL.csv", [{
        "Decision_ID": "HD-11.3-001", "Human_Reviewer": "Matheus Florindo de Deus",
        "Human_Decision_Date": DATE, "Target_Journal": "Journal of Occupational Health",
        "Target_Publisher": "Oxford University Press", "Target_Article_Type": "Review Article",
        "Target_Status": "HUMAN_SELECTED",
        "Backup_1": "Occupational Medicine", "Backup_2": "Military Medicine",
        "Rationale": "Human selection after the Batch 11.3 scientific-editorial ranking: occupational-health scope, tactical-worker relevance, compatible Review Article category, and adequate current limits.",
        "Scientific_Mutation": "0", "Claim_Ready_Mutation": "0", "CEF_Mutation": "0", "Zotero_Mutation": "0", "Brazil_Mutation": "0", "Authorship_Mutation": "0",
    }])

    guideline_rows = [
        ("Article type", "Review Article", "Review Article", "VERIFIED"),
        ("Maximum manuscript word count", "6000", str(facts["body_words"]), "VERIFIED"),
        ("Structured abstract maximum", "250", str(facts["abstract_words"]), "VERIFIED"),
        ("Abstract headings", "Objectives; Methods; Results; Conclusions", "Current abstract not journal-structured", "VERIFIED"),
        ("Keywords", "3 to 6", str(facts["keywords_current_count"]), "VERIFIED"),
        ("Key Points", "3 to 5 sentences; total maximum 250 words", "Absent from frozen manuscript", "VERIFIED"),
        ("References", "No limit", str(facts["references"]), "VERIFIED"),
        ("Figures/tables", "Maximum 6 combined", "0", "VERIFIED"),
        ("Language", "English; US spelling consistently", "Requires editorial check", "VERIFIED"),
        ("Review model", "Single-anonymized peer review", "No manuscript change now", "VERIFIED"),
        ("Required file order", "Abstract/keywords; Key Points; main text; acknowledgments; CRediT; supplementary data; COI; data availability; funding; references", "Not JOH-packaged", "VERIFIED"),
    ]
    write_csv("JOH_CURRENT_AUTHOR_GUIDELINES_REVALIDATION.csv", [
        {"Guideline_Item": item, "JOH_Current_Requirement": requirement, "Current_Manuscript_State": current,
         "Live_Revalidation_Status": status, "Guidelines_URL": JOH_GUIDELINES,
         "Guidelines_Revalidated_Date": DATE, "Author_Guideline_Change_Detected": "NO"}
        for item, requirement, current, status in guideline_rows
    ])

    reqs = [
        ("title", "Frozen title", "Journal-appropriate title assessed later", "EDITORIAL_ADAPTATION_REQUIRED", "Title fit review only; no scientific reframing."),
        ("article type", "Evidence-informed integrative synthesis", "Review Article", "READY", "Article type is editorially compatible; never call the work a systematic review."),
        ("abstract", "145 words", "Structured; maximum 250 words", "EDITORIAL_ADAPTATION_REQUIRED", "Reorganize only within frozen evidence."),
        ("abstract headings", "Not JOH-structured", "Objectives; Methods; Results; Conclusions", "EDITORIAL_ADAPTATION_REQUIRED", "Required journal structure."),
        ("keywords", f"{facts['keywords_current_count']} currently", "3 to 6", "READY", "Validate final terms at adaptation."),
        ("key points", "Absent", "3 to 5 sentences; maximum 250 words", "EDITORIAL_ADAPTATION_REQUIRED", "Draft from frozen claims only."),
        ("main-text word count", "4205 words", "Maximum 6000 words", "READY", "Scientific_content_reduction_required=NO."),
        ("headings", "Scientific freeze structure", "JOH file order", "EDITORIAL_ADAPTATION_REQUIRED", "Reorder without changing scientific claims."),
        ("references", "28", "No limit", "READY", "Citation style formatting remains editorial."),
        ("citation style", "Frozen working style", "JOH/OUP style", "EDITORIAL_ADAPTATION_REQUIRED", "Format only; do not change reference set."),
        ("tables", "0", "Maximum 6 combined figures/tables", "READY", "None required."),
        ("figures", "0", "Maximum 6 combined figures/tables", "READY", "None required."),
        ("acknowledgments", "Not JOH-packaged", "Required section in file order", "HUMAN_INPUT_REQUIRED", "No acknowledgment fact invented."),
        ("CRediT", "No role allocation in this batch", "Author Contributions (e.g., CRediT)", "HUMAN_INPUT_REQUIRED", "Use only an existing, verified human authorship record."),
        ("conflicts of interest", "NO CONFLICTS DECLARED", "Conflict of Interest section", "EDITORIAL_ADAPTATION_REQUIRED", "Render compatible wording only."),
        ("funding", "NO FUNDING", "Study Funding section", "EDITORIAL_ADAPTATION_REQUIRED", "Render compatible wording only."),
        ("data availability", "Evidence artifacts under governance", "Data Availability Statement", "HUMAN_INPUT_REQUIRED", "Do not publish private material without authorization."),
        ("AI disclosure", "No submission disclosure approved", "OUP journal AI policy applies", "HUMAN_INPUT_REQUIRED", "Determine accurate disclosure from confirmed uses at submission."),
        ("supplementary files", "None currently", "Supplementary Data section if applicable", "NOT_APPLICABLE", "No supplementary file is created in this batch."),
        ("title page", "Not JOH-packaged", "Title; authors/affiliations; one corresponding author address/email", "HUMAN_INPUT_REQUIRED", "No identity, affiliation, email, or author-role fact invented."),
        ("corresponding author", "No current human record located in versioned Batch 11 artifacts", "One corresponding author required", "HUMAN_INPUT_REQUIRED", "Do not assume Danilo is corresponding/submitting author."),
        ("cover letter", "Not created", "Submission-supporting document", "EDITORIAL_ADAPTATION_REQUIRED", "Prepare after authorship and AI-use facts are confirmed."),
        ("spelling convention", "Not checked in this batch", "US spelling consistently", "EDITORIAL_ADAPTATION_REQUIRED", "Editorial language pass only."),
        ("reporting-guideline requirements", "Non-systematic evidence-informed integrative synthesis", "PRISMA encouraged for systematic reviews/meta-analyses; no blanket PRISMA claim", "READY", "Do not declare PRISMA conformity."),
    ]
    write_csv("JOH_EDITORIAL_REQUIREMENT_MAP.csv", [
        {"Field": field, "Current_Manuscript": current, "JOH_Requirement": requirement,
         "Status": status, "Batch_11_4_Action": action}
        for field, current, requirement, status, action in reqs
    ])

    gaps = [
        ("Word count", "4205/6000", "NO_GAP", "No scientific content reduction."),
        ("Abstract", "145/250; not structured", "EDITORIAL_GAP", "Use Objectives, Methods, Results, Conclusions without expanding unsupported content."),
        ("Key Points", "Absent", "EDITORIAL_GAP", "Create 3–5 bounded sentences after scientific freeze."),
        ("Author declarations", "Not journal-packaged", "HUMAN_INPUT_GAP", "Obtain verified authorship, CRediT, corresponding-author and availability facts."),
        ("AI disclosure", "Not determined from a final author-approved declaration", "HUMAN_INPUT_GAP", "Apply current OUP policy at submission."),
        ("APC", "Exact payable amount not reproducible without eligibility inputs", "HUMAN_ELIGIBILITY_GAP", "Check institution, agreement, country, license, tax and corresponding-author conditions."),
        ("Scientific claims", "Frozen v1.3", "NO_GAP", "No scientific alteration authorized."),
    ]
    write_csv("JOH_MANUSCRIPT_GAP_ANALYSIS.csv", [
        {"Gap_Area": area, "Current_State": current, "Gap_Status": status, "Bounded_Next_Action": action}
        for area, current, status, action in gaps
    ])

    write_md("JOH_ARTICLE_TYPE_COMPATIBILITY_FINAL.md", f"""# Journal of Occupational Health — Article-type compatibility

## Decision

`Review Article` is compatible with the frozen manuscript's real design: **evidence-informed integrative synthesis with explicit evidence-governance framework**. The JOH definition permits review, evaluation, or commentary on research reports focused on a specific theme. It does not require this work to be represented as a systematic review.

## Boundary

The manuscript must not assert PRISMA compliance, systematic-review status, or a validated framework. Its framework label remains `{facts['frozen_framework_label']}`. Any material scientific change requires a `FREEZE_CHANGE_REQUEST`.

## Fit

The measured body is {facts['body_words']} words against the 6000-word limit, with {facts['references']} references and no tables or figures. No scientific-content reduction is required.

## Status

`ARTICLE_TYPE_COMPATIBLE — EDITORIAL_ADAPTATION_PENDING`
""")
    write_md("JOH_REPORTING_GUIDELINE_AUDIT.md", """# JOH reporting-guideline audit

## Current journal guidance

The JOH author guidelines encourage PRISMA for systematic reviews and meta-analyses. They also identify specific requirements for other designs where applicable, such as RECORD for studies using routinely collected health data.

## Applicability to this manuscript

The frozen manuscript is an evidence-informed integrative synthesis, not a systematic review or meta-analysis, and it does not use routinely collected health-data methods. Therefore `PRISMA_CLAIM = NO` and `RECORD_CLAIM = NO`.

## Editorial action

At adaptation, describe the real evidence-identification and governance methods accurately. Do not add a reporting-guideline compliance declaration unless a human-led methodological reassessment establishes that it is true.
""")
    write_md("JOH_AI_DISCLOSURE_POLICY_AUDIT.md", f"""# OUP journal AI-use and disclosure audit

## Live policy source

{OUP_AI_POLICY}

Access revalidated: {DATE}. The current OUP journals policy says that language-only clarity improvements and reference formatting may be permitted without disclosure; substantial editing, rewriting, reorganization, translation, data work, code, or generated illustrative material typically require disclosure. It requires disclosed AI use in both the cover letter and the manuscript acknowledgements, with tool/version, use, and author review/validation. It also states that authors remain accountable and that AI tools do not qualify as authors.

## Decision for this batch

No author-approved factual disclosure is created here. `AI_DISCLOSURE_STATUS = HUMAN_INPUT_REQUIRED`. The submission-stage disclosure must be based on an accurate, human-confirmed account of tools and uses, and must follow any JOH-specific variation that is current at submission.

## Protection

No scientific source, private manuscript material, author identity, or authorship role is disclosed or changed by this audit.
""")
    write_md("JOH_APC_FINAL_VERIFICATION.md", f"""# JOH APC verification

## Live source

{JOH_GUIDELINES}

Access revalidated: {DATE}. Journal of Occupational Health is fully open access and an article processing charge applies. OUP presents the payable charge through a dynamic selector; its result can depend on eligibility and publication choices.

## Determination

`FINAL_APC_REQUIRES_AUTHOR_ELIGIBILITY_CHECK`

`EXACT_CURRENT_APC_NOT_VERIFIABLE_WITHOUT_AUTHOR_ELIGIBILITY`

No monetary amount, tax treatment, waiver, discount, institutional agreement, or corresponding-author eligibility is asserted in this batch. These must be checked by the authors before submission.
""")

    freeze = {
        "batch": "BATCH 11.3H", "base_commit": BASE_COMMIT, "date": DATE,
        "target_journal": "Journal of Occupational Health", "target_publisher": "Oxford University Press",
        "target_article_type": "Review Article", "target_status": "HUMAN_SELECTED",
        "human_reviewer": "Matheus Florindo de Deus", "backup_journals": ["Occupational Medicine", "Military Medicine"],
        "guidelines_url": JOH_GUIDELINES, "guidelines_live_revalidated": "YES",
        "frozen_manuscript": source_before, "scientific_freeze": "FULL_MANUSCRIPT_SCIENTIFIC_FREEZE_COMPLETE",
        "guardrails": {"scientific_mutation": 0, "claim_ready_mutation": 0, "cef_mutation": 0, "zotero_mutation": 0, "brazil_mutation": 0, "authorship_mutation": 0},
        "next_gate": "GO_JOH_EDITORIAL_ADAPTATION",
    }
    (OUT / "TARGET_JOURNAL_FREEZE.json").write_text(json.dumps(freeze, indent=2) + "\n", encoding="utf-8")

    source_after = {"docx_sha256": literal_sha(DOCX), "markdown_sha256_canonical_lf": canonical_sha(MD)}
    assert source_before == source_after, "Frozen manuscript mutated during non-scientific batch"

    outputs = []
    for path in sorted(OUT.iterdir()):
        if path.is_file() and path.name not in {"BATCH11_3H_MANIFEST.json", "BATCH11_3H_REPORT.md"}:
            outputs.append({"file": path.name, "sha256_canonical_lf": canonical_sha(path)})
    manifest = {
        "batch": "BATCH 11.3H", "base_commit": BASE_COMMIT, "date": DATE,
        "gate": "TARGET_JOURNAL_HUMAN_SELECTION_PASS", "freeze_gate": "TARGET_JOURNAL_FREEZE_COMPLETE",
        "next_gate": "GO_JOH_EDITORIAL_ADAPTATION", "target": freeze,
        "input_manuscript": source_before,
        "measured_input": facts,
        "qa": {"human_journal_selection": "1/1", "official_guidelines_live_revalidated": "YES", "target_journal": "Journal of Occupational Health", "article_type": "Review Article", "backup_journals_preserved": "YES", **freeze["guardrails"]},
        "outputs": outputs,
    }
    (OUT / "BATCH11_3H_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_md("BATCH11_3H_REPORT.md", f"""# Batch 11.3H — Target journal human selection

## Gate

`TARGET_JOURNAL_HUMAN_SELECTION_PASS`

`TARGET_JOURNAL_FREEZE_COMPLETE`

`GO_JOH_EDITORIAL_ADAPTATION`

## Formal human decision

Matheus Florindo de Deus selected **Journal of Occupational Health** (Oxford University Press) as the principal target and **Review Article** as the selected category. Occupational Medicine and Military Medicine remain contingency journals only.

## Live revalidation

The current official author guidelines were revalidated on {DATE}. The expected Review Article requirements remain compatible: 6000-word maximum, 250-word structured abstract, 3–6 keywords, 3–5 Key Points sentences with a 250-word maximum, unlimited references, and up to six combined tables/figures. The frozen manuscript has a {facts['body_words']}-word body, {facts['abstract_words']}-word abstract, {facts['references']} references, zero tables, and zero figures.

## Boundaries

No manuscript, scientific claim, Evidence_ID, Result_ID, CEF-v1, Zotero, Brazil artifact, reference set, or authorship record was changed. The OUP AI-policy and APC checks identify submission-time human inputs; this batch does not create a disclosure or a price commitment.
""")

    expected = 11
    actual = len([path for path in OUT.iterdir() if path.is_file()])
    assert actual == expected, f"Expected {expected} artifacts, found {actual}"
    print(json.dumps({"artifacts": f"{actual}/{expected}", "gate": manifest["gate"], "source_unchanged": source_before == source_after}, indent=2))


if __name__ == "__main__":
    main()
