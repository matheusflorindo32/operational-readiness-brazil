# Full-text evidence qualification — pilot 01

**Execution date:** 2026-09-17

**Entry commit:** `c3dd18ac7f457f337b44dc303e2f6199a05d7afd`

**Architecture:** `FAIL_CLOSED + NONBLOCKING`

**Decision:** `GO_NONBLOCKING_HUMAN_REVIEW_REQUIRED`
**Scientific PASS:** prohibited

## 1. Estado inicial

The remote and local checkout were aligned at the entry commit, the working tree
was clean, and GitHub Actions run `35091619376` was green. The previous artifact
gate remained `GO_WITH_DOCUMENTED_NONSEMANTIC_VARIANCE`. The scientific baseline
remained 1,456 reconciled identities, 1,206 full-text candidates, 1,191 active,
15 on editorial hold, 240 pending adjudication, one retraction quarantined and
zero Claim-Ready records.

The live Zotero read-only precheck returned API/Connector HTTP 200, 1,457 unique
top-level items, 1,456 items in production collection `PE9UF4YN`, and only
`FXC7ZY9R` in controlled collection `EMHHKNTM`. No Zotero write, reimport, merge
or deletion occurred.

The existing test suite initially exposed one date-sensitive assertion: a
deterministic rebuild executed on 2026-09-17 was compared literally with the
committed `generated_on=2026-09-16`. The assertion now excludes only that
execution-date field and continues comparing every scientific and operational
field. The full suite then passed.

## 2. Registros selecionados

The pilot used the first ten P1 active records with a known PMC route, in the
existing priority-queue order. `FXC7ZY9R`, the quarantined retraction and all
editorial-hold records were excluded.

| Evidence ID | PMID | PMCID | Zotero key | AI full-text state |
|---|---:|---|---|---|
| EV-0668 | 36141388 | PMC9498760 | BHR9XD2I | INCLUDE_FULL_TEXT |
| EV-0787 | 33933923 | PMC8530836 | 4AXW7YEU | INCLUDE_FULL_TEXT |
| EV-0758 | 34622213 | PMC8116638 | CRYUZSIZ | INCLUDE_FULL_TEXT |
| EV-0753 | 34665820 | PMC8525775 | NAFL5D8I | INCLUDE_FULL_TEXT |
| EV-0727 | 35076700 | PMC8790663 | H7XKJIDC | INCLUDE_FULL_TEXT |
| EV-0593 | 37297641 | PMC10252876 | 57HE5M3N | INCLUDE_FULL_TEXT |
| EV-0523 | 38115970 | PMC10729156 | 45XR289H | HUMAN_REVIEW_REQUIRED |
| EV-0503 | 38322801 | PMC10775732 | 7Q3Z785H | INCLUDE_FULL_TEXT |
| EV-0447 | 39028235 | PMC11254139 | 5H6N3ED3 | INCLUDE_FULL_TEXT |
| EV-0425 | 39205432 | PMC12372593 | 96HF9IFT | INCLUDE_FULL_TEXT |

These are AI-assisted provisional eligibility states. They are not human
decisions and do not constitute final scientific inclusion.

## 3. Full texts encontrados

NCBI Entrez EFetch returned PubMed XML and complete PMC JATS XML for 10/10
records. The raw XML, response metadata, indexed reading copies and hashes are
preserved outside Git under the dated pilot directory. Every article exposes a
PMC permission or licence statement. Two PMC records are NIH author manuscripts;
the other eight are publisher-deposited versions of record.

The legacy PMC OA package endpoint returned HTTP 404 for these identifiers. This
did not block lawful reading because Entrez/PMC delivered the complete JATS
article and its permission statement. The failed package lookups remain in the
external diagnostics.

## 4. Identidade dos documentos

PMID, DOI and PMCID in each JATS record exactly matched the selected queue row.
Titles, journal, year, volume/issue and pagination or eLocation were extracted
from the same full text. Identity status is `MATCH_CONFIRMED` for 10/10.
All ten DOI requests resolved to a publisher or repository route. Three final
responses were HTTP 200, one was HTTP 202 and six publisher endpoints returned
HTTP 403 after a successful DOI redirect because of automated-access controls;
those 403 responses were not misclassified as missing DOI or missing full text.

## 5. Integridade

No retraction, erratum, correction, expression of concern or update relation was
present in the current PubMed records for the ten articles. The statement is
bounded to the sources checked on the execution date and is not a claim of
absolute absence. EV-0523 has `CommentOn:38020852`; this identifies it as a
commentary and is not itself an integrity alert.

The separately quarantined PMID 26159007 remains `BLOCKED_INTEGRITY / NOT USED`.

## 6. Elegibilidade full text

Nine records were provisionally retained for full-text consideration. EV-0523
was routed to `HUMAN_REVIEW_REQUIRED` because the complete article is an
editorial commentary with no original sample, methods or outcome data. No record
was finally included or excluded by a human reviewer.

## 7. Desenhos identificados

- five qualitative interview/focus-group studies;
- two mixed-methods implementation studies;
- one narrative review/program-development article;
- one conceptual implementation-tool article with descriptive cases;
- one editorial commentary.

## 8. Instrumentos de appraisal escolhidos

SANRA was applied to the narrative review; MMAT 2018 to both mixed-methods
studies; JBI Qualitative Research to the five qualitative studies; and JBI Text
and Opinion to the conceptual article and commentary. Eighty-two domain-level
judgments were recorded. All are explicitly AI-assisted and provisional; no
`human_confirmed` field was populated.

