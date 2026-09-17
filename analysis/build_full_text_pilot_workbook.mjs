import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "file:///C:/Users/mathe/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const sourcePath = "C:/Users/mathe/Documents/Codex/2026-08-26/zotero-plugin-zotero-openai-curated-remote/outputs/full-text/2026-09-17-pilot-01/workbook-source.json";
const outputPath = "outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_01.xlsx";
const source = JSON.parse(await fs.readFile(sourcePath, "utf8"));
const records = source["pilot-records"];
const appraisal = source["appraisal-domain-ledger"];
const redTeam = source["red-team-ledger"];
const provenance = source["provenance-ledger"];

const wb = Workbook.create();
const navy = "#142B4A", blue = "#1E5AA8", teal = "#147D7E", pale = "#EAF1F8";

function matrix(rows, fields, labels = fields) {
  return [labels, ...rows.map((row) => fields.map((field) => row[field] ?? ""))];
}

function styleSheet(sheet, used, headerRow = 1) {
  sheet.showGridLines = false;
  const header = used.getRow(headerRow - 1);
  header.format.fill = navy;
  header.format.font = { bold: true, color: "#FFFFFF" };
  header.format.wrapText = true;
  header.format.verticalAlignment = "center";
  header.format.rowHeight = 32;
  used.format.font = { name: "Aptos", size: 10 };
  used.format.verticalAlignment = "top";
  used.format.borders = { preset: "all", style: "thin", color: "#D8E1EA" };
  used.format.autofitColumns();
  used.format.autofitRows();
  sheet.freezePanes.freezeRows(headerRow);
}

const summary = wb.worksheets.add("Resumo");
summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["FULL-TEXT EVIDENCE QUALIFICATION — PILOTO 01"]];
summary.getRange("A1:H1").format.fill = navy;
summary.getRange("A1:H1").format.font = { bold: true, color: "#FFFFFF", size: 18 };
summary.getRange("A1:H1").format.rowHeight = 34;
summary.getRange("A3:B13").values = [
  ["Indicador", "Valor"], ["Registros no piloto", 10], ["Full text obtido", null],
  ["Identidade confirmada", null], ["Version of Record", null], ["Author Accepted Manuscript", null],
  ["Integridade sem alerta crítico atual", null], ["Proposta IA: reter", null],
  ["Revisão humana requerida", null], ["Decisões humanas", null], ["Claim-Ready", null],
];
summary.getRange("B5").formulas = [["=COUNTIF(Registros!$R$2:$R$11,\"YES\")"]];
summary.getRange("B6").formulas = [["=COUNTIF(Registros!$S$2:$S$11,\"MATCH_CONFIRMED\")"]];
summary.getRange("B7").formulas = [["=COUNTIF(Registros!$T$2:$T$11,\"VERSION_OF_RECORD\")"]];
summary.getRange("B8").formulas = [["=COUNTIF(Registros!$T$2:$T$11,\"AUTHOR_ACCEPTED_MANUSCRIPT\")"]];
summary.getRange("B9").formulas = [["=COUNTIF(Registros!$V$2:$V$11,\"INTEGRITY_CLEAR\")"]];
summary.getRange("B10").formulas = [["=COUNTIF(Registros!$X$2:$X$11,\"INCLUDE_FULL_TEXT\")"]];
summary.getRange("B11").formulas = [["=COUNTIF(Registros!$X$2:$X$11,\"HUMAN_REVIEW_REQUIRED\")"]];
summary.getRange("B12").formulas = [["=COUNTA('Adjudicação Humana'!$H$2:$H$11)"]];
summary.getRange("B13").formulas = [["=COUNTIF(Registros!$AE$2:$AE$11,\"YES\")"]];
summary.getRange("D3:H3").merge(); summary.getRange("D3").values = [["DECISÃO OPERACIONAL"]];
summary.getRange("D4:H5").merge(); summary.getRange("D4").values = [["GO_NONBLOCKING_HUMAN_REVIEW_REQUIRED"]];
summary.getRange("D7:H10").merge();
summary.getRange("D7").values = [["FAIL-CLOSED: toda decisão humana permanece vazia; Claim-Ready permanece NO. As avaliações e decisões de elegibilidade são provisórias e assistidas por IA."]];
summary.getRange("D12:H13").merge(); summary.getRange("D12").values = [["PASS científico: PROIBIDO nesta fase"]];
summary.getRange("A3:B3").format.fill = blue; summary.getRange("A3:B3").format.font = { bold: true, color: "#FFFFFF" };
summary.getRange("D3:H3").format.fill = teal; summary.getRange("D3:H3").format.font = { bold: true, color: "#FFFFFF" };
summary.getRange("D4:H5").format.fill = "#D9EAD3"; summary.getRange("D4:H5").format.font = { bold: true, color: "#215E21", size: 14 };
summary.getRange("D7:H10").format.fill = "#FFF2CC"; summary.getRange("D12:H13").format.fill = "#F4CCCC";
summary.getRange("A3:H13").format.wrapText = true;
summary.getRange("A3:H13").format.borders = { preset: "all", style: "thin", color: "#CBD5E1" };
summary.getRange("A:A").format.columnWidth = 30; summary.getRange("B:B").format.columnWidth = 14;
summary.getRange("D:H").format.columnWidth = 18; summary.freezePanes.freezeRows(1);

