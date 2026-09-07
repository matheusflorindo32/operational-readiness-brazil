# Triagem controlada por título e resumo — 2026-09-07

## Decisão

**GO somente para adjudicação humana e obtenção/leitura lícita de texto
completo.** A triagem primária assistida por IA cobre 1.456/1.456 registros, mas
não constitui seleção PRISMA, aprovação científica, avaliação metodológica,
síntese de evidência ou autorização de claim. Claim-Ready permanece 0/1.456.

## Escopo e referência

- Commit auditado de entrada: `ae25ad9054193f8ac3be82061f6fe7906d989ec9`.
- Protocolo vigente: ensaio científico conceitual e aplicado, com identificação
  estruturada de evidências.
- Rubrica prospectiva: `docs/TITLE_ABSTRACT_SCREENING_RUBRIC_2026-09-07.md`;
  amendment A-002 registrado antes da classificação de produção.
- Fonte de triagem: título, resumo, tipos documentais e
  `CommentsCorrectionsList` recuperados individualmente por PMID via NCBI Entrez
  EFetch em 2026-09-07.
- Revisor registrado: `OpenAI Codex — AI-assisted primary screen`; confirmação
  humana permanece obrigatória para todas as decisões.

## Resultado com denominadores

| Resultado | n/denominador | Percentual |
|---|---:|---:|
| Registros classificados no passe primário | 1.456/1.456 | 100,00% |
| `INCLUDE_FULL_TEXT` | 1.206/1.456 | 82,83% |
| `EXCLUDE_TITLE_ABSTRACT` | 9/1.456 | 0,62% |
| `PENDING_ADJUDICATION` | 240/1.456 | 16,48% |
| `BLOCKED_INTEGRITY` | 1/1.456 | 0,07% |
| União prioritária triada | 159/159 | 100,00% |
| DOI ausentes na fonte reconfirmados ausentes | 156/156 | 100,00% |
| DOI ausentes resolvidos | 0/156 | 0,00% |
| Comparação de metadados sem divergência | 1.366/1.456 | 93,82% |
| Comparação de identificadores sem divergência | 1.454/1.456 | 99,86% |
| Campos de integridade do PubMed examinados | 1.456/1.456 | 100,00% |
| Confirmação humana | 0/1.456 | 0,00% |
| Avaliação de qualidade/risco de viés | 0/1.456 | 0,00% |
| Claim-Ready | 0/1.456 | 0,00% |

Os 1.206 registros retidos são candidatos à leitura integral. Eles não são
artigos cientificamente “incluídos” em uma revisão nem evidência sintetizada. As
9 exclusões propostas também aguardam confirmação humana.

## Prioridades e integridade

O PMID `26159007` é identificado pelo registro corrente como `Retracted
Publication` e aponta para o aviso de retração PMID `26357708`. A linha foi
preservada, recebeu `BLOCKED_INTEGRITY`, `Not used`, URL do aviso e a limitação
explícita de que o artigo não pode sustentar conclusão científica no projeto.

Os 156 registros sem DOI foram consultados individualmente; nenhum DOI novo foi
retornado pelo EFetch. A ausência foi registrada, sem inferência ou preenchimento
por título. Dois DOI preservados de registros de livro/fonte não aparecem na
representação EFetch corrente: PMID `25121201` (`10.17226/5257`) e PMID
`24851287` (`10.17226/13380`). Permanecem pendentes de adjudicação de fonte.

Há 17 registros com errata/correção/atualização que exigem leitura humana da
relação editorial antes do uso. Os demais vínculos como comentário não foram
convertidos automaticamente em problema de integridade.

## Metadados e duplicidades

Todos os 1.456 registros tiveram PMID, título normalizado, autores, periódico ou
fonte, ano, DOI, tipo documental, URL PubMed e relações editoriais comparados
programaticamente com o registro preservado. A recuperação EFetch confirmou a
existência individual de cada PMID e fundamenta a URL gravada. Isso é controle
bibliográfico individual automatizado, não validação científica humana.

Foram registradas 90 divergências para revisão: 88 representações de lista de
autores, uma fonte/periódico (PMID `25610940`) e um ano (PMID `40198226`, fonte
preservada 2025 versus PubMed corrente 2026). Nenhum valor divergente foi
silenciosamente sobrescrito.

Os dois grupos por título permanecem separados:

