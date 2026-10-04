"""Stage bounded, reproducible PMC XML reading material for Batch 10.4B-FT1.

Raw XML is stored outside Git in the system temporary directory.  The staged
JSON contains only bounded, attributable excerpts and source hashes so that
scientific appraisal remains reviewable without committing article full text.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "batch10_4b" / "scientific" / "FULL_TEXT_SATURATION_MASTER.csv"
STAGING = ROOT / "batch10_4b" / "ft1" / "staging"
RAW = Path(tempfile.gettempdir()) / "operational_readiness_batch10_4b_ft1_xml"


def compact(node: ET.Element | None, limit: int = 4500) -> str:
    if node is None:
        return "NR — NOT REPORTED"
    value = " ".join(piece.strip() for piece in node.itertext() if piece.strip())
    return value[:limit] if value else "NR — NOT REPORTED"


def fetch_xml(pmcid: str) -> bytes:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(
        {"db": "pmc", "id": pmcid.removeprefix("PMC"), "retmode": "xml"}
    )
    request = urllib.request.Request(url, headers={"User-Agent": "operational-readiness-brazil/FT1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def sections(root: ET.Element) -> dict[str, str]:
    selected: dict[str, list[str]] = {key: [] for key in ("Methods", "Results", "Discussion", "Conclusion", "Limitations")}
    for section in root.findall(".//body//sec"):
        title = compact(section.find("title"), 240).lower()
        target = next((name for name in selected if name.lower() in title), None)
        if target and len(selected[target]) < 2:
            selected[target].append(compact(section, 3000))
    return {key: "\n\n".join(value) if value else "NR — NOT REPORTED" for key, value in selected.items()}


def table_captions(root: ET.Element) -> list[str]:
    values = []
    for table in root.findall(".//table-wrap")[:8]:
        label = compact(table.find("label"), 120)
        caption = compact(table.find("caption"), 900)
        values.append(f"{label}: {caption}")
    return values or ["NR — NOT REPORTED"]


def read_rows() -> list[dict[str, str]]:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["Full_Text_Status"] == "LAWFUL_PMC_XML"]
    return sorted(rows, key=lambda row: int(row["Batch_Order"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--lot", default="FT1-LOT-01")
    args = parser.parse_args()
    selected = read_rows()[args.offset:args.offset + args.limit]
    if not selected:
        raise SystemExit("No PMC XML records selected")
    RAW.mkdir(parents=True, exist_ok=True)
    staged = []
    for order, row in enumerate(selected, args.offset + 1):
        pmcid = row["PMCID_Verified"] or row["PMCID"]
        if not pmcid:
            raise SystemExit(f"Missing PMCID for {row['Evidence_ID']}")
        payload = fetch_xml(pmcid)
        raw_path = RAW / f"{row['Evidence_ID']}_{pmcid}.xml"
        raw_path.write_bytes(payload)
        root = ET.fromstring(payload)
        article_meta = root.find(".//article-meta")
        title = compact(article_meta.find("title-group/article-title") if article_meta is not None else None, 1200)
        staged.append({
            "Lot_Order": order,
            "Evidence_ID": row["Evidence_ID"],
            "Title_Canonical": row["Title"],
            "Title_XML": title,
            "PMID": row["PMID"],
            "PMCID": pmcid,
            "DOI": row["DOI"],
            "Canonical_Class": row["LOOP3X_Final_Class"],
            "Priority": row["LOOP3X_Priority"],
            "Domain": row["Domain"],
            "Section": row["Section"],
            "Full_Text_Source": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/",
            "Raw_XML_SHA256": hashlib.sha256(payload).hexdigest(),
            "Abstract": compact(root.find(".//abstract"), 3000),
            "Methods": sections(root)["Methods"],
            "Results": sections(root)["Results"],
            "Discussion": sections(root)["Discussion"],
            "Conclusion": sections(root)["Conclusion"],
            "Limitations": sections(root)["Limitations"],
            "Funding": compact(root.find(".//funding-group"), 1500),
            "COI": compact(root.find(".//fn[@fn-type='conflict']"), 1500),
            "Table_Captions": table_captions(root),
        })
        time.sleep(0.35)
    STAGING.mkdir(parents=True, exist_ok=True)
    target = STAGING / f"{args.lot}_FULL_TEXT_DIGEST.json"
    target.write_text(json.dumps(staged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"lot": args.lot, "staged": len(staged), "first": staged[0]["Evidence_ID"], "last": staged[-1]["Evidence_ID"], "digest": str(target.relative_to(ROOT))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
