# Batch 10.4B-FT1 — checkpoint de appraisal por texto completo

**Data:** 2026-10-03
**Commit de entrada:** `5cdc6c34e9edc18833c8b9f57ec1c21d64bb0683`
**Estado:** `PARTIAL_GO`

## Escopo concluído neste checkpoint

O primeiro lote determinístico iniciou em `EV-0386` e percorreu dez registros
da fila PMC. Nove têm corpo de artigo no XML e receberam leitura, extração
delimitada, identificação de desenho, appraisal provisório, avaliação de
integridade, citation fitness, decisão provisória e Red Team de fronteira. Dois
(`EV-0167` e `EV-0252`) reutilizam, com referência explícita, o appraisal
provisório já realizado no Pilot 03; nenhuma revisão humana foi criada ou
simulada.

`EV-0606` tem apenas metadados/resumo no XML PMC. Foi marcado
`XML_ABSTRACT_ONLY_NOT_FULL_TEXT`, permanece `UNRESOLVED` e não recebeu
appraisal, claim ou decisão de inclusão.

## Validação da fonte PMC

A verificação de todos os 100 arquivos XML já identificados encontrou:

| Estado | Registros | Percentual de 100 |
|---|---:|---:|
| Corpo de artigo suficiente para leitura | 85 | 85,00% |
| XML somente de resumo ou fragmento | 15 | 15,00% |
| Lote 01 com leitura de corpo de artigo | 9 | 9,00% |
| Lote 01 processado, incluindo XML incompleto fail-closed | 10 | 10,00% |
| Restantes sem appraisal FT1 | 90 | 90,00% |

Os 15 XML incompletos não são exclusões científicas e não alteram os 185
registros que já estavam sem rota lícita identificada. Eles formam uma
subfila adicional de acesso/versão a ser resolvida legalmente.

## Decisões provisórias do lote 01

| Decisão | n |
|---|---:|
| `PROVISIONAL_REPLACE_CANDIDATE` | 5 |
| `PROVISIONAL_INCLUDE` | 2 |
| `CONTEXT_ONLY` | 1 |
| `DISCUSSION_ONLY` | 1 |
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

Prosseguir pelo lote 02 em `EV-0837`, com os mesmos controles. Dos 90 registros
restantes, 76 têm corpo de artigo já validado e 14 aguardam fonte ou versão com
corpo completo. `PMC100_FULL_TEXT_APPRAISAL_COMPLETE`, saturação de referência,
v0.13 e aprovação científica permanecem bloqueados.
