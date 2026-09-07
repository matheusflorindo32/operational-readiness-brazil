"""Refresh PubMed records for controlled screening through the NCBI Entrez skill.

This script never writes Zotero or the workbook. Raw XML stays outside Git; the
committed report contains only compact verification facts and hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "search/exports/2026-08-28/2026-08-28_pubmed_ABC_deduplicated_metadata.json"
)


def text(element):
    return "".join(element.itertext()).strip() if element is not None else ""


def normalized(value):
    value = (
        (value or "")
        .replace("β", "beta")
        .replace("°C", " degrees C")
        .replace("®", "")
        .replace("™", "")
    )
    value = re.sub(r"\(([0-9]+)\)", r"\1", value)
    value = re.sub(r"\([Rr]\)", "", value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def doi_value(article):
    values = []
    for node in article.findall("MedlineCitation/Article/ELocationID[@EIdType='doi']"):
        values.append(text(node))
    for node in article.findall("PubmedData/ArticleIdList/ArticleId[@IdType='doi']"):
        values.append(text(node))
    return next((v.lower().removeprefix("https://doi.org/") for v in values if v), "")


def authors(parent, path):
    result = []
    for node in parent.findall(path):
        collective = text(node.find("CollectiveName"))
        last = text(node.find("LastName"))
        fore = text(node.find("ForeName"))
        value = collective or ", ".join(x for x in (last, fore) if x)
        if value:
            result.append(value)
    return result


def parse_article(article):
    citation = article.find("MedlineCitation")
    journal_article = citation.find("Article")
    pmid = text(citation.find("PMID"))
    title = text(journal_article.find("ArticleTitle"))
    abstracts = []
    for node in journal_article.findall("Abstract/AbstractText"):
        label = node.attrib.get("Label") or node.attrib.get("NlmCategory")
        value = text(node)
        abstracts.append(f"{label}: {value}" if label and value else value)
    pubdate = journal_article.find("Journal/JournalIssue/PubDate")
    year = text(pubdate.find("Year")) if pubdate is not None else ""
    if not year and pubdate is not None:
        match = re.search(r"(?:19|20)\d{2}", text(pubdate.find("MedlineDate")))
        year = match.group(0) if match else ""
    types = [
        text(node)
        for node in journal_article.findall("PublicationTypeList/PublicationType")
    ]
    corrections = []
    for node in citation.findall("CommentsCorrectionsList/CommentsCorrections"):
        corrections.append(
            {
                "ref_type": node.attrib.get("RefType", ""),
                "pmid": text(node.find("PMID")),
                "source": text(node.find("RefSource")),
            }
        )
    return {
        "pmid": pmid,
        "title": title,
        "abstract": " ".join(x for x in abstracts if x),
        "year": year,
        "doi": doi_value(article),
        "authors": authors(article, "MedlineCitation/Article/AuthorList/Author"),
        "journal": text(journal_article.find("Journal/Title")),
        "publication_types": types,
        "corrections": corrections,
        "integrity_signal": bool(
            {
                "Retracted Publication",
                "Retraction of Publication",
                "Expression of Concern",
            }
            & set(types)
            or corrections
        ),
        "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def parse_book(article):
    document = article.find("BookDocument")
    pmid = text(document.find("PMID"))
    types = [text(node) for node in document.findall("PublicationType")]
    abstracts = [text(node) for node in document.findall("Abstract/AbstractText")]
    year = text(document.find("Book/PubDate/Year"))
    identifiers = article.findall("PubmedBookData/ArticleIdList/ArticleId")
    doi = next(
        (
            text(node).lower()
            for node in identifiers
            if node.attrib.get("IdType") == "doi"
        ),
        "",
    )
    return {
        "pmid": pmid,
        "title": text(document.find("ArticleTitle"))
        or text(document.find("Book/BookTitle")),
        "abstract": " ".join(x for x in abstracts if x),
        "year": year,
        "doi": doi,
        "authors": authors(document, "AuthorList/Author"),
        "journal": text(document.find("Book/Publisher/PublisherName"))
        or text(document.find("Book/BookTitle")),
        "publication_types": types,
        "corrections": [],
        "integrity_signal": False,
        "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--helper", type=Path, required=True)
    parser.add_argument("--helper-python", type=Path, default=Path(sys.executable))
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    expected = {row["pmid"]: row for row in source}
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)
    current = {}
    raw_files = []
    pmids = list(expected)
    for index in range(0, len(pmids), 100):
        batch = pmids[index : index + 100]
        raw = args.raw_dir / f"pubmed-{index // 100 + 1:02d}.xml"
        payload = {
            "endpoint": "efetch",
            "params": {"db": "pubmed", "id": ",".join(batch), "retmode": "xml"},
            "response_format": "xml",
            "max_items": 1,
            "max_depth": 1,
            "timeout_sec": 60,
            "save_raw": True,
            "raw_output_path": str(raw),
        }
        if not raw.exists():
            result = subprocess.run(
                [str(args.helper_python), str(args.helper)],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )
            if result.returncode:
                raise RuntimeError(result.stderr or result.stdout)
            response = json.loads(result.stdout)
            if not response.get("ok") or Path(response["raw_output_path"]) != raw:
                raise RuntimeError(response)
            time.sleep(0.35)
        root = ET.parse(raw).getroot()
        for article in root.findall("PubmedArticle"):
            parsed = parse_article(article)
            current[parsed["pmid"]] = parsed
        for article in root.findall("PubmedBookArticle"):
            parsed = parse_book(article)
            current[parsed["pmid"]] = parsed
        raw_files.append(
            {
                "file": raw.name,
                "bytes": raw.stat().st_size,
                "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
            }
        )
    if set(current) != set(expected):
        raise AssertionError(
            {
                "missing": sorted(set(expected) - set(current)),
                "extra": sorted(set(current) - set(expected)),
            }
        )
    records = []
    for pmid, old in expected.items():
        now = current[pmid]
        records.append(
            {
                **now,
                "source_title": old["title"],
                "source_doi": old["doi"].lower(),
                "source_year": str(old["year"]),
                "title_match": normalized(now["title"]) == normalized(old["title"]),
                "doi_match": now["doi"] == old["doi"].lower(),
                "year_match": now["year"] == str(old["year"]),
                "authors_match": [normalized(x) for x in now["authors"]]
                == [normalized(x) for x in old["authors"]],
                "journal_match": normalized(now["journal"])
                == normalized(old["journal"]),
                "doi_newly_available": bool(now["doi"] and not old["doi"]),
            }
        )
    retrieved = datetime.now(timezone.utc).isoformat()
    summary = {
        "retrieved_at": retrieved,
        "source": "NCBI Entrez EFetch via installed ncbi-entrez skill",
        "records": len(records),
        "title_matches": sum(x["title_match"] for x in records),
        "doi_matches": sum(x["doi_match"] for x in records),
        "year_matches": sum(x["year_match"] for x in records),
        "authors_matches": sum(x["authors_match"] for x in records),
        "journal_matches": sum(x["journal_match"] for x in records),
        "doi_newly_available": sum(x["doi_newly_available"] for x in records),
        "integrity_signals": sum(x["integrity_signal"] for x in records),
        "raw_files_external": raw_files,
    }
    (args.output / "pubmed-current-records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output / "pubmed-refresh-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
