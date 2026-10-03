# Batch 10.4B-R — reconciliação canônica e desbloqueio

## Decisão

`BATCH10_4B_UNBLOCKED` para o próximo gate administrativo: `GO_FULL_TEXT_SATURATION_REVIEW`.
Esta missão não executou leitura integral, appraisal, seleção, exclusão, substituição,
análise de contraditórios, mudança de manuscrito, alteração do CEF-v1 ou FCR.

## Fonte autoritativa materializada

- Drive: [1PsCIFKpNMjrpsaHVu2mGKFYlRboKvNGgorZocCILnoY](https://docs.google.com/spreadsheets/d/1PsCIFKpNMjrpsaHVu2mGKFYlRboKvNGgorZocCILnoY/edit)
- Arquivo: `Operational_Readiness_LOOP3X_EV0001_EV1484_2026-09-21`
- Aba: `FULL_UNIVERSE_SCREENING`
- Data de modificação registrada: 2026-09-21T02:35:49.190Z
- A planilha possui três linhas de cabeçalho e 1.484 registros canônicos.

## Reconciliação

| Controle | Resultado |
| --- | ---: |
| Baseline Evidence Command Center | 1.456 |
| Adições canônicas | 28 |
| Universo canônico | 1484 |
| IDs únicos | 1484 |
| IDs ausentes | 0 |
| Classificações LOOP 3× presentes | 1484/1.484 |
| Proveniência presente | 1484/1.484 |
| Fila de full text reconciliada | 285/285 |

## Reconciliação dos dois registros anteriormente não demonstrados

| Evidence ID | Identificadores | Fonte de canonicalização | Motivo da lacuna anterior |
| --- | --- | --- | --- |
| EV-1483 | PMID 26506204; DOI 10.1519/JSC.0000000000001065 | Batch05 audit e manifest; materialização LOOP 3× | O ledger Batch02/03 contém somente as 26 adições EV-1457..EV-1482. |
| EV-1484 | PMID 36691169; DOI 10.1136/bmjopen-2021-049182; PMCID PMC9453999 | Batch05 audit e manifest; materialização LOOP 3× | O ledger Batch02/03 contém somente as 26 adições EV-1457..EV-1482. |

Os dois registros são formalmente documentados em `reporting/batch05/BATCH05_AUDIT.md`,
`reporting/batch05/manifest.json` e na planilha canônica do LOOP. O
`CANONICAL_CONFLICT_LEDGER.csv` retém a lacuna histórica e sua resolução, sem
ocultar a diferença entre o ledger de 26 e o conjunto final de 28.

## Limites preservados

- EV-1379 permanece `FAIL_CLOSED` e `INTEGRITY_BLOCK`.
- CEF-v1 não foi alterado.
- Itens adicionados continuam com status de Zotero documentado; esta missão não escreveu no Zotero.
- A classificação é materializada do LOOP 3× existente, não recriada por heurística.
