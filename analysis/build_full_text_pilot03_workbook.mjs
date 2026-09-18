import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { SpreadsheetFile, Workbook } from "file:///C:/Users/mathe/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const source = JSON.parse(await fs.readFile(path.join(os.tmpdir(), "orb-pilot-03-workbook-source.json"), "utf8"));
const outputPath = "outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_03.xlsx";
const artifactPath = "reporting/full-text/2026-09-17/pilot-03/workbook-artifact.json";
const wb = Workbook.create();

const navy = "#17324D", blue = "#2A5D8F", paleBlue = "#EAF2F8", paleAmber = "#FFF4D6", paleRed = "#FBE4E6", paleGreen = "#E7F3EA";
const font = "Arial";

function matrix(rows, fields, labels = fields) {
  return [labels, ...rows.map((row) => fields.map((field) => row[field] ?? ""))];
}

function styleTable(sheet, range, freezeColumns = 0) {
  sheet.showGridLines = false;
  const header = range.getRow(0);
  header.format.fill = navy;
  header.format.font = { name: font, bold: true, color: "#FFFFFF", size: 10 };
  header.format.horizontalAlignment = "center";
  header.format.verticalAlignment = "center";
  header.format.wrapText = true;
  header.format.rowHeight = 36;
  range.format.font = { name: font, size: 10, color: "#1F2933" };
  range.format.verticalAlignment = "top";
  range.format.borders = { insideHorizontal: { style: "thin", color: "#D7E0E8" }, bottom: { style: "thin", color: "#AAB8C5" } };
  sheet.freezePanes.freezeRows(1);
  if (freezeColumns) sheet.freezePanes.freezeColumns(freezeColumns);
  sheet.tabColor = paleBlue;
}

const summary = wb.worksheets.add("Resumo");
summary.showGridLines = false;
summary.getRange("A2").values = [["Full-Text Evidence Qualification — Piloto 03"]];
summary.getRange("A2").format.font = { name: font, bold: true, size: 16, color: navy };
summary.getRange("A3:H3").format.borders = { bottom: { style: "medium", color: blue } };
summary.getRange("A5:B18").values = [
  ["Indicador", "Valor"], ["Registros processados", 10], ["Full texts obtidos", 10], ["Identidades confirmadas", 10],
  ["Versões de registro", 7], ["AAM explícitos", 3], ["Estudos qualitativos", 4], ["Mixed methods", 1],
  ["Rotas de appraisal", 6], ["Appraisals IA provisórios", 10], ["Red Team PASS", 10],
  ["Confirmações humanas", null], ["Claim-Ready", null], ["PMC ativos processados", "30/383"],
];
summary.getRange("A5:B5").format.fill = navy;
summary.getRange("A5:B5").format.font = { name: font, bold: true, color: "#FFFFFF" };
summary.getRange("D5:H5").merge(); summary.getRange("D5").values = [["GATE FINAL"]];
summary.getRange("D5:H5").format.fill = blue; summary.getRange("D5:H5").format.font = { name: font, bold: true, color: "#FFFFFF" };
summary.getRange("D6:H7").merge(); summary.getRange("D6").values = [["GO_NEXT_BATCH | KEEP_BATCH_SIZE_10"]];
summary.getRange("D6:H7").format.fill = paleGreen; summary.getRange("D6:H7").format.font = { name: font, bold: true, size: 14, color: "#1D5C2E" };
summary.getRange("D9:H12").merge(); summary.getRange("D9").values = [["Processamento técnico concluído. Todos os julgamentos de appraisal são provisórios e assistidos por IA. Os 30 registros dos Pilotos 01, 02 e 03 permanecem em revisão humana."]];
summary.getRange("D9:H12").format.fill = paleAmber;
summary.getRange("D14:H16").merge(); summary.getRange("D14").values = [["PASS científico: PROIBIDO | Claim-Ready: 0/10 | Confirmação humana: 0/30"]];
summary.getRange("D14:H16").format.fill = paleRed;
summary.getRange("A5:H18").format.wrapText = true; summary.getRange("A5:H18").format.verticalAlignment = "center";
summary.getRange("A:A").format.columnWidth = 32; summary.getRange("B:B").format.columnWidth = 18; summary.getRange("D:H").format.columnWidth = 18;
summary.getRange("A20:C26").values = [
  ["Fonte metodológica", "URL", "Uso"],
  ["JBI Critical Appraisal Tools", "https://jbi.global/critical-appraisal-tools", "Seleção de instrumentos atuais"],
  ["JBI Qualitative Research", "https://jbi.global/sites/default/files/2026-05/2024_Checklist_for_Qualitative_Research_1.docx", "Quatro estudos qualitativos"],
  ["JBI Quasi-Experimental", "https://jbi.global/sites/default/files/2026-05/2_JBI%20checklist%20for%20quasi-experimental%20studies.docx", "Um experimento natural"],
  ["JBI Analytical Cross-Sectional", "https://jbi.global/sites/default/files/2026-03/the_revised_jbi_critical_appraisal_tool_for_the.2.pdf", "Um levantamento analítico"],
  ["MMAT 2018", "https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria%20manual_2018%20-08-01_ENG.pdf", "Um estudo misto e um levantamento descritivo"],
  ["SANRA", "https://doi.org/10.1186/s41073-019-0064-8", "Uma revisão narrativa; qualidade metodológica"],
];
summary.getRange("A20:C20").format.fill = navy; summary.getRange("A20:C20").format.font = { name: font, bold: true, color: "#FFFFFF" };
summary.getRange("A20:C26").format.wrapText = true; summary.getRange("B:B").format.columnWidth = 55; summary.getRange("C:C").format.columnWidth = 38;
summary.tabColor = blue;

