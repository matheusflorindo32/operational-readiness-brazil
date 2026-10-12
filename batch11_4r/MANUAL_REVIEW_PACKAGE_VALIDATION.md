# Manual review package validation

## Required files

- Required artifacts: 7/7.
- English review DOCX: byte-for-byte source copy verified.
- PT-BR review DOCX: required Portuguese non-submission banner verified.

## Evidence controls

- Active references reconciled: 28/28.
- Frozen claims imported: 20/20.
- Numeric tokens reconciled: 244/244 after permitted locale punctuation normalization.
- Translation, DOI/reference, governance-label and scientific drift: 0.

## Workbook

- Worksheets: 20/20, in `00`–`19` order.
- Filters and frozen headers: present.
- Frozen scientific fields: protected.
- Human-review fields: editable.

## Technical validation

- Both DOCX files: valid ZIP/OOXML with `word/document.xml`.
- Workbook: valid ZIP/OOXML.
- CSV: UTF-8 and parsed.
- JSON: parsed.
- Regression suite: 262 passed, 13 subtests passed.
- Visual render unavailable: LibreOffice `soffice.exe` is absent from PATH.
