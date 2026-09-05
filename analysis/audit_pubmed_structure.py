"""Read-only PubMed/Zotero structural audit; never screens or writes to Zotero.

Run with Python 3, --helper pointing to the installed Zotero skill's zotero.py.
Only standard-library modules are required. Outputs contain bibliographic metadata,
not attachment contents, credentials, or database copies.
"""

import argparse
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "reporting/zotero-runs/2026-09-02T13-40-38-0300"
WORKBOOK = (
    ROOT / "outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx"
)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
BASELINE = "912db0a4d3d6b9551fba228cd94d797b46370c50"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def workbook_cells(path):
    """Read stored values without altering formulas, styles or native features."""
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            strings = [
                "".join(si.itertext())
                for si in ET.fromstring(z.read("xl/sharedStrings.xml"))
            ]
        rels = {
            r.attrib["Id"]: r.attrib["Target"]
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        }
        sheets = {}
        for sheet in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS):
            rid = sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            target = rels[rid]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            cells = {}
            for c in ET.fromstring(z.read(target)).findall(
                ".//m:sheetData/m:row/m:c", NS
            ):
                val = c.find("m:v", NS)
                text = val.text if val is not None else ""
                if c.attrib.get("t") == "s":
                    text = strings[int(text)]
                elif c.attrib.get("t") == "inlineStr":
                    text = "".join(t.text or "" for t in c.findall(".//m:t", NS))
                cells[c.attrib["r"]] = text or ""
            sheets[sheet.attrib["name"]] = cells
        return sheets


def ris_records(path):
    records, current, field = [], None, None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^([A-Z0-9]{2})  - ?(.*)$", line)
        if match:
            field, value = match.groups()
            if field == "TY":
                assert current is None, "Nested RIS record"
                current = defaultdict(list)
            assert current is not None, "RIS field outside record"
            current[field].append(value)
            if field == "ER":
                records.append(dict(current))
                current = None
        elif line.strip() and current is not None:
            current[field][-1] += " " + line.strip()
    assert current is None, "Unclosed RIS record"
    return records


def bib_records(path):
    """Parse Zotero's braced BibTeX export, validating balanced field braces."""
    text = path.read_text(encoding="utf-8-sig")
    starts = list(re.finditer(r"^@(\w+)\{([^,]+),", text, re.MULTILINE))
    records = []
    for n, match in enumerate(starts):
        end = starts[n + 1].start() if n + 1 < len(starts) else len(text)
        block = text[match.end() : end]
        fields = {"type": match[1].lower(), "key": match[2]}
        pos = 0
        while True:
            field = re.match(r"\s*,?\s*(\w+)\s*=\s*\{", block[pos:])
            if not field:
                assert block[pos:].strip() in ("}", ",\n}"), "Unsupported BibTeX tail"
                break
            pos += field.end()
            begin, depth = pos, 1
            while depth:
                assert pos < len(block), "Unclosed BibTeX value"
                char = block[pos]
                if char == "\\":
                    pos += 2
                    continue
                depth += (char == "{") - (char == "}")
                pos += 1
            fields[field[1].lower()] = block[begin : pos - 1]
        records.append(fields)
    return records


def normalize_title(value):
    value = value.replace("\\textgreater", ">").replace("\\textless", "<")
    value = (
        value.replace("\\textbackslash", "\\")
        .replace("\\_", "_")
        .replace("\\&", "&")
        .replace("\\%", "%")
    )
    value = value.replace("{", "").replace("}", "")
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split()).rstrip(".")


def normalize_doi(value):
    return re.sub(
        r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", value.strip(), flags=re.IGNORECASE
    ).lower()


def pmid(value):
    match = re.search(
        r"(?:PMID:\s*|pubmed\.ncbi\.nlm\.nih\.gov/)(\d+)", value, re.IGNORECASE
    )
    return match[1] if match else ""


def api_items(route):
    rows, start = [], 0
    while True:
        with urlopen(
            "http://127.0.0.1:23119/api/users/0/"
            + route
            + f"?format=json&limit=100&start={start}",
            timeout=30,
        ) as response:
            assert response.status == 200
            batch = json.load(response)
        rows.extend(batch)
        if len(batch) < 100:
            return rows
        start += len(batch)


