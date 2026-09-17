# Full-text Pilot 01 — methodological correction before scale

**Execution date:** 2026-09-17

**Audited source commit:** `455dde313c9a2f81749189baf601334b733b0dbd`

**Entry gate:** `GO_NONBLOCKING_CORRECTION_REQUIRED_BEFORE_SCALE`

**Final methodological gate:** `GO_PILOT_02`

**Scientific PASS:** prohibited
**Pilot 02 processed:** no

## 1. Gate de entrada

Local `main`, `origin/main` and the audited source commit were aligned before
the correction, the worktree was clean and the exact-commit GitHub Actions run
was successful. The correction started because the Pilot 01 architecture was
operationally sound but its appraisal representation was incomplete or
outdated in three places. The original ten-record pilot, its workbook, ledgers,
hashes and provisional decisions were treated as immutable inputs.

No title/abstract screening was restarted. Zotero and the canonical Master
Evidence workbook were not written. The next batch was not processed.

## 2. Problemas confirmados

1. `EV-0787` and `EV-0593` recorded MMAT screening and integration criteria but
   omitted the five qualitative and five applicable quantitative-component
   criteria.
2. `EV-0758` and `EV-0523` used the legacy `JBI Text and Opinion 2017` label.
   JBI now provides distinct Narrative, Expert Opinion and Policy tools.
3. SANRA was not explicitly separated from formal risk-of-bias appraisal.
4. `appraisal_complete_ai=YES` could be read without the necessary provisional
   and human-confirmation qualifiers.
5. The two author accepted manuscripts required an explicit Version of Record
   audit.
6. Evidence classes were implicit in free text and could therefore confer the
   same semantic weight on empirical studies, conceptual articles and opinion.

## 3. MMAT corrigido

Both mixed-methods records now have 17 explicit MMAT 2018 judgments: `S1/S2`,
`1.1–1.5`, `4.1–4.5` and `5.1–5.5`. Their quantitative components were
classified as **quantitative descriptive**, because they report descriptive
survey or questionnaire measurements and do not randomize an intervention or
estimate an analytic exposure-outcome effect.

| Record | Screening | Qualitative | Quantitative descriptive | Integration | Complete |
|---|---:|---:|---:|---:|---:|
| EV-0787 / PMID 33933923 | 2/2 | 5/5 | 5/5 | 5/5 | 17/17 |
| EV-0593 / PMID 37297641 | 2/2 | 5/5 | 5/5 | 5/5 | 17/17 |

`5.5` is now informed by the actual component appraisals and is `NO` in both
records. The generic `component quality adequate` field was removed from the
corrected ledger. No global MMAT score was calculated. The criteria and the
no-global-score rule follow the [official MMAT 2018 manual](https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria%20manual_2018%20-08-01_ENG.pdf).

## 4. JBI atualizado