- PMID `38280817`, DOI `10.1016/j.ccep.2023.09.010`, 2024, e PMID `36368814`,
  DOI `10.1016/j.ccl.2022.08.008`, 2023;
- PMID `33721322`, DOI `10.55460/j774-n297`, 2021, e PMID `11469036`, sem DOI,
  2001.

Os quatro têm identidades bibliográficas distintas e foram retidos para texto
completo. Decisão: `DO NOT MERGE`, até revisão humana da história de publicação.

## Master Evidence e testes

Cada uma das 1.456 linhas contém decisão, motivo, revisor assistido por IA, data,
fonte, próximo passo, estado de metadados/identificadores/integridade e “What
this article does NOT allow us to claim”. Os campos de data/revisor de análise
humana continuam vazios. O Dashboard mostra 1.366 metadados reconciliados, 1.456
checagens de integridade, 1.446 amarelos, 10 vermelhos, 1.456 `Analysis pending`
e zero Claim-Ready.

Validações executadas:

- cinco testes unitários da rubrica, incluindo retração, errata, registro sem
  resumo, inclusão contextual e exclusão negativa;
- comparação célula a célula contra o XLSX pré-triagem: nenhuma mudança fora dos
  campos autorizados;
- preservação de 14 planilhas, 10 tabelas, dois gráficos, painéis congelados,
  fórmulas e 1.456 tripletas Evidence ID–PMID–Zotero key;
- varredura de erros de fórmula com zero ocorrências;
- cenários negativos para retração, correção, ausência de resumo, pares por
  título, Claim-Ready e campos humanos;
- teste integral em cópia nativa descartável do Google Sheets, seguido de
  exclusão da cópia de teste;
- comparação funcional XLSX/Google Sheets em 1.456/1.456 identidades e nas
  contagens de decisão, metadados, identificadores, integridade, semáforo,
  Claim-Ready e campos humanos.

## Zotero, backups e Drive

O auditor estrutural passou 44/44 controles antes e depois. Os JSON de status,
coleções, tags, inventário e identificadores são byte a byte idênticos entre as
duas leituras: API/Connector HTTP 200; `PE9UF4YN` com 1.456 itens; `EMHHKNTM`
somente com `FXC7ZY9R`; biblioteca com 1.457 itens principais. O PMID `37415704`
continua em produção como `8XVBQIYE`. Nenhuma importação, alteração de coleção,
tag, anexo ou merge ocorreu.

O backup XLSX pré-triagem tem SHA-256
`e8a751ba0f455a8453a27c11b8fc1d3aeb003adad942e063d1eb4422b1d130d8`.
Os XML EFetch, inventários completos, decisões detalhadas e valores usados na
sincronização ficam fora do Git, sob o diretório de backup registrado em
`reporting/screening/2026-09-07/run-manifest.json`. O ledger compacto por artigo
permanece versionado.

A planilha nativa canônica mantém o ID
`1X6MerTU2oZYup6LMI0SVBxFg3FcH_smstrBOf_wSRDM`, a pasta `04_EXTRACAO` e a
permissão privada somente do proprietário. O backup nativo pré-triagem
`1LREN6gUfMgllEd7g0IKWKQmZrAe2wMmIfivCG4o5teg` foi preservado em `10_ARQUIVO`.
O snapshot XLSX atual é `1MnfmkDR8cuQGKz3nvT5i9O7rcyXyJdlS`; cópias
históricas não foram sobrescritas.

## Riscos, pendências e próxima ação exata

- O passe primário é assistido por IA e exige confirmação humana de 1.456/1.456
  decisões.
- Priorizar a adjudicação do bloqueio por retração, dos 17 vínculos de
  correção/atualização, das 90 divergências de metadados, dos dois conflitos de
  DOI e dos 240 casos pendentes.
- Depois, obter licitamente e ler o texto completo dos 1.206 candidatos retidos,
  escolher instrumento de avaliação compatível com cada desenho e registrar
  resultado/localização precisa antes de qualquer Claim-Ready.
- As buscas nas demais bases e literatura brasileira continuam pendentes; os
  percentuais administrativos permanecem 52/74 (70,27%) no geral e 3/14
  (21,43%) na identificação.

Próxima ação exata: iniciar segunda revisão humana pelas 18 linhas de maior risco
editorial (uma retração bloqueada + 17 correções/atualizações), registrar
concordância/conflito e adjudicação, e então revisar as 90 divergências de
metadados antes da fila geral de 240 pendências e da leitura integral.
