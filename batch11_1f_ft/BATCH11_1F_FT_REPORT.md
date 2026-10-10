# Batch 11.1F-FT — external full-text verification and appraisal

## Scope

This batch evaluated exactly the 55 new external PubMed discovery records from Batch 11.1F-SEARCH. It did not edit the International working manuscript, CEF-v1, Zotero, Brazil outputs, or the 1,484-record internal universe. Text was accepted only from the official NCBI PMC BioC route when a matching article title and accessible Methods and Results were found.

## Results

- Tier A: 7; Tier B: 8; Tier C: 14; Tier D: 26.
- Lawful PMC bodies retrieved: 12/55; verified full texts: 12/55.
- Result-located full-text packets: 12; new Evidence_IDs (EV-1485 onward) assigned after full-text verification: 4; Result_IDs: 4.
- Automatic supporting claims: 0; Claim-Ready promotions: 0; automatic active-reference additions: 0.
- Explicitly identified null results preserved: 1.

## Boundaries

Every assigned evidence/result packet remains an AI-provisional human-adjudication candidate. Formal appraisal, integrity clearance, study-family comparison, transferability, materiality, and claim-to-sentence fitness still require human confirmation. Records that were retrieved but did not pass all identity/Methods/Results checks remain unadmitted. The result locator cites the official BioC passage; raw source bodies are not committed.

## Identifier correction

The prior discovery artifact used a descendant XML identifier extraction. Of 55 records, 41 PMCID values were corrected because they belonged to cited references rather than the primary article. Retrieval used only the batch PubMed `PubmedData/ArticleIdList` capture recorded in `EXTERNAL_55_PRIORITY_TRIAGE.csv`; no mismatched PMC body was accepted.

## Gate

`EXTERNAL_FULLTEXT_APPRAISAL_PARTIAL`

`EXTERNAL_EVIDENCE_STILL_INSUFFICIENT_FOR_6500_WORD_TARGET`

The batch produced traceable new full-text packets, but they cannot automatically increase the active reference set or establish a 6,500-word manuscript. Next action: human adjudication of the materiality queue, then a controlled reconstruction decision.