const recordFields = ["evidence_id","pmid","doi","pmcid","zotero_key","title","authors","journal","year","volume","issue","pages_or_elocation","full_text_source","access_type","lawful_access","discovered_on","article_type_jats","full_text_obtained","identity_status","version_status","country_context","integrity_status","integrity_detail","ai_full_text_decision","decision_reason","design","appraisal_tool","tool_version","appraisal_complete_ai","human_confirmation","claim_ready","record_status"];
const recordLabels = ["Evidence ID","PMID","DOI","PMCID","Zotero key","Título","Autores","Periódico","Ano","Volume","Número","Páginas/eLocation","Fonte full text","Acesso","Acesso lícito","Descoberta","Tipo JATS","Full text obtido","Identidade","Versão","Contexto","Integridade","Detalhe integridade","Decisão IA provisória","Justificativa","Desenho","Instrumento","Versão instrumento","Appraisal IA","Confirmação humana","Claim-Ready","Status"];
const reg = wb.worksheets.add("Registros");
reg.getRange("A1").write(matrix(records, recordFields, recordLabels));
styleSheet(reg, reg.getUsedRange()); reg.freezePanes.freezeColumns(5);
reg.getRange("F:F").format.columnWidth = 48; reg.getRange("G:G").format.columnWidth = 34; reg.getRange("M:M").format.columnWidth = 38;
reg.getRange("U:Y").format.columnWidth = 32; reg.getRange("A1:AF11").format.wrapText = true;

const extractionFields = ["evidence_id","pmid","title","population","design","extraction","result","exact_evidence_location","supported_claims","unsupported_claims","transferability_limits","red_team_finding"];
const extractionLabels = ["Evidence ID","PMID","Título","População/amostra","Desenho","Extração verificável","Resultado verificável","Localização exata","SUPPORTED_CLAIMS","UNSUPPORTED_CLAIMS","TRANSFERABILITY_LIMITS","Red Team"];
const ext = wb.worksheets.add("Extração"); ext.getRange("A1").write(matrix(records, extractionFields, extractionLabels));
styleSheet(ext, ext.getUsedRange()); ext.freezePanes.freezeColumns(2); ext.getRange("C:L").format.columnWidth = 42; ext.getRange("A1:L11").format.wrapText = true;

const appFields = ["evidence_id","tool","domain","judgment","basis","human_confirmed"];
const app = wb.worksheets.add("Appraisal"); app.getRange("A1").write(matrix(appraisal, appFields, ["Evidence ID","Instrumento","Domínio","Julgamento IA provisório","Base no texto","Confirmação humana"]));
styleSheet(app, app.getUsedRange()); app.freezePanes.freezeColumns(2); app.getRange("C:E").format.columnWidth = 42; app.getRange(`A1:F${appraisal.length + 1}`).format.wrapText = true;

const redFields = Object.keys(redTeam[0]); const red = wb.worksheets.add("Red Team"); red.getRange("A1").write(matrix(redTeam, redFields));
styleSheet(red, red.getUsedRange()); red.freezePanes.freezeColumns(1); red.getRange("R:R").format.columnWidth = 58; red.getRange(`A1:R${redTeam.length + 1}`).format.wrapText = true;

const provFields = ["evidence_id","stage","source","path_external","sha256","timestamp","tool","transformation"];
const prov = wb.worksheets.add("Proveniência"); prov.getRange("A1").write(matrix(provenance, provFields));
styleSheet(prov, prov.getUsedRange()); prov.freezePanes.freezeColumns(2); prov.getRange("C:H").format.columnWidth = 38; prov.getRange(`A1:H${provenance.length + 1}`).format.wrapText = true;

const human = wb.worksheets.add("Adjudicação Humana");
const humanRows = records.map((r) => ({ evidence_id: r.evidence_id, pmid: r.pmid, title: r.title, ai: r.ai_full_text_decision, reason: r.decision_reason, reviewer: "", date: "", decision: "", justification: "", confirmation: "", claim: "NO" }));
human.getRange("A1").write(matrix(humanRows, ["evidence_id","pmid","title","ai","reason","reviewer","date","decision","justification","confirmation","claim"], ["Evidence ID","PMID","Título","Decisão IA provisória","Justificativa IA","Revisor humano","Data humana","Decisão humana","Justificativa humana","Confirmação humana","Claim-Ready"]));
styleSheet(human, human.getUsedRange()); human.freezePanes.freezeColumns(2); human.getRange("C:E").format.columnWidth = 42; human.getRange("I:I").format.columnWidth = 42;
human.getRange("F2:J11").format.fill = "#FFFBE6"; human.getRange("A1:K11").format.wrapText = true;
human.getRange("H2:H11").dataValidation = { rule: { type: "list", values: ["Confirmar retenção", "Confirmar exclusão", "Solicitar esclarecimento", "Solicitar nova avaliação"] } };
human.getRange("J2:J11").dataValidation = { rule: { type: "list", values: ["YES", "NO"] } };

for (const sheet of [reg, ext, app, red, prov, human]) sheet.tabColor = blue;
summary.tabColor = teal;
wb.recalculate();
await fs.mkdir("outputs/full-text/2026-09-17", { recursive: true });
const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(outputPath);
const inspection = await wb.inspect({ kind: "sheet", include: "id,name", maxChars: 3000 });
console.log(inspection.ndjson);
console.log(outputPath);
