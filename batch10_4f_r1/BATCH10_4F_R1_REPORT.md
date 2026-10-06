# Batch 10.4F-R1 sentence-level reconciliation

Sentence inventory created: 613 total; 168 heuristically identified scientific sentences require manual citation extraction. The v0.13 DOCX text layer does not expose deterministic citation-number anchors for those sentences. Existing reference-use counts cannot establish exact sentence support without forcing a link.

Gate: `MANUSCRIPT_SENTENCE_LEVEL_RECONCILIATION_BLOCKED`. Blocking resolution: extract/normalize citation anchors from the Word field/run structure or use an authoritative citation-marked source, then adjudicate every scientific sentence. FT8 claims are ledger candidates and retain non-forced dispositions. No freeze, manuscript, CEF-v1 or Zotero action occurred.
