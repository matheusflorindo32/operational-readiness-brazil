# BATCH 11.4R — Bilingual manual review package

## Decision

`BILINGUAL_MANUAL_REVIEW_PACKAGE_PASS`

`GO_MANUAL_AUTHOR_REVIEW`

## Scope

This package supports human author review only. The English document is a byte-for-byte copy of the frozen editorial adaptation. The PT-BR document is a faithful review translation, carries the required non-submission banner, and preserves the framework and Claim-Ready governance labels where they occur.

## Reconciliation

- Active references: 28/28.
- Frozen claims: 20/20.
- Numeric tokens: 244/244 after locale-only decimal/thousands punctuation normalization.
- New scientific claims, promoted Claim-Ready records, reference substitutions, CEF-v1 changes, Zotero changes and Brazil-manuscript changes: 0.
- Workbook: 20/20 named worksheets, ordered 00–19; frozen fields protected and human-review fields editable.

## Validation

- DOCX ZIP/OOXML and `word/document.xml`: valid for EN and PT-BR.
- English review copy SHA-256 equals the Batch 11.4 source document SHA-256.
- XLSX ZIP/OOXML, CSV UTF-8, JSON, formulas, sheet order, filters and frozen panes: valid.
- Regression tests: `262 passed, 13 subtests passed`, including `5` Batch 11.4R package tests.
- `git diff --check`: pass.
- Visual rendering: not executed because LibreOffice `soffice.exe` is unavailable in this workstation environment; this is a presentation-QA limitation, not an OOXML-integrity failure.

## Human review required

The package retains the existing manual review and JOH input queues. No human decision is simulated. Reviewers should record comments and decisions in `15_REVISAO_MANUAL`, `18_HUMAN_INPUTS`, and `19_CHANGE_LOG`.
