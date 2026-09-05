# PubMed A/B/C — auditoria estrutural de publicação

## Escopo e resultado local

Auditoria posterior à importação, sobre o baseline pré-execução
`912db0a4d3d6b9551fba228cd94d797b46370c50`, confirmado em `main` local e remoto
antes das alterações desta rodada. Os 44 controles locais passaram.
**Reconciliação estrutural: 1.456/1.456.** Este resultado não significa
verificação científica individual dos metadados, integridade das fontes,
elegibilidade ou prontidão para sustentar afirmações. Triagem: **0/1.456**.

`PUBMED PASS` depende adicionalmente da publicação das correções, igualdade do
commit local/remoto e CI bem-sucedida nesse commit. O resultado da publicação
deve ser consultado no histórico de commits e na execução da CI correspondente;
o JSON local não se apresenta como prova de publicação.

## Controles executados

A skill Zotero 0.1.2 foi utilizada para reexecutar `status --json`,
`inventory --json`, `collections --json` e `tags --json`. As consultas diretas
de itens foram somente GET, paginadas, na API local.

| Superfície | Resultado observado |
|---|---|
| API / Connector | HTTP 200 / HTTP 200; Zotero 10.0.1 |
| Biblioteca, itens principais | 1.457; conjunto de produção mais FXC7ZY9R |
| Raiz PE9UF4YN | 1.456 itens, 1.456 keys únicas |
| Coleção controlada EMHHKNTM | Somente FXC7ZY9R |
| RIS de entrada | 1.456 registros completos, 1.456 PMIDs únicos |
| Rollback manifest | 1.456 keys únicas, conjunto idêntico à produção |
| RIS final | 1.456 registros, mesmo conjunto de PMIDs |
| BibTeX final | 1.456 registros, 1.456 citation keys distintas, mesmo conjunto de PMIDs |
| Master Evidence | 1.456 linhas contíguas, 1.456 keys únicas e preenchidas |
| Correspondência linha a linha | Cada PMID da planilha aponta para a respectiva key real do Zotero |
| PMID 37415704 | Produção 8XVBQIYE no Zotero e na planilha |
| Exclusão controlada | FXC7ZY9R fora da raiz, manifesto e coluna de keys da planilha |
| Exportações finais | Sem FXC7ZY9R; identidade bibliográfica reconciliada com a produção |
| Triagem / verificação individual | Não iniciada / pendente |

As menções a FXC7ZY9R em notas de auditoria são explicações da exclusão, não
linhas de evidência. RIS/BibTeX não carregam necessariamente a Zotero item key:
a exclusão foi conferida também pelo conjunto de produção e por PMID/DOI/título.

## Controle bibliográfico estrutural

Fonte de comparação: metadados PubMed A/B/C preservados em 2026-08-28.
Comparação por PMID, DOI normalizado, título normalizado e ano: **zero
divergências** entre os metadados, RIS original, Zotero, RIS final, BibTeX e
Master Evidence. Não foram consultadas ou avaliadas individualmente as fontes.

- 1.456 PMIDs preenchidos e distintos; nenhum PMID duplicado na produção.
- 1.300 DOIs preenchidos, sintaticamente válidos e distintos. Os 156 vazios
  também estão vazios na fonte; nenhum identificador foi inventado.
- Títulos, anos e tipos documentais preenchidos nos 1.456 registros.
- Dois grupos por título normalizado, preservados sem merge:

| PMIDs | Anos | Distinção estrutural |
|---|---|---|
| 38280817 / 36368814 | 2024 / 2023 | DOIs 10.1016/j.ccep.2023.09.010 / 10.1016/j.ccl.2022.08.008 |
| 33721322 / 11469036 | 2021 / 2001 | DOI 10.55460/j774-n297 / DOI ausente na fonte |

Esses candidatos por título não são o grupo da interface nativa. A igualdade
de título não autoriza deduplicação automática nem conclui equivalência científica.

Tipos documentais: a conversão existente utiliza `JOUR` no RIS,
`journalArticle` no Zotero e `article` no BibTeX para todos os registros. A
planilha preserva integralmente as categorias PubMed, inclusive 35 registros
sem a categoria `Journal Article`. Portanto, a representação genérica do Zotero
não comprova o tipo documental individual. Entre os rótulos já existentes na
fonte estão `Retracted Publication` (1), `Published Erratum` (3), `Preprint` (3),
`Book` (3) e `Book Chapter` (6). São rótulos importados, não novas decisões
de integridade, exclusão ou triagem. A verificação individual continua pendente.

