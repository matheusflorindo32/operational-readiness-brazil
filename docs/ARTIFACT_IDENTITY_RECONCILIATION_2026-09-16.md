# Artifact identity reconciliation — 2026-09-16

## Incident

The published control workbook had a canonical SHA-256 of
`808985682db5bb553fd4709795e1066f9b62fdd8a8fd608e1ba2e004565ca082`,
while a later Downloads copy had SHA-256
`8a7879cb6b9be661894b475874f03ac8f04907112e221b66a3d73e10c1e60434`.
The incident was opened as `ARTIFACT_IDENTITY_RECONCILIATION_REQUIRED`.
Neither difference was treated as corruption without evidence.

## Initial state

- Entry commit and `origin/main`: `763ca9f7336fef343cc05cce0d43564653528fea`.
- Branch: `main`; checkout clean before the audit.
- Canonical Git blob: `017d01379e44d17eee02565360e8aa6f9e7be685`.
- Canonical Master Evidence remained SHA-256
  `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b`.
- Both compared XLSX files were copied to the external dated preservation
  directory and marked read-only. No canonical or historical artifact was
  overwritten.

## Compared artifacts

| Attribute | Artifact A — Git canonical | Artifact B — Downloads copy |
|---|---:|---:|
| Origin | Git `outputs/triage/2026-09-16/` | local `Downloads/` copy |
| Size | 279,049 bytes | 280,343 bytes |
| Binary SHA-256 | `808985682db5bb553fd4709795e1066f9b62fdd8a8fd608e1ba2e004565ca082` | `8a7879cb6b9be661894b475874f03ac8f04907112e221b66a3d73e10c1e60434` |
| ZIP members | 14 | 29 |
| Semantic SHA-256 | `803e007a00129ee9ab5b361bc9a2c1ade1dc917554d2e9186d75f3f223953dc2` | `803e007a00129ee9ab5b361bc9a2c1ade1dc917554d2e9186d75f3f223953dc2` |
| Scientific invariants | 17/17 pass | 17/17 pass |

The complete origin, timestamp, size, binary hash, Git blob, commit, toolchain
and status records are in `reporting/artifact_reconciliation/2026-09-16/artifact-manifest.json`.

## Binary comparison

The central directories differ in member count, order, timestamps, CRCs,
compressed sizes and compression representation. Artifact A stores 14 members;
Artifact B stores 29. Artifact B adds seven worksheet relationships, seven empty
drawing parts and one empty person-list part. `_rels/.rels` also changes from a
stored representation to DEFLATE. No ZIP entry fails CRC validation.

## OOXML comparison

| Components | Observed difference | Classification |
|---|---|---|
| `[Content_Types].xml`, root/workbook relationships | Added registrations for empty drawings and person list; relationship IDs reordered | `ZIP_PACKAGING_ONLY` |
| `xl/sharedStrings.xml` | 115 to 469,470 uncompressed bytes; inline/direct text was reserialized into shared strings | `ZIP_PACKAGING_ONLY` |
| `xl/workbook.xml` | Added empty `<calcPr/>`; sheet relationship IDs shifted | `METADATA_ONLY` |
| `xl/persons/person.xml` | Empty person list added | `METADATA_ONLY` |
| `xl/styles.xml`, `xl/theme/theme1.xml` | Styles/theme rewritten without populated-cell value change | `PRESENTATION_ONLY` |
| Seven drawing parts and seven sheet relationship parts | Empty drawing containers added and linked | `PRESENTATION_ONLY` |
| Seven worksheet XML files | Text storage, empty-cell records, row/column presentation records and drawing links reserialized | `PRESENTATION_ONLY` |
| Three data validations | Same list formula and ranges; Artifact B adds `allowBlank="1"` | `PRESENTATION_ONLY` interface behavior; no human value added |

`docProps/core.xml`, `docProps/app.xml` and `xl/calcChain.xml` are absent from
both artifacts. There are no tables or autofilters in either copy. Freeze panes
and merged ranges are identical. The full per-member CRC, size, method, ZIP
timestamp, payload hash and classification are recorded in
`zip-ooxml-comparison.json`.

## Semantic comparison

The `orb-xlsx-semantic-v1` representation serializes UTF-8 canonical JSON with
sorted keys and no insignificant whitespace. It includes sheet order/name,
logical row and column bounds, every populated cell coordinate, normalized
value, formula, hyperlink and logical data type, plus defined names. Empty
strings and physically absent blank cells normalize to the same logical blank.

