# FULL-TEXT EVIDENCE QUALIFICATION — PILOT 04 — 2026-09-20

## 1. Gate de entrada
- `origin/main` auditado remotamente.
- SHA inicial: `383cb7d24900d81611679b250995a2ef6d46530a`.
- GitHub Actions `Security baseline` do SHA inicial: `success`.
- Pilotos 01–03 e Master Evidence não foram modificados por esta execução.
- Limitação: o checkout local Windows do usuário não é exposto nesta sessão; limpeza do working tree local não foi simulada.

## 2. Seleção determinística
Regra: `FIRST_10_P1_PMC_AVAILABLE_NOT_IN_PILOTS_01_02_03`.

Selecionados: EV-0103, EV-1301, EV-1039, EV-0796, EV-0632, EV-0458, EV-0376, EV-0880, EV-0862, EV-0813.

## 3. Full text e identidade
- 10/10 com rota pública/lícita PMC confirmada.
- PMID/PMCID/DOI reconciliados 10/10.
- Nenhum PDF privado/anexo pessoal usado.
- A camada web desta execução não expôs bytes XML brutos uniformemente; hashes brutos de fonte não foram inventados.

## 4. Versões
- Version of Record: 8/10.
- Author Accepted Manuscript: 2/10.
- `EV-0632`: `VOR_COMPARISON_PENDING`.
- `EV-0376`: `VOR_COMPARISON_PENDING`.
- Pendência histórica `EV-0252` permanece preservada separadamente.

## 5. Integridade editorial
A consulta corrente de PubMed/publisher não mostrou relação de retração/Expression of Concern nos dez registros. Formulação é temporal e não garante ausência futura de avisos.

## 6. Desenhos e rotas
Sete rotas metodológicas foram necessárias:
- JBI Qualitative Research;
- JBI Textual Evidence / Expert Opinion;
- SPIRIT completeness (protocolo, não RoB);
- JBI Quasi-Experimental;
- RoB 2;
- JBI Systematic Reviews and Research Syntheses;
- SANRA.

Foram registrados 89 itens/domínios provisórios, todos `AI_ASSISTED_PROVISIONAL_APPRAISAL`.

## 7. Extração e claims
Extrações foram limitadas ao conteúdo verificável. Cada registro contém supported claim, unsupported/prohibited inference, localização reproduzível por seção e limites de transferibilidade.

## 8. Red Team
- 10/10 registros.
- 23 controles por registro.
- 230/230 controles técnicos = PASS.
- PASS técnico não é PASS científico.

## 9. Revisão humana
- Fila acumulada: 40.
- Revisor humano: 0/40.
- Decisões humanas: 0/40.
- Claim-Ready: 0/40.
- Nenhum campo humano foi preenchido em nome de pesquisador.

## 10. Workbook
- XLSX gerado e validado no sandbox de execução: `Operational_Readiness_Full_Text_Pilot_04.xlsx`.
- SHA-256 binário: `6aad700b8b35930c272ce86967a9d508295191303dececbdae352503004ef841`.
- SHA-256 semântico: `ce963365f3454b3afbc09fbe1d0fef6cf97a7f8aa085223611699a550d311598`.
- O conector GitHub desta sessão permite escrita UTF-8, mas não recebe o arquivo binário do sandbox. O binário não foi convertido, falsificado ou publicado como se estivesse no repositório; `workbook-artifact.json` registra explicitamente `repository_binary_present=false`.

## 11. Progresso
- candidatos ativos: 40/1.191 = 3,36%;
- candidatos PMC ativos: 40/383 = 10,44%;
- checklist formal: 52/74 = 70,27%;
- Claim-Ready global: 0/1.456.

## 12. Scale Readiness
`KEEP_BATCH_SIZE_10`.

Motivo central: sete rotas metodológicas, dois AAMs pendentes de comparação VOR e fila humana de 40 sem adjudicação.

## 13. Gate científico-operacional
`HUMAN_REVIEW_PRIORITY`.

O fluxo técnico pode continuar em lotes de no máximo 10, mas a prioridade científica passa a ser iniciar revisão humana progressiva. `PASS científico` permanece proibido.