Instrument sources: [SANRA](https://doi.org/10.1186/s41073-019-0064-8),
[MMAT 2018](https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/127916259/MMAT_2018_criteria-manual_2018-08-01_ENG.pdf),
[JBI critical appraisal tools](https://jbi.global/critical-appraisal-tools).

## 9. Extração científica

The extraction ledger records identification, context, sample, design,
intervention or implementation focus, verifiable results, appraisal summary and
claim boundaries. Numeric statements preserve their reported denominators. In
particular, EV-0593's percentages are tied to 19 questionnaire respondents;
EV-0753 has 21 interviews with 27 informants; EV-0727 has 31 participants;
EV-0447 has 32 interviewees; and EV-0425 has 13 interviewees.

## 10. Localização das evidências

Every record has reproducible section/table/paragraph locations in
`exact_evidence_location`. External indexed reading copies preserve hierarchical
section and paragraph identifiers derived directly from the JATS structure.

## 11. Supported claims

The permitted claims are descriptive and bounded: program components, reported
implementation determinants, stakeholder perceptions, service-user preferences,
and the authors' conceptual proposals. They are stored per record in
`SUPPORTED_CLAIMS`.

## 12. Unsupported claims

No pilot record may establish global effectiveness, causal benefit, mortality
reduction, cost-effectiveness, Brazilian transferability or institutional
recommendations solely from this extraction. Each row records its specific
`UNSUPPORTED_CLAIMS`.

## 13. Transferibilidade

Transferability was evaluated separately from methodological appraisal. The
main constraints are US/Canadian/Australian/Pakistani legal and health systems,
small self-selected samples, qualitative designs, local implementation
arrangements, population differences and absence of Brazilian public-safety
outcomes.

## 14. Problemas encontrados

1. The baseline counted 393 PMC routes across all 1,206 candidates; only 383 are
   active and outside editorial hold. The pilot uses the active subset.
2. The PMC package service returned 404 while complete lawful JATS text remained
   available through Entrez/PMC.
3. EV-0787 and EV-0425 are author accepted manuscripts, not silent substitutes
   for a version of record.
4. EV-0523 is commentary rather than an empirical study.
5. Several articles use effectiveness language for perceptions or program
   rationale without an outcome design capable of establishing effectiveness.

## 15. Red Team

The red-team ledger tests identity, DOI, supplement confusion, editorial
relations, retraction, duplication, design, tool compatibility, result and
denominator extraction, table interpretation, outcome hierarchy, adjustment,
causal overreach, population generalization and claim boundaries for every
record. No identity, DOI, duplicate, retraction or denominator defect remained.
Design/claim attention was retained for the narrative, conceptual and commentary
records.

## 16. Correções realizadas

- repaired the date-sensitive reproducibility test without relaxing scientific
  comparisons;
- distinguished non-integrity `CommentOn` relations from correction/retraction
  signals;
- classified the two NIH manuscripts explicitly;
- routed the commentary to human review;
- constrained perceived or proposed benefits to non-causal descriptive claims;
- added fail-closed pipeline validation and provenance hashes.

## 17. Testes

The suite passes 55/55 tests. New controls verify missing full text, unresolved
identity, editorial hold, integrity block, missing appraisal, missing exact
location, missing claim boundary, missing transferability, absent human
confirmation, exclusion of `FXC7ZY9R`, continued quarantine of PMID 26159007,
blank human fields, design-specific tools, provenance hashes and manifest
coverage. The generated workbook was reopened with artifact-tool; all seven
sheets, formulas and blank human-decision fields were verified.

## 18. Arquivos gerados/modificados

Machine-readable ledgers and manifest are under
`reporting/full-text/2026-09-17/pilot-01/`. The separate seven-sheet workbook is
`outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_01.xlsx`.
Raw full texts remain external to Git. Zotero and the canonical Master Evidence
were not modified.

## 19. Commit e CI

The commit and CI identifiers are populated in the final execution report after
publication. The entry CI was green and local validation is green.

## 20. Registros que exigem decisão humana

All 10 require final human review before scientific use. EV-0523 additionally
requires a direct eligibility decision because it is commentary. Reviewer,
review date, decision, justification and confirmation remain blank in 10/10.

## 21. Próximo lote recomendado

After human review of this pilot architecture, process the next ten active P1
PMC records in priority order. Keep records independent, preserve version and
integrity signals, and do not release Claim-Ready until every fail-closed
prerequisite and identifiable human confirmation are present.

## Visible checklist

- [x] Entry state, Git, CI and invariants audited.
- [x] Zotero read-only state reconfirmed.
- [x] Ten lawful full texts obtained and hashed.
- [x] Ten identities and versions checked.
- [x] Ten integrity checks completed with bounded wording.
- [x] Ten designs classified.
- [x] Ten AI-assisted appraisals completed with compatible instruments.
- [x] Ten extractions have exact location, claim boundary and transferability.
- [x] Red Team completed for 10/10.
- [x] Regression suite passes 55/55.
- [x] Human fields blank and Claim-Ready 0/10.
- [ ] Identifiable human review completed: 0/10.

Pilot operational completion is 10/10 (100%). Human confirmation is 0/10
(0.00%). Claim-Ready is 0/10 (0.00%) and remains 0/1,456 globally. The formal
decision is `GO_NONBLOCKING_HUMAN_REVIEW_REQUIRED`; no scientific PASS is made.