- Sheet order and names: identical, seven of seven.
- Populated cells: 29,936 versus 29,936, all identical.
- Formulas: zero versus zero.
- Hyperlinks: zero versus zero; source URLs are stored as text values in both.
- Freeze panes: identical on all seven sheets.
- Merged ranges: identical.
- Tables and autofilters: absent in both.
- Data-validation lists, target ranges and permitted options: identical.
- Only validation serialization differs through `allowBlank="1"` in Artifact B.

Both semantic hashes are
`803e007a00129ee9ab5b361bc9a2c1ade1dc917554d2e9186d75f3f223953dc2`.
The conclusion is `SEMANTICALLY_IDENTICAL` for scientific content.

## Root cause

`ROOT_CAUSE = ZIP_SERIALIZATION_DIFFERENCE`

Artifact B was reserialized by a downstream OOXML producer. This is proved by
the conversion to shared-string storage, new empty drawing/person parts,
rewritten styles/theme, new relationship ordering, changed compression and ZIP
timestamps, and the added empty `calcPr`. The producer identity is not encoded
in `docProps`, so attributing the change to Excel, Google Sheets or another
specific application would be unsupported. The exact cause class is established
even though the application name cannot be recovered from the file.

The added `allowBlank="1"` relaxes three empty human-decision inputs but does
not fill them, change the decision options, release Claim-Ready or alter any
scientific record.

## Scientific invariants

Both artifacts pass every mandatory invariant:

| Invariant | Result |
|---|---:|
| Reconciled identities | 1,456 |
| Claim-Ready | 0 |
| Editorial review | 18 |
| Full-text candidates | 1,206 |
| Active candidates | 1,191 |
| Editorial hold | 15 |
| Pending adjudication | 240 |
| Metadata resolutions | 90 |
| DOI resolutions | 2 |
| Human reviewer/date/decision/justification populated | 0 |
| Risk-of-bias appraisal simulated | 0 |
| `FXC7ZY9R` in scientific queues | 0 |
| Retracted record status | `BLOCKED_INTEGRITY / NOT USED` |
| Master Evidence change | none |

## Resolution

The Git artifact remains canonical and was not replaced. Chain of custody now
uses two complementary hashes:

- `binary_sha256` identifies an exact byte stream.
- `semantic_sha256` identifies normalized scientific workbook content.

For deterministic packaging of a fixed OOXML input, the normalizer sorts ZIP
members in a fixed order, fixes timestamps and permissions, and uses DEFLATE
level 9. Two independent runs produced binary SHA-256
`e2ec8fc04fabce0e59a18e114beafac5c04373361fa51378c17011962bbac6f0`
and preserved the semantic hash. This normalizer is an audit mechanism; it does
not overwrite the canonical XLSX.

The environment used Python 3.11.15 on Windows with `pt_BR` process locale and
`America/Sao_Paulo` operational timezone. A separate save/reopen check used
Python 3.12.14 and openpyxl 3.1.5. That save changed the binary hash to
`cdc6eb7b40232ab179560b9003c1f25081358cf5af45eee10cdf191298817398`
while preserving the semantic hash and all scientific invariants. This directly
demonstrates why a binary hash alone is insufficient after workbook reserialization.

## Tests

- Seven exact sheet names and dimensions.
- ZIP CRC integrity.
- Scientific counts and statuses.
- Human fields empty and Claim-Ready zero.
- Retraction quarantine and controlled-key exclusion.
- Canonical Master Evidence SHA-256.
- Stable semantic hash under deterministic ZIP save/reopen.
- Binary reproducibility for identical normalizer input.
- Independent openpyxl save/reopen and workbook reopening.
- Artifact-tool import and inspection of both copies.

## Residual risks

- The specific application that reserialized Artifact B cannot be proven from
  the package because both `docProps` files are absent.
- Any future editor may legitimately change `binary_sha256`; both hashes must be
  recorded after each deliberate publication/export.
- `allowBlank="1"` exists only in the downloaded variant. The Git canonical
  remains the authoritative source, and human fields must remain blank until an
  identified reviewer acts.
- This audit does not approve any article, full text, quality appraisal or claim.

## Release decision

**`GO_WITH_DOCUMENTED_NONSEMANTIC_VARIANCE`**

The XLSX-dependent identity incident is reconciled. Independent scientific
queues remain `GO_NONBLOCKING`. Scientific PASS remains prohibited.
