# Full-text evidence qualification — Pilot 02

**Execution date:** 2026-09-17

**Entry commit:** `fdcf61ea56d89ed7838583fc865c2a56b5873af1`

**Policy:** `FAIL_CLOSED + NONBLOCKING`

**Decision:** `GO_PILOT_03`

**Scientific PASS:** prohibited

**Human confirmation:** 0/10

**Claim-Ready:** 0/10 in Pilot 02 and 0/1,456 globally

## 1. Gate de entrada

The local `main`, `origin/main` and audited entry commit matched at
`fdcf61ea56d89ed7838583fc865c2a56b5873af1`; the working tree was clean and the
exact-commit GitHub Actions run was successful before the pilot. The corrected
Pilot 01 gate was `GO_PILOT_02`. The canonical Master Evidence binary SHA-256
was `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b` before
execution and remains identical. Zotero and the canonical Master Evidence were
read-only inputs.

## 2. Dez registros selecionados

The existing queue rule selected the first ten active `P1` candidates with a
PMC route after excluding every Pilot 01 record. No relevance judgment or
result direction changed the order.

| Order | Evidence ID | PMID | PMCID | Zotero key |
|---:|---|---:|---|---|
| 1 | EV-0367 | 39808097 | PMC12064357 | Q45USE2S |
| 2 | EV-0176 | 41492854 | PMC12771649 | 2KBKDFBY |
| 3 | EV-0171 | 41520119 | PMC12882353 | P5KDUIF2 |
| 4 | EV-0160 | 41626406 | PMC12852583 | FU3CE6LR |
| 5 | EV-0157 | 41673910 | PMC12998156 | 9S3E8CNQ |
| 6 | EV-0091 | 42196761 | PMC13206323 | ME325L4C |
| 7 | EV-1328 | 19947877 | PMC3413284 | NCPMCR97 |
| 8 | EV-0896 | 32191195 | PMC7081854 | FISZESIY |
| 9 | EV-0791 | 33909512 | PMC8626520 | JL2TE34F |
| 10 | EV-0723 | 35120531 | PMC8814788 | NDHXQXSC |

The exact selection proof is in `selection-audit.csv`. `FXC7ZY9R` and PMID
26159007 are absent.

## 3. Full texts

Lawful PMC full text was obtained for 10/10 records. The preserved raw PubMed
and PMC XML inputs are held outside Git in the dated external execution backup;
the repository stores source URLs, timestamps and SHA-256 values in
`provenance-ledger.csv`. No publisher PDF, attachment or personal file was
committed.

## 4. Identidade

PMID, DOI, PMCID, title and article identity matched for 10/10. The checks use
current PubMed XML and the corresponding PMC article. No identifier was
inferred. The production Zotero keys were carried forward from the existing
reconciled queue without a Zotero write.

## 5. Versões

Seven PMC articles are identified as `VERSION_OF_RECORD`. Three are
`AUTHOR_ACCEPTED_MANUSCRIPT`: EV-0367, EV-1328 and EV-0791. EV-0367 received a
lawful publisher-section comparison covering identity, abstract, methods,
results and limitations; no material difference was observed in the compared
content, without asserting document equivalence. EV-1328 and EV-0791 retain
`VERSION_OF_RECORD_COMPARISON_PENDING` because only publisher metadata and
abstract were accessible. All three AAM records require VOR-specific locations
before Claim-Ready.

## 6. Integridade

Current PubMed XML showed no correction, retraction, update or expression-of-
concern relation for these ten records. This is a dated source check, not proof
that no future or unindexed notice exists. All ten are provisionally
`INTEGRITY_CLEAR`; continuing human and final pre-use checks remain mandatory.

## 7. Elegibilidade

All ten received the provisional AI status `RETAIN_FOR_HUMAN_CONFIRMATION`
after full-text assessment. This is neither final inclusion nor permission to
use the article in synthesis. Each ends as `HUMAN_REVIEW_REQUIRED`.

## 8. Desenhos

The pilot contains four qualitative studies, two mixed-methods studies and four
quasi-experimental or uncontrolled before-after evaluations. Design labels are
record-specific in `pilot-records.csv`; no narrative review, commentary or
purely conceptual record entered this deterministic batch.

## 9. Classes de evidência

Four records are `QUALITATIVE_EVIDENCE`, two are `MIXED_METHODS_EVIDENCE`, and
four are `QUANTITATIVE_EVIDENCE`. The ledger separately records empirical
origin, original-data status and whether an empirical effect estimate is
present. No cross-class global score was calculated.

## 10. Instrumentos

Qualitative studies use the current JBI Qualitative Research checklist. Mixed-
methods studies use MMAT 2018 with screening, qualitative, applicable
quantitative and integration criteria. Quasi-experimental studies use the
current revised JBI Quasi-Experimental Studies checklist. Instrument labels,
versions and appraisal type are explicit in the ledgers.

Primary methodological sources:

