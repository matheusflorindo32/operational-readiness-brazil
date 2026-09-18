"""Fetch the deterministic Pilot 03 PubMed and PMC source records from NCBI."""

from __future__ import annotations

import argparse
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path(
    os.environ.get(
        "ORB_PILOT03_RAW_ROOT",
        ROOT.parents[1] / "outputs/full-text/2026-09-17-pilot-03",
    )
)

SELECTED = [
    ("EV-0629", "36747268", "PMC9902242"),
    ("EV-0592", "37326779", "PMC10689544"),
    ("EV-0515", "38233933", "PMC10795311"),
    ("EV-0439", "39119394", "PMC11307241"),
    ("EV-0405", "39425094", "PMC11490149"),
    ("EV-0335", "40156033", "PMC11951663"),
    ("EV-0316", "40406195", "PMC12094109"),
    ("EV-0282", "40710431", "PMC12298807"),
    ("EV-0252", "40979841", "PMC12448121"),
    ("EV-0167", "41537090", "PMC12798756"),
]


def fetch(database: str, identifier: str, path: Path) -> None:
    query = urllib.parse.urlencode(
        {"db": database, "id": identifier, "retmode": "xml", "tool": "operational_readiness_brazil"}
    )
    request = urllib.request.Request(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{query}",
        headers={"User-Agent": "operational-readiness-brazil/1.0 (research audit)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    if not payload.startswith((b"<?xml", b"<")):
        raise RuntimeError(f"NCBI did not return XML for {database}:{identifier}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def main(output: Path) -> None:
    for evidence_id, pmid, pmcid in SELECTED:
        targets = [
            ("pubmed", pmid, output / "raw/pubmed" / f"{pmid}.xml"),
            ("pmc", pmcid.removeprefix("PMC"), output / "raw/pmc" / f"{pmcid}.xml"),
        ]
        for database, identifier, path in targets:
            fetch(database, identifier, path)
            print(f"{evidence_id}\t{database}\t{identifier}\t{path.stat().st_size}")
            time.sleep(0.35)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    main(args.output)
