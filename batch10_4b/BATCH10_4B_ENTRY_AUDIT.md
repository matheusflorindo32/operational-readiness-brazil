# Deep Evidence Batch 10.4B — Auditoria de entrada

**Estado:** `BLOCKED` por falha estrutural de rastreabilidade. Esta auditoria não
realizou triagem, download de texto completo, alteração no Zotero, merge,
alteração no CEF-v1 ou decisão científica.

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

## Bloqueio

O repositório não contém um artefato canônico de **1.484 linhas** com, ao menos,
`Evidence_ID`, classificação final, proveniência da decisão e vínculo com o
registro bibliográfico. A única tabela do LOOP 3× possui os 285 sobreviventes;
o ledger de checkpoint só apresenta totais por lote. Portanto, não é possível
recomputar independentemente os alegados zero IDs ausentes e zero registros sem
classificação.

O mapa de identidade preservado possui 1.456 linhas. O ledger de reconciliação
posterior contém apenas 26 adições, embora a passagem para 1.484 exija 28; assim,
ele reconcilia apenas 1.482 identidades e deixa duas adições sem linha nesse
caminho. Mesmo 1.484 linhas reconciliadas não substituiriam a classificação final
por linha exigida para seleção bibliográfica final.

## Decisão

`BLOCKED` para a execução científica do Batch 10.4B. Processar os 285 agora
atribuiria decisões finais sobre um subconjunto cuja completude não pode ser
auditada, contrariando o critério de liberação do próprio Batch.

O próximo passo exato é reconstruir e versionar o ledger canônico de 1.484
linhas, reconciliando o mapa de 1.456 com todas as 28 adições (incluindo as duas
ausentes no ledger disponível) e registrando a classificação final e a fonte de
cada decisão. Depois, esta auditoria pode ser reexecutada e a fila de 285 pode
avançar em lotes de 20–25.
