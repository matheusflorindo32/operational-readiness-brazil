# Gate 2 — primeiro ciclo de adjudicação humana controlada

**Modo:** `CONTROLLED HUMAN ADJUDICATION — HIGH-RIGOR MODE`
**Status inicial obrigatório:** `AGUARDANDO ADJUDICAÇÃO HUMANA`
**Status após preparação:** `PILOT_READY`
**Verificação:** `2026-09-15T23:05:40-03:00`
**Limite:** preparação de um caso crítico e cinco casos-piloto; nenhuma decisão humana, importação ou Gate 3.

## Estado de entrada

- [x] Gate 1 revalidado: 10 vermelhos, 1.446 amarelos e zero verdes no XLSX e Google Sheets.
- [x] Commit auditado de referência: `cbd1643308f35f03ce5bff80beb755cb927ca46c`.
- [x] Estado publicado de entrada: `12e1fa06cb09a70bba81074fcca19e6f4b90b50e`; CI verde.
- [x] Fila existente: 18/18 dossiês, 18 PMIDs únicos e 18 Zotero keys únicas.
- [x] Campos humanos vazios em 18/18; Claim-Ready bloqueado em 18/18.
- [x] Zotero local disponível; API e Connector HTTP 200; biblioteca com 1.457 itens principais.
- [x] Master Evidence SHA-256 inicial: `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b`.

## Dossiê crítico — retração

