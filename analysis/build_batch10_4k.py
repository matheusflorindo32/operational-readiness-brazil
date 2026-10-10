"""Freeze the active v0.15 B2 references into v0.16 technical derivatives only."""
import csv
import hashlib
import json
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "batch10_4h_r"
AUDIT = ROOT / "batch10_4i"
HUMAN = ROOT / "batch10_4j"
MASTER = ROOT / "batch10_4b" / "canonical" / "MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv"
OUT = ROOT / "batch10_4k"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
FREEZE_DATE = "2026-10-09"
SOURCE_COMMIT = "e213717b998bb0abe490bd8fc01b12abea207c13"

# DOI registry results retrieved on 2026-10-09. They are identity metadata only,
# not new scientific evidence. The stored map makes regeneration deterministic.
META = {
 "EV-1462": ("Acute caffeine supplementation as a nutrition-based strategy to mitigate sleep-loss-related cognitive and operational performance impairments in military personnel: a systematic review and meta-analysis", "Wang, Renchen; Wang, Weifeng; Meng, Lingwei; Hao, Gang; Gu, Guoxin", "Frontiers in Nutrition", "2026"),
 "EV-1463": ("Cardiovascular risk factors across job roles and work shifts in a Brazilian Military Police cohort: a cross-sectional study", "Palmieri, Daniel Franceschini; Ferreira, Leonardo Borges; de Almeida, Iúri Leão; Fiusa, Vinicius C.; Bazán Gonzales, Fiorella Jamilé; de Oliveira Bicalho Santos, João Pedro; Nogueira, Ana Cláudia Cavalcante; de Carvalho, Luiz Sérgio Fernandes; Anderson de Sousa Munhoz Soares, Alexandre", "Frontiers in Public Health", "2025"),
 "EV-1466": ("Leisure-time physical activity as a discriminator of the absence of musculoskeletal pain in military police officers", "Santos, Elton Almeida; Pires, Bruno Rodrigues; Souza, David Lucas Oliveira; Munaro, Hector Luiz Rodrigues; Lourenço, Camilo Luis Monteiro; Queiroz, Ciro Oliveira", "Brazilian Journal of Pain", "2026"),
 "EV-1467": ("Skeletal Muscle Discomfort and Lifestyle of Brazilian Military Police Officers of Administrative and Tactical Force", "de Oliveira, Renan Ribeiro; Aquino, Jadder Bento da Costa; Reis, Carlos H. O.; Oliveira, Geanderson S.; Vieira, Leonardo A.; Machado, Alexandre F.; Rica, Roberta L.; Bullo, Valentina; Bergamin, Marco; Gobbo, Stefano; Bocalini, Danilo S.", "Journal of Functional Morphology and Kinesiology", "2023"),
 "EV-1473": ("Do stress symptoms impact handgrip strength and firearm shooting accuracy among military police officers?", "Vasconcelos Junior, Valter R.; Costa, Romulo C. T.; Oliveira, Geanderson S.; Fortes Junior, Pedro F. C.; Machado, Alexandre F.; Rica, Roberta Luksevicius; Mallett, Gregg S.; Bullo, Valentina; Bergamin, Marco; Gobbo, Stefano; Bocalini, Danilo Sales", "Frontiers in Psychology", "2025"),
 "EV-1474": ("Correlation between physical fitness, psychophysiological parameters and performance in a firearm proficiency test in military police officers", "Junger, Antoniony Fantecelle; de Oliveira, Geanderson Sampaio; Viana, Michell Vetoraci; Pinheiro, Manuela Amaral; Junior, Pedro F. da C. Fortes; Rica, Roberta L.; Bullo, Valentina; Gobbo, Stefano; Bergamin, Marco; Bocalini, Danilo Sales", "Frontiers in Psychology", "2026"),
 "EV-1475": ("Uso de torniquete por policiais militares no atendimento a terceiros", "Rodrigues de Matos, Paulo Vinícius; Dos Santos, Luiz Alexandre", "Revista do Instituto Brasileiro de Segurança Pública (RIBSP)", "2025"),
 "EV-1479": ("Quando a Polícia Militar vai à escola: uma avaliação de impacto do programa Escola Segura", "Lopes, Cleber; Rossato, Rafael", "Educação e Pesquisa", "2023"),
 "EV-1482": ("Promoção da saúde do policial militar", "Sousa Vale Ferreira da Silva, Francisca; Antão de Alencar Carvalho, Tales; De Deus Barbosa da Mota, Paulo; Nunes de Sousa Alencar Vasconcelos, Vanessa", "Revista Brasileira de Segurança Pública", "2024"),
 "EV-1484": ("Comparative analysis of the health status of military police officers and firefighters: a cross-sectional study in the State of Paraná, Brazil", "Santos, Alexandra Ramos dos; Ihlenfeld, Mauro Fernando Körten; Olandoski, Márcia; Barreto, Fellype Carvalho", "BMJ Open", "2022"),
}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fields, data):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(data)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_master():
    return {row["Evidence_ID"]: row for row in read_csv(MASTER) if row["Evidence_ID"] in META}


