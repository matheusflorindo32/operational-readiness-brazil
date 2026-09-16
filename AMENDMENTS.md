# Protocol Amendments

The initial protocol architecture was frozen on 2026-08-25. A major design correction was made and publicly registered on OSF on 2026-08-26 before definitive evidence identification.

| ID | Date | Type | Section | Change | Rationale | Impact on already-screened records | Approved by |
|---|---|---|---|---|---|---|---|
| A-001 | 2026-08-26 | Major | Study design and reporting architecture | Replaced the pre-registration JBI scoping-review framing with a conceptual and applied scientific essay informed by structured and reproducible evidence identification, critical synthesis, Brazilian contextual analysis, transferability assessment, and implementation-science concepts. Removed PRISMA-ScR/JBI as governing study-design requirements and reframed the A/B/C architecture as evidence identification rather than systematic-review searching. | The intended scientific product is an applied conceptual essay/framework, not a scoping review. The correction aligns the registered design with the actual scholarly intent and the paradigm-shift objective for Brazilian public-safety professionals. | None. Definitive evidence identification, production screening, final extraction, and synthesis had not begun. A 15-study seed-set pilot had only tested conceptual coverage of search terms and is retained as a development artifact, not as systematic-review sensitivity. | Project lead |
| A-002 | 2026-09-07 | Minor | Operational title/abstract screening | Added a conservative, reproducible four-state rubric (`INCLUDE_FULL_TEXT`, `EXCLUDE_TITLE_ABSTRACT`, `PENDING_ADJUDICATION`, `BLOCKED_INTEGRITY`) and mandatory disclosure of AI-assisted primary review. | The registered protocol defines substantive scope but did not specify row-level title/abstract decision mechanics. The rubric operationalizes that scope without changing the primary question, evidence families, transferability logic or intended product. It is not a PRISMA selection process and cannot approve claims. | Applied prospectively before the first production title/abstract classification. All 1,456 records were unscreened; no prior decision was reclassified. | Project lead instruction; AI-assisted execution pending human confirmation |
| A-003 | 2026-09-16 | Minor | Operational progression and exception handling | Added a non-blocking workflow: formal retractions are quarantined as `BLOCKED_INTEGRITY / NOT USED`; correction/update, DOI and metadata ambiguity are routed to `REVIEW_REQUIRED`; unrelated eligible records continue to lawful full-text discovery and preparation. Claim-Ready remains fail-closed. | A record-level exception must not interrupt independent records when identity, counts, protocol, backup and traceability remain intact. Human decisions are batched and remain explicitly pending. | No prior title/abstract classification was changed. The retraction remains audit-only; 18 current correction/update records are held; 1,191 clear candidates can progress. Zotero and the canonical Master Evidence are unchanged. | Project lead instruction; scientific adjudication remains pending |

## Interpretation of A-001

This amendment does **not** erase the earlier design history. The previous scoping-review framing is treated as a superseded pre-registration draft. The OSF-registered **Conceptual Essay Protocol v1.0** dated 2026-08-26 is the current public methodological baseline.

## Current amendment classification

- **Technical amendment:** correction that does not change the conceptual argument, primary question, or substantive scope.
- **Minor amendment:** clarification or operational refinement that does not materially alter the essay's central proposition, evidence domains, transferability logic, or intended framework.
- **Major amendment:** changes the central proposition, primary question, substantive evidence scope, transferability logic, implementation architecture, or expected scientific product.

All future substantive changes must be prospectively documented with date, rationale, scope, and expected impact before they are used in the project.
