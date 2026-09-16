# Gate 2 — preparação para adjudicação humana

**Data:** 2026-09-15

**Escopo:** preparação de dossiês e fila; nenhuma adjudicação humana executada

**Decisão:** AGUARDANDO ADJUDICAÇÃO HUMANA

## Condição de entrada

O Gate 1 foi revalidado antes de qualquer alteração. Checkout e `origin/main`
apontavam para `cbd1643308f35f03ce5bff80beb755cb927ca46c`; a execução 35043070339 da
CI estava verde. O Dashboard do XLSX e a Google Sheet canônica apresentavam
zero verdes, 1.446 amarelos e 10 vermelhos. A suíte de regressão concluiu 19/19
testes com sucesso.

## Entrega

Foi criada uma fila separada com 18 registros prioritários: PMID 26159007 e os
17 registros identificados pelo PubMed com relações de correção ou atualização.
Cada linha contém Evidence ID, PMID, DOI quando disponível, Zotero key, título,
tipo de relação, registro relacionado, URLs primárias, recomendação assistida por
IA, risco, justificativa, limite de claim e próxima ação.

A recomendação assistida é `Confirmar bloqueio` somente para a publicação
retratada. Os 17 demais registros recebem `Investigar relação editorial`, sem
substituir a decisão humana. Os campos `Revisor humano`, `Data humana`, `Decisão
humana` e `Justificativa humana` permanecem vazios em 18/18 linhas.

## Controles

| Controle | Resultado |
|---|---:|
| Dossiês preparados | 18/18 (100,00%) |
| PMIDs únicos | 18/18 (100,00%) |
| Zotero keys únicas | 18/18 (100,00%) |
| Retração | 1/18 (5,56%) |
| Relações de correção/atualização | 17/18 (94,44%) |
| Decisões humanas preenchidas | 0/18 (0,00%) |
| Claim-Ready liberado | 0/18 (0,00%) |
| Item-controlado `FXC7ZY9R` | 0/18 (0,00%) |
| Registros sem DOI | 2/18 (11,11%) |
| Relações sem PMID do aviso | 2/18 (11,11%) |

Os dois artigos sem DOI são preservados sem valor inventado. Para dois vínculos
`ErratumIn`, o PubMed fornece a citação do aviso, mas não um PMID relacionado;
esses casos exigem localização editorial pelo periódico durante a adjudicação.

## Artefatos e rastreabilidade

- XLSX: `outputs/adjudication/2026-09-15/GATE_2_Fila_Adjudicacao_Humana_18_Registros.xlsx`
- Fonte estruturada: `reporting/adjudication/2026-09-15/priority-adjudication-source.json`
- Fila CSV: `reporting/adjudication/2026-09-15/priority-adjudication-queue.csv`
- Validação do Drive: `reporting/adjudication/2026-09-15/drive-validation.json`
- Google Sheet: https://docs.google.com/spreadsheets/d/1pP_1ZpLvsfuX3vZUyFydgrr3JGxmVDGWt4PqGtyyAQs/edit

O XLSX final tem SHA-256
`83601c6d1322dc9ef3830b2a1833d043e70382a06669c27ec97589672d6936ef`.
A fonte JSON tem SHA-256
`84f633afb38a2f48651ab7d4a8ad03fd6987a967903f66d029676b73a0f6b34f`;
a fila CSV tem SHA-256
`1c67c887a6eb22e6662e074837127ab3b33834d887698a07e2c13dc400f9bb21`.

As relações editoriais foram reconsultadas por NCBI Entrez EFetch. A Google
Sheet é nativa, privada, somente do proprietário e está no mesmo diretório do
projeto. As tabelas `FilaAdjudicacao` e `DossiesPrioritarios` cobrem exatamente
as 18 linhas; a coluna de decisão humana oferece cinco opções controladas.

## Limites

Nenhum campo humano foi preenchido ou simulado. Zotero, a Master Evidence e a
Sheet canônica não foram alterados. Não houve reimportação, merge, exclusão
física, liberação de Claim-Ready, leitura de texto completo ou avaliação de
qualidade/risco de viés. Gate 3 e etapas posteriores não foram iniciados.
