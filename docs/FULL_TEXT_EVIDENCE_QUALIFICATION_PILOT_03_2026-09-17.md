# Full-text evidence qualification — Pilot 03

**Execution date:** 2026-09-17
**Entry commit:** `fc1442d04a5c4c52b46d8a6c70d1531a58ea7ec4`
**Policy:** `FAIL_CLOSED + NONBLOCKING + HUMAN_IN_THE_LOOP`
**Technical decision:** `GO_NEXT_BATCH`
**Scale readiness:** `KEEP_BATCH_SIZE_10`
**Scientific PASS:** prohibited
**Human confirmation:** 0/30 cumulative
**Claim-Ready:** 0/10 in Pilot 03 and 0/1,456 globally

## 1. Gate de entrada

Local `HEAD` and `origin/main` matched the clean audited entry commit. Its GitHub
Actions run was green. Pilot 01 Corrected and Pilot 02 invariants passed, all
human fields were empty, and Claim-Ready was zero. Master Evidence SHA-256 was
`2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b`
before and after the execution. Zotero and Master Evidence remained read-only.

The available external Pilot 02 derivative was audited. Its populated values
match the canonical workbook, but strict semantic identity is false: `Resumo!B17`
uses equivalent sheet-name quoting and two human-review validations add
`allowBlank=1`. It is recorded as `DOCUMENTED_DERIVED_FUNCTIONAL_VARIANCE`; the
Git-canonical Pilot 02 workbook was not replaced.

## 2. Registros selecionados

The deterministic rule selected the first ten active `P1` records with a PMC
route after excluding Pilots 01 and 02.

| Order | Evidence ID | PMID | PMCID | Zotero key |
|---:|---|---:|---|---|
| 1 | EV-0629 | 36747268 | PMC9902242 | LCFHG7J2 |
| 2 | EV-0592 | 37326779 | PMC10689544 | C3CAQKDL |
| 3 | EV-0515 | 38233933 | PMC10795311 | FV2SE2HG |
| 4 | EV-0439 | 39119394 | PMC11307241 | AGAPQVEJ |
| 5 | EV-0405 | 39425094 | PMC11490149 | N3LQZTNN |
| 6 | EV-0335 | 40156033 | PMC11951663 | RALPHKM3 |
| 7 | EV-0316 | 40406195 | PMC12094109 | IPT4R6IA |
| 8 | EV-0282 | 40710431 | PMC12298807 | DSDH9DAX |
| 9 | EV-0252 | 40979841 | PMC12448121 | CGBGDU6Y |
| 10 | EV-0167 | 41537090 | PMC12798756 | X6PMUAYB |

No record was reused. `FXC7ZY9R` and PMID 26159007 are absent.

## 3. Full texts

Lawful PMC full text was obtained for 10/10. Raw PubMed and PMC XML are preserved
outside Git with source URLs and byte hashes recorded in the provenance ledger.
No publisher PDF, personal attachment or Zotero database was committed.

## 4. Identidade

PMID, PMCID and DOI matched the full-text metadata for 10/10; title, article and
production Zotero key are recorded. There were zero identity failures and zero
duplicates within or across the three pilots.

## 5. Versões

Seven records use a PMC version of record. Three are author accepted
manuscripts: EV-0316, EV-0252 and EV-0167. Lawful publisher full text allowed a
section-level comparison for EV-0316 and EV-0167, with no material difference
observed in the compared content. EV-0252 retains `VOR_COMPARISON_PENDING`
because publisher metadata and abstract did not permit sufficient comparison of
methods, results, tables and limitations.

## 6. Integridade

Current PubMed XML showed no correction, retraction, update or expression-of-
concern relation for 10/10. `INTEGRITY_CLEAR` is a dated search result, not proof
that no future or unindexed notice exists. PMID 26159007 remains quarantined and
was not processed.

## 7. Elegibilidade

All ten records are provisionally `RETAIN_FOR_HUMAN_CONFIRMATION` and terminate
as `HUMAN_REVIEW_REQUIRED`. This is not final inclusion and does not authorize
scientific synthesis.

## 8. Desenhos

The batch contains four qualitative studies, one analytical cross-sectional
survey, one prospective evaluation protocol, one narrative review, one mixed-
methods secondary evaluation, one quantitative descriptive survey and one
natural experiment.

## 9. Classes de evidência

The classifications are four `QUALITATIVE_EVIDENCE`, three
`QUANTITATIVE_EVIDENCE`, one `MIXED_METHODS_EVIDENCE`, one
`NARRATIVE_REVIEW_EVIDENCE` and one `STUDY_PROTOCOL_EVIDENCE`. Empirical status,
original-data status and effect-estimate status are separate fields.

## 10. Appraisal

AI-provisional domain appraisal covers 95/95 expected domains. Four qualitative
studies use JBI Qualitative; EV-0439 uses the revised JBI analytical cross-
sectional tool; EV-0167 uses JBI Quasi-Experimental; EV-0282 uses full MMAT
screening, qualitative, non-randomized quantitative and integration domains;
EV-0252 uses MMAT screening plus quantitative-descriptive domains; EV-0316 uses
SANRA only as methodological-quality appraisal. EV-0405 receives a transparent,
non-scored protocol-methods completeness check because it reports no outcomes.
No global cross-design score was calculated.

