import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { SpreadsheetFile, Workbook } from "file:///C:/Users/mathe/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const sourcePath = path.join(os.tmpdir(), "orb-pilot-01-correction-workbook-source.json");
const outputPath = "outputs/full-text/2026-09-17/Operational_Readiness_Full_Text_Pilot_01_Corrected.xlsx";
const source = JSON.parse(await fs.readFile(sourcePath, "utf8"));
const records = source.records;
const appraisal = source.appraisal;
const delta = source.delta;
const aam = source.aam;
const redTeam = source.redTeam;

const wb = Workbook.create();
const navy = "#17324D";
const blue = "#2A5D8F";
const amber = "#F4B942";
const paleBlue = "#EAF2F8";
const paleAmber = "#FFF4D6";
const paleRed = "#FBE4E6";
const paleGreen = "#E7F3EA";
const bodyFont = "Arial";

function matrix(rows, fields, labels = fields) {
  return [labels, ...rows.map((row) => fields.map((field) => row[field] ?? ""))];
}

function tableStyle(sheet, range, headerRow = 1) {
  sheet.showGridLines = false;
  const header = range.getRow(headerRow - 1);
  header.format.fill = navy;
  header.format.font = { name: bodyFont, bold: true, color: "#FFFFFF", size: 10 };
  header.format.horizontalAlignment = "center";
  header.format.verticalAlignment = "center";
  header.format.wrapText = true;
  header.format.rowHeight = 34;
  range.format.font = { name: bodyFont, size: 10, color: "#1F2933" };
  range.format.verticalAlignment = "top";
  range.format.borders = {
    insideHorizontal: { style: "thin", color: "#D7E0E8" },
    bottom: { style: "thin", color: "#AAB8C5" },
  };
  sheet.freezePanes.freezeRows(headerRow);
}

function title(sheet, address, value) {
  sheet.getRange(address).values = [[value]];
  sheet.getRange(address).format.font = { name: bodyFont, bold: true, size: 16, color: navy };
}

const summary = wb.worksheets.add("Resumo");
summary.showGridLines = false;
title(summary, "A2", "Correção metodológica do Piloto 01");
summary.getRange("A3:H3").format.borders = { bottom: { style: "medium", color: blue } };
summary.getRange("A5:B13").values = [
  ["Indicador", "Valor"],
  ["Registros corrigidos", 10],
  ["MMAT completos", null],
  ["JBI textual atual", null],
  ["AAM auditados", null],
  ["Red Team PASS", null],
  ["Confirmações humanas", null],
  ["Claim-Ready", null],
  ["Piloto 02 processado", "NO"],
];
summary.getRange("D5:H5").merge();
summary.getRange("D5").values = [["GATE FINAL"]];
summary.getRange("D6:H7").merge();
summary.getRange("D6").values = [["GO_PILOT_02"]];
summary.getRange("D9:H11").merge();
summary.getRange("D9").values = [["A arquitetura de appraisal foi corrigida. O próximo lote não foi processado. Toda avaliação continua assistida por IA e provisória; confirmação humana permanece pendente."]];
summary.getRange("D13:H14").merge();
summary.getRange("D13").values = [["PASS científico: PROIBIDO | Claim-Ready: 0"]];
summary.getRange("A5:B5").format.fill = navy;
summary.getRange("A5:B5").format.font = { name: bodyFont, bold: true, color: "#FFFFFF" };
summary.getRange("D5:H5").format.fill = blue;
summary.getRange("D5:H5").format.font = { name: bodyFont, bold: true, color: "#FFFFFF" };
summary.getRange("D6:H7").format.fill = paleGreen;
summary.getRange("D6:H7").format.font = { name: bodyFont, bold: true, color: "#1D5C2E", size: 14 };
summary.getRange("D9:H11").format.fill = paleAmber;
summary.getRange("D13:H14").format.fill = paleRed;
summary.getRange("A5:H14").format.wrapText = true;
summary.getRange("A5:H14").format.verticalAlignment = "center";
summary.getRange("A:A").format.columnWidth = 31;
summary.getRange("B:B").format.columnWidth = 15;
summary.getRange("D:H").format.columnWidth = 18;
summary.getRange("A16:H21").values = [
  ["Fontes metodológicas", "URL", "Uso", "", "", "", "", ""],
  ["MMAT 2018", "https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria%20manual_2018%20-08-01_ENG.pdf", "S1/S2, componentes 1.x e 4.x, integração 5.x", "", "", "", "", ""],
  ["JBI Critical Appraisal Tools", "https://jbi.global/critical-appraisal-tools", "Seleção da ferramenta textual atual", "", "", "", "", ""],
  ["JBI Expert Opinion", "https://jbi.global/sites/default/files/2026-05/2.Checklist_Textual_Evidence_Opinion.docx", "Reavaliação domínio a domínio", "", "", "", "", ""],
  ["SANRA", "https://doi.org/10.1186/s41073-019-0064-8", "Qualidade metodológica de revisão narrativa", "", "", "", "", ""],
  ["Commit de origem", "455dde313c9a2f81749189baf601334b733b0dbd", "Artefatos originais preservados por hash", "", "", "", "", ""],
];
summary.getRange("A16:C16").format.fill = navy;
summary.getRange("A16:C16").format.font = { name: bodyFont, bold: true, color: "#FFFFFF" };
summary.getRange("A16:C21").format.wrapText = true;
summary.getRange("B:B").format.columnWidth = 48;
summary.getRange("C:C").format.columnWidth = 38;
summary.tabColor = blue;

