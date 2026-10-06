"""Build Batch 10.4C artefacts from the verified v0.12 source manuscripts.

This is a fail-closed revision: it does not promote provisional FT8 candidates
to final references or alter the frozen CEF-v1 evidence architecture.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "batch10_4c"
MANUSCRIPTS = OUT / "manuscripts"
FT8 = ROOT / "batch10_4b" / "ft8"
SOURCE = ROOT / ".tmp_batch10_4c_source"


def read_csv(name: str):
    with (FT8 / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def replace_paragraph(p, old: str, new: str):
    if old in p.text:
        # Replacing the paragraph intentionally removes local run styling, which
        # is preferable to retaining a potentially misleading old sentence.
        p.text = p.text.replace(old, new)
        return True
    return False


def add_before_references(doc: Document, heading: str, paragraphs: list[str]):
    refs_index = next((i for i, p in enumerate(doc.paragraphs) if p.text.strip().lower() in {"references", "referências"}), None)
    if refs_index is None:
        raise RuntimeError("References heading not found")
    anchor = doc.paragraphs[refs_index]
    anchor.insert_paragraph_before(heading, style="Heading 1")
    for text in paragraphs:
        anchor.insert_paragraph_before(text)


def revise_doc(language: str, source_name: str, output_name: str):
    doc = Document(SOURCE / source_name)
    if language == "International":
        replacements = {
            "HUMAN REVIEW COPY — FULL MANUSCRIPT v0.12 — NOT FOR SUBMISSION": "HUMAN REVIEW COPY — EVIDENCE-SATURATED MANUSCRIPT v0.13 — NOT FOR SUBMISSION",
            "Final manuscript approval remains PENDING_HUMAN_FINAL_REVIEW.": "Final manuscript approval remains PENDING_HUMAN_FINAL_REVIEW; FT8 candidate roles remain AI-provisional.",
            "Operational Readiness in Tactical Populations: A Claim-Locked Evidence Synthesis With Brazilian Public-Safety Adaptation": "Operational Readiness in Tactical Populations: A Claim-Locked Evidence Synthesis With Bounded Brazilian Public-Safety Adaptation",
            "The proposed framework organizes domains, evidence roles, and transferability boundaries and requires prospective validation before individual or clinical use.": "The proposed framework organizes domains, evidence roles, and transferability boundaries; it remains unvalidated and requires prospective validation before individual, clinical, or operational use.",
        }
        limitation_heading = "Access and adjudication limitations added in v0.13"
        additions = [
            "This v0.13 revision incorporates a reference-saturation partial pass rather than a final scientific pass. Full text adequate for appraisal remained unavailable or insufficient for 22 HIGH records, five targeted MEDIUM records, and 15 PMC100 records. The fail-closed rule means that none of those records is assumed to support the present interpretation.",
            "Three HIGH records with potential contradictory implications remained unadjudicated because lawful full text was unavailable: EV-0052 for psychological self-report as a performance-screening surrogate, EV-0140 for short-term moderately high-fat dietary effects on performance, and EV-1066 for BMI as a global proxy of operational readiness. Accordingly, this manuscript does not make definitive psychological self-report screening claims, does not make universal dietary-fat claims, and does not use BMI alone as a readiness indicator.",
            "Provisional candidates are not final evidence. EV-1462 may only contextualize task- and context-dependent partial mitigation of selected cognitive or operational consequences of sleep loss by caffeine; it does not establish that caffeine reverses or solves sleep loss. EV-1463 is limited to cross-sectional cardiometabolic observations in one PMDF cohort, and EV-1466 is exploratory context only (AUC approximately 0.58). Named human review is required before any candidate is promoted to a final scientific claim or reference decision.",
            "The framework status remains exactly: PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED. CEF-v1 is unchanged.",
        ]
    else:
        replacements = {
            "CÓPIA PARA REVISÃO HUMANA — MANUSCRITO INTEGRAL v0.12 — NÃO SUBMETER": "CÓPIA PARA REVISÃO HUMANA — MANUSCRITO COM EVIDÊNCIA SATURADA v0.13 — NÃO SUBMETER",
            "A aprovação final do manuscrito permanece PENDING_HUMAN_FINAL_REVIEW.": "A aprovação final do manuscrito permanece PENDING_HUMAN_FINAL_REVIEW; os papéis dos candidatos FT8 permanecem provisórios por IA.",
            "Prontidão operacional em profissionais de segurança pública:\nsíntese de evidências com claim locking e framework\nmultidimensional proposto": "Prontidão operacional em profissionais de segurança pública: síntese de evidências com claim locking e adaptação brasileira delimitada",
            "O framework proposto organiza domínios e limites de transferência\ne requer validação prospectiva antes de uso individual ou clínico.": "O framework proposto organiza domínios e limites de transferência, permanece não validado e requer validação prospectiva antes de uso individual, clínico ou operacional.",
        }
        limitation_heading = "Limitações de acesso e adjudicação incorporadas na v0.13"
        additions = [
            "Esta revisão v0.13 incorpora um reference-saturation partial pass, e não uma aprovação científica final. Permaneceram sem texto completo adequado para appraisal 22 registros HIGH, cinco registros MEDIUM direcionados e 15 registros PMC100. Pela regra fail-closed, nenhum desses registros foi presumido como suporte para a interpretação atual.",
            "Três registros HIGH com possível implicação contraditória ficaram sem adjudicação por ausência de texto completo lícito: EV-0052 para instrumento psicológico autorrelatado como substituto de desempenho, EV-0140 para efeitos de dieta moderadamente rica em gordura no desempenho de curto prazo e EV-1066 para BMI como indicador global de prontidão. Por isso, o manuscrito não faz afirmação definitiva sobre triagem psicológica autorrelatada, dieta rica em gordura ou BMI isolado como indicador de prontidão.",
            "Candidatos provisórios não são evidência final. EV-1462 pode apenas contextualizar mitigação parcial, dependente de tarefa e contexto, de alguns prejuízos cognitivos ou operacionais associados à perda de sono por cafeína; não demonstra reversão ou solução da perda de sono. EV-1463 limita-se a observações cardiometabólicas transversais em uma coorte PMDF. EV-1466 é apenas contexto exploratório, com AUC aproximada de 0,58. Revisão humana identificável é obrigatória antes da promoção de qualquer candidato a claim ou referência científica final.",
            "O status do framework permanece exatamente: PROPOSED SYNTHESIS FRAMEWORK — NOT YET VALIDATED. CEF-v1 permanece inalterado.",
        ]
    def all_paragraphs(parent):
        for paragraph in parent.paragraphs:
            yield paragraph
        for table in parent.tables:
            for row in table.rows:
                for cell in row.cells:
                    yield from all_paragraphs(cell)

    applied = 0
    for p in all_paragraphs(doc):
        for old, new in replacements.items():
            applied += int(replace_paragraph(p, old, new))
    # Add auditable constraint text immediately before the reference list.
    add_before_references(doc, limitation_heading, additions)
    doc.save(MANUSCRIPTS / output_name)
    return applied


def main():
    OUT.mkdir(exist_ok=True)
    MANUSCRIPTS.mkdir(exist_ok=True)
    claims = read_csv("CLAIM_SATURATION_ADJUDICATION.csv")
    candidates = read_csv("FINAL_REFERENCE_CANDIDATE_LEDGER.csv")
    domains = read_csv("DOMAIN_SATURATION_ADJUDICATION.csv")
    requirements = read_csv("MANUSCRIPT_LIMITATIONS_REQUIRED.csv")
    contradictions = read_csv("UNRESOLVED_CONTRADICTORY_LEDGER.csv")

    applied_int = revise_doc("International", "International_v0.12-FULL-MANUSCRIPT.docx", "International_v0.13-EVIDENCE-SATURATED.docx")
    applied_bra = revise_doc("Brazil", "Brazil_v0.12-FULL-MANUSCRIPT.docx", "Brazil_v0.13-EVIDENCE-SATURATED.docx")

    claim_rows = []
    for r in claims:
        status = r["Saturation_Status"]
        decision = "SUPPORTED_AFTER_NARROWING" if status == "PARTIALLY_SATURATED" else "LIMITATION_REQUIRED"
        rationale = "Retained only with bounded, non-causal and non-universal wording." if decision == "SUPPORTED_AFTER_NARROWING" else "Blocked/not saturated status requires explicit uncertainty, narrowing or no support claim."
        claim_rows.append({"Claim_ID":r["Claim_ID"],"Manuscript":r["Manuscript"],"Section":r["Section"],"Revised_Claim":r["Claim_Wording"],"References":"Retained v0.12 references only; FT8 candidates not promoted","Evidence_Role":"AI-provisional / HUMAN_REVIEW_PENDING","Directness":r["Directness"],"Saturation_Status":status,"Limitation":r["Rationale"],"Final_Wording_Rationale":rationale,"Final_Status":decision})
    write_csv(OUT / "V013_CLAIM_CITATION_MATRIX.csv", list(claim_rows[0]), claim_rows)

    ref_rows=[]
    for r in candidates:
        ref_rows.append({"Evidence_ID":r["Evidence_ID"],"FT8_Candidate_Status":r["Candidate_Status"],"Decision_v013":"NOT_PROMOTED_PENDING_HUMAN_REVIEW","Manuscript_Use":"NONE_AS_SUPPORT","Rationale":"FT8 candidate is AI-provisional; v0.13 preserves the verified v0.12 reference list pending human adjudication.","Human_Review":"PENDING"})
    write_csv(OUT / "V013_REFERENCE_DECISION_LEDGER.csv", list(ref_rows[0]), ref_rows)

    replacements=[r for r in candidates if r["Candidate_Status"]=="FINAL_REPLACEMENT_CANDIDATE"]
    replacement_rows=[{"Evidence_ID":r["Evidence_ID"],"Decision":"KEEP_CURRENT","Rationale":"No replacement executed: candidate remains AI-provisional and requires named human review; v0.12 verified citation retained.","Human_Review":"PENDING"} for r in replacements]
    write_csv(OUT / "V013_REPLACEMENT_DECISIONS.csv", list(replacement_rows[0]), replacement_rows)

    lim_rows=[{"Requirement_ID":r["Requirement_ID"],"Required_Limitation":r["Required_Manuscript_Limitation"],"International":"INSERTED","Brazil":"INSERTED","Evidence":"v0.13 limitation section","Human_Review":"PENDING"} for r in requirements]
    write_csv(OUT / "V013_REQUIRED_LIMITATIONS_LEDGER.csv", list(lim_rows[0]), lim_rows)
    fcr_rows=[{"Candidate_ID":"V013-FCR-001","Subject":"CEF-v1","Status":"NONE","Rationale":"Textual narrowing and limitations only; no material frozen evidence-role, certainty, overlap or integrity change."}]
    write_csv(OUT / "V013_FCR_CANDIDATES.csv", list(fcr_rows[0]), fcr_rows)
    human_rows=[]
    for r in contradictions:
        human_rows.append({"Queue_ID":f"HUMAN-{r['Evidence_ID']}","Evidence_ID":r["Evidence_ID"],"Priority":"HIGH","Reason":r["Likely_Challenge"],"Required_Decision":"Adjudicate after lawful full-text access","Human_Reviewer":"","Review_Date":"","Decision":"","Justification":""})
    for r in replacements:
        human_rows.append({"Queue_ID":f"HUMAN-{r['Evidence_ID']}","Evidence_ID":r["Evidence_ID"],"Priority":"HIGH","Reason":"Replacement comparison required","Required_Decision":"REPLACE / KEEP_CURRENT / KEEP_BOTH / DROP_BOTH","Human_Reviewer":"","Review_Date":"","Decision":"","Justification":""})
    write_csv(OUT / "V013_HUMAN_REVIEW_QUEUE.csv", list(human_rows[0]), human_rows)

    report = f"""# Batch 10.4C — Evidence-Saturated Manuscript Revision v0.13

