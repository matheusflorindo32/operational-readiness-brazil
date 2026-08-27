# Premium Elite Diamante — Evidence Workbook Specification

## Purpose
The scientific workbook is the structured evidence command center for the project **From Tactical Athlete to Operational Readiness: An Applied Human Performance Framework for Brazilian Public Safety**.

> **Atleta tático é o ponto de partida, não o ponto final.**

The workbook must remain compatible with the official study design: a **conceptual and applied scientific essay informed by structured and reproducible evidence identification**, not a systematic or scoping review.

## Non-negotiable rule
Every reference formally entering the project's evidence workflow must receive an individual row in `Master Evidence`. Identification alone does not mean the source is suitable for a manuscript claim.

Required progression:

`Identified → metadata verified → relevance classified → integrity checked → critically appraised → transferability assessed → claim-ready / contextual / not used`.

## Master Evidence fields
The master table must include, at minimum:

### Identification
- internal Evidence ID
- scientific workflow status
- objective scientific traffic-light status
- priority
- role in essay
- evidence family A/B/C or regional/official/citation chasing
- title and Portuguese working title
- authors, year, source/journal, publication type, peer-review status, open-access status

### Identifiers and provenance
- DOI and normalized DOI
- PMID / PMCID / other identifiers when applicable
- source URL
- database/platform
- exact strategy/query provenance
- identification date and access date
- Zotero item key and BibTeX key
- Zotero collection and tags

### Population and context
- country and Brazil flag
- institution/context
- occupation/population
- operational role/unit
- sample size
- sex/composition
- age
- service time
- occupational environment/exposure
- equipment/load when relevant

### Methods and measurement
- study design
- objective
- intervention/exposure
- comparator
- primary and secondary outcomes
- instruments/measures
- instrument validity when relevant
- follow-up
- missing data/attrition when relevant

### Results and statistics
- main findings
- effect estimate
- 95% CI
- p value
- OR/RR/HR where applicable
- correlation/regression estimates where applicable
- other relevant statistics
- operational/clinical significance
- consistency or conflict with the broader literature

### Operational-readiness domains
- primary and secondary domains
- tactical-athlete relationship
- operational-readiness relationship
- APHT/TEMS/TCCC/TECC relationship
- health
- physical capability
- cognition
- sleep/recovery
- occupational load
- musculoskeletal injury
- nutrition/hydration
- medical readiness
- monitoring/wearables
- occupational longevity

### Quality and research integrity
- design-appropriate quality/risk-of-bias instrument
- methodological-quality classification
- risk-of-bias result
- transparent project quality score when used
- metadata verification
- DOI/PMID verification
- correction/retraction/Expression of Concern check
- integrity status
- funding
- conflicts of interest
- limitations reported by authors
- limitations identified by the project team

### Transferability to Brazilian public safety
Score each domain 0–2:
1. task/demand similarity
2. equipment/load similarity
3. environment/exposure
4. construct/outcome relevance
5. population comparability
6. assessment/intervention feasibility
7. legal/ethical/institutional compatibility

Calculate raw score 0–14 and normalized score 0–10:
- 8–10 = HIGH
- 5–7 = CONDITIONAL
- 0–4 = LOW

**Safety override:** highly combat-specific military evidence must never independently justify a Brazilian institutional recommendation even when the numeric transferability score is high.

### Implementation science
When applicable record:
- CFIR Innovation
- CFIR Outer Setting
- CFIR Inner Setting
- CFIR Individuals
- CFIR Process
- Proctor implementation outcomes
- ERIC strategy terminology only when context/evidence supports it
- barriers
- facilitators
- required resources
- responsible institutional actor
- implementation horizon: 0–30 days / 31–90 days / 3–12 months / >12 months
- implementation indicator

### Claim traceability
For evidence used in manuscript reasoning record:
- manuscript claim supported
- page/section
- table/figure
- exact result supporting the claim
- controlled paraphrase/note
- **What this article does NOT allow us to claim**
- strength for claim
- use decision
- rationale
- next action
- lawful PDF availability/location
- Zotero note status
- analysis date
- reviewer

## Objective scientific traffic light
The workbook should support an operational traffic-light system, but final judgment remains human.

- 🟢 **Claim-ready:** metadata and integrity verified, appropriate methodological confidence, claim within study limits.
- 🟡 **Caution/context:** potentially useful but one or more important limitations, checks, or transferability constraints remain.
- 🔴 **Do not use for conclusion:** retracted, critically unreliable, clearly out of scope, or formally classified as not usable.
- 🔵 **Official/contextual:** official or institutional source primarily supporting context, governance, regulation, implementation, or system description.
- 🟣 **Conceptual key source:** structurally important source for definition, paradigm shift, theoretical architecture, or framework logic.

Traffic-light color must never replace critical appraisal or automatically create a scientific conclusion.

## Required analytical views
The workbook should provide automated/filterable views or matrices for:
- Brazil vs international evidence
- military transferable evidence
- APHT / medical readiness
- implementation science
- tactical athlete
- operational readiness
- study quality / risk of bias
- transferability
- claim-to-source traceability
- CFIR × Proctor × ERIC
- candidate framework domains
- search provenance/log
- Zotero control
- metadata and integrity verification
- corrections/retractions
- full-text control
- manuscript evidence
- gaps and future research
- release gates and project checklist

The workbook should use a single canonical `Master Evidence` table and avoid manual duplication of the same article across multiple sheets whenever formulas/filters/automation can create the analytical view.

## Dashboard minimum
Dashboard should show at least:
- total identified references
- metadata verified
- integrity/retraction checked
- core/claim-ready evidence
- contextual evidence
- Brazil evidence
- international evidence
- military evidence
- APHT evidence
- implementation-science evidence
- transferability HIGH / CONDITIONAL / LOW
- full text pending
- analysis pending
- claim-ready items
- domain coverage
- current release-gate state

## Release-gate dependency
The Premium Elite Diamante workbook may be prepared before definitive evidence identification, but no definitive evidence-search results may be entered as if formally executed until the **Zotero Release Gate** is PASS.

Current required Zotero PASS evidence:
- `status --json` executed locally
- local API on port 23119 functional
- initial inventory captured
- root collection created
- exactly 25 planned subcollections materialized
- required tags materialized
- controlled RIS/BibTeX import executed
- DOI normalization checked
- duplicate detection and controlled merge executed
- tags, notes, attachments preserved
- BibTeX export verified
- RIS export verified
- real Zotero version and test timestamp recorded

Until then:

**ZOTERO: BLOCKED | STRUCTURED EVIDENCE IDENTIFICATION: LOCKED**
