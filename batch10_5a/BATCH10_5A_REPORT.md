# BATCH 10.5A — current target journal fit audit

**Editorial verification date:** 2026-10-09
**Base commit:** `43e0141e7874035f9d091dea3e58f32b1cd71b58`

`TARGET_JOURNAL_FIT_AUDIT_PASS`
`GO_TARGET_JOURNAL_HUMAN_SELECTION`

## Preserved input

- International: `SHORT_FORM`, 1,627 body words, four frozen references.
- Brazil: `SHORT_FORM`, 1,879 body words, nine frozen references.
- Both frozen DOCX SHA-256 values were checked before artifact generation.

## Ranked shortlist

### International

1. **Frontiers in Sports and Active Living — Mini Review** (46/50). Strongest scope/type/length fit; its CHF 2,195 B-type APC and specialty confirmation remain material.
2. **Journal of Occupational Health — Review Article** (45/50). Bounded review fit; obtain its live APC quote before selection.
3. **Frontiers in Public Health — Mini Review** (41/50). Conditional on public-health specialty confirmation; CHF 2,500 B-type APC.

### Brazil

1. **Revista Brasileira de Saúde Ocupacional — Ensaio** (47/50). Direct occupational-health scope and non-systematic essay category.
2. **Cadernos de Saúde Pública — Ensaio** (46/50). Compatible non-systematic essay and no APC, but broader collective-health audience.
3. **Revista Brasileira de Medicina do Trabalho — Artigo de Revisão** (46/50). Strong work-medicine alignment; current granular template must be reconfirmed after selection.

## Exclusions

- **RBSP** is `HARD_EXCLUDE`: its official page says submissions are closed and it has a 5,000-word minimum. No scientific expansion is permitted.
- **RBSO Review Article** is excluded as a route because it would require a review design not held by the frozen scientific layer. RBSO **Ensaio** remains independently compatible.

## Controls and limits

No manuscript, claim, Result_ID, reference, Zotero record or CEF-v1 record changed. The audit includes 7 International and 8 Brazil candidates plus a separate editorial-integrity ledger. The human queue has exactly `INT-TARGET-SELECTION` and `BRA-TARGET-SELECTION`, with all human fields blank. Fields not supplied by current official sources are deliberately marked `NOT_STATED_IN_OFFICIAL_SOURCES_CAPTURED`.

Next exact action: the author chooses one International and one Brazil target in `TARGET_JOURNAL_HUMAN_DECISION_QUEUE.csv`; only then may Batch 10.5B begin.
