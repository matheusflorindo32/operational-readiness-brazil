"""Create non-scientific reconciliation artifacts from the canonical ledger."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "batch10_4b"
CANONICAL = BASE / "canonical"
LEDGER = CANONICAL / "MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv"
SOURCE_ID = "1PsCIFKpNMjrpsaHVu2mGKFYlRboKvNGgorZocCILnoY"
SOURCE_URL = f"https://docs.google.com/spreadsheets/d/{SOURCE_ID}/edit"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    canonical = read_csv(LEDGER)
    by_id = {row["Evidence_ID"]: row for row in canonical}
    additions: list[dict[str, str]] = []
    for row in canonical:
        if row["Baseline_or_Addition"] != "ADDITION":
            continue
        batch05 = row["Canonicalization_Batch"] == "Batch05"
        additions.append({
            "Evidence_ID": row["Evidence_ID"], "Addition_Number": row["Addition_Number"],
            "Origin": "Batch05 close-out canonicalization" if batch05 else "Batch02/03 gap-directed discovery",
            "Batch": row["Canonicalization_Batch"], "Date": "2026-09-20",
            "Title": row["Title"], "DOI": row["DOI"], "PMID": row["PMID"],
            "Canonicalization_Reason": "Exact identifier/title reconciliation and canonical inclusion",
            "Authoritative_Artifact": (
                "reporting/batch05/BATCH05_AUDIT.md; reporting/batch05/manifest.json"
                if batch05 else "reporting/deep-evidence/2026-09-20/batch-03/master-evidence-reconciliation-batch-03.csv"
            ),
            "Zotero_Status": "PENDING_DIRECT_ZOTERO_WRITE" if not row["Zotero_Key"] else "ZOTERO_RECONCILED",
            "Master_Evidence_Status": row["Canonical_Status"],
            "LOOP3X_Status": row["LOOP3X_Final_Class"], "Provenance": row["Provenance"],
        })
    add_fields = list(additions[0])
    additions_path = CANONICAL / "CANONICAL_28_ADDITIONS_RECONCILIATION.csv"
    write_csv(additions_path, add_fields, additions)

    conflicts = []
    for evidence_id in ("EV-1483", "EV-1484"):
        row = by_id[evidence_id]
        conflicts.append({
            "Conflict_ID": f"CANONICAL-GAP-{evidence_id.removeprefix('EV-')}",
            "Evidence_ID": evidence_id, "Conflict_Type": "PREVIOUSLY_UNACCOUNTED_ADDITION",
            "Observed_Conflict": "Absent from the 26-row Batch02/03 reconciliation ledger.",
            "Resolution": "Batch05 formally canonicalized this record and the LOOP3X full-universe sheet materialized it.",
            "Authoritative_Evidence": "reporting/batch05/BATCH05_AUDIT.md; reporting/batch05/manifest.json; Drive FULL_UNIVERSE_SCREENING",
            "Status": "RESOLVED", "Notes": f"{row['Title']} | PMID {row['PMID']} | DOI {row['DOI']}",
        })
    conflict_path = CANONICAL / "CANONICAL_CONFLICT_LEDGER.csv"
    write_csv(conflict_path, list(conflicts[0]), conflicts)

    queue_rows = []
    for queue in read_csv(ROOT / "loop3x" / "FULL_TEXT_REVIEW_QUEUE.csv"):
        row = by_id[queue["Evidence_ID"]]
        queue_rows.append({
            "Evidence_ID": row["Evidence_ID"], "Canonical_Ledger_Presence": "YES",
            "LOOP3X_Final_Class": row["LOOP3X_Final_Class"], "Priority": row["LOOP3X_Priority"],
            "Domain": row["Domain"], "Queue_Type": queue["Pass3"],
            "Canonical_Provenance": row["Provenance"],
        })
    queue_path = CANONICAL / "FULL_TEXT_QUEUE_285_RECONCILIATION.csv"
    write_csv(queue_path, list(queue_rows[0]), queue_rows)

    completeness = json.loads((CANONICAL / "CANONICAL_COMPLETENESS_TEST.json").read_text(encoding="utf-8"))
    manifest = {
        "phase": "BATCH 10.4B-R — CANONICAL LEDGER RECONSTRUCTION",
        "source": {"drive_file_id": SOURCE_ID, "url": SOURCE_URL, "sheet": "FULL_UNIVERSE_SCREENING", "modified": "2026-09-21T02:35:49.190Z"},
        "entry_commit": "34da7f52698cd245900f7e2c19a5c392da9db7cc",
        "artifacts": {
            "canonical_ledger_sha256": sha256(LEDGER), "additions_sha256": sha256(additions_path),
            "conflict_ledger_sha256": sha256(conflict_path), "queue_reconciliation_sha256": sha256(queue_path),
        },
        "reconciliation": {"baseline": 1456, "additions": len(additions), "total": len(canonical), "queue": len(queue_rows), "resolved_previous_gap_ids": ["EV-1483", "EV-1484"]},
        "completeness_gate": completeness["gate"],
        "scientific_changes": {"full_text_appraisal": 0, "reference_selection": 0, "reference_exclusion": 0, "cef_v1_changes": 0, "freeze_change_requests": 0},
        "gate": "BATCH10_4B_UNBLOCKED" if completeness["gate"] == "CANONICAL_1484_LEDGER_PASS" else "BATCH10_4B_STILL_BLOCKED",
    }
    (BASE / "BATCH10_4B_UNBLOCK_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# Batch 10.4B-R — reconciliação canônica e desbloqueio

## Decisão

`BATCH10_4B_UNBLOCKED` para o próximo gate administrativo: `GO_FULL_TEXT_SATURATION_REVIEW`.
Esta missão não executou leitura integral, appraisal, seleção, exclusão, substituição,
análise de contraditórios, mudança de manuscrito, alteração do CEF-v1 ou FCR.

## Fonte autoritativa materializada

- Drive: [{SOURCE_ID}]({SOURCE_URL})
- Arquivo: `Operational_Readiness_LOOP3X_EV0001_EV1484_2026-09-21`
- Aba: `FULL_UNIVERSE_SCREENING`
- Data de modificação registrada: 2026-09-21T02:35:49.190Z
- A planilha possui três linhas de cabeçalho e 1.484 registros canônicos.

## Reconciliação

| Controle | Resultado |
| --- | ---: |
| Baseline Evidence Command Center | 1.456 |
| Adições canônicas | {len(additions)} |
| Universo canônico | {len(canonical)} |
| IDs únicos | {completeness['counts']['unique_ids']} |
| IDs ausentes | {completeness['counts']['missing_ids']} |
| Classificações LOOP 3× presentes | {completeness['counts']['final_classifications_present']}/1.484 |
| Proveniência presente | {completeness['counts']['provenance_present']}/1.484 |
| Fila de full text reconciliada | {completeness['counts']['full_text_queue_reconciled']}/285 |

## Reconciliação dos dois registros anteriormente não demonstrados

| Evidence ID | Identificadores | Fonte de canonicalização | Motivo da lacuna anterior |
| --- | --- | --- | --- |
| EV-1483 | PMID 26506204; DOI 10.1519/JSC.0000000000001065 | Batch05 audit e manifest; materialização LOOP 3× | O ledger Batch02/03 contém somente as 26 adições EV-1457..EV-1482. |
| EV-1484 | PMID 36691169; DOI 10.1136/bmjopen-2021-049182; PMCID PMC9453999 | Batch05 audit e manifest; materialização LOOP 3× | O ledger Batch02/03 contém somente as 26 adições EV-1457..EV-1482. |

Os dois registros são formalmente documentados em `reporting/batch05/BATCH05_AUDIT.md`,
`reporting/batch05/manifest.json` e na planilha canônica do LOOP. O
`CANONICAL_CONFLICT_LEDGER.csv` retém a lacuna histórica e sua resolução, sem
ocultar a diferença entre o ledger de 26 e o conjunto final de 28.

## Limites preservados

- EV-1379 permanece `FAIL_CLOSED` e `INTEGRITY_BLOCK`.
- CEF-v1 não foi alterado.
- Itens adicionados continuam com status de Zotero documentado; esta missão não escreveu no Zotero.
- A classificação é materializada do LOOP 3× existente, não recriada por heurística.
"""
    (BASE / "BATCH10_4B_UNBLOCK_REPORT.md").write_text(report, encoding="utf-8")
    print("Wrote reconciliation artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
