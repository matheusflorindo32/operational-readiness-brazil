# Deep Evidence Batch 10.4B — relatório de estado da seleção por texto completo

**Data:** 2026-10-03
**Base de entrada:** commit `00f093933f579e6430a7ae14bc1808e63613099c`
**Decisão do gate:** `PARTIAL_GO`
**Escopo efetivamente concluído:** descoberta de fonte primária e de rota lícita de texto completo para os 285 candidatos.
**Escopo ainda não concluído:** leitura integral, extração, appraisal por desenho, citation fitness, comparação de substituição, adjudicação humana e seleção final de referências.

## Controles de entrada preservados

- Universo canônico: **1.484/1.484** Evidence IDs únicos; zero IDs ausentes e zero classificações finais ausentes.
- Reconciliação: **1.456** registros de baseline + **28** adições = **1.484**.
- Fila B10.4B: **285/285** IDs únicos — 266 `FULL_TEXT_REVIEW`, 16 `REPLACE_EXISTING_CANDIDATE` e três `CONTRADICTORY_CANDIDATE`.
- `CEF-v1` continua congelado; `EV-1379` permanece `FAIL_CLOSED` e está ausente desta fila.
- Nenhum Zotero, RIS/BibTeX, planilha canônica, manuscrito ou item controlado foi modificado; não houve reimportação nem merge.

## Resultado da descoberta em 15 lotes controlados

| Medida | Resultado | Percentual da fila (n=285) |
|---|---:|---:|
| Registros com proveniência pesquisada | 285 | 100,00% |
| XML PMC de rota lícita registrado | 100 | 35,09% |
| Sem rota lícita de texto completo identificada nesta execução | 185 | 64,91% |
| Leitura integral/appraisal completo | 0 | 0,00% |
| Inclusões finais | 0 | 0,00% |
| Substituições de referência atual | 0 | 0,00% |
| Referências `Claim-Ready` | 0 | 0,00% |
| Adjudicações humanas preenchidas | 0 | 0,00% |

As 185 linhas sem rota foram registradas como
`ACCESS_PENDING_NOT_SCIENTIFIC_EXCLUSION` no arquivo solicitado
`FINAL_EXCLUSION_LEDGER.csv`. Não são exclusões metodológicas ou científicas.

## Tier 0 e evidência contraditória

Os 19 registros Tier 0 foram processados antes das filas P0/P1. Os três
contraditórios preservam apenas impactos provisórios baseados no limite do
resumo e aguardam texto completo e appraisal:

| Evidence ID | PMID | Impacto provisório | Estado |
|---|---:|---|---|
| EV-0052 | 42489479 | `MINOR_QUALIFICATION` | `FULL_TEXT_UNAVAILABLE` |
| EV-0140 | 41843415 | `MINOR_QUALIFICATION` | `FULL_TEXT_UNAVAILABLE` |
| EV-1066 | 28919497 | `CLAIM_NARROWING` | `FULL_TEXT_UNAVAILABLE` |

Nenhum contraditório foi ocultado, incluído em manuscrito ou usado para mudar
certeza/claim. Dos 16 candidatos a substituição, cinco têm rota PMC lícita e
onze permanecem sem texto completo acessível nesta execução; todas as 16
comparações seguem `UNRESOLVED`.

## Saturação, integridade e congelamento

Nenhum domínio recebeu status de saturado: os 12 domínios estão `UNRESOLVED`.
O `INTEGRITY_FINAL_LEDGER.csv` preserva os sinais recuperados do PubMed, mas a
checagem editorial individual de artigos potencialmente citáveis ainda depende
de leitura, versão final/publicada e revisão humana. Não houve
`FREEZE_CHANGE_REQUEST`, nem alteração de `CEF-v1` ou do manuscrito v0.12.

## Artefatos e testes

Os 15 artefatos solicitados estão em `batch10_4b/scientific/`, junto dos 15
checkpoints de lote. O `BATCH10_4B_MANIFEST.json` raiz continua como o
manifesto da auditoria de entrada; o manifesto desta fase é
`scientific/BATCH10_4B_SOURCE_DISCOVERY_MANIFEST.json` e sua auditoria é
`scientific/BATCH10_4B_SOURCE_DISCOVERY_AUDIT.json`.

Foram aprovados:

- `python analysis/audit_master_evidence_1484.py` — `CANONICAL_1484_LEDGER_PASS`;
- `python analysis/audit_batch10_4b_source_discovery.py` — todos os 13 controles fail-closed;
- `python -m pytest analysis/test_batch10_4b_source_discovery.py analysis/test_audit_master_evidence_1484.py -q` — **2 passed**.

## Próxima ação exata

Iniciar appraisal em lote pequeno dos 100 registros com XML PMC, mantendo a
ordem por Tier 0/P0/P1, com extração localizável, instrumento compatível com o
desenho e matriz claim–citação. Em paralelo, a busca de texto integral para os
185 registros deve usar somente vias lícitas. A fase não autoriza v0.13,
seleção final, substituição de referências ou aprovação científica global.
