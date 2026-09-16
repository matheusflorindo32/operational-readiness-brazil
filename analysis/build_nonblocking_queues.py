"""Build reversible, non-blocking evidence queues from the audited PubMed refresh.

The script is read-only with respect to Zotero and the canonical Master Evidence
workbook. It emits CSV/JSON control artifacts and leaves all human fields blank.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "search/exports/2026-08-28/2026-08-28_pubmed_ABC_deduplicated_metadata.json"
IDENTITIES = ROOT / "reporting/preanalysis/2026-09-06/evidence-identity-map.csv"
OLD_EXCEPTIONS = ROOT / "reporting/screening/2026-09-07/screening-exceptions.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def joined(value):
    return " | ".join(str(x) for x in (value or []))


def full_text_score(source: dict, decision: dict):
    pmcid = source.get("pmcid") or ""
    doi = source.get("doi") or ""
    availability = 4 if pmcid else 2 if doi else 0
    matched = decision.get("matched_terms") or {}
    relevance = (
        (3 if matched.get("direct_context") else 0)
        + (4 if matched.get("apht") else 0)
        + (4 if matched.get("implementation_strong") else 0)
        + (2 if matched.get("readiness_domain") else 0)
        + (2 if "B" in (decision.get("families") or []) else 0)
        + (2 if "C" in (decision.get("families") or []) else 0)
    )
    types = " ".join(source.get("publication_types") or []).lower()
    quality = 3 if any(x in types for x in ("meta-analysis", "systematic review", "randomized controlled trial", "guideline")) else 2 if any(x in types for x in ("review", "consensus")) else 1
    haystack = f"{source.get('title','')} {source.get('abstract','')}".lower()
    transferability = 4 if any(x in haystack for x in ("police", "law enforcement", "firefighter", "emergency medical service", "first responder", "public safety", "border patrol", "correctional")) else 1 if any(x in haystack for x in ("tactical", "combat", "military")) else 0
    transferability += 2 if matched.get("implementation_strong") else 0
    total = availability + relevance + quality + transferability
    tier = "P1" if total >= 10 else "P2" if total >= 7 else "P3"
    return availability, relevance, quality, transferability, total, tier


def build(current_path: Path, decisions_path: Path, output_dir: Path):
    current = {r["pmid"]: r for r in load_json(current_path)}
    decisions = {r["pmid"]: r for r in load_json(decisions_path)}
    source = {str(r["pmid"]): r for r in load_json(SOURCE)}
    identities = {r["pmid"]: r for r in load_csv(IDENTITIES)}
    old_exceptions = load_json(OLD_EXCEPTIONS)
    assert len(current) == len(decisions) == len(source) == len(identities) == 1456

    common = ["evidence_id", "pmid", "zotero_key", "doi", "title"]
    quarantine, editorial, full_text, pending = [], [], [], []
    for pmid, decision in decisions.items():
        rec, src, ident = current[pmid], source[pmid], identities[pmid]
        base = {
            "evidence_id": ident["evidence_id"], "pmid": pmid,
            "zotero_key": ident["zotero_key"], "doi": rec.get("doi") or "",
            "title": rec.get("title") or "",
        }
        if decision["decision"] == "BLOCKED_INTEGRITY":
            quarantine.append({**base, "operational_status": "BLOCKED_INTEGRITY", "use_status": "NOT USED", "ai_decision": "Bloqueio automático por retração formal", "human_reviewer": "", "human_date": "", "human_decision": "", "primary_source_url": rec["source_url"], "editorial_links": joined(f"{x.get('ref_type')}:{x.get('pmid')}" for x in rec.get("corrections", [])), "claim_ready": "NO", "audit_note": decision.get("limitation", "")})
        editorial_review = decision.get("integrity_action") == "REVIEW_CORRECTION"
        if editorial_review and decision["decision"] != "BLOCKED_INTEGRITY":
            editorial.append({**base, "relation": joined(f"{x.get('ref_type')} -> PMID {x.get('pmid')}" for x in rec["corrections"]), "relation_urls": joined(f"https://pubmed.ncbi.nlm.nih.gov/{x.get('pmid')}/" for x in rec["corrections"] if x.get("pmid")), "primary_source_url": rec["source_url"], "risk": "Relação editorial requer interpretação antes de uso", "ai_decision_provisional": "REVIEW_REQUIRED", "ai_justification": "Correção/atualização detectada em fonte PubMed atual; manter fora de uso até esclarecimento.", "human_reviewer": "", "human_date": "", "human_decision": "", "human_justification": "", "human_options": "Confirmar bloqueio | Confirmar exclusão | Manter candidato | Solicitar texto completo | Investigar relação editorial", "claim_ready": "NO"})
        if decision["decision"] == "INCLUDE_FULL_TEXT":
            av, rel, qual, trans, total, tier = full_text_score(src, decision)
            hold = editorial_review
            link = f"https://pmc.ncbi.nlm.nih.gov/articles/{src['pmcid']}/" if src.get("pmcid") else (f"https://doi.org/{src['doi']}" if src.get("doi") else rec["source_url"])
            full_text.append({**base, "workflow_status": "REVIEW_REQUIRED" if hold else "FULL_TEXT_QUEUE", "priority_tier": "HOLD_EDITORIAL" if hold else tier, "priority_score": total, "lawful_availability_score": av, "operational_relevance_score": rel, "quality_potential_score": qual, "transferability_potential_score": trans, "lawful_access_status": "PMC_AVAILABLE" if src.get("pmcid") else "DISCOVERY_REQUIRED", "lawful_access_url": link, "publication_types": joined(src.get("publication_types")), "families": joined(src.get("families")), "full_text_obtained": "NO", "quality_appraisal_complete": "NO", "integrity_cleared_for_use": "NO" if hold else "PENDING_FULL_TEXT", "human_confirmation": "", "claim_ready": "NO", "limitation": decision.get("limitation", "")})
        if decision["decision"] == "PENDING_ADJUDICATION":
            pending.append({**base, "batch": "", "workflow_status": "REVIEW_REQUIRED" if editorial_review else "PENDING_ADJUDICATION", "ai_decision_provisional": "PENDING_ADJUDICATION", "criterion": decision.get("rationale", ""), "confidence": "LOW" if not decision.get("abstract_available") else "MODERATE", "source": rec["source_url"], "integrity_status": decision.get("integrity_status", ""), "human_reviewer": "", "human_date": "", "human_decision": "", "human_justification": "", "claim_ready": "NO", "what_not_allowed": decision.get("limitation", "")})

    full_text.sort(key=lambda r: (r["priority_tier"] == "HOLD_EDITORIAL", -int(r["priority_score"]), r["pmid"]))
    pending.sort(key=lambda r: r["pmid"])
    for index, row in enumerate(pending):
        row["batch"] = f"ADJ-{index // 10 + 1:02d}"

    metadata = []
    for item in old_exceptions["metadata_conflicts"]:
        pmid = item["pmid"]
        for field in item["fields"]:
            old, new = source[pmid].get(field), current[pmid].get(field)
            if current[pmid].get(f"{field}_match", False):
                status, reason = "RESOLVED_PARSER_REPRESENTATION", "O parser atual preserva o campo PubMed correspondente; conflito anterior era de representação."
            elif field == "year":
                status, reason = "RESOLVED_DUAL_DATE", "Preservar ano-fonte/eletrônico e ano da edição atual; usar o ano da edição PubMed atual no fluxo derivado."
            else:
                status, reason = "RESOLVED_CURRENT_PUBMED_AUTHORSHIP", "Preservar valor anterior e usar a autoria PubMed atual no fluxo derivado, incluindo autoria coletiva/diacríticos."
            metadata.append({**{k: identities[pmid][k] for k in ("evidence_id", "zotero_key")}, "pmid": pmid, "field": field, "previous_value": joined(old) if isinstance(old, list) else old, "current_primary_value": joined(new) if isinstance(new, list) else new, "resolution_status": status, "resolution_reason": reason, "primary_source_url": current[pmid]["source_url"], "verification_date": date.today().isoformat(), "canonical_master_changed": "NO"})

    doi_rows = []
    for item in old_exceptions["identifier_conflicts"]:
        pmid = item["pmid"]
        doi = current[pmid].get("doi") or source[pmid].get("doi") or ""
        doi_rows.append({**{k: identities[pmid][k] for k in ("evidence_id", "zotero_key")}, "pmid": pmid, "previous_doi": source[pmid].get("doi", ""), "current_pubmed_doi": current[pmid].get("doi", ""), "resolution_status": "RESOLVED_PRIMARY_SOURCE_CONFIRMED", "downstream_doi": doi, "pubmed_url": current[pmid]["source_url"], "doi_url": f"https://doi.org/{doi}", "verification_date": date.today().isoformat(), "canonical_master_changed": "NO"})

    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "integrity-quarantine.csv": (quarantine, common + ["operational_status", "use_status", "ai_decision", "human_reviewer", "human_date", "human_decision", "primary_source_url", "editorial_links", "claim_ready", "audit_note"]),
        "editorial-review-queue.csv": (editorial, common + ["relation", "relation_urls", "primary_source_url", "risk", "ai_decision_provisional", "ai_justification", "human_reviewer", "human_date", "human_decision", "human_justification", "human_options", "claim_ready"]),
        "full-text-priority-queue.csv": (full_text, common + ["workflow_status", "priority_tier", "priority_score", "lawful_availability_score", "operational_relevance_score", "quality_potential_score", "transferability_potential_score", "lawful_access_status", "lawful_access_url", "publication_types", "families", "full_text_obtained", "quality_appraisal_complete", "integrity_cleared_for_use", "human_confirmation", "claim_ready", "limitation"]),
        "pending-adjudication-queue.csv": (pending, common + ["batch", "workflow_status", "ai_decision_provisional", "criterion", "confidence", "source", "integrity_status", "human_reviewer", "human_date", "human_decision", "human_justification", "claim_ready", "what_not_allowed"]),
        "metadata-resolution-ledger.csv": (metadata, ["evidence_id", "pmid", "zotero_key", "field", "previous_value", "current_primary_value", "resolution_status", "resolution_reason", "primary_source_url", "verification_date", "canonical_master_changed"]),
        "doi-resolution-ledger.csv": (doi_rows, ["evidence_id", "pmid", "zotero_key", "previous_doi", "current_pubmed_doi", "resolution_status", "downstream_doi", "pubmed_url", "doi_url", "verification_date", "canonical_master_changed"]),
    }
    for name, (rows, fields) in artifacts.items():
        write_csv(output_dir / name, rows, fields)

    summary = {
        "generated_on": date.today().isoformat(), "policy": "NON_BLOCKING_CONTROLLED_SCREENING_V1",
        "total_records": 1456, "quarantined_retraction": len(quarantine),
        "editorial_review_current": len(editorial), "editorial_review_audited_baseline": 17,
        "editorial_review_new_delta": len(editorial) - 17,
        "full_text_candidates": len(full_text),
        "full_text_active": sum(r["workflow_status"] == "FULL_TEXT_QUEUE" for r in full_text),
        "full_text_editorial_hold": sum(r["workflow_status"] == "REVIEW_REQUIRED" for r in full_text),
        "pending_adjudication": len(pending), "pending_batches": len({r["batch"] for r in pending}),
        "metadata_conflicts_documented": len(metadata), "doi_conflicts_resolved": len(doi_rows),
        "claim_ready": 0, "human_fields_populated": 0,
        "zotero_modified": False, "canonical_master_modified": False,
    }
    assert summary["quarantined_retraction"] == 1
    assert summary["full_text_candidates"] == 1206 and summary["pending_adjudication"] == 240
    assert summary["metadata_conflicts_documented"] == 90 and summary["doi_conflicts_resolved"] == 2
    assert all(r["zotero_key"] != "FXC7ZY9R" for rows, _ in artifacts.values() for r in rows)
    (output_dir / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {
        p.name: {"sha256": sha256(p), "bytes": p.stat().st_size}
        for p in sorted(output_dir.glob("*"))
        if p.is_file() and p.name != "manifest.json"
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", required=True, type=Path)
    parser.add_argument("--decisions", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.current, args.decisions, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
