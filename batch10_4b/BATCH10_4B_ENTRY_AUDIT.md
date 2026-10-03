# Deep Evidence Batch 10.4B — Auditoria de entrada reexecutada

**Estado atual:** `GO_FULL_TEXT_SATURATION_REVIEW`. O bloqueio estrutural foi
resolvido pela materialização de um ledger canônico de 1.484 linhas a partir do
workbook autoritativo do LOOP 3×. Esta missão não realizou triagem, download de
texto completo, alteração no Zotero, merge, alteração no CEF-v1 ou decisão científica.

## Fonte de entrada auditada

- Branch de continuação: `codex/deep-evidence-batch10-4b`.
- Commit de entrada: `a0fcb99fe67f4009526668acf3e43028ad83e646`.
- Artefatos do LOOP 3×: manifesto, relatório final, 15 checkpoints, fila de
  texto completo, lista de substituições, contraditórios, candidatos de freeze
  e cobertura por domínio.
- CI do commit de entrada: dois workflows `Security baseline` concluídos com
  sucesso (runs `35554838731` e `35554832092`).

## O que foi confirmado

| Controle | Resultado |
| --- | --- |
| Manifesto declarado do LOOP 3× | 1.484 processados; 1.484 IDs únicos; zero IDs e classificações ausentes |
| Checkpoints auditáveis | 15 lotes somam 1.484 processados |
| Fila de saturação | 285/285 linhas e IDs únicos: 266 `FULL_TEXT_REVIEW`, 16 `REPLACE_EXISTING_CANDIDATE`, 3 `CONTRADICTORY_CANDIDATE` |
| CEF-v1 | preservado, com 9 core, 1 supporting, 4 contextual e 1 hold integrity |
| EV-1379 | `FAIL_CLOSED`; proibido como suporte científico |
| Referências v0.12 atuais | 16 na matriz de QA para International e 16 para Brazil |

## Resolução do bloqueio histórico

A busca no Google Drive localizou o workbook canônico
`Operational_Readiness_LOOP3X_EV0001_EV1484_2026-09-21`, aba
`FULL_UNIVERSE_SCREENING`. Ele possui 1.484 registros e os campos de Pass 1,
Pass 2, classe final, prioridade, domínio e proveniência. Sua exportação foi
materializada de modo reexecutável em
`canonical/MASTER_EVIDENCE_CANONICAL_EV0001_EV1484.csv`.

O mapa preservado de 1.456 linhas mais o ledger Batch02/03 de 26 linhas ainda
explica apenas 1.482 registros. O conflito foi resolvido documentalmente: Batch05
formalizou EV-1483 (PMID 26506204; DOI 10.1519/JSC.0000000000001065) e EV-1484
(PMID 36691169; DOI 10.1136/bmjopen-2021-049182), ambos presentes no workbook
canônico. O conflito histórico permanece visível no ledger dedicado.

## Decisão

`CANONICAL_1484_LEDGER_PASS` e `GO_FULL_TEXT_SATURATION_REVIEW`.
O próximo gate pode iniciar o Batch 10.4B original pelos 285 registros, em lotes
de 20–25, sem repetir o LOOP 3×. Esta reexecução não concede aprovação científica
e não inicia a leitura integral nesta missão.