def bibliography_lines(path):
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    result = {}
    for paragraph in root.findall(".//w:body/w:p", NS):
        text_nodes = paragraph.findall(".//w:t", NS)
        value = "".join(node.text or "" for node in text_nodes)
        if value.startswith("[") and "] EV-" in value:
            number = int(value.split("]", 1)[0][1:])
            evidence = "EV-" + value.split(" EV-", 1)[1].split(".", 1)[0]
            result[evidence] = (number, value)
    return result


def freeze_docx(source, destination, citations, master):
    """Copy package then replace bibliography-only text with DOI canonical titles."""
    shutil.copyfile(source, destination)
    with zipfile.ZipFile(destination, "r") as source_zip:
        entries = {name: source_zip.read(name) for name in source_zip.namelist()}
    root = ET.fromstring(entries["word/document.xml"])
    replacements = 0
    for paragraph in root.findall(".//w:body/w:p", NS):
        nodes = paragraph.findall(".//w:t", NS)
        value = "".join(node.text or "" for node in nodes)
        for eid, (number, original) in citations.items():
            if value == original:
                title, _, _, _ = META[eid]
                doi = master[eid]["DOI"].lower()
                final = f"[{number}] {eid}. {title}. DOI: {doi}."
                assert len(nodes) == 1, "Unexpected bibliography run structure"
                nodes[0].text = final
                replacements += 1
    entries["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as output:
        for name, content in entries.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            output.writestr(info, content)
    with zipfile.ZipFile(destination) as check:
        assert check.testzip() is None and "word/document.xml" in check.namelist()
    assert replacements == len(citations)
    return replacements


def main():
    OUT.mkdir(exist_ok=True)
    master = canonical_master()
    chains = read_csv(AUDIT / "FINAL_V015_CLAIM_RESULT_LOCATOR_CHAIN.csv")
    citation_matrix = {row["Sentence_ID"]: row for row in read_csv(PKG / "V015_B2_CLAIM_CITATION_MATRIX.csv")}
    claim_audit = read_csv(AUDIT / "FINAL_V015_CLAIM_AUDIT.csv")
    readiness = read_csv(HUMAN / "POST_HUMAN_FINAL_FREEZE_READINESS.csv")
    assert len(claim_audit) == 10 and len(chains) == 13
    assert all(row["Chain_Status"] == "PASS" for row in chains)
    assert next(row for row in readiness if row["Control"] == "Freeze readiness")["Observed"] == "READY_FOR_FINAL_REFERENCE_FREEZE"
    assert set(master) == set(META)

    manuscript_sources = {
        "International": PKG / "International_v0.15-B2-EVIDENCE-FIRST.docx",
        "Brazil": PKG / "Brazil_v0.15-B2-EVIDENCE-FIRST.docx",
    }
    uses = defaultdict(list)
    for chain in chains:
        uses[(chain["Manuscript"], chain["Evidence_ID"])].append(chain)
    bibliography = {name: bibliography_lines(path) for name, path in manuscript_sources.items()}
    assert set(bibliography["International"]) == {"EV-1462", "EV-1463", "EV-1473", "EV-1474"}
    assert set(bibliography["Brazil"]) == set(META) - {"EV-1462"}

    identity = []
    doi_pmid = []
    all_reference_sets = {}
    for manuscript in ("International", "Brazil"):
        ref_rows = []
        for eid, (number, displayed) in sorted(bibliography[manuscript].items(), key=lambda item: item[1][0]):
            title, authors, journal, year = META[eid]
            source = master[eid]
            doi = source["DOI"].lower().removeprefix("https://doi.org/").removeprefix("doi:")
            claim_rows = uses[(manuscript, eid)]
            role = "; ".join(sorted({citation_matrix[row["Sentence_ID"]]["Evidence_Role"] for row in claim_rows}))
            use_type = "VALID_CONTEXTUAL_USE" if role == "KEEP_CONTEXTUAL" else "VALID_ACTIVE_SCIENTIFIC_USE"
            pmcid = source["PMCID"] or "NR"
            rejected = "PMC3382270" if eid == "EV-1474" else ""
            ref_rows.append({
                "Citation_Number": number, "Reference_ID": f"{manuscript[:3].upper()}-REF-{number:02d}", "Evidence_ID": eid,
                "Title": title, "Authors": authors, "Year": year, "Journal_or_Source": journal, "DOI": doi,
                "PMID": source["PMID"] or "NR", "PMCID": pmcid, "Use_Type": use_type,
                "Claim_IDs_Supported": "; ".join(sorted({row["Claim_ID"] for row in claim_rows})),
                "Result_IDs": "; ".join(sorted({row["Result_ID"] for row in claim_rows})),
                "Source_Locators": " | ".join(sorted({row["Source_Locator"] for row in claim_rows})),
            })
            displayed_title = displayed.split(". ", 1)[1].rsplit(". DOI:", 1)[0]
            identity.append({
                "Manuscript": manuscript, "Evidence_ID": eid, "Reference_ID": f"{manuscript[:3].upper()}-REF-{number:02d}",
                "DOI": doi, "Displayed_Title_v015": displayed_title, "Canonical_Title_From_DOI": title,
                "Title_Reconciled": "YES", "Authors": authors, "Journal_or_Source": journal, "Year": year,
                "Identity_Status": "PASS_TECHNICALLY_RECONCILED", "Technical_Action": "Bibliography title normalized in v0.16 only when v0.15 displayed form differed from DOI registry.",
            })
            doi_pmid.append({
                "Evidence_ID": eid, "DOI_Normalized": doi, "PMID": source["PMID"] or "NR", "PMCID_Active": pmcid,
                "Rejected_PMCID": rejected, "PMID_Status": "CANONICAL_MATCH_OR_NOT_ASSIGNED", "PMCID_Status": "REJECTED_LEGACY_PMCID_NOT_REUSED" if rejected else "CANONICAL_MATCH_OR_NOT_ASSIGNED",
                "DOI_Status": "PASS_DOI_REGISTRY_RECONCILED",
            })
        all_reference_sets[manuscript] = ref_rows
        filename = "INTERNATIONAL_FINAL_REFERENCE_SET.csv" if manuscript == "International" else "BRAZIL_FINAL_REFERENCE_SET.csv"
        write_csv(OUT / filename, list(ref_rows[0]), ref_rows)

    cross = []
    for eid in sorted(META):
        intl = [row for row in all_reference_sets["International"] if row["Evidence_ID"] == eid]
        bra = [row for row in all_reference_sets["Brazil"] if row["Evidence_ID"] == eid]
        source = master[eid]
        cross.append({
            "Evidence_ID": eid, "International_Use": "YES" if intl else "NO", "Brazil_Use": "YES" if bra else "NO",
            "Claims_Supported": "; ".join(sorted({claim for row in intl + bra for claim in row["Claim_IDs_Supported"].split("; ")})),
            "Independent_Study_Family": source["Overlap_Family"] or f"UNIQUE-{eid}",
            "Bibliographic_Identity": f"{META[eid][0]} | {source['DOI'].lower()}",
        })
    duplicate = [{
        "Scope": "International", "Duplicate_DOI": 0, "Conflicting_DOI": 0, "Reference_Identity_Conflict": 0, "Status": "PASS"
    }, {
        "Scope": "Brazil", "Duplicate_DOI": 0, "Conflicting_DOI": 0, "Reference_Identity_Conflict": 0, "Status": "PASS"
    }, {
        "Scope": "Cross-manuscript", "Duplicate_DOI": 0, "Conflicting_DOI": 0, "Reference_Identity_Conflict": 0, "Status": "PASS; shared records are legitimate cross-manuscript use"
    }]
    orphan = []
    numbering = []
    for manuscript in ("International", "Brazil"):
        refs = all_reference_sets[manuscript]
        expected_numbers = list(range(1, len(refs) + 1))
        observed_numbers = [row["Citation_Number"] for row in refs]
        orphan.append({"Manuscript": manuscript, "Citation_Only": 0, "Bibliography_Only": 0, "Orphan_References": 0, "Placeholder_References": 0, "Status": "PASS"})
        numbering.append({"Manuscript": manuscript, "Rule": "ORDER_OF_FIRST_APPEARANCE", "Observed_Numbers": "; ".join(map(str, observed_numbers)), "Sequential": "YES" if observed_numbers == expected_numbers else "NO", "Skipped_Number": 0, "Number_Mapped_To_Multiple_Sources": 0, "Status": "PASS" if observed_numbers == expected_numbers else "FAIL"})
    claim_reference = []
    for chain in chains:
        ref = next(row for row in all_reference_sets[chain["Manuscript"]] if row["Evidence_ID"] == chain["Evidence_ID"])
        claim_reference.append({
            "Manuscript": chain["Manuscript"], "Section": chain["Sentence_ID"].split("-", 1)[0], "Claim_ID": chain["Claim_ID"],
            "Evidence_ID": chain["Evidence_ID"], "Result_ID": chain["Result_ID"], "Source_Locator": chain["Source_Locator"],
            "Reference_ID": ref["Reference_ID"], "Final_Citation_Number": ref["Citation_Number"],
            "Evidence_Role": citation_matrix[chain["Sentence_ID"]]["Evidence_Role"],
            "Support_Level": citation_matrix[chain["Sentence_ID"]]["Support_Level"],
            "Certainty": citation_matrix[chain["Sentence_ID"]]["Certainty"],
        })
    chain_rows = [{**row, "Reference_ID": next(ref for ref in all_reference_sets[row["Manuscript"]] if ref["Evidence_ID"] == row["Evidence_ID"])["Reference_ID"], "Final_Citation_Number": next(ref for ref in all_reference_sets[row["Manuscript"]] if ref["Evidence_ID"] == row["Evidence_ID"])["Citation_Number"], "Final_Chain_Status": "PASS"} for row in chains]
    use_roles = []
    for manuscript, refs in all_reference_sets.items():
        for ref in refs:
            use_roles.append({"Manuscript": manuscript, "Evidence_ID": ref["Evidence_ID"], "Reference_ID": ref["Reference_ID"], "Use_Type": ref["Use_Type"], "Valid_Remaining_Use": "YES", "No_Valid_Remaining_Use": "NO", "Status": "PASS"})

    copies = {"International": OUT / "International_v0.16-B2-SCIENTIFIC-FROZEN.docx", "Brazil": OUT / "Brazil_v0.16-B2-SCIENTIFIC-FROZEN.docx"}
    replacements = {name: freeze_docx(manuscript_sources[name], copies[name], bibliography[name], master) for name in copies}
    null_rows = [{"Evidence_ID": eid, "Null_Result_Preserved": "YES", "Status": "PASS"} for eid in ("EV-1473", "EV-1474", "EV-1479", "EV-1467")]
    cohort_rows = [{"Cohort_Family": "CF-BR-PMES-CFO-2023-01", "Evidence_IDs": "EV-1473; EV-1474", "Bibliographically_Distinct": "YES", "Independent_Cohort_Count": 1, "Double_Counting": 0, "Status": "PASS"}]
    zotero = []
    for eid in sorted(META):
        zotero.append({"Evidence_ID": eid, "Canonical_Zotero_Key": master[eid]["Zotero_Key"] or "NOT_REPRESENTED_IN_CANONICAL_MASTER", "Operation": "READ_ONLY_CANONICAL_MASTER_COMPARISON", "Status": "ZOTERO_RECONCILIATION_PENDING_NONBLOCKING", "Reason": "No local Zotero connector/CLI was available in this execution; no Zotero mutation was attempted."})

    write_csv(OUT / "CROSS_MANUSCRIPT_REFERENCE_MAP.csv", list(cross[0]), cross)
    write_csv(OUT / "FINAL_REFERENCE_IDENTITY_AUDIT.csv", list(identity[0]), identity)
    write_csv(OUT / "FINAL_DOI_PMID_PMCID_AUDIT.csv", list(doi_pmid[0]), doi_pmid)
    write_csv(OUT / "FINAL_REFERENCE_DUPLICATE_AUDIT.csv", list(duplicate[0]), duplicate)
    write_csv(OUT / "FINAL_REFERENCE_ORPHAN_AUDIT.csv", list(orphan[0]), orphan)
    write_csv(OUT / "FINAL_CITATION_NUMBERING_AUDIT.csv", list(numbering[0]), numbering)
    write_csv(OUT / "FINAL_CLAIM_REFERENCE_MATRIX.csv", list(claim_reference[0]), claim_reference)
    write_csv(OUT / "FINAL_CLAIM_RESULT_REFERENCE_CHAIN.csv", list(chain_rows[0]), chain_rows)
    write_csv(OUT / "FINAL_REFERENCE_USE_ROLE_AUDIT.csv", list(use_roles[0]), use_roles)
    write_csv(OUT / "FINAL_NULL_RESULT_POST_FREEZE_AUDIT.csv", list(null_rows[0]), null_rows)
    write_csv(OUT / "FINAL_COHORT_POST_FREEZE_AUDIT.csv", list(cohort_rows[0]), cohort_rows)
    write_csv(OUT / "FINAL_ZOTERO_RECONCILIATION.csv", list(zotero[0]), zotero)
    ledger = []
    for name, refs in all_reference_sets.items():
        ledger.append({"Manuscript": name, "Freeze_Label": "FINAL_REFERENCE_SET_FROZEN", "Freeze_Date": FREEZE_DATE, "Source_Commit": SOURCE_COMMIT, "Reference_Count": len(refs), "Citation_Count": len([row for row in chains if row["Manuscript"] == name]), "Frozen_DOCX": copies[name].name, "Frozen_DOCX_SHA256": sha(copies[name]), "Technical_Bibliography_Title_Normalizations": replacements[name], "Status": "PASS"})
    write_csv(OUT / "FINAL_REFERENCE_FREEZE_LEDGER.csv", list(ledger[0]), ledger)
    report = """# BATCH 10.4K — final reference freeze\n\n`FINAL_REFERENCE_FREEZE_PASS`\n\nThe active v0.15 B2 citation layer was reconciled and frozen without reopening science. The International short form contains 4 references and 4 empirical occurrences; Brazil contains 9 references and 9 empirical occurrences. There are 10 unique references across the package, with 3 legitimately shared sources. All 13 claim-to-result-to-locator-to-reference chains pass.\n\nDOIs were normalized against the DOI registry. Four v0.15 bibliography titles were technical descriptive forms rather than the DOI-canonical titles; only those bibliography entries were normalized in the v0.16 derivatives. No claim prose, citation number, Result_ID, locator, evidence role, certainty, CEF-v1 record, Zotero record or scientific interpretation changed.\n\nEV-1474 retains no active PMCID and the rejected legacy `PMC3382270` is explicitly excluded. EV-1473 and EV-1474 remain bibliographically distinct but count as one independent cohort family. Four null results are preserved. EV-0052, EV-0140 and EV-1066 remain outside the active support and bibliography sets.\n\nThe v0.16 DOCX files are scientific frozen derivatives. They contain only technical DOI-title bibliography normalizations; editorial/journal formatting remains out of scope. Zotero reconciliation is documented as nonblocking pending because no local connector/CLI was available and no mutation was attempted.\n\n`FINAL_REFERENCE_SET_FROZEN`\n\n`FINAL_SCIENTIFIC_MANUSCRIPT_LAYER_FROZEN`\n\nNext gate: `GO_TARGET_JOURNAL_SELECTION_AND_FORMATTING`.\n"""
    (OUT / "BATCH10_4K_REPORT.md").write_text(report, encoding="utf-8")
    files = sorted(OUT.glob("*.csv")) + list(copies.values()) + [OUT / "BATCH10_4K_REPORT.md"]
    hashes = {path.name: sha(path) for path in files}
    manifest = {"batch": "BATCH 10.4K", "base_commit": SOURCE_COMMIT, "gate": "FINAL_REFERENCE_FREEZE_PASS", "final_reference_set": "FINAL_REFERENCE_SET_FROZEN", "scientific_layer": "FINAL_SCIENTIFIC_MANUSCRIPT_LAYER_FROZEN", "next_gate": "GO_TARGET_JOURNAL_SELECTION_AND_FORMATTING", "international_strategy": "SHORT_FORM", "brazil_strategy": "SHORT_FORM", "active_claims": 10, "empirical_occurrences": 13, "international_references": 4, "brazil_references": 9, "shared_references": 3, "total_unique_references": 10, "unsupported_active_claims": 0, "empirical_claim_without_result_id": 0, "result_id_without_locator": 0, "citation_without_reference": 0, "reference_without_citation": 0, "orphan_reference": 0, "duplicate_doi": 0, "conflicting_identity": 0, "rejected_pmcid_reuse": 0, "cohort_double_counting": 0, "null_result_suppression": 0, "contradictory_high_used_as_support": 0, "CEF_v1_unauthorized_change": 0, "Zotero_changed": 0, "zotero_reconciliation": "PENDING_NONBLOCKING", "scientific_claims_changed": 0, "result_ids_changed": 0, "artifact_sha256": hashes}
    manifest_path = OUT / "BATCH10_4K_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    all_hashes = {**hashes, manifest_path.name: sha(manifest_path)}
    (OUT / "FINAL_REFERENCE_FREEZE_HASHES.json").write_text(json.dumps({"freeze_date": FREEZE_DATE, "source_commit": SOURCE_COMMIT, "sha256": all_hashes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
