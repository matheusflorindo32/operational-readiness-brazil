# Search Strategy

The frozen search has three independent families per database/platform:

- A — Core readiness/performance
- B — APHT/medical readiness
- C — Implementation science

The audit performed before the first production execution found that the workbook
contained the provenance table but no exact A/B/C strings. The initial prospective
PubMed freeze was therefore created on 2026-08-28 rather than reconstructed from
a nonexistent prior string.

Authoritative exact strings:

- `strategies/2026-08-28_pubmed_A_core.query.txt`
- `strategies/2026-08-28_pubmed_B_apht.query.txt`
- `strategies/2026-08-28_pubmed_C_implementation.query.txt`

For each family, `exports/2026-08-28/` contains the raw ESearch JSON, NBIB export,
and a manifest with filters, UTC execution interval, result count, PubMed URL,
query translation, file hashes, and audit status. The combined deduplicated RIS is
staging material for Zotero import; its deterministic deduplication is not a
substitute for the required Zotero-native duplicate audit.

Do not alter frozen search concepts without recording an amendment.
