"""Verify whether a staged PMC XML contains an article body adequate for FT1."""

from __future__ import annotations

import csv
import glob
import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4b" / "ft1" / "artifacts"
RAW = Path(tempfile.gettempdir()) / "operational_readiness_batch10_4b_ft1_xml"


def main() -> int:
    rows = []
    for name in sorted(glob.glob(str(RAW / "EV-*_PMC*.xml"))):
        root = ET.parse(name).getroot()
        body = root.find(".//body")
        words = len(" ".join(part.strip() for part in body.itertext() if part.strip()).split()) if body is not None else 0
        evidence_id, pmcid_xml = Path(name).stem.split("_", 1)
        status = "FULL_ARTICLE_BODY_AVAILABLE" if words >= 500 else "XML_ABSTRACT_OR_FRAGMENT_ONLY"
        rows.append({"Evidence_ID": evidence_id, "PMCID": pmcid_xml, "Body_Word_Count": words, "FT1_Source_Body_Status": status})
    if len(rows) != 100 or len({row["Evidence_ID"] for row in rows}) != 100:
        raise SystemExit(f"Expected 100 staged PMC XML records, found {len(rows)}")
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "PMC100_SOURCE_BODY_VALIDATION.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print({"total": len(rows), "full_article_body": sum(row["FT1_Source_Body_Status"] == "FULL_ARTICLE_BODY_AVAILABLE" for row in rows), "xml_abstract_or_fragment_only": sum(row["FT1_Source_Body_Status"] != "FULL_ARTICLE_BODY_AVAILABLE" for row in rows)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