const selectionFields = ["pilot_order","evidence_id","pmid","priority_tier","priority_score","access_status","queue_position_after_pilots_01_02_exclusion","selection_rule"];
const selection = wb.worksheets.add("Seleção");
selection.getRange("A1").write(matrix(source.selection, selectionFields, ["Ordem","Evidence ID","PMID","Prioridade","Score","Acesso","Posição após excluir Pilotos 01/02","Regra determinística"]));
styleTable(selection, selection.getUsedRange(), 3); selection.getRange("F:H").format.columnWidth = 38; selection.getRange("A1:H11").format.wrapText = true;

const recordFields = ["pilot_order","evidence_id","pmid","doi","pmcid","zotero_key","title","country_context","population","design","evidence_origin","evidence_class","original_data","empirical_effect_estimate","version_status","integrity_status","eligibility_full_text","appraisal_tool","appraisal_version","appraisal_type","appraisal_summary","extraction","result","exact_evidence_location","supported_claims","unsupported_claims","transferability_limits","human_reviewer","human_review_date","human_decision","human_justification","human_confirmation","claim_ready","record_status","global_quality_score"];
const records = wb.worksheets.add("Registros");
records.getRange("A1").write(matrix(source.records, recordFields, ["Ordem","Evidence ID","PMID","DOI","PMCID","Zotero key","Título","Contexto","População","Desenho","Origem","Classe","Dados originais","Estimativa de efeito","Versão","Integridade","Elegibilidade","Instrumento","Versão instrumento","Tipo appraisal","Resumo appraisal","Extração","Resultado","Localização exata","Supported claims","Unsupported claims","Limites de transferibilidade","Revisor humano","Data humana","Decisão humana","Justificativa humana","Confirmação humana","Claim-Ready","Status","Score global"]));
styleTable(records, records.getUsedRange(), 6); records.getRange("G:AA").format.columnWidth = 38; records.getRange("AB:AF").format.columnWidth = 25; records.getRange("AB2:AF11").format.fill = paleAmber; records.getRange("A1:AI11").format.wrapText = true;

const appraisalFields = ["evidence_id","tool","tool_version","appraisal_type","component","criterion_code","domain","judgment_ai_provisional","basis","source_url","human_confirmed"];
const appraisal = wb.worksheets.add("Appraisal");
appraisal.getRange("A1").write(matrix(source.appraisal, appraisalFields, ["Evidence ID","Instrumento","Versão","Tipo","Componente","Critério","Domínio","Julgamento IA provisório","Base textual","Fonte oficial","Confirmação humana"]));
styleTable(appraisal, appraisal.getUsedRange(), 2); appraisal.getRange("B:H").format.columnWidth = 29; appraisal.getRange("I:J").format.columnWidth = 50; appraisal.getRange(`K2:K${source.appraisal.length + 1}`).format.fill = paleAmber; appraisal.getRange(`A1:K${source.appraisal.length + 1}`).format.wrapText = true;