- [JBI Critical Appraisal Tools](https://jbi.global/critical-appraisal-tools)
- [JBI Checklist for Qualitative Research](https://jbi.global/sites/default/files/2026-05/2024_Checklist_for_Qualitative_Research_1.docx)
- [JBI Checklist for Quasi-Experimental Studies](https://jbi.global/sites/default/files/2026-05/2_JBI%20checklist%20for%20quasi-experimental%20studies.docx)
- [MMAT 2018 criteria manual](https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria%20manual_2018%20-08-01_ENG.pdf)

## 11. Appraisal

AI-provisional domain appraisal is complete for 10/10 records: 40 JBI
qualitative domain rows, 34 MMAT rows and 36 JBI quasi-experimental rows, for
110/110 expected rows. Both mixed-methods records contain S1/S2, 1.1–1.5,
4.1–4.5 and 5.1–5.5. No global quality score was created. Human confirmation
of every appraisal remains 0/10.

## 12. Extrações

The record ledger contains verifiable population, context, design, sample,
intervention or exposure, findings, denominators, statistics where reported,
limitations and provisional interpretation. Values were transcribed from the
full text; absent values were not imputed and causal effects were not
reconstructed.

## 13. Localizações

Every extracted statement has a named section, table or figure location in the
accessible source. The seven VOR records have PMC VOR locations. The three AAM
records retain the explicit restriction that a VOR-specific location is still
required before Claim-Ready.

## 14. Supported claims

Each record contains a narrow statement supported by its observed design and
population. Qualitative perceptions remain perceptions; implementation
descriptions remain implementation evidence; uncontrolled changes remain
non-causal observations; and simulation performance remains simulation
performance. These boundaries are provisional pending human review.

## 15. Unsupported claims

Every record states what it cannot establish. The prohibited inferences include
effectiveness from perception, causality from uncontrolled comparisons,
clinical benefit from simulation, general population effects from selected
samples, and automatic applicability to Brazilian public safety.

## 16. Transferibilidade

Transferability limits explicitly cover jurisdiction, health and public-safety
systems, workforce, setting, sample size, service access, measurement and study
design. No foreign finding was converted into a Brazilian recommendation.

## 17. Red Team

The Red Team evaluated 16 failure modes per record: wrong article, DOI, PMCID,
duplicate, version, design, tool, incomplete appraisal, denominator, outcome,
table or figure interpretation, causal overreach, exaggerated claim,
geographic generalization, textual evidence treated as original data, and AAM
silently treated as VOR. Results: 10/10 record gates and 160/160 individual
checks passed. Passing means the documented fail-closed controls detected no
current contradiction; it is not scientific approval.

## 18. Pendências humanas

The combined Pilot 01 corrected plus Pilot 02 review queue contains 20 rows.
Reviewer name, human date, human decision, human justification and confirmation
are empty in 20/20. Pilot 02 has 10/10 `HUMAN_REVIEW_REQUIRED`; Claim-Ready is
0/10. EV-1328 and EV-0791 also require VOR comparison, while EV-0367 requires
VOR-specific evidence locations before any later claim release.

## 19. Testes

Fifteen focused Pilot 02 tests cover deterministic selection, non-reuse of
Pilot 01, identity, full text, exclusion of the controlled and retracted
records, blank human fields, fail-closed Claim-Ready, tool compatibility,
complete MMAT, JBI domain counts, no global score, AAM status, Red Team, the
combined human queue, preserved hashes, manifest integrity and workbook ZIP and
semantic integrity. The complete repository suite is rerun before publication.

## 20. Hashes

| Artifact | SHA-256 |
|---|---|
| Canonical Master Evidence | `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b` |
| Pilot 02 workbook binary | `9c1695b19b5eaa26844c27c1bb9893c54956b0b1f4722c5f7f12cd4e4c3abc7c` |
| Pilot 02 workbook semantic | `18db89464f16777e335f28268b3d0c89976f0eca0097c43b49cf9df4f760eb48` |

The complete per-file manifest is `reporting/full-text/2026-09-17/pilot-02/manifest.json`.
Repository text-file hashes use an explicit `NORMALIZED_LF` basis so the same
canonical digest is obtained on Windows and Linux checkouts; the XLSX hashes
remain byte-exact and semantic hashes as labeled.

## 21. Arquivos

The dated Pilot 02 directory contains selection, records, appraisal, version,
provenance, Red Team, combined human-review, source-preservation, summary,
workbook-identity and manifest files. The separate eight-sheet workbook is
`outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_02.xlsx`.
Pilot 01 and Pilot 01 Corrected artifacts remain unchanged.

## 22. Commit

The publication unit is the atomic Git commit that contains this report, the
Pilot 02 ledgers, generator, regression tests, workbook and documentation
updates. Its immutable SHA is reported from Git after commit and push; it is not
self-inserted into the commit payload.

## 23. CI

The entry commit CI was green. The new exact-commit CI is validated after push
and reported with its immutable GitHub Actions URL. A local test result is not
used as a substitute for remote CI.

## 24. Progresso acumulado

- Pilot 02 technical processing: 10/10 (100.00%).
- Pilots 01 and 02: 20/1,191 active candidates (1.68%).
- Active candidates with PMC route processed: 20/383 (5.22%).
- Pilot 02 human confirmation: 0/10 (0.00%).
- Combined pilot human queue: 0/20 (0.00%).
- Pilot 02 Claim-Ready: 0/10 (0.00%).
- Global Claim-Ready: 0/1,456 (0.00%).

These percentages measure technical workflow progress, not scientific approval.

## 25. Gate final

**`GO_PILOT_03`**. The deterministic batch, full-text identity, version ledger,
design-specific appraisal architecture, claim boundaries, Red Team, preservation
checks and reproducible artifacts are complete. Individual human adjudication,
VOR comparison for two AAMs, VOR-specific locations for all three AAMs and all
Claim-Ready decisions remain pending. No scientific PASS is declared.
