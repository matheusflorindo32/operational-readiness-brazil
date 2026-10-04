"""Lawful-source discovery and bounded extraction for Batch 10.4B.

This is intentionally not a scientific decision engine. It retrieves PubMed
metadata and legally available PMC XML, records the exact route, and leaves
methodological appraisal and human confirmation fail-closed.
"""

from __future__ import annotations

import csv
import argparse
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "batch10_4b"
CANONICAL = BASE / "canonical" / "MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv"
OUT = BASE / "scientific"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text(node: ET.Element | None) -> str:
    return " ".join(piece.strip() for piece in node.itertext() if piece.strip()) if node is not None else ""


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "operational-readiness-brazil/10.4B contact: repository-audit"})
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.read()


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index:index + size] for index in range(0, len(values), size)]


def pubmed_records(pmids: list[str]) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for group in chunks(pmids, 80):
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(group), "retmode": "xml"})
        try:
            root = ET.fromstring(fetch(url))
        except Exception:
            time.sleep(0.35)
            continue
        for article in root.findall(".//PubmedArticle"):
            pmid = text(article.find("./MedlineCitation/PMID"))
            citation = article.find("./MedlineCitation/Article")
            abstract = " ".join(text(item) for item in citation.findall("./Abstract/AbstractText")) if citation is not None else ""
            publication_types = "; ".join(text(item) for item in citation.findall("./PublicationTypeList/PublicationType")) if citation is not None else ""
            pmcid = ""
            doi = ""
            for identifier in article.findall("./PubmedData/ArticleIdList/ArticleId"):
                if identifier.get("IdType") == "pmc":
                    pmcid = text(identifier)
                elif identifier.get("IdType") == "doi":
                    doi = text(identifier)
            notices = []
            for notice in article.findall("./PubmedData/History/../..//CommentsCorrectionsList/CommentsCorrections"):
                ref = text(notice.find("RefSource"))
                notices.append(f"{notice.get('RefType', 'NOTICE')}: {ref}".strip())
            grants = "; ".join(text(grant) for grant in article.findall(".//GrantList/Grant"))
            records[pmid] = {"Abstract": abstract, "Publication_Types": publication_types, "PMCID_Detected": pmcid, "DOI_Detected": doi, "Integrity_Notices": " | ".join(notices), "Funding": grants}
        time.sleep(0.35)
    return records


