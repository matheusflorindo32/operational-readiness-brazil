# Operational Readiness Brazil

## Do Atleta Tático à Prontidão Operacional

**Título em português:**  
**Do Atleta Tático à Prontidão Operacional: um framework aplicado de desempenho humano para a segurança pública brasileira**

**English title:**  
**From Tactical Athlete to Operational Readiness: An Applied Human Performance Framework for Brazilian Public Safety**

## Scientific status

- **Study design:** conceptual and applied scientific essay informed by structured and reproducible evidence identification, critical synthesis, Brazilian contextual analysis, transferability assessment, and implementation-science concepts.
- **Not a systematic review, scoping review, meta-analysis, or experimental study.**
- **Implementation science:** CFIR + Proctor Implementation Outcomes; ERIC as a subsidiary strategy taxonomy only when applicable.
- **Registered protocol:** Conceptual Essay Protocol v1.0, OSF, 2026-08-26.
- **OSF associated project:** https://osf.io/djgax
- **Structured evidence architecture:** families A/B/C; seed-set conceptual coverage pilot 15/15.
- **Primary journal positioning:** Strength & Conditioning Journal.

> **Atleta tático é o ponto de partida, não o ponto final.**

The project advances from the **tactical athlete** construct toward a multidimensional, longitudinal, and implementation-oriented model of **operational readiness**, health, sustainable human performance, and occupational longevity for Brazilian public safety.

## Paradigm-shift rationale

The essay responds to an emerging need for a paradigm shift in attention to Brazilian public-safety professionals: from fragmented, episodic, and predominantly physical approaches toward an integrated model combining health, physical capability, occupational performance, cognition, sleep/recovery, occupational load, injury prevention, medical readiness, monitoring, implementation conditions, and occupational longevity.

## Primary research question

**Português**  
Quais componentes, indicadores e estratégias de implementação, sustentados pelas evidências disponíveis, podem compor um framework factível para avaliar, desenvolver e manter a prontidão operacional de profissionais da segurança pública no Brasil?

**English**  
Which evidence-supported components, indicators, and implementation strategies can inform a feasible framework for assessing, developing, and maintaining operational readiness among Brazilian public safety professionals?

## Evidence identification

Evidence will be identified through a **structured and reproducible evidence-identification strategy**. The strategy is designed to support a rigorous conceptual essay and does **not** claim the exhaustive completeness of a systematic review.

Three complementary evidence families are retained:
1. Tactical human performance and operational readiness.
2. APHT / medical readiness.
3. Implementation science.

Planned sources include PubMed/MEDLINE, Scopus, Web of Science Core Collection, SPORTDiscus, CINAHL Complete, APA PsycINFO, Embase, Cochrane Library, SciELO, LILACS/BVS, Brazilian official/grey literature, and citation chasing when appropriate.

## Repository roles

This repository is the **canonical versioned scientific core** of the project. It stores protocol decisions, structured evidence-identification documentation, analysis code, framework-development artifacts, transparency records, and the master manuscript source.

- **Zotero:** bibliographic single source of truth.
- **Google Drive:** collaboration, administrative documents, licensed PDFs, and large files.
- **OSF:** public preservation of the registered Conceptual Essay Protocol v1.0.
- **Evidence Command Center:** [`outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx`](outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx), formula-driven, audited, and populated with the production PubMed identification set.

## Evidence governance

Every substantive scientific claim should be traceable to a source and, where applicable, to the relevant result, page, table, or figure. DOI/metadata verification, corrections/retractions, methodological relevance, and transferability to Brazilian public safety are documented separately rather than inferred from citation alone.

Military and other tactical evidence is **not automatically treated as equivalent** to Brazilian public-safety evidence. Transferability is explicitly assessed.

## APHT / Tactical Medicine

APHT is treated as a **readiness domain**, not as a disconnected general TCCC/TECC review. Relevant evidence may include self/buddy care, hemorrhage control, casualty movement/extraction, and medical-task performance under operational stress, fatigue, or load.

## Security and data handling

Never commit credentials, API keys, `.env` files, private keys, sensitive personal data, restricted operational data, or copyrighted article PDFs. See [`SECURITY.md`](SECURITY.md).

## Current release gate

- [x] GitHub repository materialized
- [x] Security CI active
- [x] Google Drive structure created
- [x] Conceptual Essay Protocol v1.0 registered on OSF
- [x] Premium Elite Diamante Evidence Command Center materialized and audited
- [x] Zotero root collection and 25 subcollections materialized
- [x] Zotero import/deduplication/export release test passed on 2026-08-27
- [x] Definitive structured evidence identification released
- [x] PubMed A/B/C production searches executed on 2026-08-28
- [x] 1,456 unique PubMed records entered individually in `Master Evidence`
- [x] Production RIS imported and audited natively for duplicates in Zotero Desktop

The production Zotero phase was completed on the computer exposing the real
Desktop API and Connector. The root collection `PE9UF4YN` contains 1,456 unique
production items, all mapped one-to-one to the 1,456 `Master Evidence` rows.
The native duplicate view contains one intentional controlled pair:
`FXC7ZY9R` versus production key `8XVBQIYE` for PMID `37415704`. No merge was
performed. `FXC7ZY9R` remains exclusively in the separate top-level collection
`EMHHKNTM` and is not evidence; the recovered PubMed article remains legitimate
Family A evidence under its production key. Scientific screening has not started,
and no production item is claim-ready solely because it was imported.

Raw diagnostics, backup evidence, the 1,456-key rollback manifest, and the native
duplicate audit are recorded under
[`reporting/zotero-runs/2026-09-02T13-40-38-0300`](reporting/zotero-runs/2026-09-02T13-40-38-0300).
The full execution report is
[`docs/ZOTERO_PUBMED_IMPORT_AUDIT_2026-09-03.md`](docs/ZOTERO_PUBMED_IMPORT_AUDIT_2026-09-03.md).

## PubMed structural publication audit — 2026-09-05

The post-import audit reconciles source RIS, production Zotero, rollback keys,
production RIS/BibTeX and Master Evidence at **1,456/1,456**. It checks PMID,
DOI, normalized title, year, document-type representation and duplicate candidates.
There are 156 missing DOIs already absent from the source and two same-title
pairs with distinct PMIDs and years. No merge or scientific screening occurred.
Individual metadata and source-integrity verification remain pending.

The workbook now states the pre-execution baseline
`912db0a4d3d6b9551fba228cd94d797b46370c50` and that PubMed A/B/C was executed,
imported and reconciled, with screening not started. Only those two cells changed.
See [the structural audit](docs/PUBMED_STRUCTURAL_AUDIT_2026-09-05.md) for
controls, backup validation, preserved limitations and publication criteria.

Reproduce the live, read-only structural checks with Python 3:

```text
python analysis/audit_pubmed_structure.py --helper "<installed Zotero skill>/scripts/zotero.py"
python -m unittest discover -s analysis -p "test_*.py"
```

The helper must run on the computer exposing Zotero API/Connector at
`127.0.0.1:23119`. No credentials, new dependencies or database migrations are
required. Local audit success alone does not attest a remote commit or CI result.

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). The OSF DOI will be added only after it is explicitly verified.
