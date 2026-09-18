"""Fetch the deterministic Pilot 02 PubMed and PMC source records from NCBI."""

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
        "ORB_PILOT02_RAW_ROOT",
        ROOT.parents[1] / "outputs/full-text/2026-09-17-pilot-02",
    )
)

SELECTED = [
    ("EV-0367", "39808097", "PMC12064357"),
    ("EV-0176", "41492854", "PMC12771649"),
    ("EV-0171", "41520119", "PMC12882353"),
    ("EV-0160", "41626406", "PMC12852583"),
    ("EV-0157", "41673910", "PMC12998156"),
    ("EV-0091", "42196761", "PMC13206323"),
    ("EV-1328", "19947877", "PMC3413284"),
    ("EV-0896", "32191195", "PMC7081854"),
    ("EV-0791", "33909512", "PMC8626520"),
    ("EV-0723", "35120531", "PMC8814788"),
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
    if not payload.startswith(b"<?xml") and not payload.startswith(b"<"):
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
