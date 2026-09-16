"""Fail-closed controls for Gate 2 human-adjudication imports.

This module validates a proposed import payload.  It never writes to Zotero,
Master Evidence, or Google Sheets.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable


ALLOWED_HUMAN_DECISIONS = {
    "Confirmar bloqueio",
    "Confirmar exclusão",
    "Manter candidato",
    "Solicitar texto completo",
    "Investigar relação editorial",
}

HUMAN_FIELDS = (
    "revisor_humano",
    "data_humana",
    "decisao_humana",
    "justificativa_humana",
)


def _present(value: Any) -> bool:
    return bool(str(value or "").strip())


def validate_row(row: dict[str, Any]) -> list[str]:
    """Return blocking reasons for one proposed adjudication row."""
    errors: list[str] = []
    decision = str(row.get("decisao_humana", "")).strip()

    if decision and decision not in ALLOWED_HUMAN_DECISIONS:
        errors.append("unsupported_human_decision")
    if decision and decision == str(row.get("decisao_assistida_ia", "")).strip() and row.get(
        "human_decision_provenance"
    ) != "human_entered":
        errors.append("ai_recommendation_cannot_populate_human_decision")
    if decision and any(not _present(row.get(field)) for field in HUMAN_FIELDS):
        errors.append("incomplete_human_adjudication")
    if str(row.get("claim_ready", "")).strip().casefold() not in {
        "",
        "no",
        "no / pending",
        "bloqueado",
        "false",
        "0",
    }:
        errors.append("claim_ready_must_remain_blocked")

    relation = str(row.get("relacao_editorial", "")).strip()
    if row.get("integrity_signal") == "retraction" and relation not in {
        "RetractionIn",
        "RetractionOf",
    }:
        errors.append("retraction_relation_not_preserved")

    if not _present(row.get("doi")) and row.get("doi_status") != "NOT FOUND IN AUDITED SOURCE":
        errors.append("missing_doi_not_explicit")
    if relation and not _present(row.get("pmid_relacionado")) and row.get(
        "editorial_notice_pmid_status"
    ) != "NOT FOUND":
        errors.append("missing_editorial_notice_pmid_not_explicit")

    if row.get("human_conflict") is True:
        errors.append("human_conflict_requires_resolution")
    return errors


def evaluate_import_gate(
    rows: Iterable[dict[str, Any]],
    *,
    dry_run_present: bool,
    zotero_unchanged: bool,
    master_evidence_unchanged: bool,
) -> dict[str, Any]:
    """Validate a complete proposed batch and return a fail-closed result."""
    materialized = list(rows)
    reasons: list[str] = []
    if not dry_run_present:
        reasons.append("dry_run_required")
    if not zotero_unchanged:
        reasons.append("zotero_changed")
    if not master_evidence_unchanged:
        reasons.append("master_evidence_changed")

    pmids = [str(row.get("pmid", "")).strip() for row in materialized]
    keys = [str(row.get("zotero_key", "")).strip() for row in materialized]
    if any(not value for value in pmids) or any(count > 1 for count in Counter(pmids).values()):
        reasons.append("pmid_identity_not_unique")
    if any(not value for value in keys) or any(count > 1 for count in Counter(keys).values()):
        reasons.append("zotero_identity_not_unique")

    row_errors: dict[str, list[str]] = {}
    for row in materialized:
        errors = validate_row(row)
        if errors:
            row_errors[str(row.get("pmid", "<missing>"))] = errors

    if row_errors:
        reasons.append("row_validation_failed")
    return {
        "ready": not reasons,
        "reasons": reasons,
        "row_errors": row_errors,
        "row_count": len(materialized),
    }