const versionFields = ["evidence_id","pmid","pmcid","source_version","publisher_url","publisher_access","vor_comparison","comparison_scope","claim_location_status","human_confirmed"];
const versions = wb.worksheets.add("Versões");
versions.getRange("A1").write(matrix(source.versions, versionFields, ["Evidence ID","PMID","PMCID","Versão fonte","URL publisher","Acesso publisher","Comparação VOR","Escopo comparado","Localização de claim","Confirmação humana"]));
styleTable(versions, versions.getUsedRange(), 3); versions.getRange("D:I").format.columnWidth = 42; versions.getRange("J2:J11").format.fill = paleAmber; versions.getRange("A1:J11").format.wrapText = true;

const redFields = Object.keys(source.redTeam[0]);
const red = wb.worksheets.add("Red Team");
red.getRange("A1").write(matrix(source.redTeam, redFields));
styleTable(red, red.getUsedRange(), 2); red.getRange("C:T").format.columnWidth = 23; red.getRange("S:S").format.columnWidth = 55; red.getRange(`A1:T${source.redTeam.length + 1}`).format.wrapText = true;

const provenanceFields = ["evidence_id","stage","source","path_external","sha256","timestamp","tool","transformation"];
const provenance = wb.worksheets.add("Proveniência");
provenance.getRange("A1").write(matrix(source.provenance, provenanceFields, ["Evidence ID","Etapa","Fonte","Caminho externo","SHA-256","Data","Ferramenta","Transformação"]));
styleTable(provenance, provenance.getUsedRange(), 2); provenance.getRange("C:H").format.columnWidth = 44; provenance.getRange(`A1:H${source.provenance.length + 1}`).format.wrapText = true;

const humanFields = ["pilot","evidence_id","pmid","title","ai_decision_provisional","design","evidence_class","instrument","main_findings","limitations","supported_claims","unsupported_claims","pending_items","version","integrity","human_reviewer","human_review_date","human_decision","human_justification","human_confirmation","claim_ready"];
const human = wb.worksheets.add("Revisão humana");
human.getRange("A1").write(matrix(source.humanQueue, humanFields, ["Piloto","Evidence ID","PMID","Título","Decisão IA provisória","Desenho","Classe","Instrumento","Principais achados","Limitações","Supported claims","Unsupported claims","Pendências","Versão","Integridade","Revisor humano","Data humana","Decisão humana","Justificativa humana","Confirmação humana","Claim-Ready"]));
styleTable(human, human.getUsedRange(), 3); human.getRange("D:O").format.columnWidth = 40; human.getRange("P:T").format.columnWidth = 25; human.getRange("P2:T31").format.fill = paleAmber; human.getRange("A1:U31").format.wrapText = true;
human.getRange("R2:R31").dataValidation = { rule: { type: "list", values: ["Confirmar retenção", "Confirmar exclusão", "Solicitar esclarecimento", "Solicitar nova avaliação"] } };
human.getRange("T2:T31").dataValidation = { rule: { type: "list", values: ["YES", "NO"] } };

summary.getRange("B16").formulas = [["=COUNTIF('Revisão humana'!$T$2:$T$31,\"YES\")"]];
summary.getRange("B17").formulas = [["=COUNTIF('Registros'!$AG$2:$AG$11,\"YES\")"]];
wb.recalculate();

const summaryCheck = await wb.inspect({ kind: "table", range: "Resumo!A5:H18", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 10, maxChars: 8000 });
console.log(summaryCheck.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
console.log(errors.ndjson);

const previewDir = path.join(os.tmpdir(), "orb-pilot-03-previews");
await fs.mkdir(previewDir, { recursive: true });
for (const sheetName of ["Resumo","Seleção","Registros","Appraisal","Versões","Red Team","Proveniência","Revisão humana"]) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${sheetName.replaceAll(" ", "_")}.png`), new Uint8Array(await preview.arrayBuffer()));
}

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(outputPath);
const workbookBytes = await fs.readFile(outputPath);
const artifact = {
  path: outputPath.replaceAll("\\", "/"), bytes: workbookBytes.length,
  binary_sha256: crypto.createHash("sha256").update(workbookBytes).digest("hex"),
  sheets: ["Resumo","Seleção","Registros","Appraisal","Versões","Red Team","Proveniência","Revisão humana"],
  summary: { records: 10, full_text: 10, identity: 10, appraisals: 10, red_team: 10, human_confirmations: 0, claim_ready: 0, decision: "GO_NEXT_BATCH", scale_readiness: "KEEP_BATCH_SIZE_10" },
};
await fs.writeFile(artifactPath, JSON.stringify(artifact, null, 2) + "\n", "utf8");
console.log(JSON.stringify({ outputPath, previewDir, sheets: 8 }));