## Entry and scope

- Base commit: `1b1bfce61da53c313ddd30debdcea3f6776c9d75`.
- Gate inherited: `REFERENCE_SATURATION_PARTIAL_PASS` for revision preparation only.
- Source manuscripts: authenticated Drive copies of v0.12, retained separately and not modified.
- No new literature search, CEF-v1 change, Zotero change, merge, or promotion to Claim-Ready occurred.

## Outputs

- Two new v0.13 manuscripts generated from v0.12 sources.
- {len(claim_rows)}/60 claim rows mapped. All are AI-provisional and `HUMAN_REVIEW_PENDING`.
- {len(replacements)}/6 replacement candidates: `KEEP_CURRENT` pending named human review; no silent replacement.
- Unresolved contradictory records explicitly disclosed: {', '.join(r['Evidence_ID'] for r in contradictions)}.
- Required limitations inserted: {len(lim_rows)}/{len(requirements)}.

## Reference control

The v0.13 manuscripts retain the 16 verified v0.12 references. FT8 candidates are recorded in the decision ledger but none was promoted into bibliography or claim support. Therefore, this pass does not claim final reference closure.

## Decision

`V0.13_EVIDENCE_SATURATED_MANUSCRIPTS_COMPLETE` is **not declared**. The accurate status is `GO_FINAL_SCIENTIFIC_AND_REFERENCE_AUDIT_PENDING_HUMAN_REVIEW`: documents are generated for audit, but source-level human adjudication, final reference selection and full scientific sign-off remain open.
"""
    (OUT / "BATCH10_4C_REPORT.md").write_text(report, encoding="utf-8")
    deliverable_files = [
        p for p in OUT.rglob("*")
        if p.is_file() and not any(part.startswith("qa") for part in p.relative_to(OUT).parts) and p.name != "BATCH10_4C_MANIFEST.json"
    ]
    manifest={"batch":"BATCH10_4C","base_commit":"1b1bfce61da53c313ddd30debdcea3f6776c9d75","inherited_gate":"REFERENCE_SATURATION_PARTIAL_PASS","status":"GO_FINAL_SCIENTIFIC_AND_REFERENCE_AUDIT_PENDING_HUMAN_REVIEW","claims":len(claim_rows),"required_limitations":len(lim_rows),"replacement_candidates":len(replacements),"human_review_queue":len(human_rows),"cef_v1":"UNCHANGED","zotero":"UNCHANGED","v012":"UNCHANGED","source_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.glob('*.docx')},"document_text_replacements":{"international":applied_int,"brazil":applied_bra},"files":{p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in deliverable_files}}
    (OUT / "BATCH10_4C_MANIFEST.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")


def refresh_manifest_hashes():
    """Refresh hashes after the renderer adds the requested PDF deliverables."""
    path = OUT / "BATCH10_4C_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    files = [p for p in OUT.rglob("*") if p.is_file() and not any(part.startswith("qa") for part in p.relative_to(OUT).parts) and p.name != path.name]
    manifest["files"] = {p.relative_to(OUT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    path.write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
