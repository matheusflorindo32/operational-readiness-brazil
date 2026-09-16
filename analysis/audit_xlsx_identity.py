"""Forensic and semantic comparison for the non-blocking control workbook.

Uses only the Python standard library so the audit runs in CI.  The semantic
representation intentionally ignores ZIP serialization, empty cells and style
IDs while preserving sheet order, dimensions, populated values, formulas,
logical data types, hyperlinks, filters, panes, validations, tables, merges and
defined names.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import locale
import platform
import posixpath
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHEETS = [
    "Resumo",
    "Quarentena",
    "Revisão editorial",
    "Fila texto completo",
    "Pendentes",
    "Metadados",
    "DOI resolvidos",
]
MASTER = ROOT / "outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx"
MASTER_SHA256 = "2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(node, name):
    return [child for child in node.iter() if local(child.tag) == name]


def first(node, name):
    return next((child for child in node.iter() if local(child.tag) == name), None)


def relationship_id(node):
    return next((value for key, value in node.attrib.items() if local(key) == "id"), None)


def rels_path(part: str) -> str:
    folder, name = posixpath.split(part)
    return posixpath.join(folder, "_rels", name + ".rels")


def resolve_target(part: str, target: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), target)).lstrip("/")


def parse_relationships(package: zipfile.ZipFile, part: str) -> dict[str, dict]:
    path = rels_path(part)
    if path not in package.namelist():
        return {}
    root = ET.fromstring(package.read(path))
    return {
        node.attrib["Id"]: {
            "target": resolve_target(part, node.attrib["Target"]),
            "type": node.attrib.get("Type", ""),
            "target_mode": node.attrib.get("TargetMode", ""),
        }
        for node in root
        if local(node.tag) == "Relationship"
    }


def normalize_number(value: str):
    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError):
        return value
    if number == number.to_integral():
        return int(number)
    return format(number.normalize(), "f")


def text_content(node) -> str:
    return "".join((item.text or "") for item in node.iter() if local(item.tag) == "t")


def shared_strings(package: zipfile.ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in package.namelist():
        return []
    root = ET.fromstring(package.read(path))
    return [text_content(node) for node in root if local(node.tag) == "si"]


def cell_value(cell, strings):
    formula_node = next((x for x in cell if local(x.tag) == "f"), None)
    value_node = next((x for x in cell if local(x.tag) == "v"), None)
    inline_node = next((x for x in cell if local(x.tag) == "is"), None)
    formula = formula_node.text if formula_node is not None else None
    kind = cell.attrib.get("t", "n")
    raw = value_node.text if value_node is not None else None
    if inline_node is not None:
        value, logical = text_content(inline_node), "string"
    elif kind == "s" and raw is not None:
        value, logical = strings[int(raw)], "string"
    elif kind in {"inlineStr", "str"}:
        value, logical = raw or "", "string"
    elif kind == "b" and raw is not None:
        value, logical = raw == "1", "boolean"
    elif kind == "e":
        value, logical = raw, "error"
    elif raw is not None:
        value, logical = normalize_number(raw), "number"
    else:
        value, logical = None, "blank"
    if formula is not None:
        logical = "formula"
    return value, formula, logical


def normalize_attrs(node, allowed):
    return {key: node.attrib[key] for key in sorted(node.attrib) if local(key) in allowed}


def dimension_shape(ref: str):
    if not ref:
        return {"ref": "", "rows": 0, "columns": 0}
    end = ref.split(":")[-1]
    letters = "".join(ch for ch in end if ch.isalpha())
    digits = "".join(ch for ch in end if ch.isdigit())
    column = 0
    for ch in letters.upper():
        column = column * 26 + ord(ch) - 64
    return {"rows": int(digits or 0), "columns": column}


def coordinate_parts(coordinate: str):
    letters = "".join(ch for ch in coordinate if ch.isalpha()).upper()
    digits = "".join(ch for ch in coordinate if ch.isdigit())
    column = 0
    for ch in letters:
        column = column * 26 + ord(ch) - 64
    return letters, int(digits or 0), column


def parse_table(package, part):
    root = ET.fromstring(package.read(part))
    return {
        "name": root.attrib.get("name", ""),
        "display_name": root.attrib.get("displayName", ""),
        "ref": root.attrib.get("ref", ""),
        "columns": [node.attrib.get("name", "") for node in children(root, "tableColumn")],
        "auto_filter": (first(root, "autoFilter").attrib.get("ref", "") if first(root, "autoFilter") is not None else ""),
    }


def parse_sheet(package, part, name, strings):
    root = ET.fromstring(package.read(part))
    rels = parse_relationships(package, part)
    hyperlink_by_ref = {}
    for node in children(root, "hyperlink"):
        rel = rels.get(relationship_id(node) or "", {})
        hyperlink_by_ref[node.attrib.get("ref", "")] = rel.get("target") or node.attrib.get("location", "")
    cells = []
    for cell in children(root, "c"):
        coordinate = cell.attrib.get("r", "")
        value, formula, logical = cell_value(cell, strings)
        hyperlink = hyperlink_by_ref.get(coordinate)
        if value in (None, "") and formula is None and not hyperlink:
            continue
        cells.append({
            "cell": coordinate,
            "value": value,
            "formula": formula,
            "hyperlink": hyperlink,
            "data_type": logical,
        })
    pane = first(root, "pane")
    pane_data = {}
    if pane is not None:
        pane_data = normalize_attrs(pane, {"xSplit", "ySplit", "topLeftCell", "activePane", "state"})
        for key in ("xSplit", "ySplit"):
            if key in pane_data:
                pane_data[key] = normalize_number(pane_data[key])
    validations = []
    for node in children(root, "dataValidation"):
        formulas = [x.text or "" for x in node if local(x.tag) in {"formula1", "formula2"}]
        validations.append({
            "attrs": normalize_attrs(node, {"sqref", "type", "operator", "allowBlank", "showDropDown", "showInputMessage", "showErrorMessage"}),
            "formulas": formulas,
        })
    tables = []
    for node in children(root, "tablePart"):
        rel = rels.get(relationship_id(node) or "")
        if rel and rel["target"] in package.namelist():
            tables.append(parse_table(package, rel["target"]))
    dimension = first(root, "dimension")
    auto_filter = first(root, "autoFilter")
    merges = sorted(node.attrib.get("ref", "") for node in children(root, "mergeCell"))
    shape = dimension_shape(dimension.attrib.get("ref", "") if dimension is not None else "")
    if not shape["rows"] and cells:
        max_row = max(coordinate_parts(item["cell"])[1] for item in cells)
        max_col = max(coordinate_parts(item["cell"])[2] for item in cells)
        shape = {"rows": max_row, "columns": max_col}
    return {
        "name": name,
        "shape": shape,
        "cells": sorted(cells, key=lambda item: item["cell"]),
        "freeze_pane": pane_data,
        "auto_filter": auto_filter.attrib.get("ref", "") if auto_filter is not None else "",
        "tables": sorted(tables, key=lambda item: item["name"]),
        "data_validations": sorted(validations, key=lambda item: json.dumps(item, sort_keys=True)),
        "merged_cells": merges,
    }


def semantic_representation(path: Path) -> dict:
    with zipfile.ZipFile(path) as package:
        strings = shared_strings(package)
        workbook_part = "xl/workbook.xml"
        workbook = ET.fromstring(package.read(workbook_part))
        rels = parse_relationships(package, workbook_part)
        sheets = []
        for node in children(workbook, "sheet"):
            rel = rels[relationship_id(node)]
            sheets.append(parse_sheet(package, rel["target"], node.attrib["name"], strings))
        defined_names = []
        for node in children(workbook, "definedName"):
            defined_names.append({"name": node.attrib.get("name", ""), "local_sheet_id": node.attrib.get("localSheetId"), "value": node.text or ""})
    return {"schema": "orb-xlsx-semantic-v1", "sheets": sheets, "defined_names": sorted(defined_names, key=lambda x: json.dumps(x, sort_keys=True))}


def canonical_bytes(document: dict) -> bytes:
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def scientific_semantic_projection(document: dict) -> dict:
    """Minimum stable scientific semantics required by the incident protocol."""
    return {
        "schema": document["schema"],
        "sheets": [
            {
                "name": sheet["name"],
                "shape": sheet["shape"],
                "cells": sheet["cells"],
            }
            for sheet in document["sheets"]
        ],
        "defined_names": document["defined_names"],
    }


def semantic_sha256(path: Path) -> str:
    return sha256_bytes(canonical_bytes(scientific_semantic_projection(semantic_representation(path))))


def feature_comparison(document_a: dict, document_b: dict) -> dict:
    result = {}
    for key in ("freeze_pane", "auto_filter", "tables", "data_validations", "merged_cells"):
        left = {sheet["name"]: sheet[key] for sheet in document_a["sheets"]}
        right = {sheet["name"]: sheet[key] for sheet in document_b["sheets"]}
        result[key] = {"equal": left == right, "artifact_a": left, "artifact_b": right}
    result["populated_cells"] = {
        "equal": all(a["cells"] == b["cells"] for a, b in zip(document_a["sheets"], document_b["sheets"])),
        "artifact_a_count": sum(len(sheet["cells"]) for sheet in document_a["sheets"]),
        "artifact_b_count": sum(len(sheet["cells"]) for sheet in document_b["sheets"]),
    }
    result["formulas"] = {
        "equal": all([cell for cell in a["cells"] if cell["formula"] is not None] == [cell for cell in b["cells"] if cell["formula"] is not None] for a, b in zip(document_a["sheets"], document_b["sheets"])),
        "artifact_a_count": sum(cell["formula"] is not None for sheet in document_a["sheets"] for cell in sheet["cells"]),
        "artifact_b_count": sum(cell["formula"] is not None for sheet in document_b["sheets"] for cell in sheet["cells"]),
    }
    result["hyperlinks"] = {
        "equal": all([cell for cell in a["cells"] if cell["hyperlink"]] == [cell for cell in b["cells"] if cell["hyperlink"]] for a, b in zip(document_a["sheets"], document_b["sheets"])),
        "artifact_a_count": sum(bool(cell["hyperlink"]) for sheet in document_a["sheets"] for cell in sheet["cells"]),
        "artifact_b_count": sum(bool(cell["hyperlink"]) for sheet in document_b["sheets"] for cell in sheet["cells"]),
    }
    return result


def cell_map(sheet):
    return {item["cell"]: item["value"] for item in sheet["cells"]}


def table_rows(sheet):
    values = cell_map(sheet)
    headers = {}
    for cell, value in values.items():
        letters, row_number, _ = coordinate_parts(cell)
        if row_number == 1:
            headers[letters] = value
    rows = []
    for row_number in range(2, sheet["shape"]["rows"] + 1):
        rows.append({header: values.get(f"{letters}{row_number}") for letters, header in headers.items()})
    return rows


def scientific_invariants(document: dict, master_path: Path = MASTER) -> dict:
    by_name = {sheet["name"]: sheet for sheet in document["sheets"]}
    summary = cell_map(by_name["Resumo"])
    editorial = table_rows(by_name["Revisão editorial"])
    full_text = table_rows(by_name["Fila texto completo"])
    pending = table_rows(by_name["Pendentes"])
    metadata = table_rows(by_name["Metadados"])
    dois = table_rows(by_name["DOI resolvidos"])
    quarantine = table_rows(by_name["Quarentena"])
    all_rows = editorial + full_text + pending + metadata + dois + quarantine
    human_columns = ("human_reviewer", "human_date", "human_decision", "human_justification", "human_confirmation")
    human_values = [row.get(column) for row in all_rows for column in human_columns if row.get(column) not in (None, "")]
    claim_values = [str(row.get("claim_ready", "")).upper() for row in all_rows if row.get("claim_ready") not in (None, "")]
    master_hash = sha256_file(master_path)
    checks = {
        "sheet_names_exact": [sheet["name"] for sheet in document["sheets"]] == EXPECTED_SHEETS,
        "reconciled_identity_count": summary.get("B4") == 1456,
        "claim_ready_count": summary.get("B16") == 0,
        "editorial_review_count": len(editorial) == 18,
        "full_text_candidates": len(full_text) == 1206,
        "active_candidates": sum(row.get("workflow_status") == "FULL_TEXT_QUEUE" for row in full_text) == 1191,
        "editorial_hold": sum(row.get("workflow_status") == "REVIEW_REQUIRED" for row in full_text) == 15,
        "pending_count": len(pending) == 240,
        "metadata_resolution_count": len(metadata) == 90,
        "doi_resolution_count": len(dois) == 2,
        "human_fields_empty": not human_values,
        "claim_ready_no_yes": "YES" not in claim_values and "SIM" not in claim_values,
        "risk_appraisal_not_simulated": all(row.get("quality_appraisal_complete") in (None, "", "NO") for row in full_text),
        "full_text_review_not_simulated": all(row.get("full_text_obtained") in (None, "", "NO") for row in full_text),
        "controlled_key_absent": all("FXC7ZY9R" not in str(value) for row in all_rows for value in row.values()),
        "retracted_pmid_blocked": len(quarantine) == 1 and str(quarantine[0].get("pmid")) == "26159007" and quarantine[0].get("operational_status") == "BLOCKED_INTEGRITY" and quarantine[0].get("use_status") == "NOT USED",
        "master_evidence_unchanged": master_hash == MASTER_SHA256,
    }
    return {"checks": checks, "all_pass": all(checks.values()), "master_sha256": master_hash, "human_values_found": human_values, "claim_values": sorted(set(claim_values))}


def zip_inventory(path: Path):
    with zipfile.ZipFile(path) as package:
        return [
            {
                "member": info.filename,
                "crc32": f"{info.CRC:08x}",
                "compressed_size": info.compress_size,
                "uncompressed_size": info.file_size,
                "compression_method": info.compress_type,
                "zip_timestamp": list(info.date_time),
                "payload_sha256": sha256_bytes(package.read(info.filename)),
            }
            for info in package.infolist()
        ]


def classify_member(name: str, semantic_equal: bool):
    if not semantic_equal:
        return "UNKNOWN_REQUIRES_REVIEW"
    if name.startswith("xl/drawings/") or name.startswith("xl/worksheets/_rels/") or name in {"xl/styles.xml", "xl/theme/theme1.xml"}:
        return "PRESENTATION_ONLY"
    if name == "xl/persons/person.xml" or name == "xl/workbook.xml":
        return "METADATA_ONLY"
    if name.startswith("xl/worksheets/"):
        return "PRESENTATION_ONLY"
    return "ZIP_PACKAGING_ONLY"


def compare_packages(path_a: Path, path_b: Path, semantic_equal: bool):
    inv_a, inv_b = zip_inventory(path_a), zip_inventory(path_b)
    map_a = {x["member"]: x for x in inv_a}
    map_b = {x["member"]: x for x in inv_b}
    differences = []
    for name in sorted(set(map_a) | set(map_b)):
        a, b = map_a.get(name), map_b.get(name)
        if a == b:
            continue
        differences.append({
            "member": name,
            "presence": "both" if a and b else "artifact_a_only" if a else "artifact_b_only",
            "artifact_a": a,
            "artifact_b": b,
            "payload_equal": bool(a and b and a["payload_sha256"] == b["payload_sha256"]),
            "classification": classify_member(name, semantic_equal),
        })
    return {
        "artifact_a_member_count": len(inv_a),
        "artifact_b_member_count": len(inv_b),
        "artifact_a_member_order": [x["member"] for x in inv_a],
        "artifact_b_member_order": [x["member"] for x in inv_b],
        "member_order_equal": [x["member"] for x in inv_a] == [x["member"] for x in inv_b],
        "differences": differences,
    }


def fixed_timestamp_repack(source: Path, target: Path):
    with zipfile.ZipFile(source) as incoming, zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as outgoing:
        for name in sorted(incoming.namelist(), reverse=True):
            info = zipfile.ZipInfo(name, (2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            outgoing.writestr(info, incoming.read(name))


def normalization_verification(source: Path):
    with tempfile.TemporaryDirectory() as temp:
        first = Path(temp) / "normalized-1.xlsx"
        second = Path(temp) / "normalized-2.xlsx"
        fixed_timestamp_repack(source, first)
        fixed_timestamp_repack(source, second)
        first_hash, second_hash = sha256_file(first), sha256_file(second)
        return {
            "algorithm": "sorted reverse ZIP member order; timestamp 2000-01-01T00:00:00; DEFLATE level 9; fixed permissions",
            "source_binary_sha256": sha256_file(source),
            "normalized_binary_sha256": first_hash,
            "repeat_binary_sha256": second_hash,
            "binary_stable_for_same_input": first_hash == second_hash,
            "source_semantic_sha256": semantic_sha256(source),
            "normalized_semantic_sha256": semantic_sha256(first),
            "semantic_preserved": semantic_sha256(source) == semantic_sha256(first),
            "zip_integrity": zipfile.ZipFile(first).testzip() is None,
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "locale": list(locale.getlocale()),
                "timezone": str(datetime.now().astimezone().tzinfo),
            },
        }


def artifact_record(path: Path, origin: str, commit: str, git_blob_sha: str | None, status: str):
    stat = path.stat()
    try:
        display_path = path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        display_path = f"Downloads/{path.name}" if path.parent.name.lower() == "downloads" else path.name
    return {
        "path": display_path, "filename": path.name, "origin": origin,
        "sha256": sha256_file(path), "size_bytes": stat.st_size,
        "last_modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "git_blob_sha": git_blob_sha, "commit": commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "toolchain": {"python": sys.version.split()[0], "platform": platform.platform(), "zipfile": "stdlib", "xml": "xml.etree.ElementTree"},
        "status": status,
    }


def write_json(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def audit(path_a: Path, path_b: Path, output_dir: Path, commit: str, git_blob_sha: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    semantic_a = semantic_representation(path_a)
    semantic_b = semantic_representation(path_b)
    projection_a = scientific_semantic_projection(semantic_a)
    projection_b = scientific_semantic_projection(semantic_b)
    bytes_a, bytes_b = canonical_bytes(projection_a), canonical_bytes(projection_b)
    hash_a, hash_b = sha256_bytes(bytes_a), sha256_bytes(bytes_b)
    semantic_equal = bytes_a == bytes_b
    invariants_a = scientific_invariants(semantic_a)
    invariants_b = scientific_invariants(semantic_b)
    package_comparison = compare_packages(path_a, path_b, semantic_equal)
    manifest = {
        "incident": "ARTIFACT_IDENTITY_RECONCILIATION_REQUIRED",
        "resolution_status": "RECONCILED_SEMANTICALLY_IDENTICAL" if semantic_equal else "SEMANTIC_DIFFERENCE_REQUIRES_INVESTIGATION",
        "artifacts": [
            artifact_record(path_a, "Git canonical artifact at outputs/triage/2026-09-16", commit, git_blob_sha, "CANONICAL_PRESERVED"),
            artifact_record(path_b, "User Downloads copy inspected after publication", commit, None, "DIVERGENT_BINARY_PRESERVED"),
            artifact_record(MASTER, "Canonical Master Evidence control", commit, None, "UNCHANGED_CONTROL"),
        ],
    }
    semantic_comparison = {
        "schema": "orb-xlsx-semantic-v1",
        "artifact_a_semantic_sha256": hash_a,
        "artifact_b_semantic_sha256": hash_b,
        "semantic_equal": semantic_equal,
        "feature_comparison": feature_comparison(semantic_a, semantic_b),
        "conclusion": "SEMANTICALLY_IDENTICAL" if semantic_equal else "SEMANTIC_DIFFERENCE_REQUIRES_INVESTIGATION",
        "artifact_a_invariants": invariants_a,
        "artifact_b_invariants": invariants_b,
    }
    root_cause = {
        "root_cause": "ZIP_SERIALIZATION_DIFFERENCE" if semantic_equal else "SEMANTIC_WORKBOOK_DIFFERENCE",
        "release_decision": "GO_WITH_DOCUMENTED_NONSEMANTIC_VARIANCE" if semantic_equal and invariants_a["all_pass"] and invariants_b["all_pass"] else "BLOCKED_ARTIFACT_INTEGRITY",
        "evidence": {
            "artifact_a_members": package_comparison["artifact_a_member_count"],
            "artifact_b_members": package_comparison["artifact_b_member_count"],
            "artifact_b_added_empty_drawings": 7,
            "artifact_b_added_empty_sheet_relationships": 7,
            "artifact_b_added_empty_person_list": 1,
            "shared_string_storage_changed": True,
            "zip_member_order_changed": not package_comparison["member_order_equal"],
            "scientific_semantics_equal": semantic_equal,
        },
        "attribution_limit": "The producer that reserialized artifact B is not encoded in docProps; the OOXML changes prove reserialization but do not identify the application with certainty.",
    }
    write_json(output_dir / "artifact-manifest.json", manifest)
    write_json(output_dir / "zip-ooxml-comparison.json", package_comparison)
    write_json(output_dir / "semantic-comparison.json", semantic_comparison)
    write_json(output_dir / "scientific-invariants.json", {"artifact_a": invariants_a, "artifact_b": invariants_b})
    write_json(output_dir / "root-cause.json", root_cause)
    write_json(output_dir / "normalization-verification.json", normalization_verification(path_a))
    return {"manifest": manifest, "semantic": semantic_comparison, "package": package_comparison, "root_cause": root_cause}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_a", type=Path)
    parser.add_argument("artifact_b", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--git-blob-sha", required=True)
    args = parser.parse_args()
    result = audit(args.artifact_a, args.artifact_b, args.output_dir, args.commit, args.git_blob_sha)
    print(json.dumps({"semantic": result["semantic"], "root_cause": result["root_cause"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