const recordFields = ["evidence_id","pmid","doi","zotero_key","title","design","evidence_origin","evidence_class","original_data","empirical_effect_estimate","eligibility_contextual_source","version_status","extraction_version","vor_access_status","vor_comparison_status","appraisal_tool","appraisal_tool_version","appraisal_type","methodological_quality_appraisal","risk_of_bias_appraisal","textual_evidence_appraisal","appraisal_completeness","appraisal_review_status","ai_appraisal_complete_provisional","human_appraisal_confirmed","human_reviewer","human_review_date","human_decision","human_justification","human_confirmation","claim_ready","record_status","unsupported_claims","exact_evidence_location","preferred_claim_locator","global_quality_score"];
const recordLabels = ["Evidence ID","PMID","DOI","Zotero key","Título","Desenho","Origem","Classe de evidência","Dados originais","Estimativa de efeito empírico","Elegibilidade contextual","Versão fonte","Versão usada na extração","Acesso VOR","Comparação VOR","Instrumento","Versão do instrumento","Tipo de appraisal","Qualidade metodológica","Risco de viés","Evidência textual","Completude","Status da revisão","Appraisal IA provisório completo","Appraisal humano confirmado","Revisor humano","Data humana","Decisão humana","Justificativa humana","Confirmação humana","Claim-Ready","Status do registro","O que NÃO permite afirmar","Localização exata","Localização exigida antes de claim","Score global"];
const reg = wb.worksheets.add("Registros corrigidos");
reg.getRange("A1").write(matrix(records, recordFields, recordLabels));
tableStyle(reg, reg.getUsedRange());
reg.freezePanes.freezeColumns(4);
reg.getRange("E:F").format.columnWidth = 44;
reg.getRange("G:AF").format.columnWidth = 25;
reg.getRange("AG:AI").format.columnWidth = 45;
reg.getRange("A1:AJ11").format.wrapText = true;
reg.getRange("Y2:AE11").format.fill = paleAmber;

const appraisalFields = ["evidence_id","tool","tool_version","appraisal_type","component","criterion_code","domain","judgment_ai_provisional","basis","classification_reason","source_url","human_confirmed"];
const app = wb.worksheets.add("Appraisal corrigido");
app.getRange("A1").write(matrix(appraisal, appraisalFields, ["Evidence ID","Instrumento","Versão","Tipo","Componente","Critério","Domínio","Julgamento IA provisório","Base textual","Razão de classificação","Fonte oficial","Confirmação humana"]));
tableStyle(app, app.getUsedRange());
app.freezePanes.freezeColumns(2);
app.getRange("B:D").format.columnWidth = 28;
app.getRange("E:H").format.columnWidth = 28;
app.getRange("I:K").format.columnWidth = 50;
app.getRange(`A1:L${appraisal.length + 1}`).format.wrapText = true;
app.getRange(`L2:L${appraisal.length + 1}`).format.fill = paleAmber;

const deltaFields = ["evidence_id","field","before","after","reason","source"];
const deltaSheet = wb.worksheets.add("Delta");
deltaSheet.getRange("A1").write(matrix(delta, deltaFields, ["Evidence ID","Campo","BEFORE","AFTER","REASON","SOURCE"]));
tableStyle(deltaSheet, deltaSheet.getUsedRange());
deltaSheet.freezePanes.freezeColumns(2);
deltaSheet.getRange("B:F").format.columnWidth = 48;
deltaSheet.getRange(`A1:F${delta.length + 1}`).format.wrapText = true;

const aamFields = ["evidence_id","pmid","doi","source_version","publisher_url","publisher_access","comparison","comparison_scope","extraction_state","claim_location_state","human_confirmed"];
const aamSheet = wb.worksheets.add("AAM-VOR");
aamSheet.getRange("A1").write(matrix(aam, aamFields, ["Evidence ID","PMID","DOI","Versão fonte","URL publisher","Acesso publisher","Comparação","Escopo da comparação","Estado de extração","Localização de claim","Confirmação humana"]));
tableStyle(aamSheet, aamSheet.getUsedRange());
aamSheet.getRange("D:J").format.columnWidth = 40;
aamSheet.getRange("A1:K3").format.wrapText = true;
aamSheet.getRange("K2:K3").format.fill = paleAmber;

