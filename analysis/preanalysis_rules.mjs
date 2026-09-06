// Shared XLSX/Sheets formula source. This is a release guard, not a scientific decision.
export const transferColumns = ['CU','CV','CW','CX','CY','CZ','DA'];
export const importedLimitation = 'Identification metadata alone does not permit any substantive scientific, causal, operational, or institutional claim.';
export function textPresent(ref) {
  return `AND(LEN(TRIM(${ref}))>0,LEFT(LOWER(TRIM(${ref})),7)<>"pending")`;
}
export function gateReason(r) {
  const has = c => textPresent(`${c}${r}`);
  const signal = `OR(ISNUMBER(SEARCH("Retracted Publication",Q${r})),CM${r}="Retracted",CN${r}="Retracted",CM${r}="Expression of Concern",CN${r}="Expression of Concern",F${r}="Not used",CG${r}="Critical",CH${r}="High",CH${r}="Critical")`;
  const gates = [
    [`AND(CJ${r}="Yes",CK${r}="Yes",CL${r}="Yes")`, 'PENDING — verification'],
    [`AND(CM${r}="Clear",CN${r}="Verified — clear")`, 'PENDING — integrity resolution'],
    [`AND(${has('CF')},OR(CG${r}="High",CG${r}="Moderate"),OR(CH${r}="Low",CH${r}="Some concerns",CH${r}="Not applicable"))`, 'PENDING — appropriate appraisal'],
    [`AND(DD${r}="No",OR(DE${r}="HIGH",DE${r}="CONDITIONAL"),${has('DF')})`, 'PENDING — transferability and safety'],
    [`AND(${has('DT')},${has('DU')},OR(${has('DV')},${has('DW')}),${has('DX')})`, 'PENDING — claim, result and source location'],
    [`AND(F${r}="Claim-ready",OR(EA${r}="Strong",EA${r}="Moderate"),${has('G')},G${r}<>"No substantive use decision is permitted from identification metadata alone.",${has('DZ')},DZ${r}<>"${importedLimitation}",${has('EI')},ISNUMBER(EH${r}),EH${r}>0)`, 'PENDING — specific limitation and human review'],
  ];
  let result = '"READY"';
  for (const [condition, reason] of gates.reverse()) result = `IF(${condition},${result},"${reason}")`;
  return `=IF(L${r}="","",IF(${signal},"BLOCKED — integrity or use restriction",${result}))`;
}
export function rawTransfer(r) {
  return `=IF(L${r}="","",IF(AND(COUNT(CU${r}:DA${r})=7,${transferColumns.map(c=>`OR(${c}${r}=0,${c}${r}=1,${c}${r}=2)`).join(',')}),SUM(CU${r}:DA${r}),""))`;
}
export function rowFormulas(r) {
  return {
    EC:gateReason(r),
    EB:`=IF(L${r}="","",IF(EC${r}="READY","Yes","No / Pending"))`,
    C:`=IF(L${r}="","",IF(LEFT(EC${r},7)="BLOCKED","🔴 Do not use for conclusion",IF(EB${r}="Yes","🟢 Claim-ready","🟡 Caution / context")))`,
    D:`=IF(L${r}="","",EC${r})`,
    DB:rawTransfer(r),
  };
}
export const dashboardEdits = {
  B22:'=COUNTIF(\'Master Evidence\'!$EB$4:$EB$1459,"Yes")',
  B24:'=COUNTIF(\'Master Evidence\'!$EC$4:$EC$1459,"BLOCKED — integrity or use restriction")',
  J16:'=COUNTA(\'Master Evidence\'!$A$4:$A$1459)-COUNTIF(\'Master Evidence\'!$EH$4:$EH$1459,">0")',
  A15:'Primary family B (identified)', D15:'Primary family C (identified)',
  J15:'Analysis pending (undated)',
  A4:'PUBMED IDENTIFICATION/IMPORT: 1,456/1,456 reconciled. Scientific review not started; claims require the conservative row gate and named human review.',
  N14:'Identification/import reconciled; scientific approval pending',
};
export const positive = {F:'Claim-ready',CJ:'Yes',CK:'Yes',CL:'Yes',CM:'Clear',CN:'Verified — clear',CF:'Synthetic appraisal instrument',CG:'High',CH:'Low',DD:'No',DF:'Synthetic task and context applicability rationale',DT:'Synthetic bounded claim',DU:'Synthetic manuscript section',DV:'Synthetic source section 3',DX:'Synthetic exact result',G:'Synthetic justified applicability decision',DZ:'Synthetic limitation: no causal or institutional generalization',EI:'Synthetic human reviewer',EH:46271,EA:'Strong',CU:2,CV:2,CW:2,CX:2,CY:2,CZ:2,DA:2};
export const scenarios = [
  {name:'positive_complete',changes:{},ready:true},
  {name:'manual_ready_without_traceability',changes:{DT:'',DX:'',DV:''}},
  {name:'retracted',changes:{CM:'Retracted'}},
  {name:'expression_of_concern',changes:{CN:'Expression of Concern'}},
  {name:'imported_retraction_signal',changes:{Q:'Journal Article; Retracted Publication'}},
  {name:'integrity_pending',changes:{CN:'Pending'}},
  {name:'correction_without_specific_resolution',changes:{CM:'Correction',CN:'Verified — correction'}},
  {name:'identifiers_unverified',changes:{CK:'Pending'}},
  {name:'missing_result',changes:{DX:''}},
  {name:'missing_source_location',changes:{DV:'',DW:''}},
  {name:'missing_reviewer',changes:{EI:''}},
  {name:'whitespace_reviewer',changes:{EI:'   '}},
  {name:'pending_reviewer',changes:{EI:'Pending'}},
  {name:'missing_analysis_date',changes:{EH:''}},
  {name:'missing_instrument',changes:{CF:''}},
  {name:'pending_risk_of_bias',changes:{CH:'Pending'}},
  {name:'generic_limitation',changes:{DZ:importedLimitation}},
  {name:'safety_override',changes:{DD:'Yes'}},
  {name:'decimal_scale',changes:{CU:0.5}},
  {name:'negative_scale',changes:{CU:-1}},
  {name:'above_scale',changes:{CU:3}},
  {name:'blank_scale',changes:{CU:''}},
  {name:'zero_scale_valid',changes:{CU:0},ready:true},
  {name:'one_scale_valid',changes:{CU:1},ready:true},
];