def pmc_extract(pmcid: str) -> dict[str, str]:
    identifier = pmcid.removeprefix("PMC")
    url = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/"  # unused, retained as source family note
    try:
        xml_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode({"db": "pmc", "id": identifier, "retmode": "xml"})
        root = ET.fromstring(fetch(xml_url))
        sections = []
        for sec in root.findall(".//body//sec"):
            title = text(sec.find("title"))
            normalized = title.lower()
            if normalized in {"results", "conclusion", "conclusions", "discussion"}:
                paragraph = text(sec.find("p"))
                if paragraph:
                    sections.append(f"{title}: {paragraph[:1200]}")
            if len(sections) >= 3:
                break
        conflicts = "; ".join(text(item) for item in root.findall(".//fn[@fn-type='conflict']"))
        return {"Full_Text_Status": "LAWFUL_PMC_XML", "Full_Text_URL": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/", "Exact_Location": "PMC XML: " + " | ".join(item.split(":", 1)[0] for item in sections), "Results_Excerpt": " | ".join(sections), "COI": conflicts, "Retrieval_Error": ""}
    except Exception as error:  # network/access failures are evidence, not retried as a hidden fallback
        return {"Full_Text_Status": "FULL_TEXT_UNAVAILABLE", "Full_Text_URL": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/", "Exact_Location": "", "Results_Excerpt": "", "COI": "", "Retrieval_Error": type(error).__name__}


def instrument(design: str, pub_types: str) -> str:
    source = f"{design} {pub_types}".lower()
    if "systematic review" in source or "meta-analysis" in source:
        return "AMSTAR 2"
    if "randomized" in source or "clinical trial" in source:
        return "RoB 2"
    if "qualitative" in source:
        return "JBI Qualitative Checklist"
    if "guideline" in source or "consensus" in source:
        return "AGREE II / RIGHT as applicable"
    if "cross-sectional" in source or "observational" in source or "cohort" in source:
        return "JBI analytical cross-sectional/cohort checklist as applicable"
    return "Design classification required before appraisal"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--lot", default="LOT-01")
    args = parser.parse_args()
    canonical = read_csv(CANONICAL)
    candidates = [row for row in canonical if row["LOOP3X_Final_Class"] in {"FULL_TEXT_REVIEW", "REPLACE_EXISTING_CANDIDATE", "CONTRADICTORY_CANDIDATE"}]
    rank = {"CONTRADICTORY_CANDIDATE": 0, "REPLACE_EXISTING_CANDIDATE": 1, "FULL_TEXT_REVIEW": 2}
    candidates.sort(key=lambda row: (rank[row["LOOP3X_Final_Class"]], 0 if row["LOOP3X_Priority"] == "P0 — CRITICAL" else 1, row["Evidence_ID"]))
    candidates = candidates[args.offset:args.offset + args.limit]
    pmids = [row["PMID"] for row in candidates if row["PMID"]]
    metadata = pubmed_records(pmids)
    pmc_cache: dict[str, dict[str, str]] = {}
    output = []
    for index, row in enumerate(candidates, start=1):
        meta = metadata.get(row["PMID"], {})
        pmcid = row["PMCID"] or meta.get("PMCID_Detected", "")
        if pmcid and pmcid not in pmc_cache:
            pmc_cache[pmcid] = pmc_extract(pmcid)
            time.sleep(0.35)
        full = pmc_cache.get(pmcid, {"Full_Text_Status": "FULL_TEXT_UNAVAILABLE", "Full_Text_URL": "", "Exact_Location": "", "Results_Excerpt": "", "COI": "", "Retrieval_Error": "NO_PMCID_IN_PRIMARY_METADATA"})
        source_url = f"https://pubmed.ncbi.nlm.nih.gov/{row['PMID']}/" if row["PMID"] else (f"https://doi.org/{row['DOI']}" if row["DOI"] else "")
        final = "UNRESOLVED" if full["Full_Text_Status"] == "LAWFUL_PMC_XML" else "FULL_TEXT_UNAVAILABLE"
        output.append({
            **row, "Batch_Order": args.offset + index, "Batch": args.lot,
            "Primary_Metadata_Source": source_url, "Abstract": meta.get("Abstract", ""),
            "Publication_Types": meta.get("Publication_Types", ""), "PMCID_Verified": pmcid,
            "Integrity_Notices": meta.get("Integrity_Notices", ""), "Funding": meta.get("Funding", ""),
            **full, "Appraisal_Instrument": instrument(row["Study_Design"], meta.get("Publication_Types", "")),
            "Appraisal_Status": "PENDING_AI_FULL_TEXT_REVIEW" if final == "UNRESOLVED" else "NOT_POSSIBLE_WITHOUT_LAWFUL_FULL_TEXT",
            "Citation_Fitness_Provisional": row["LOOP3X_Final_Class"].replace("_CANDIDATE", "") + "_AWAITING_APPRAISAL",
            "Final_Decision_AI_Provisional": final, "Human_Review_Status": "PENDING", "Claim_Ready": "NO",
            "Decision_Rationale": "Source discovery completed; no final scientific inclusion without full-text appraisal, exact claim mapping and human confirmation.",
        })
    OUT.mkdir(exist_ok=True)
    lot_dir = OUT / "lots"
    lot_dir.mkdir(exist_ok=True)
    fields = list(output[0])
    write_csv(lot_dir / f"{args.lot}_SOURCE_DISCOVERY.csv", fields, output)
    appraisal = [{key: row[key] for key in ("Evidence_ID", "Title", "Study_Design", "Publication_Types", "Appraisal_Instrument", "Appraisal_Status", "Full_Text_Status", "Human_Review_Status", "Claim_Ready")} for row in output]
    write_csv(lot_dir / f"{args.lot}_APPRAISAL_LEDGER.csv", list(appraisal[0]), appraisal)
    integrity = [{key: row[key] for key in ("Evidence_ID", "PMID", "DOI", "Primary_Metadata_Source", "Integrity_Status", "Integrity_Notices", "Full_Text_Status", "Full_Text_URL", "Retrieval_Error")} for row in output]
    write_csv(lot_dir / f"{args.lot}_INTEGRITY_LEDGER.csv", list(integrity[0]), integrity)
    checkpoint = {"queue": len(output), "lawful_pmc_xml": sum(row["Full_Text_Status"] == "LAWFUL_PMC_XML" for row in output), "full_text_unavailable": sum(row["Final_Decision_AI_Provisional"] == "FULL_TEXT_UNAVAILABLE" for row in output), "unresolved_with_pmc_full_text": sum(row["Final_Decision_AI_Provisional"] == "UNRESOLVED" for row in output), "next_unreviewed_ev_id": output[0]["Evidence_ID"], "gate": "PARTIAL_GO_SOURCE_DISCOVERY_COMPLETE"}
    (lot_dir / f"{args.lot}_SOURCE_DISCOVERY_CHECKPOINT.json").write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checkpoint, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