def duplicates(rows, field):
    groups = defaultdict(list)
    for row in rows:
        if row[field]:
            groups[row[field]].append(row.get("pmid") or row.get("key"))
    return {k: v for k, v in groups.items() if len(v) > 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--helper", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reporting/zotero-runs/2026-09-05-structural-audit",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    checks, errors = {}, []

    def check(name, condition, detail=None):
        checks[name] = {"pass": bool(condition), "detail": detail}
        if not condition:
            errors.append(name)

    helper_results = {}
    for command in ("status", "inventory", "collections", "tags"):
        proc = subprocess.run(
            [sys.executable, str(args.helper), command, "--json"],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        result = json.loads(proc.stdout)
        if command == "status":
            result = {
                k: v for k, v in result.items() if k not in ("profile", "prefs_file")
            }
        helper_results[command] = result
        save_json(args.output / f"{command}.json", result)
    status = helper_results["status"]
    check(
        "api_connector_http_200",
        status["api_status"] == status["connector_status"] == 200,
        status,
    )
    library = api_items("items/top")
    production = api_items("collections/PE9UF4YN/items/top")
    controlled = api_items("collections/EMHHKNTM/items/top")
    keys = {item["key"] for item in production}
    check("production_1456", len(production) == len(keys) == 1456, len(production))
    check(
        "library_1457",
        len(library) == len(helper_results["inventory"]) == 1457,
        len(library),
    )
    check(
        "controlled_collection_only_FXC7ZY9R",
        [x["key"] for x in controlled] == ["FXC7ZY9R"],
    )
    check("controlled_excluded_from_production", "FXC7ZY9R" not in keys)
    check(
        "library_set_equals_production_plus_control",
        {x["key"] for x in library} == keys | {"FXC7ZY9R"},
    )
    control = next(x for x in library if x["key"] == "FXC7ZY9R")
    check("controlled_membership", control["data"]["collections"] == ["EMHHKNTM"])
    check(
        "controlled_tags_32_children_4",
        len(control["data"]["tags"]) == 32 and control["meta"]["numChildren"] == 4,
    )
    manifest = read_json(RUN / "rollback-manifest.json")
    mkeys = manifest["imported_item_keys"]
    check(
        "manifest_1456_unique_exact_production",
        len(mkeys) == len(set(mkeys)) == 1456 and set(mkeys) == keys,
    )
    source = ROOT / manifest["source"]
    export_base = (
        ROOT / "search/exports/2026-09-02/2026-09-02_pubmed_ABC_zotero_production"
    )
    ris = ris_records(export_base.with_suffix(".ris"))
    original_ris = ris_records(source)
    bib = bib_records(export_base.with_suffix(".bib"))
    metadata = read_json(
        ROOT
        / "search/exports/2026-08-28/2026-08-28_pubmed_ABC_deduplicated_metadata.json"
    )
    sheets = workbook_cells(WORKBOOK)
    master = sheets["Master Evidence"]
    row_numbers = sorted(
        int(c[1:])
        for c, v in master.items()
        if re.fullmatch(r"A\d+", c) and int(c[1:]) >= 4 and v
    )
    master_keys = [master.get(f"AF{r}", "") for r in row_numbers]
    check(
        "master_1456_keys_unique_nonempty_exact_production",
        len(row_numbers) == len(set(master_keys)) == 1456
        and "" not in master_keys
        and set(master_keys) == keys,
    )
    check("master_contiguous_1456_rows", row_numbers == list(range(4, 1460)))
    check(
        "master_screening_not_started",
        all(master.get(f"K{r}") == "IDENTIFIED" for r in row_numbers),
        dict(Counter(master.get(f"K{r}") for r in row_numbers)),
    )
    check(
        "individual_metadata_verification_pending",
        all(
            master.get(f"CJ{r}") != "Yes" and master.get(f"CK{r}") != "Yes"
            for r in row_numbers
        ),
    )
    datasets = {
        "metadata": [
            {
                "pmid": str(x["pmid"]),
                "doi": normalize_doi(x["doi"]),
                "title": normalize_title(x["title"]),
                "year": str(x["year"]),
                "type": "; ".join(x["publication_types"]),
            }
            for x in metadata
        ],
        "zotero": [
            {
                "pmid": pmid(
                    x["data"].get("extra", "") + " " + x["data"].get("url", "")
                ),
                "doi": normalize_doi(x["data"].get("DOI", "")),
                "title": normalize_title(x["data"]["title"]),
                "year": re.search(r"\d{4}", x["data"].get("date", ""))[0],
                "type": x["data"]["itemType"],
                "key": x["key"],
            }
            for x in production
        ],
        "bibtex": [
            {
                "pmid": pmid(x.get("url", "")),
                "doi": normalize_doi(x.get("doi", "")),
                "title": normalize_title(x.get("title", "")),
                "year": x.get("year", ""),
                "type": x["type"],
                "key": x["key"],
            }
            for x in bib
        ],
        "master": [
            {
                "pmid": master.get(f"X{r}", ""),
                "doi": normalize_doi(master.get(f"V{r}", "")),
                "title": normalize_title(master.get(f"L{r}", "")),
                "year": master.get(f"O{r}", ""),
                "type": master.get(f"Q{r}", ""),
                "key": master.get(f"AF{r}", ""),
            }
            for r in row_numbers
        ],
    }
    for name, rows in [("source_ris", original_ris), ("ris_export", ris)]:
        datasets[name] = [
            {
                "pmid": pmid(" ".join(x.get("AN", []) + x.get("UR", []))),
                "doi": normalize_doi(x.get("DO", [""])[0]),
                "title": normalize_title(x.get("TI", [""])[0]),
                "year": x.get("PY", [""])[0],
                "type": x["TY"][0],
            }
            for x in rows
        ]
    baseline = {x["pmid"]: x for x in datasets["metadata"]}
    zotero_by_pmid = {x["pmid"]: x for x in datasets["zotero"]}
    check(
        "master_each_pmid_maps_to_exact_zotero_key",
        all(
            x["key"] == zotero_by_pmid.get(x["pmid"], {}).get("key")
            for x in datasets["master"]
        ),
    )
    check(
        "bibtex_citation_keys_unique",
        len({x["key"] for x in datasets["bibtex"]}) == 1456,
    )
    structural = {}
    for name, rows in datasets.items():
        ids = [x["pmid"] for x in rows]
        check(
            f"{name}_1456_unique_pmids",
            len(rows) == len(set(ids)) == 1456
            and all(re.fullmatch(r"\d+", x) for x in ids)
            and set(ids) == set(baseline),
        )
        missing = {
            f: sum(not x[f] for x in rows)
            for f in ("pmid", "doi", "title", "year", "type")
        }
        malformed = {
            f: [x["pmid"] for x in rows if x[f] and not re.fullmatch(pattern, x[f])]
            for f, pattern in [("doi", r"10\.\d{4,9}/\S+"), ("year", r"\d{4}")]
        }
        mismatches = [
            {
                "pmid": x["pmid"],
                "fields": [
                    f
                    for f in ("doi", "title", "year")
                    if x[f] != baseline.get(x["pmid"], {}).get(f)
                ],
            }
            for x in rows
        ]
        mismatches = [x for x in mismatches if x["fields"]]
        structural[name] = {
            "count": len(rows),
            "missing": missing,
            "malformed": malformed,
            "types": dict(Counter(x["type"] for x in rows)),
            "duplicates": {f: duplicates(rows, f) for f in ("pmid", "doi", "title")},
            "metadata_mismatches": mismatches,
        }
        check(
            f"{name}_structural_fields",
            not any(missing[f] for f in ("pmid", "title", "year", "type"))
            and not any(malformed.values())
            and not mismatches,
            mismatches[:10],
        )
        check(
            f"{name}_no_duplicate_pmids_or_dois",
            not duplicates(rows, "pmid") and not duplicates(rows, "doi"),
        )
    check(
        "document_type_mapping",
        all(
            x["type"] == "JOUR" for x in datasets["source_ris"] + datasets["ris_export"]
        )
        and all(x["type"] == "journalArticle" for x in datasets["zotero"])
        and all(x["type"] == "article" for x in datasets["bibtex"]),
    )
    check(
        "master_retains_pubmed_publication_types",
        all(x["type"] == baseline[x["pmid"]]["type"] for x in datasets["master"]),
    )
    prod = next(x for x in datasets["zotero"] if x["pmid"] == "37415704")
    check(
        "pmid_37415704_production_8XVBQIYE",
        prod["key"] == "8XVBQIYE"
        and next(x for x in datasets["master"] if x["pmid"] == "37415704")["key"]
        == "8XVBQIYE",
    )
    native = read_json(RUN / "12-native-duplicate-audit.json")
    check(
        "native_audit_DO_NOT_MERGE",
        native["candidate_groups"] == 1
        and native["merges_performed"] == 0
        and set(native["candidates"][0]["item_keys"]) == {"FXC7ZY9R", "8XVBQIYE"}
        and native["candidates"][0]["decision"].startswith("DO NOT MERGE"),
    )
    control_pmid = pmid(
        (control["data"].get("extra") or "") + " " + (control["data"].get("url") or "")
    )
    check(
        "live_controlled_pair_identity",
        control_pmid in ("", "37415704")
        and normalize_doi(control["data"].get("DOI", "")) == prod["doi"]
        and normalize_title(control["data"]["title"]) == prod["title"],
        {
            "stored_pmid": control_pmid or None,
            "pmid_mapping_basis": "Matching DOI and normalized title against production record 8XVBQIYE; controlled record does not store a PMID.",
        },
    )
    check(
        "exports_exclude_controlled_key",
        all(
            "FXC7ZY9R" not in p.read_text(encoding="utf-8-sig")
            for p in [export_base.with_suffix(".ris"), export_base.with_suffix(".bib")]
        ),
    )
    expected_text = "baseline pré-execução " + BASELINE
    check(
        "workbook_baseline_corrected",
        sheets["README"]["B11"] == expected_text,
        sheets["README"]["B11"],
    )
    check(
        "workbook_provenance_corrected",
        sheets["Search Provenance"]["A2"]
        == "PubMed A/B/C foi executado, importado e reconciliado; triagem científica ainda não iniciada.",
        sheets["Search Provenance"]["A2"],
    )
    backup = read_json(RUN / "backup-manifest.json")
    backup_results = []
    for f in backup["files"]:
        path = Path(backup["backup_directory"]) / f["relative_path"]
        valid = (
            path.is_file()
            and path.stat().st_size == f["bytes"]
            and digest(path) == f["sha256"]
        )
        backup_results.append(
            {
                "file": f["relative_path"],
                "bytes": path.stat().st_size if path.exists() else None,
                "hash_matches": valid,
            }
        )
    check("backup_manifest_files_match", all(x["hash_matches"] for x in backup_results))
    db = Path(backup["backup_directory"]) / "zotero-before.sqlite"
    with sqlite3.connect(db.as_uri() + "?mode=ro", uri=True) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        tables = {
            r[0]
            for r in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        backup_keys = (
            [r[0] for r in connection.execute("SELECT key FROM items")]
            if "items" in tables
            else []
        )
    check(
        "backup_sqlite_valid_nonempty",
        integrity == "ok" and "items" in tables and "FXC7ZY9R" in backup_keys,
        {"integrity": integrity, "tables": len(tables), "items": len(backup_keys)},
    )
    artifacts = [
        source,
        export_base.with_suffix(".ris"),
        export_base.with_suffix(".bib"),
        WORKBOOK,
        RUN / "rollback-manifest.json",
        RUN / "backup-manifest.json",
    ]
    source_lf = hashlib.sha256(source.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    check("source_canonical_hash", source_lf == manifest["source_sha256_lf"])
    result = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "baseline_pre_execution": BASELINE,
        "scope": "Structural reconciliation only; scientific screening and individual source verification pending; no Zotero writes or merges.",
        "checks": checks,
        "structural": structural,
        "backup": backup_results,
        "artifacts": {
            str(p.relative_to(ROOT)).replace("\\", "/"): {
                "sha256": digest(p),
                "bytes": p.stat().st_size,
                "sha256_lf": hashlib.sha256(
                    p.read_bytes().replace(b"\r\n", b"\n")
                ).hexdigest()
                if p.suffix in (".ris", ".bib", ".json")
                else None,
            }
            for p in artifacts
        },
        "native_audit_basis": "Direct inspection of preserved native-view audit dated 2026-09-03, with live pair identity and membership checked. Native UI not reopened in this audit.",
        "failed_controls": errors,
        "local_controls_pass": not errors,
        "publication": "Not established by this local audit. Verify remote commit and CI separately.",
    }
    save_json(args.output / "audit.json", result)
    save_json(args.output / "production-identifiers.json", datasets["zotero"])
    print(
        json.dumps(
            {
                "checks": len(checks),
                "failed_controls": errors,
                "datasets": {
                    k: {
                        "count": v["count"],
                        "missing": v["missing"],
                        "mismatches": v["metadata_mismatches"][:8],
                        "duplicate_groups": {
                            f: len(g) for f, g in v["duplicates"].items()
                        },
                    }
                    for k, v in structural.items()
                },
                "backup": checks["backup_sqlite_valid_nonempty"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
