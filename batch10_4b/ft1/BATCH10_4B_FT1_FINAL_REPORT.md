# Batch 10.4B-FT1 — checkpoint de appraisal por texto completo

**Data:** 2026-10-05
**Commit de entrada:** `136d30d22161118f27a1d2bc00fdb9d27388db84`
**Estado:** `PARTIAL_GO`

## Escopo concluído neste checkpoint

Os sete primeiros lotes determinísticos iniciaram em `EV-0386` e percorreram 70 registros
da fila PMC. Sessenta e três têm corpo de artigo no XML e receberam leitura, extração
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
| Corpos com leitura FT1 nos lotes 01-07 | 63 | 63,00% |
| Registros processados, incluindo XML incompleto fail-closed | 70 | 70,00% |
| Restantes sem appraisal FT1 | 30 | 30,00% |

Os 15 XML incompletos não são exclusões científicas e não alteram os 185
registros que já estavam sem rota lícita identificada. Eles formam uma
subfila adicional de acesso/versão a ser resolvida legalmente.

## Decisões provisórias acumuladas

| Decisão | n |
|---|---:|
| `PROVISIONAL_REPLACE_CANDIDATE` | 5 |
| `PROVISIONAL_INCLUDE` | 21 |
| `CONTEXT_ONLY` | 21 |
| `DISCUSSION_ONLY` | 13 |
| `QUALITY_EXCLUDE` | 1 |
| `MISALIGNED_EXCLUDE` | 2 |
| `FULL_TEXT_INSUFFICIENT` | 6 |
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

O lote 04 foi integrado a partir de `EV-0195`: um protocolo, duas revisões sem
método reprodutível suficiente, uma coorte policial, duas análises transversais,
uma análise de bombeiros, um XML sem corpo e um ensaio crossover. A coorte policial,
a análise de estresse militar, a análise de bombeiros e o ensaio nutricional foram
mantidos somente como candidatos provisórios, com limites explícitos e sem liberação
de claim. O lote 05 integrou uma simulação não ocupacional, um protocolo de reabilitação,
evidência observacional de bombeiros e militares, análise de política, consenso Delphi e
um experimento com população não bombeira. Preservou resultados nulos e recusou usar a
simulação não ocupacional como evidência de bombeiros. Prosseguir pelo lote 06 em
`EV-0390`, com os mesmos controles. Os lotes 06-07 avançaram até `EV-0650`; preservaram
protocolos sem resultados, resultados nulos e limitações de população, e bloquearam
`EV-0534`, `EV-0616` e `EV-0640` por XML sem corpo. Prosseguir pelo lote 08 em `EV-0655`.
Dos 30 registros restantes, 22 têm corpo de artigo já validado e 8 aguardam fonte ou versão
com corpo completo. `PMC100_FULL_TEXT_APPRAISAL_COMPLETE`, saturação de referência,
v0.13 e aprovação científica permanecem bloqueados.
