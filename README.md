# Operational Readiness Brazil

## Do Atleta Tático à Prontidão Operacional

**Título em português:**  
**Do Atleta Tático à Prontidão Operacional: um framework aplicado de desempenho humano para a segurança pública brasileira**

**English title:**  
**From Tactical Athlete to Operational Readiness: An Applied Human Performance Framework for Brazilian Public Safety**

## Scientific status

- **Study design:** JBI scoping review
- **Primary reporting guideline:** PRISMA-ScR
- **Search reporting:** PRISMA-S
- **Implementation science:** CFIR + Proctor Implementation Outcomes; ERIC as a subsidiary strategy taxonomy
- **Protocol:** v1.0 FROZEN
- **Search strategy:** families A/B/C, seed sensitivity pilot 15/15
- **Primary journal positioning:** Strength & Conditioning Journal

> **Atleta tático é o ponto de partida, não o ponto final.**

The project moves beyond describing the tactical athlete toward a multidimensional and implementation-oriented model of **operational readiness** for Brazilian public safety.

## Primary research question

**Português**  
Quais componentes, indicadores e estratégias de implementação, sustentados pelas evidências disponíveis, podem compor um framework factível para avaliar, desenvolver e manter a prontidão operacional de profissionais da segurança pública no Brasil?

**English**  
Which evidence-supported components, indicators, and implementation strategies can inform a feasible framework for assessing, developing, and maintaining operational readiness among Brazilian public safety professionals?

## Repository roles

This repository is the **canonical versioned scientific core** of the project. It stores protocol decisions, reproducible search documentation, extraction schemas, analysis code, framework development, reporting checklists, and the master manuscript source.

Other systems have distinct roles:

- **Zotero:** bibliographic single source of truth.
- **Google Drive:** collaboration, administrative documents, licensed PDFs, and large files.
- **OSF:** protocol registration and preservation of scientific project versions.

## Repository structure

```text
protocol/       Frozen protocol assets and amendments
search/         Reproducible search strategies and search logs
references/     Exported/open bibliographic metadata only
data/           Extraction schemas and reproducible non-sensitive data
analysis/       Analysis scripts and reproducible computational work
framework/      Framework-development artifacts
manuscript/     Canonical manuscript source, figures, and tables
reporting/      PRISMA and methodological checklists
osf/            OSF registration materials
drive/          Drive structure documentation
zotero/         Zotero collection/taxonomy documentation
docs/           Project documentation
```

## Evidence governance

Every substantive scientific claim should be traceable to a source and, where applicable, to the relevant result, page, table, or figure. DOI and metadata verification, corrections/retractions, study quality, risk of bias, and transferability to Brazilian public safety are documented separately rather than inferred from citation alone.

Military and other tactical evidence is **not automatically treated as equivalent** to Brazilian public safety evidence. Transferability is explicitly assessed.

## APHT / Tactical Medicine

APHT is treated as a **readiness domain**, not as a separate general TCCC/TECC review. Relevant evidence may include self/buddy care, hemorrhage control, casualty movement/extraction, and medical-task performance under operational stress, fatigue, or load.

## Security and data handling

Never commit credentials, API keys, `.env` files, private keys, sensitive personal data, restricted operational data, or copyrighted article PDFs. See [`SECURITY.md`](SECURITY.md).

## Current release gate

The protocol and search architecture are scientifically frozen. Definitive searches must not begin until the project’s registration/reference infrastructure is operational according to the release checklist.

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff) and will be updated after OSF registration and repository stabilization.