- **ARTICLE PMID:** [PMID 26159007](https://pubmed.ncbi.nlm.nih.gov/26159007/)
- **ZOTERO KEY:** `9UE7LEZP`
- **TITLE:** Performance differences between male and female marines on standardized physical fitness tests and combat proxy tasks: identifying the gap.
- **AUTHORS:** Jason Jameson; Leon Pappa; Brian McGuire; Karen R Kelly
- **JOURNAL / YEAR / CURRENT STATUS:** US Army Med Dep J; 2015; `ppublish`; Retracted Publication.
- **DOI:** `NOT FOUND IN AUDITED SOURCE`
- **EDITORIAL RELATION:** `RetractionIn` → [PMID 26357708](https://pubmed.ncbi.nlm.nih.gov/26357708/) (`RetractionOf` recíproco no aviso).
- **PRIMARY SOURCES:** [PMID 26159007](https://pubmed.ncbi.nlm.nih.gov/26159007/) e [PMID 26357708](https://pubmed.ncbi.nlm.nih.gov/26357708/).
- **EVIDENCE / STATUS:** PubMed classifica o artigo como Retracted Publication e liga o aviso de retração.
- **IMPLICATION FOR REVIEW:** manter o registro na trilha, bloquear qualquer uso em claims e submeter a decisão ao revisor humano.
- **ASSISTED RECOMMENDATION:** `Confirmar bloqueio`.
- **CONFIDENCE:** alta para a relação bibliográfica; não aplicável à decisão humana.
- **SCIENTIFIC IMPACT NOT VERIFIED:** A motivação detalhada e o efeito sobre cada resultado não foram verificados além do registro e do aviso PubMed.
- **HUMAN REVIEWER:** *(vazio)*
- **HUMAN DATE:** *(vazio)*
- **HUMAN DECISION:** *(vazio — aguardando ação explícita de pessoa identificável)*
- **HUMAN JUSTIFICATION:** *(vazio)*
- **CLAIM-READY:** `NO / BLOQUEADO`.

A recomendação acima permanece separada da decisão humana. Não houve adjudicação humana nesta execução.

## Lote-piloto selecionado

| Ordem | Registro | Padrão coberto | DOI | Zotero key | Relação | Registro relacionado |
|---:|---|---|---|---|---|---|
| 1 | [PMID 42412865](https://pubmed.ncbi.nlm.nih.gov/42412865/) | piloto: ErratumFor com DOI e PMID relacionado | [10.1371/journal.pone.0353341](https://doi.org/10.1371/journal.pone.0353341) | `UR4UXGB5` | `ErratumFor` | [PMID 40299918](https://pubmed.ncbi.nlm.nih.gov/40299918/) |
| 2 | [PMID 37952191](https://pubmed.ncbi.nlm.nih.gov/37952191/) | piloto: ErratumIn com DOI e PMID relacionado | [10.1093/milmed/usad431](https://doi.org/10.1093/milmed/usad431) | `KXHMGT9N` | `ErratumIn` | [PMID 39846215](https://pubmed.ncbi.nlm.nih.gov/39846215/) |
| 3 | [PMID 42400068](https://pubmed.ncbi.nlm.nih.gov/42400068/) | piloto: UpdateOf (publicação atualiza preprint) | [10.1186/s13011-026-00746-1](https://doi.org/10.1186/s13011-026-00746-1) | `MRP2ZHSP` | `UpdateOf` | [PMID 41646313](https://pubmed.ncbi.nlm.nih.gov/41646313/) |
| 4 | [PMID 32908996](https://pubmed.ncbi.nlm.nih.gov/32908996/) | piloto: UpdateIn (preprint atualizado por publicação) | [10.1101/2020.08.31.20185140](https://doi.org/10.1101/2020.08.31.20185140) | `XHQD4258` | `UpdateIn` | [PMID 33332151](https://pubmed.ncbi.nlm.nih.gov/33332151/) |
| 5 | [PMID 15460628](https://pubmed.ncbi.nlm.nih.gov/15460628/) | piloto: DOI ausente e PMID do aviso ausente | `NOT FOUND IN AUDITED SOURCE` | `Q3MG2N6N` | `ErratumIn` | `NOT FOUND` |

O conjunto cobre `ErratumFor`, `ErratumIn`, `UpdateOf`, `UpdateIn`, DOI ausente e aviso sem PMID usando cinco registros. O último caso cobre simultaneamente as duas ausências, sem inventar identificadores.

## Dossiês do piloto

### [PMID 42412865](https://pubmed.ncbi.nlm.nih.gov/42412865/) — `ErratumFor`

- **ARTICLE PMID / ZOTERO KEY:** [PMID 42412865](https://pubmed.ncbi.nlm.nih.gov/42412865/) / `UR4UXGB5`
- **TITLE:** Correction: Salivary biomarkers of tactical athlete readiness: A systematic review.
- **CURRENT STATUS:** `epublish`; Published Erratum.
- **EDITORIAL RELATION:** `ErratumFor`
- **RELATED PMID / DOI / TITLE:** [PMID 40299918](https://pubmed.ncbi.nlm.nih.gov/40299918/) / [10.1371/journal.pone.0321223](https://doi.org/10.1371/journal.pone.0321223) / Salivary biomarkers of tactical athlete readiness: A systematic review.
- **PRIMARY SOURCE:** [PMID 42412865](https://pubmed.ncbi.nlm.nih.gov/42412865/); related source [PMID 40299918](https://pubmed.ncbi.nlm.nih.gov/40299918/).
- **SECONDARY SOURCE:** não usada para determinar impacto científico.
- **WHAT CHANGED:** NOT VERIFIED from the available primary metadata; requires comparison of the editorial notice/full texts.
- **SCIENTIFIC IMPACT KNOWN:** PubMed registra Published Erratum/ErratumFor e identifica o artigo corrigido.
- **SCIENTIFIC IMPACT NOT VERIFIED:** O impacto da correção sobre dados, métodos, resultados e conclusões ainda não foi verificado no texto editorial completo.
- **ASSISTED RECOMMENDATION / CONFIDENCE / REASON:** `Investigar relação editorial` / alta para a relação bibliográfica; não aplicável à decisão humana / O registro é uma correção do PMID 40299918; deve ser vinculado ao artigo corrigido sem ser tratado como evidência independente.
- **HUMAN REVIEWER / DATE / DECISION / JUSTIFICATION:** *(todos vazios)*
- **CLAIM-READY:** `NO / BLOQUEADO`.

### [PMID 37952191](https://pubmed.ncbi.nlm.nih.gov/37952191/) — `ErratumIn`

- **ARTICLE PMID / ZOTERO KEY:** [PMID 37952191](https://pubmed.ncbi.nlm.nih.gov/37952191/) / `KXHMGT9N`
- **TITLE:** Nasal Decolonization in Congregant Settings: Reducing Infection Spread, Cutting Costs, and Improving Operational Readiness.
- **CURRENT STATUS:** `ppublish`; Journal Article.
- **EDITORIAL RELATION:** `ErratumIn`
- **RELATED PMID / DOI / TITLE:** [PMID 39846215](https://pubmed.ncbi.nlm.nih.gov/39846215/) / [10.1093/milmed/usaf019](https://doi.org/10.1093/milmed/usaf019) / Correction To: Nasal Decolonization in Congregant Settings: Reducing Infection Spread, Cutting Costs, and Improving Operational Readiness.
- **PRIMARY SOURCE:** [PMID 37952191](https://pubmed.ncbi.nlm.nih.gov/37952191/); related source [PMID 39846215](https://pubmed.ncbi.nlm.nih.gov/39846215/).
- **SECONDARY SOURCE:** não usada para determinar impacto científico.
- **WHAT CHANGED:** NOT VERIFIED from the available primary metadata; requires comparison of the editorial notice/full texts.
- **SCIENTIFIC IMPACT KNOWN:** PubMed registra ErratumIn e identifica aviso posterior com DOI e PMID.
- **SCIENTIFIC IMPACT NOT VERIFIED:** O conteúdo exato da correção e seu impacto científico ainda não foram verificados no texto editorial completo.
- **ASSISTED RECOMMENDATION / CONFIDENCE / REASON:** `Investigar relação editorial` / alta para a relação bibliográfica; não aplicável à decisão humana / PubMed informa correção posterior no PMID 39846215; conteúdo, metadados ou interpretação podem ter sido alterados.
- **HUMAN REVIEWER / DATE / DECISION / JUSTIFICATION:** *(todos vazios)*
- **CLAIM-READY:** `NO / BLOQUEADO`.

### [PMID 42400068](https://pubmed.ncbi.nlm.nih.gov/42400068/) — `UpdateOf`

- **ARTICLE PMID / ZOTERO KEY:** [PMID 42400068](https://pubmed.ncbi.nlm.nih.gov/42400068/) / `MRP2ZHSP`
- **TITLE:** Perspectives on harm reduction kit implementation in heterogeneous outpatient clinics.
- **CURRENT STATUS:** `aheadofprint`; Journal Article.
- **EDITORIAL RELATION:** `UpdateOf`
- **RELATED PMID / DOI / TITLE:** [PMID 41646313](https://pubmed.ncbi.nlm.nih.gov/41646313/) / [10.21203/rs.3.rs-6059606/v1](https://doi.org/10.21203/rs.3.rs-6059606/v1) / Perspectives on Harm Reduction Kit Implementation in Heterogeneous Outpatient Clinics.
- **PRIMARY SOURCE:** [PMID 42400068](https://pubmed.ncbi.nlm.nih.gov/42400068/); related source [PMID 41646313](https://pubmed.ncbi.nlm.nih.gov/41646313/).
- **SECONDARY SOURCE:** não usada para determinar impacto científico.
- **WHAT CHANGED:** NOT VERIFIED from the available primary metadata; requires comparison of the editorial notice/full texts.
- **SCIENTIFIC IMPACT KNOWN:** PubMed registra UpdateOf e liga a publicação ao preprint anterior.
- **SCIENTIFIC IMPACT NOT VERIFIED:** Diferenças de dados, métodos, resultados e conclusões entre as versões ainda não foram verificadas integralmente.
- **ASSISTED RECOMMENDATION / CONFIDENCE / REASON:** `Investigar relação editorial` / alta para a relação bibliográfica; não aplicável à decisão humana / O registro atualiza o preprint PMID 41646313; é necessário confirmar a versão de registro e evitar dupla contagem.
- **HUMAN REVIEWER / DATE / DECISION / JUSTIFICATION:** *(todos vazios)*
- **CLAIM-READY:** `NO / BLOQUEADO`.

### [PMID 32908996](https://pubmed.ncbi.nlm.nih.gov/32908996/) — `UpdateIn`

- **ARTICLE PMID / ZOTERO KEY:** [PMID 32908996](https://pubmed.ncbi.nlm.nih.gov/32908996/) / `XHQD4258`
- **TITLE:** COVID-19 Myocardial Pathology Evaluated Through scrEening Cardiac Magnetic Resonance (COMPETE CMR).
- **CURRENT STATUS:** `epublish`; Preprint; Journal Article.
- **EDITORIAL RELATION:** `UpdateIn`
- **RELATED PMID / DOI / TITLE:** [PMID 33332151](https://pubmed.ncbi.nlm.nih.gov/33332151/) / [10.1161/CIRCULATIONAHA.120.052573](https://doi.org/10.1161/CIRCULATIONAHA.120.052573) / COVID-19 Myocardial Pathology Evaluation in Athletes With Cardiac Magnetic Resonance (COMPETE CMR).
- **PRIMARY SOURCE:** [PMID 32908996](https://pubmed.ncbi.nlm.nih.gov/32908996/); related source [PMID 33332151](https://pubmed.ncbi.nlm.nih.gov/33332151/).
- **SECONDARY SOURCE:** não usada para determinar impacto científico.
- **WHAT CHANGED:** NOT VERIFIED from the available primary metadata; requires comparison of the editorial notice/full texts.
- **SCIENTIFIC IMPACT KNOWN:** PubMed registra UpdateIn e liga o preprint à versão publicada.
- **SCIENTIFIC IMPACT NOT VERIFIED:** Diferenças de dados, métodos, resultados e conclusões entre as versões ainda não foram verificadas integralmente.
- **ASSISTED RECOMMENDATION / CONFIDENCE / REASON:** `Investigar relação editorial` / alta para a relação bibliográfica; não aplicável à decisão humana / O registro foi atualizado pelo PMID 33332151; a versão publicada deve ser examinada antes de decidir sobre o registro anterior.
- **HUMAN REVIEWER / DATE / DECISION / JUSTIFICATION:** *(todos vazios)*
- **CLAIM-READY:** `NO / BLOQUEADO`.

### [PMID 15460628](https://pubmed.ncbi.nlm.nih.gov/15460628/) — `ErratumIn`

- **ARTICLE PMID / ZOTERO KEY:** [PMID 15460628](https://pubmed.ncbi.nlm.nih.gov/15460628/) / `Q3MG2N6N`
- **TITLE:** Caffeine restores engagement speed but not shooting precision following 22 h of active wakefulness.
- **CURRENT STATUS:** `ppublish`; Clinical Trial; Controlled Clinical Trial; Journal Article.
- **EDITORIAL RELATION:** `ErratumIn`
- **RELATED PMID / DOI / TITLE:** `NOT FOUND` / `NOT FOUND IN AUDITED SOURCE` / NOT FOUND
- **PRIMARY SOURCE:** [PMID 15460628](https://pubmed.ncbi.nlm.nih.gov/15460628/).
- **SECONDARY SOURCE:** não usada para determinar impacto científico.
- **WHAT CHANGED:** NOT VERIFIED from the available primary metadata; requires comparison of the editorial notice/full texts.
- **SCIENTIFIC IMPACT KNOWN:** PubMed registra ErratumIn e fornece a citação bibliográfica do aviso.
- **SCIENTIFIC IMPACT NOT VERIFIED:** O aviso não tem PMID no registro auditado; DOI, texto do aviso e impacto científico não foram localizados nesta etapa.
- **ASSISTED RECOMMENDATION / CONFIDENCE / REASON:** `Investigar relação editorial` / alta para a relação bibliográfica; não aplicável à decisão humana / PubMed informa correção posterior sem PMID relacionado; localizar o aviso editorial no periódico antes de qualquer uso.
- **HUMAN REVIEWER / DATE / DECISION / JUSTIFICATION:** *(todos vazios)*
- **CLAIM-READY:** `NO / BLOQUEADO`.

## QC intermediário dos dados preparados

| Controle | Resultado |
|---|---:|
| Fontes PubMed atuais consultadas para 6/6 | PASS |
| Relações editoriais preservadas em 6/6 | PASS |
| Recomendação assistida separada da decisão humana em 6/6 | PASS |
| Claim-Ready bloqueado em 6/6 | PASS |
| PMIDs únicos em 6/6 | PASS |
| Zotero keys únicas em 6/6 | PASS |
| DOI ausente explicitamente registrado | PASS |
| PMID de aviso ausente explicitamente registrado | PASS |
| Reviewer humano preenchido | 0/6 — pendente |
| Data humana preenchida | 0/6 — pendente |
| Decisão humana preenchida | 0/6 — pendente |
| Justificativa humana preenchida | 0/6 — pendente |
| Importação executada | 0/1 — não autorizada nesta etapa |
| Gate 3 iniciado | 0/1 — proibido nesta etapa |

Os campos humanos vazios são o estado correto antes da ação do revisor. O QC de adjudicação não pode passar e os 12 casos restantes não podem avançar até o piloto receber seis decisões humanas completas e passar por novo QC.

## Testes e trilha de auditoria

- [x] Controles `T-G2-001` a `T-G2-015` materializados como testes fail-closed.
- [x] XML PubMed da consulta atual preservado e hasheado.
- [x] Inventário Zotero e Master Evidence comparados antes/depois em modo somente leitura.
- [x] Nenhuma mutação em Zotero, Master Evidence ou planilha canônica.
- [x] Nenhum merge, reimportação, exclusão física ou alteração de `FXC7ZY9R`.

Arquivos de auditoria: `reporting/adjudication/2026-09-15/first-cycle-high-rigor.json`, `first-cycle-pilot-queue.csv` e `pubmed-first-cycle-2026-09-15.xml`.

## Métricas separadas

- **Preparation:** 6/6 dossiês deste ciclo preparados (100,00%); fila prioritária total permanece 18/18 preparada.
- **Human adjudication:** 0/18 (0,00%); piloto 0/6 (0,00%).
- **QC dos dados preparados:** 15/15 controles implementados; 15/15 passaram; a suíte local completa passou 38/38 e a comparação pós-leitura confirmou zero alterações.
- **Import:** 0/18 (0,00%).
- **Claim-Ready:** 0/1.456 (0,00%).

## Decisão e próxima ação

**Decisão:** `PILOT_READY`. Isto não significa aprovação científica nem conclusão do Gate 2.

**NEXT MINIMUM ACTION:** `HUMAN REVIEW — ADJUDICATE PMID 26159007`.
