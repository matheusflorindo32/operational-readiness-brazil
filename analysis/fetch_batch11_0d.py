from pathlib import Path
import csv
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path.cwd()
OUTPUT = ROOT / "batch11_0d"
OUTPUT.mkdir(exist_ok=True)


def fetch(url, method="GET"):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "operational-readiness-brazil-integrity-audit/1.0"},
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            return {
                "ok": True,
                "status": response.status,
                "url": response.geturl(),
                "body": response.read().decode("utf-8", "replace"),
            }
    except Exception as error:
        return {"ok": False, "status": "", "url": url, "error": str(error)}


def value(element, path):
    target = element.find(path)
    return "".join(target.itertext()).strip() if target is not None else ""


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


source = {
    row["Evidence_ID"]: row
    for row in read_csv(ROOT / "batch10_4b/ft1/artifacts/PMC100_FULL_TEXT_EXTRACTION.csv")
}
decisions = read_csv(ROOT / "batch11_0c/HUMAN_EXPANSION_DECISIONS_FINAL.csv")
evidence_ids = [row["Evidence_ID"] for row in decisions]
pmids = [source[evidence_id]["PMID"] for evidence_id in evidence_ids]

pubmed_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(
    {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
)
pubmed_response = fetch(pubmed_url)
if not pubmed_response["ok"]:
    raise RuntimeError(pubmed_response)

pubmed = {}
for article in ET.fromstring(pubmed_response["body"]).findall(".//PubmedArticle"):
    pmid = value(article, "MedlineCitation/PMID")
    article_data = article.find("MedlineCitation/Article")
    authors = []
    for author in article_data.findall("AuthorList/Author"):
        author_name = " ".join(
            item
            for item in [value(author, "LastName"), value(author, "ForeName"), value(author, "CollectiveName")]
            if item
        )
        authors.append(author_name)
    identifiers = {
        item.attrib.get("IdType", ""): "".join(item.itertext()).strip()
        for item in article.findall("PubmedData/ArticleIdList/ArticleId")
    }
    comments = [
        {
            "type": item.attrib.get("RefType", ""),
            "pmid": value(item, "PMID"),
            "text": value(item, "RefSource"),
        }
        for item in article.findall("MedlineCitation/CommentsCorrectionsList/CommentsCorrections")
    ]
    publication_types = [
        "".join(item.itertext()).strip()
        for item in article.findall("MedlineCitation/Article/PublicationTypeList/PublicationType")
    ]
    year_candidates = [
        value(article_data, "Journal/JournalIssue/PubDate/Year"),
        value(article_data, "ArticleDate/Year"),
        value(article_data, "Journal/JournalIssue/PubDate/MedlineDate"),
    ]
    pubmed[pmid] = {
        "pmid": pmid,
        "title": value(article, "MedlineCitation/Article/ArticleTitle"),
        "journal": value(article, "MedlineCitation/Article/Journal/Title"),
        "year": next((item for item in year_candidates if item), ""),
        "authors": authors,
        "doi": identifiers.get("doi", ""),
        "pmcid": identifiers.get("pmc", ""),
        "publication_types": publication_types,
        "comments_corrections": comments,
        "publication_status": value(article, "PubmedData/PublicationStatus"),
        "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }

if len(pubmed) != 26:
    raise RuntimeError(f"Expected 26 PubMed records, received {len(pubmed)}")

crossref = {}
resolver = {}


def fetch_external(evidence_id):
    record = source[evidence_id]
    doi = record["DOI"].strip().lower()
    if doi:
        response = fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))
        if response["ok"]:
            try:
                message = json.loads(response["body"])["message"]
                crossref[evidence_id] = {
                    "ok": True,
                    "doi": message.get("DOI", ""),
                    "title": (message.get("title") or [""])[0],
                    "publisher": message.get("publisher", ""),
                    "type": message.get("type", ""),
                    "relation": message.get("relation", {}),
                    "update_to": message.get("update-to", []),
                    "url": message.get("URL", ""),
                }
            except Exception as error:
                crossref[evidence_id] = {"ok": False, "error": f"json: {error}"}
        else:
            crossref[evidence_id] = {"ok": False, "error": response["error"]}
        response = fetch("https://doi.org/" + urllib.parse.quote(doi, safe=""), "HEAD")
        resolver[evidence_id] = {
            "ok": response["ok"],
            "status": response.get("status", ""),
            "final_url": response.get("url", ""),
            "error": response.get("error", ""),
        }
    else:
        crossref[evidence_id] = {"ok": False, "error": "NO_DOI"}
        resolver[evidence_id] = {"ok": False, "error": "NO_DOI", "status": "", "final_url": ""}


with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(fetch_external, evidence_id) for evidence_id in evidence_ids]
    for future in as_completed(futures):
        future.result()

snapshot = {
    "check_date": "2026-10-10",
    "pubmed_batch_url": pubmed_url,
    "pubmed": pubmed,
    "crossref": crossref,
    "doi_resolver": resolver,
}
(OUTPUT / "_live_integrity_snapshot.json").write_text(
    json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(
    json.dumps(
        {
            "pubmed": len(pubmed),
            "crossref": sum(item.get("ok", False) for item in crossref.values()),
            "resolver": sum(item.get("ok", False) for item in resolver.values()),
        }
    )
)
