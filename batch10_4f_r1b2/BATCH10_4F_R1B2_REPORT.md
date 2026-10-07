# BATCH 10.4F-R1B2 — sentence support readjudication

## Gate

`SENTENCE_SUPPORT_READJUDICATION_PASS`

`GO_RECONCILED_MANUSCRIPT_BUILD_R1C`

All **168/168** scientific sentences have one final disposition. The decision standard is fail-closed: no source relationship was inferred from topic, bibliography order or a static number without a recovered reference relation.

## Results

- Dispositions: {'NON_EVIDENTIARY_NO_SUPPORT_NEEDED': 37, 'DELETE_REQUIRED': 123, 'RETAIN_WITH_LIMITATION': 5, 'NARROWING_REQUIRED': 3}.
- Support-fit categories: {'NON_EVIDENTIARY_NOT_APPLICABLE': 37, 'NO_RESULT_LEVEL_SUPPORT': 123, 'CONTEXTUAL_SUPPORT': 3, 'PARTIAL_SUPPORT': 3, 'DIRECT_SUPPORT': 2}.
- The 12 recovered sentence-reference relations were adjudicated against result IDs and locators.
- The remaining sentences without deterministic source links were either identified as internal method/limitation/framework text (`NON_EVIDENTIARY_NO_SUPPORT_NEEDED`) or assigned `DELETE_REQUIRED` when they made factual scientific claims.
- No citation change was fabricated: a change requires an existing better, deterministically linked source.

## Integrity controls

- `forced_semantic_links = 0`
- `blocked_evidence_used = 0`
- `PMC3382270` reused = 0
- cohort double counting = 0
- null-result suppression = 0
- unsupported causal claim retained = 0

EV-1473 and EV-1474 remain one cohort family. EV-1477 remains guidance only. The six source-insufficient records are not credited with result-level support.

## Next phase

R1C may apply only the recorded narrowing and deletion actions, retain bounded source-supported language, and handle any FCR candidates. It must not add literature or silently change CEF-v1.
