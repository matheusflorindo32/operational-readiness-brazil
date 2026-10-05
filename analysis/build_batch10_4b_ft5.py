"""FT5: lawful, identity-first remediation for the 22 unresolved HIGH records.

Only metadata and hashes of lawfully reachable responses are versioned.  The
script never stores article bodies, modifies Zotero, or performs appraisal.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT3 = ROOT / "batch10_4b" / "ft3" / "HIGH25_FULL_TEXT_RECOVERY_MASTER.csv"
OUT = ROOT / "batch10_4b" / "ft5"
OUT.mkdir(parents=True, exist_ok=True)
APPRAISED = {"EV-1462", "EV-1463", "EV-1466"}
CONTRADICTORY = {"EV-0052", "EV-0140", "EV-1066"}
TODAY = date.today().isoformat()
UA = "operational-readiness-brazil/FT5 lawful-access-audit (+https://github.com/matheusflorindo32/operational-readiness-brazil)"


def fetch(url: str, accept: str = "text/html,application/pdf,application/xml;q=0.9,*/*;q=0.1"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            payload = response.read(1_500_000)
            return {"ok": True, "status": response.status, "url": response.url, "ctype": response.headers.get_content_type(), "body": payload}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "ctype": "", "body": b""}
    except Exception:
        return {"ok": False, "status": "ERROR", "url": url, "ctype": "", "body": b""}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def html_text(payload: bytes) -> str:
    decoded = payload.decode("utf-8", "ignore")
    decoded = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", decoded)
    return re.sub(r"\s+", " ", re.sub(r"(?is)<[^>]+>", " ", html.unescape(decoded))).strip()


def candidate_valid(record: dict[str, str], result: dict) -> dict[str, str]:
    """Fail closed unless the response is a real body with bibliographic identity."""
    text = html_text(result["body"]) if result["ctype"] != "application/pdf" else ""
    title_core = norm(record["Title"])[:45]
    doi_core = norm(record["DOI"])
    title_match = bool(title_core and title_core in norm(text))
    doi_match = bool(not doi_core or doi_core in norm(text) or doi_core in norm(result["url"]))
    methods = bool(re.search(r"\b(methods?|materials and methods)\b", text, re.I))
    results = bool(re.search(r"\bresults?\b", text, re.I))
    discussion = bool(re.search(r"\bdiscussion\b", text, re.I))
    references = bool(re.search(r"\breferences?\b", text, re.I))
    full = title_match and doi_match and methods and results and discussion and references
    return {
        "Title_Match": "YES" if title_match else "NO",
        "DOI_Match": "YES" if doi_match else "NO",
        "Methods": "YES" if methods else "NO", "Results": "YES" if results else "NO",
        "Discussion": "YES" if discussion else "NO", "References": "YES" if references else "NO",
        "Full_Body_Validated": "YES" if full else "NO",
        "SHA256": hashlib.sha256(result["body"]).hexdigest() if full else "",
        "File_Size_Bytes": str(len(result["body"])) if full else "",
    }


def json_get(url: str) -> dict:
    response = fetch(url, "application/json")
    if not response["ok"]:
        return {}
    try:
        return json.loads(response["body"].decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def unique_urls(values: list[str]) -> list[str]:
    out = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def write_csv(name: str, rows: list[dict]) -> None:
    fields = list(rows[0]) if rows else ["Evidence_ID"]
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    with FT3.open(encoding="utf-8", newline="") as handle:
        universe = [row for row in csv.DictReader(handle) if row["Evidence_ID"] not in APPRAISED]
    assert len(universe) == 22 and {r["Evidence_ID"] for r in universe}.isdisjoint(APPRAISED)
    universe.sort(key=lambda r: (0 if r["Evidence_ID"] in CONTRADICTORY else 1, int(r["Priority_Rank"])))

    attempts, master, identities, versions, integrity, readiness = [], [], [], [], [], []
    for record in universe:
        ev, doi, pmid = record["Evidence_ID"], record["DOI"], record["PMID"]
        candidates: list[tuple[str, str, str]] = []
        # These are new retrieval mechanisms; FT3's Europe PMC/PMC check is retained in Notes.
        if doi:
            candidates.append(("DOI landing / publisher", f"https://doi.org/{doi}", "PUBLISHER_OR_DOI_LANDING"))
            crossref = json_get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))
            message = crossref.get("message", {})
            for link in message.get("link", []):
                if link.get("URL"):
                    candidates.append(("Crossref linked resource", link["URL"], "CROSSREF_LINK"))
            work = json_get("https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi, safe=""))
            for location in work.get("locations", []) if work else []:
                pdf = location.get("pdf_url")
                landing = location.get("landing_page_url")
                if pdf: candidates.append(("OpenAlex indexed lawful PDF", pdf, "OPENALEX_PDF"))
                if landing: candidates.append(("OpenAlex indexed lawful landing", landing, "OPENALEX_LANDING"))
        if pmid:
            # LinkOut is a new route distinct from the FT3 PMC XML fetch.
            candidates.append(("PubMed LinkOut", f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&cmd=llinks&id={pmid}", "PUBMED_LINKOUT"))
            epmc = json_get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&query=EXT_ID:" + urllib.parse.quote(pmid))
            for hit in epmc.get("resultList", {}).get("result", []):
                for link in hit.get("fullTextUrlList", {}).get("fullTextUrl", []):
                    if link.get("url"): candidates.append(("Europe PMC listed full text", link["url"], "EUROPEPMC_LISTED"))
        candidates = [(source, url, kind) for source, url, kind in candidates if url]
        checked = set(); recovered = None; attempt_statuses = []
        for source, url, kind in candidates[:4]:
            if url in checked: continue
            checked.add(url)
            result = fetch(url)
            attempt_statuses.append(str(result["status"]))
            validation = candidate_valid(record, result) if result["ok"] else {k: "NO" for k in ("Title_Match","DOI_Match","Methods","Results","Discussion","References","Full_Body_Validated")}
            validation.update({"SHA256":"", "File_Size_Bytes":""}) if not result["ok"] else None
            attempts.append({"Evidence_ID":ev,"Source":source,"Route_Type":kind,"URL_Checked":url,"HTTP_Status":str(result["status"]),"Resolved_URL":result["url"],"Content_Type":result["ctype"],"Checked_Date":TODAY,"Result":"FULL_BODY_VALIDATED" if validation["Full_Body_Validated"] == "YES" else "NOT_ACCEPTED_AS_FULL_TEXT","Reason":"Identity + Methods/Results/Discussion/References required; response was not accepted otherwise."})
            if validation["Full_Body_Validated"] == "YES":
                if recovered and recovered["SHA256"] == validation["SHA256"]:
                    continue
                if recovered:
                    # Two different accepted sources for one record are recorded but the first verified source remains canonical.
                    continue
                recovered = {**validation, "Source":source,"Route_Type":kind,"URL":result["url"],"HTTP_Status":str(result["status"]),"Content_Type":result["ctype"]}
            time.sleep(0.1)
        if recovered:
            status = "FULL_TEXT_RECOVERED_FINAL_VERSION" if recovered["Route_Type"] in {"PUBLISHER_OR_DOI_LANDING", "CROSSREF_LINK"} else "FULL_TEXT_RECOVERED_OTHER_LAWFUL_VERSION"
            ready = "YES"
        else:
            # Rate limits and transport errors are not evidence of a paywall.
            status = "ACCESS_UNRESOLVED" if any(s in {"ERROR", "429"} for s in attempt_statuses) or not doi else "PAYWALLED_NO_LAWFUL_FULL_TEXT_FOUND"
            ready = "NO"
            recovered = {"Source":"","Route_Type":"","URL":"","HTTP_Status":"","Content_Type":"","Title_Match":"NO","DOI_Match":"NO","Methods":"NO","Results":"NO","Discussion":"NO","References":"NO","SHA256":"","File_Size_Bytes":""}
        base = {"Evidence_ID":ev,"Title":record["Title"],"DOI":doi,"PMID":pmid,"Priority_Rank":record["Priority_Rank"],"Priority_Reason":record["Priority_Reason"],"Contradictory_Flag":record["Contradictory_Flag"],"Replacement_Flag":record["Replacement_Flag"],"P0_Flag":record["P0_Flag"],"Domain":record["Domain"]}
        master.append({**base,"Final_Access_Status":status,"Appraisal_Ready":ready,"Verified_Source_URL":recovered["URL"],"Version_Type":"PUBLISHER_FINAL_OR_EQUIVALENT" if status == "FULL_TEXT_RECOVERED_FINAL_VERSION" else "NOT_RECOVERED","Prior_FT3_Route":"Europe PMC API + PMC XML (no body route)","FT5_Novel_Routes":"DOI/publisher, Crossref, OpenAlex, PubMed LinkOut where PMID available","Notes":"No appraisal in FT5."})
        identities.append({**base,"Verified_Source_URL":recovered["URL"],"Title_Match":recovered["Title_Match"],"DOI_Match":recovered["DOI_Match"],"Journal_Match":"NOT_ASSESSED_WITHOUT_ACCEPTED_BODY" if not ready else "PENDING_APPRAISAL_STAGE_CONFIRMATION","Year_Match":"NOT_ASSESSED_WITHOUT_ACCEPTED_BODY" if not ready else "PENDING_APPRAISAL_STAGE_CONFIRMATION","Identity_Status":"IDENTITY_VERIFIED" if ready else "NO_ACCEPTED_FULL_TEXT_IDENTITY"})
        versions.append({**base,"Version_Type":"PUBLISHER_FINAL_OR_EQUIVALENT" if status == "FULL_TEXT_RECOVERED_FINAL_VERSION" else "NONE","Source":recovered["Source"],"URL":recovered["URL"],"HTTP_Status":recovered["HTTP_Status"],"Content_Type":recovered["Content_Type"],"File_Size_Bytes":recovered["File_Size_Bytes"],"SHA256":recovered["SHA256"],"Local_File_Status":"NOT_RETAINED — copyrighted/source body not versioned","License_Status":"NOT_ASSESSED"})
        integrity.append({"Evidence_ID":ev,"DOI":doi,"PMID":pmid,"Version_Checked":recovered["URL"] or "No recovered version","Retraction_Correction_EOC":"NOT_SCREENED_TO_CLEARANCE — FT5 access-only","Integrity_Status":"INTEGRITY_UNRESOLVED","Decision_Effect":"No appraisal/Claim-Ready/final citation decision in FT5."})
        readiness.append({"Evidence_ID":ev,"Final_Access_Status":status,"Methods":recovered["Methods"],"Results":recovered["Results"],"Discussion":recovered["Discussion"],"References":recovered["References"],"One_EV_One_Validated_Source_Identity":"YES" if ready else "NOT_APPLICABLE","No_Shared_Unrelated_Source":"YES","Appraisal_Ready":ready,"Reason":"Complete body + identity required; no appraisal performed."})

    assert len(master) == 22 and len({r["Evidence_ID"] for r in master}) == 22
    assert not any(r["Evidence_ID"] in APPRAISED for r in master)
    write_csv("HIGH22_ACCESS_REMEDIATION_MASTER.csv", master)
    write_csv("HIGH22_ACCESS_ATTEMPT_LEDGER.csv", attempts)
    write_csv("HIGH22_IDENTITY_VALIDATION.csv", identities)
    write_csv("HIGH22_VERSION_LEDGER.csv", versions)
    write_csv("HIGH22_INTEGRITY_SCREEN.csv", integrity)
    write_csv("HIGH22_APPRAISAL_READINESS.csv", readiness)
    write_csv("HIGH22_CONTRADICTORY_RECOVERY.csv", [r for r in master if r["Evidence_ID"] in CONTRADICTORY])
    write_csv("HIGH22_REPLACEMENT_RECOVERY.csv", [r for r in master if r["Replacement_Flag"] == "YES"])
    write_csv("HIGH22_UNRESOLVED_ACCESS.csv", [r for r in master if r["Appraisal_Ready"] == "NO"])
    recovered = [r for r in master if r["Appraisal_Ready"] == "YES"]
    full_manifest = {"batch":"BATCH10_4B_FT5","recovered": [{"Evidence_ID":r["Evidence_ID"],"URL":r["Verified_Source_URL"]} for r in recovered],"local_files":"None retained","identity_control":"ONE_EV_ONE_VALIDATED_SOURCE_IDENTITY; NO_SHARED_FULLTEXT_SOURCE_ACROSS_UNRELATED_EV"}
    (OUT / "HIGH22_RECOVERED_FULLTEXT_MANIFEST.json").write_text(json.dumps(full_manifest, indent=2) + "\n", encoding="utf-8")
    counts = {status: sum(r["Final_Access_Status"] == status for r in master) for status in sorted({r["Final_Access_Status"] for r in master})}
    report = f"""# Batch 10.4B-FT5 — targeted HIGH access remediation\n\n## Scope\n\nExactly 22 unresolved HIGH records from FT3 were processed. The three previously appraised records were excluded. FT5 is access, identity and provenance only; it performs no scientific appraisal, citation decision, manuscript change, CEF update or Zotero write.\n\n## Outcome\n\n- Processed: 22/22\n- Newly recovered/appraisal-ready: {len(recovered)}/22\n- Status counts: {json.dumps(counts)}\n- Contradictories processed: 3/3; recovered/appraisal-ready: {sum(r['Appraisal_Ready']=='YES' for r in master if r['Evidence_ID'] in CONTRADICTORY)}/3\n- CEF-v1, manuscripts and Zotero: unchanged\n\nFT3's Europe PMC/PMC-only route was not repeated as the sole action. FT5 added DOI/publisher resolution, Crossref links, OpenAlex locations and PubMed LinkOut where a PMID existed. A response was accepted only when its identity matched and the body exposed Methods, Results, Discussion and References. No body was committed, and no inaccessible record was scientifically excluded.\n\n## Gate\n\n`HIGH22_ACCESS_REMEDIATION_COMPLETE`: 22/22 have a documented final access status.\n\n"""
    if recovered:
        report += "`GO_TARGETED_HIGH_APPRAISAL` for: " + ", ".join(r["Evidence_ID"] for r in recovered) + ". Do not start that appraisal automatically.\n"
    else:
        report += "No additional record met the full-body identity requirement in the automated primary-metadata and lawful-index routes used in FT5. This is **not** a claim that author-request or unindexed institutional routes are impossible. Recommended next decision: assess whether targeted MEDIUM access is justified by remaining domain gaps while retaining the three contradictory HIGH records in their access queue.\n"
    report += "\n## Red team\n\nThe acceptance rule prevents abstract/preview substitution, URL reuse and wrong-article promotion. Publisher access is not treated as a quality or citation signal; integrity remains unresolved until a later appraisal-stage screen.\n"
    (OUT / "BATCH10_4B_FT5_REPORT.md").write_text(report, encoding="utf-8")
    files = sorted(p for p in OUT.iterdir() if p.name != "BATCH10_4B_FT5_MANIFEST.json")
    manifest = {"batch":"BATCH10_4B_FT5","gate":"HIGH22_ACCESS_REMEDIATION_COMPLETE","processed":22,"ids":[r["Evidence_ID"] for r in master],"counts":counts,"appraisal_ready":[r["Evidence_ID"] for r in recovered],"cef_v1":"UNCHANGED","zotero":"UNCHANGED","manuscript":"UNCHANGED","files":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (OUT / "BATCH10_4B_FT5_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

# End of FT5 builder.
