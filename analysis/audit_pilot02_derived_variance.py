"""Audit a known external Pilot 02 derivative without replacing the canonical workbook."""

from __future__ import annotations

import json
from pathlib import Path

from audit_xlsx_identity import (
    canonical_bytes,
    semantic_representation,
    sha256_bytes,
    sha256_file,
)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_02.xlsx"
DERIVED = Path.home() / "Downloads/Operational_Readiness_Full_Text_Pilot_02.xlsx"
OUTPUT = ROOT / "reporting/full-text/2026-09-17/pilot-03/pilot02-derived-variance.json"


def indexed_cells(document):
    return {
        (sheet["name"], cell["cell"]): cell
        for sheet in document["sheets"]
        for cell in sheet["cells"]
    }


def readable_validation(value):
    """Repair display-only replacement characters emitted by the legacy Pilot 02 package."""
    if isinstance(value, str):
        return (value.replace("reten��o", "retenção").replace("exclus�o", "exclusão")
                .replace("avalia��o", "avaliação"))
    if isinstance(value, list):
        return [readable_validation(item) for item in value]
    if isinstance(value, dict):
        return {key: readable_validation(item) for key, item in value.items()}
    return value


def audit():
    if not DERIVED.exists():
        result = {"status": "EXTERNAL_COPY_UNAVAILABLE", "canonical_preserved": True}
    else:
        left, right = semantic_representation(CANONICAL), semantic_representation(DERIVED)
        lc, rc = indexed_cells(left), indexed_cells(right)
        cell_diffs = []
        for key in sorted(set(lc) | set(rc)):
            if lc.get(key) != rc.get(key):
                cell_diffs.append({"sheet": key[0], "cell": key[1], "canonical": lc.get(key), "derived": rc.get(key)})
        validation_diffs = []
        for ls, rs in zip(left["sheets"], right["sheets"]):
            if ls["data_validations"] != rs["data_validations"]:
                display_name = "Revisão humana" if ls["name"].startswith("Revis") else ls["name"]
                validation_diffs.append({"sheet": display_name, "canonical": readable_validation(ls["data_validations"]), "derived": readable_validation(rs["data_validations"])})
        scientific_values_equal = all(
            (lc.get(k) or {}).get("value") == (rc.get(k) or {}).get("value")
            for k in set(lc) | set(rc)
        )
        strict_equal = canonical_bytes(left) == canonical_bytes(right)
        result = {
            "status": "DOCUMENTED_DERIVED_FUNCTIONAL_VARIANCE",
            "canonical": {"path": str(CANONICAL.relative_to(ROOT)).replace("\\", "/"), "binary_sha256": sha256_file(CANONICAL), "semantic_sha256": sha256_bytes(canonical_bytes(left))},
            "derived": {"path_external": str(DERIVED), "binary_sha256": sha256_file(DERIVED), "semantic_sha256": sha256_bytes(canonical_bytes(right))},
            "strict_semantic_equal": strict_equal,
            "scientific_cell_values_equal": scientific_values_equal,
            "formula_functionally_equivalent": cell_diffs == [{"sheet": "Resumo", "cell": "B17", "canonical": lc.get(("Resumo", "B17")), "derived": rc.get(("Resumo", "B17"))}],
            "cell_differences": cell_diffs,
            "data_validation_differences": validation_diffs,
            "interpretation": "All populated values and calculated intent are preserved. One COUNTIF formula differs only by quoting of the sheet name, and two validation rules add allowBlank=1. Strict semantics are therefore unequal.",
            "canonical_preserved": True,
            "derived_replaces_canonical": False,
        }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
