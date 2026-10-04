# Batch 10.4B-FT1 — checkpoint de appraisal por texto completo

**Data:** 2026-10-03
**Commit de entrada:** `5cdc6c34e9edc18833c8b9f57ec1c21d64bb0683`
**Estado:** `PARTIAL_GO`

## Escopo concluído neste checkpoint

Os três primeiros lotes determinísticos iniciaram em `EV-0386` e percorreram 30 registros
da fila PMC. Vinte e sete têm corpo de artigo no XML e receberam leitura, extração
delimitada, identificação de desenho, appraisal provisório, avaliação de
integridade, citation fitness, decisão provisória e Red Team de fronteira. Dois
(`EV-0167` e `EV-0252`) reutilizam, com referência explícita, o appraisal
provisório já realizado no Pilot 03; nenhuma revisão humana foi criada ou
simulada.

`EV-0606`, `EV-0846` e `EV-0143` têm apenas metadados/resumo no XML PMC. Todos foram marcados
`XML_ABSTRACT_ONLY_NOT_FULL_TEXT`; `EV-0606` preserva sua decisão prévia `UNRESOLVED` e os dois
novos registros recebem `FULL_TEXT_INSUFFICIENT`. Nenhum recebeu appraisal, claim ou inclusão.

## Validação da fonte PMC

A verificação de todos os 100 arquivos XML já identificados encontrou:

| Estado | Registros | Percentual de 100 |
|---|---:|---:|
| Corpo de artigo suficiente para leitura | 85 | 85,00% |
| XML somente de resumo ou fragmento | 15 | 15,00% |
| Corpos com leitura FT1 nos lotes 01-03 | 27 | 27,00% |
| Registros processados, incluindo XML incompleto fail-closed | 30 | 30,00% |
| Restantes sem appraisal FT1 | 70 | 70,00% |

Os 15 XML incompletos não são exclusões científicas e não alteram os 185
registros que já estavam sem rota lícita identificada. Eles formam uma
subfila adicional de acesso/versão a ser resolvida legalmente.

## Decisões provisórias acumuladas

| Decisão | n |
|---|---:|
| `PROVISIONAL_REPLACE_CANDIDATE` | 5 |
| `PROVISIONAL_INCLUDE` | 9 |
| `CONTEXT_ONLY` | 7 |
| `DISCUSSION_ONLY` | 4 |
| `QUALITY_EXCLUDE` | 1 |
| `MISALIGNED_EXCLUDE` | 1 |
| `FULL_TEXT_INSUFFICIENT` | 2 |
| `UNRESOLVED` | 1 |

As cinco substituições são somente comparações candidatas: quatro ficaram
`KEEP_BOTH_PROVISIONAL` e nenhuma referência atual foi removida. Não houve
FCR, mudança de CEF-v1, decisão humana, Claim-Ready provisório ou definitivo,
alteração de manuscrito, escrita Zotero, reimportação ou merge.

## Limites metodológicos preservados

- O pequeno ensaio de astaxantina (`EV-0386`) não mostrou benefício clínico ou
  de desempenho ocupacional estatisticamente significativo; seus sinais de
  biomarcadores permanecem insuficientes para recomendação.
- O ensaio de creatina/proteína/carboidrato (`EV-0521`) sustenta apenas a
  melhora de tarefas específicas na amostra masculina estudada, não um efeito
  universal de suplementação.
- As evidências de implementação de `EV-0167` e `EV-0252` sustentam somente
  percepções/associações no contexto policial norte-americano especificado.
- `EV-0402` é narrativa e contextual; `EV-0523` é comentário editorial;
  nenhuma delas é evidência de efetividade.

## Próxima ação exata

Prosseguir pelo lote 04 em `EV-0195`, com os mesmos controles. Dos 70 registros
restantes, 58 têm corpo de artigo já validado e 12 aguardam fonte ou versão com
corpo completo. `PMC100_FULL_TEXT_APPRAISAL_COMPLETE`, saturação de referência,
v0.13 e aprovação científica permanecem bloqueados.
