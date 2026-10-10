# BATCH 11.0D report

## Gate

`EXTERNAL_INTEGRITY_RECHECK_PASS`

All 26 adjudicated records were checked against current PubMed/NCBI metadata. The 25 records with an indexed DOI were corroborated by Crossref; EV-1461 has no DOI indexed and was corroborated using its PubMed Central identity page. No PubMed-indexed correction, retraction, expression of concern, withdrawal, or duplicate publication was identified for the 26 records.

The 12 human-approved expansion claims therefore advance only to `CLAIM_READY_CANDIDATE = YES`. They remain `Claim-Ready = NO`, are not frozen, and still require final scientific audit before citation or manuscript reconstruction. Four null results remain preserved. DOI resolver HEAD requests that returned HTTP 403 are recorded as automated access limitations; DOI identity was instead confirmed by the matching PubMed and Crossref metadata.

The canonical guard for EV-1379 returned `Integrity_Status = BLOCKED`; its project-level `FAIL_CLOSED / HOLD_INTEGRITY` designation remains preserved and was not reopened. EV-0052, EV-0140 and EV-1066 remain `UNADJUDICATED_CONTRADICTORY_EVIDENCE` with support use zero. No human decision, CEF-v1, Zotero, short-form baseline, manuscript, or evidence universe change occurred.

International is cleared for the next technical gate: `GO_FULL_MANUSCRIPT_RECONSTRUCTION`. Brazil remains `BRAZIL_EXPANSION_INSUFFICIENT`.