The official [JBI Critical Appraisal Tools page](https://jbi.global/critical-appraisal-tools)
and its current checklists distinguish Narrative, Expert Opinion and Policy.
Both records were classified before appraisal and were reassessed from scratch
with the current [Expert Opinion checklist](https://jbi.global/sites/default/files/2026-05/2.Checklist_Textual_Evidence_Opinion.docx),
cited to McArthur et al. (2025), DOI `10.11124/JBIES-24-00293`.

- `EV-0758` advances and defends a conceptual implementation tool with
  illustrative cases. It is neither a first-person event narrative nor a
  policy/consensus guideline.
- `EV-0523` is explicitly `article-commentary` in PMC and gives a named author's
  evaluative opinion on another article. It is neither narrative testimony nor
  policy/consensus guidance.

Each has six new domain judgments with record-specific textual bases. No 2017
judgment was copied mechanically. Human confirmation remains blank for 12/12
JBI textual domains.

## 5. SANRA auditado

`EV-0668` is JATS `review-article`, labels its method a narrative review and
does not report a systematic-review method. SANRA therefore remains compatible.
The corrected model states:

- `SANRA = narrative-review methodological-quality appraisal`;
- `risk_of_bias_appraisal = NO`;
- `textual_evidence_appraisal = NO`.

This follows SANRA's stated purpose as a scale for the quality of narrative
review articles ([Baethge et al., 2019](https://doi.org/10.1186/s41073-019-0064-8)).

## 6. Version of Record/AAM

| Record | Source used | Publisher check | Result |
|---|---|---|---|
| EV-0787 | Author accepted manuscript | Lawful open-access [ScienceDirect VOR](https://www.sciencedirect.com/science/article/pii/S095539592100164X) | Bibliographic identity and material sections were compared; no material difference was observed in the compared scope. The AAM identity remains recorded and no absolute equivalence is claimed. VOR section/table location is required before Claim-Ready. |
| EV-0425 | Author accepted manuscript | [Wiley publisher record](https://onlinelibrary.wiley.com/doi/10.1111/dar.13926) | Bibliographic identity and abstract were compared. Lawful publisher full text was not available in this execution; `AAM_USED_FOR_EXTRACTION` and `VERSION_OF_RECORD_COMPARISON_PENDING` remain explicit. |

## 7. Classificação dos tipos de evidência

All ten records now have explicit `evidence_origin`, `evidence_class`,
`original_data` and `empirical_effect_estimate` fields:

| Class | Count | Share |
|---|---:|---:|
| Mixed-methods evidence | 2/10 | 20.00% |
| Qualitative evidence | 5/10 | 50.00% |
| Narrative review evidence | 1/10 | 10.00% |
| Conceptual evidence | 1/10 | 10.00% |
| Commentary/expert opinion | 1/10 | 10.00% |

Seven records contain original empirical data. None of the ten supplies an
empirical effect estimate suitable for a causal effectiveness claim. No global
quality score was created.

## 8. Red Team

The Red Team rechecked all 10/10 records against 13 failure modes: tool/design
compatibility, tool version, both mixed-method components, textual versus
empirical evidence, quality versus risk of bias, AAM versus VOR, commentary
versus study, opinion versus result, perception versus effectiveness,
association versus causality, international transfer and exact claim location.

All 130/130 record-level controls pass after correction. `EV-0523` remains an
independent `HOLD_RECORD` for human contextual-source eligibility; that hold
does not invalidate the corrected architecture or block other records.

## 9. Testes

Fourteen new correction tests pass. They include the 12 named regressions from
the corrective instruction plus preservation-hash and complete Red Team tests.
The earlier test suite remains present and also passes. The corrected workbook
was reopened after export with seven sheets, exact summary values and zero
formula-error matches. All seven rendered sheets received visual review.

## 10. Dados alterados

Only additive correction artifacts and project documentation changed:

- corrected record, appraisal, AAM/VOR, Red Team and delta ledgers;
- source-preservation record and correction manifest;
- a separate corrected seven-sheet workbook;
- reproducible correction builders and regression tests;
- README, checklist, changelog and this report.

## 11. Dados preservados

The original Pilot 01 directory and workbook were not overwritten. The
`source-preservation.json` ledger records the source commit, byte size and
SHA-256 of each original file. The original workbook remains SHA-256
`19033a732cfdb870c49676529877ff303bf91b875ae84e79f7a017c78674ee09`.

The canonical Master Evidence workbook remains SHA-256
`2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b`.
No Zotero import, edit, merge or deletion occurred. `FXC7ZY9R` remains outside
all scientific queues and PMID `26159007` remains `BLOCKED_INTEGRITY / NOT USED`.

## 12. Campos humanos

Human reviewer, human date, human decision, human justification, human
confirmation and `HUMAN_APPRAISAL_CONFIRMED` remain blank for 10/10 records and
all 102 domain judgments. AI work is labelled
`AI_APPRAISAL_COMPLETE_PROVISIONAL`; no human review is represented as complete.

`EV-0523` remains `HUMAN_REVIEW_REQUIRED`, with:

- `ORIGINAL_DATA = NO`;
- `EMPIRICAL_EFFECT_ESTIMATE = NO`;
- `ELIGIBILITY_CONTEXTUAL_SOURCE = HUMAN_DECISION_REQUIRED`.

## 13. Claim-Ready

Claim-Ready remains 0/10 in the pilot and 0/1,456 globally. A full-text file and
a provisional appraisal are insufficient. Human confirmation, integrity,
quality/appraisal, exact source location and the remaining fail-closed controls
are still mandatory.

## 14. Commit

The correction is published as one focused commit after the full local test and
artifact audit. The exact immutable commit identifier is supplied by Git history
and the release response because a commit cannot embed its own final SHA without
changing that SHA.

## 15. CI

The entry commit CI was green. The correction may be treated as published only
after the containing remote commit is confirmed and its GitHub Actions run is
successful. The exact run is reported with the release result.

## 16. Gate final

- [x] Estado real auditado.
- [x] MMAT EV-0787 corrigido.
- [x] MMAT EV-0593 corrigido.
- [x] Componentes qualitativos avaliados.
- [x] Componentes quantitativos avaliados.
- [x] JBI textual atualizado e reavaliado.
- [x] SANRA semanticamente corrigido.
- [x] Appraisal e risco de viés explicitamente separados.
- [x] AAMs auditados.
- [x] EV-0523 preservado em human review.
- [x] Red Team executado em 10/10.
- [x] Testes corretivos adicionados.
- [x] Testes antigos preservados.
- [x] Campos humanos vazios.
- [x] Claim-Ready = 0.
- [x] Piloto 01 original preservado por hash.
- [ ] Confirmação humana científica: 0/10.

The correction stage is 17/17 complete (100.00%). Appraisal architecture is
corrected for 10/10 records (100.00%), human confirmation is 0/10 (0.00%),
Claim-Ready is 0/10 (0.00%) and Pilot 02 processing is 0 records. The formal
methodological decision is `GO_PILOT_02`. This authorizes the next controlled
batch after publication/CI; it is not scientific inclusion or scientific PASS.