## 11. Extração

Population, sample, setting, design, exposure/intervention, comparator where
available, outcomes, instruments, timing, statistics, denominators, results and
limitations were recorded only when present in the accessible full text. No
missing value was imputed and no derived effect was introduced.

## 12. Evidências localizadas

All 10 records have reproducible section, paragraph, table or figure locations.
EV-0252 still requires VOR-specific confirmation before any later claim release.

## 13. Supported claims

Every record has a bounded statement consistent with its design: perceptions
remain perceptions, descriptive surveys remain descriptive, protocol content
remains planned methods, and the natural experiment remains limited to the two
studied agencies and measured implementation perceptions.

## 14. Unsupported claims

Each record states prohibited inferences, including perception to effectiveness,
association to causality, protocol to outcome, implementation to clinical or
public-safety benefit, modeled savings to realized savings, and foreign setting
to automatic Brazilian applicability.

## 15. Transferibilidade

Country, legal regime, institution, profession, sample, technology, emergency or
policing structure and relevant differences from Brazilian public safety are
documented separately from methodological appraisal. No universal score was used.

## 16. Red Team

Twenty-three checks per record covered the twenty required failure modes plus
human-gate, controlled-item and retracted-record exclusions. Result: 230/230
checks and 10/10 record gates passed. This control result is not scientific
approval.

## 17. AAM/VOR

Pilot 03 contains three AAMs: two comparisons have
`NO_MATERIAL_DIFFERENCE_OBSERVED` within their documented scope and one remains
pending. Earlier Pilot 01/02 pendencies for EV-0367, EV-1328 and EV-0791 remain
tracked in the cumulative human queue; no earlier ledger was silently rewritten.

## 18. Fila humana

The cumulative queue contains 30 records. Reviewer, date, decision,
justification and confirmation are blank in 30/30. Human confirmation is 0/30
and Claim-Ready is 0/30. Each row includes design, class, instrument, findings,
limitations, claim boundaries, version, integrity and pending work.

## 19. Testes

Eighteen Pilot 03 regressions cover deterministic selection, cross-pilot
uniqueness, identity, lawful full text, forbidden-record exclusion, integrity,
blank human fields, Claim-Ready, design/tool compatibility, MMAT completeness,
all domain counts, no global score, AAM/VOR status, at least twenty Red Team
checks, cumulative queue, source preservation, Pilot 02 derivative variance,
scale gate, normalized-LF manifest and XLSX ZIP/binary/semantic integrity. The
complete repository suite is required before publication.

## 20. Hashes

| Artifact | SHA-256 |
|---|---|
| Canonical Master Evidence before/after | `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b` |
| Pilot 03 workbook binary | `934d71055dbf53c89505f6de45be856b4d6c02154e2633d0eb2e82c8291c234c` |
| Pilot 03 workbook semantic | `023dd6084b1a2e8dc2016692c30c1c921aafbdd0b01a702a21e8dddb35216e7f` |
| Pilot 02 canonical binary | `9c1695b19b5eaa26844c27c1bb9893c54956b0b1f4722c5f7f12cd4e4c3abc7c` |
| Pilot 02 derivative binary | `81b505eee25b7c2738b431d30c3910b623b9a68f44e2508c4079a00626229aae` |

All CSV/JSON normalized-LF hashes are in `manifest.json`.

## 21. Artefatos

The Pilot 03 directory contains selection, record, appraisal, version,
provenance, Red Team, cumulative human-review, source-preservation, derivative-
variance, scale-readiness, execution-summary, workbook-artifact and manifest
files. The separate eight-sheet workbook is
`outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_03.xlsx`.

## 22. Commit

This report, ledgers, workbook, builders, tests and documentation form one atomic
publication unit. The immutable commit is reported after commit and push rather
than self-inserted into the payload.

## 23. CI

Entry CI was green. The exact publication commit must pass GitHub Actions after
push; local verification does not substitute for remote CI.

## 24. Progresso acumulado

- Pilot 03 technical processing: 10/10 (100.00%).
- Active candidates processed across three pilots: 30/1,191 (2.52%).
- Active PMC-route candidates processed: 30/383 (7.83%).
- Human confirmation: 0/30 (0.00%).
- Pilot 03 Claim-Ready: 0/10 (0.00%).
- Global Claim-Ready: 0/1,456 (0.00%).

These percentages describe technical workflow, not scientific validation.

## 25. Scale Readiness

Decision: **`KEEP_BATCH_SIZE_10`**. Identity, provenance, tests and Red Team were
stable, but Pilot 01 required a methodological correction, Pilot 03 introduced
several new appraisal routes, and AAM/VOR work remains material. Another
heterogeneous batch of ten should pass without methodological correction before
considering 20 or 25.

## 26. Gate final

**`GO_NEXT_BATCH` with `SCALE_READINESS = KEEP_BATCH_SIZE_10`.** Technical Pilot
03 requirements are complete. Human adjudication, EV-0252 VOR comparison,
claim-level human source audit and every Claim-Ready decision remain pending.
Scientific PASS remains prohibited.
