# AI DEEP EVIDENCE QUALIFICATION & SCIENTIFIC SYNTHESIS — Workflow Amendment v1.0

Date: 2026-09-20
Entry SHA: `7abf5c073cf241d12e58bf4c84ce9c460f4fb5a2`

## Decision

The workflow is formally amended so that identifiable human scientific adjudication is deferred until after intensive AI-assisted evidence qualification and a pre-review manuscript are available.

Human adjudication remains mandatory for final scientific use. It is not simulated or removed.

## State model

- `AI_QUALIFIED = YES/NO`
- `HUMAN_CLAIM_READY = YES/NO`

`AI_QUALIFIED=YES` permits provisional synthesis only.
`HUMAN_CLAIM_READY=YES` requires identifiable human scientific adjudication.

## Provisional evidence tiers

`CORE_EVIDENCE`, `SUPPORTING_EVIDENCE`, `CONTEXTUAL_EVIDENCE`, `METHODS_ONLY`, `LOW_PRIORITY`, `HOLD_VERSION`, `HOLD_INTEGRITY`, `PROPOSED_EXCLUDE`.

## Pipeline

IDENTIFY → LAWFUL FULL TEXT → IDENTITY → INTEGRITY → VERSION → DESIGN → EXTRACTION → APPRAISAL → STATISTICS → LIMITATIONS → TRANSFERABILITY → CLAIM BOUNDARIES → MANUSCRIPT UTILITY → REDUNDANCY → PRIORITY → SYNTHESIS.

A blocked record does not stop independent records.

## Batch 01

Ten records from the former Pilot 05 preflight were deep-qualified:
EV-0643, EV-0588, EV-0465, EV-0394, EV-0387, EV-0224, EV-1103, EV-1038, EV-0966, EV-0946.

The pre-existing Pilot 06 canonical block remains preserved and is not silently bypassed.

## Scientific safeguards

No automatic human decision; no retracted source for claims; version holds remain fail-closed; association is not converted to causality; surrogate/simulated outcomes are not presented as patient outcomes; negative/null findings are retained; source and claim boundaries remain auditable.

## Current macro-gate

`CONTINUE_AI_DEEP_QUALIFICATION`

`READY_FOR_HUMAN_SCIENTIFIC_ADJUDICATION = FALSE`