const redFields = Object.keys(redTeam[0]);
const red = wb.worksheets.add("Red Team");
red.getRange("A1").write(matrix(redTeam, redFields));
tableStyle(red, red.getUsedRange());
red.freezePanes.freezeColumns(2);
red.getRange("C:R").format.columnWidth = 22;
red.getRange("Q:Q").format.columnWidth = 52;
red.getRange(`A1:R${redTeam.length + 1}`).format.wrapText = true;

const humanRows = records.map((r) => ({evidence_id:r.evidence_id,pmid:r.pmid,title:r.title,ai:r.ai_full_text_decision,status:r.record_status,reviewer:"",date:"",decision:"",justification:"",confirmation:"",claim:"NO"}));
const human = wb.worksheets.add("Revisão humana");
human.getRange("A1").write(matrix(humanRows,["evidence_id","pmid","title","ai","status","reviewer","date","decision","justification","confirmation","claim"],["Evidence ID","PMID","Título","Decisão IA provisória","Status atual","Revisor humano","Data humana","Decisão humana","Justificativa humana","Confirmação humana","Claim-Ready"]));
tableStyle(human, human.getUsedRange());
human.freezePanes.freezeColumns(2);
human.getRange("C:E").format.columnWidth = 42;
human.getRange("F:J").format.columnWidth = 28;
human.getRange("I:I").format.columnWidth = 45;
human.getRange("F2:J11").format.fill = paleAmber;
human.getRange("A1:K11").format.wrapText = true;
human.getRange("H2:H11").dataValidation = { rule: { type: "list", values: ["Confirmar retenção", "Confirmar exclusão", "Solicitar esclarecimento", "Solicitar nova avaliação"] } };
human.getRange("J2:J11").dataValidation = { rule: { type: "list", values: ["YES", "NO"] } };

for (const sheet of [reg, app, deltaSheet, aamSheet, red, human]) sheet.tabColor = paleBlue;
summary.getRange("B7").formulas = [["=COUNTIF('Appraisal corrigido'!$B$2:$B$200,\"MMAT\")/17"]];
summary.getRange("B8").formulas = [["=COUNTIF('Registros corrigidos'!$P$2:$P$11,\"JBI Textual Evidence: Expert Opinion\")"]];
summary.getRange("B9").formulas = [["=COUNTA('AAM-VOR'!$A$2:$A$3)"]];
summary.getRange("B10").formulas = [["=COUNTIF('Red Team'!$R$2:$R$11,\"PASS\")"]];
summary.getRange("B11").formulas = [["=COUNTIF('Revisão humana'!$J$2:$J$11,\"YES\")"]];
summary.getRange("B12").formulas = [["=COUNTIF('Registros corrigidos'!$AE$2:$AE$11,\"YES\")"]];
wb.recalculate();

const keyCheck = await wb.inspect({kind:"table",range:"Resumo!A5:H14",include:"values,formulas",tableMaxRows:20,tableMaxCols:10,maxChars:8000});
console.log(keyCheck.ndjson);
const errors = await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",options:{useRegex:true,maxResults:300},summary:"final formula error scan"});
console.log(errors.ndjson);

const previewDir = path.join(os.tmpdir(), "orb-pilot-01-correction-previews");
await fs.mkdir(previewDir, {recursive:true});
for (const sheetName of ["Resumo","Registros corrigidos","Appraisal corrigido","Delta","AAM-VOR","Red Team","Revisão humana"]) {
  const preview = await wb.render({sheetName, autoCrop:"all", scale:1, format:"png"});
  await fs.writeFile(path.join(previewDir, `${sheetName.replaceAll(" ", "_")}.png`), new Uint8Array(await preview.arrayBuffer()));
}

await fs.mkdir(path.dirname(outputPath), {recursive:true});
const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(outputPath);
const workbookBytes = await fs.readFile(outputPath);
const workbookArtifact = {
  path: outputPath.replaceAll("\\", "/"),
  bytes: workbookBytes.length,
  sha256: crypto.createHash("sha256").update(workbookBytes).digest("hex"),
  sheets: ["Resumo","Registros corrigidos","Appraisal corrigido","Delta","AAM-VOR","Red Team","Revisão humana"],
  summary: {records:10, mmat_complete:2, jbi_textual_current:2, aam_audited:2, red_team_pass:10, human_confirmations:0, claim_ready:0, pilot_02_processed:false},
};
await fs.writeFile("reporting/full-text/2026-09-17/pilot-01-methodological-correction/workbook-artifact.json", JSON.stringify(workbookArtifact, null, 2) + "\n", "utf8");
console.log(JSON.stringify({outputPath, previewDir, sheets:7}));