Os hashes em `audit.json` distinguem bytes locais (`sha256`) e representação
canônica LF (`sha256_lf`). A exportação RIS local contém CRLF; `.gitattributes`
normaliza RIS/BibTeX no Git para LF. A diferença de bytes não altera os 1.456
registros e é auditada explicitamente contra o blob preparado para publicação.

## Grupo controlado e auditoria nativa

O arquivo `12-native-duplicate-audit.json`, de 2026-09-03, registra um grupo:
**FXC7ZY9R / 8XVBQIYE — DO NOT MERGE**. Esse registro foi auditado diretamente.
A interface nativa não foi reaberta nesta rodada; a API atual confirmou as
duas identidades por DOI/título, keys e coleções. Não se apresenta a comparação
por API como nova execução da interface nativa.

FXC7ZY9R permanece somente em EMHHKNTM, com 32 tags e quatro objetos filhos.
O diagnóstico preservado registra duas notas e dois anexos. O item controlado
não armazena PMID no campo Extra: a ligação ao PMID 37415704 decorre do DOI e
título correspondentes ao registro de produção 8XVBQIYE. Nenhum merge ocorreu.

## Backups e rastreabilidade

Os 15 arquivos do backup externo corresponderam aos tamanhos e SHA-256 do
manifesto. O `zotero-before.sqlite` válido tem **5.013.504 bytes**, hash
`e4243178e4c7d50a35aaae24d7b0ad2fd148e67189adf4764ea4e5da08ce02b4`,
`integrity_check = ok`, 59 tabelas e seis linhas em `items`, incluindo FXC7ZY9R.
A conexão foi aberta somente para leitura. Nenhum banco ou conteúdo de anexo
foi copiado para a publicação.

O conjunto publicável exclui SQLite válido ou inválido/vazio, bancos Zotero,
snapshots privados em `before/`, anexos, credenciais e arquivos temporários.
Não foi encontrado SQLite no workspace; o backup verificado permanece externo.
Os manifests e diagnósticos preservados continuam como evidência histórica.
Os dez JSON da execução anterior foram lidos e validados sintaticamente.

A resposta original do POST de importação não foi capturada após expirar a
sessão de execução. Essa lacuna histórica permanece explícita e não foi
reconstruída. A evidência de conclusão é a reconciliação do estado posterior.

## Planilha e documentação

- `README!B11`: `baseline pré-execução 912db0a4d3d6b9551fba228cd94d797b46370c50`.
- `Search Provenance!A2`: `PubMed A/B/C foi executado, importado e reconciliado; triagem científica ainda não iniciada.`

As duas células foram editadas com Artifact Tool. Para preservar exatamente o
pacote original, somente as duas células geradas foram transferidas ao XLSX
original. A comparação do pacote confirma que os demais conteúdos, fórmulas,
estilos, validações e objetos permaneceram inalterados. A busca por erros de
fórmula retornou zero ocorrências. O hash atual da planilha está em `audit.json`;
o hash de 2026-09-03 permanece como histórico do arquivo anterior.

README, checklist, changelog e relatórios foram atualizados. O auditor é
somente leitura para Zotero, usa a biblioteca padrão do Python e não requer
variáveis de ambiente, credenciais ou migrations. A CI inclui testes dos parsers.
O limite pre-commit de 2 MB possui exceção somente para os dois exports finais
nomeados, que têm aproximadamente 3,3 MB cada.

## Evidências e reprodução

- `reporting/zotero-runs/2026-09-05-structural-audit/audit.json`: 44 controles, contagens, diferenças, tipos e hashes.
- `reporting/zotero-runs/2026-09-05-structural-audit/production-identifiers.json`: mapa PMID/DOI/título/ano/key de produção.
- `reporting/zotero-runs/2026-09-05-structural-audit/status.json`, `inventory.json`, `collections.json`, `tags.json`: nova execução da skill.
- `reporting/zotero-runs/2026-09-05-structural-audit/workbook-preservation.json`: escopo exato e hashes da edição.
- `reporting/zotero-runs/2026-09-02T13-40-38-0300/`: manifests e diagnósticos históricos publicáveis.

```text
python analysis/audit_pubmed_structure.py --helper "<installed Zotero skill>/scripts/zotero.py"
python -m unittest discover -s analysis -p "test_*.py"
```

O auditor retorna código 1 quando um controle registrado falha e também
interrompe com erro diante de falhas de leitura ou parse. Nenhum resultado local
autoriza merge ou início de triagem.
