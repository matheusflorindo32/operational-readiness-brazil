# Fechamento operacional PubMed — 2026-09-06

## Escopo e referência

Referência auditada: `8560422f8b16560d4d9aa5f849421c09247799f5`.
Checkout inicialmente limpo; HEAD e main remoto coincidiam com essa referência.
Foi lida integralmente a [auditoria fornecida](https://drive.google.com/file/d/1a7-f5R9BP5brFfOCIcYMHeFNoqUg05GD/view), juntamente com protocolo, checklist e plano Zotero.
As skills Zotero e Spreadsheets foram aplicadas. Não houve reimportação, merge,
triagem, exclusão bibliográfica ou verificação científica individual.

## Controles e resultados

| Controle | Resultado e denominador |
|---|---|
| Auditor estrutural ao final | 44/44, 100% |
| RIS de entrada, Zotero, manifesto, RIS/BibTeX e Master Evidence | 1.456/1.456 em cada conjunto, 100% |
| Evidence ID ↔ PMID ↔ Zotero key preservados | 1.456/1.456, 100% |
| Paridade dos resultados C/EB/EC XLSX e Sheets | 1.456/1.456 linhas, 100% |
| Cenários funcionais XLSX / Sheets | 24/24 em cada motor, 100% |
| DOI presente na fonte | 1.300/1.456, 89,29%; ausente 156/1.456, 10,71% |
| Triagem científica | 0/1.456, 0% |
| Claims aprovados | 0/1.456, 0% |
| Analysis pending | 1.456/1.456, 100% |

O Zotero Desktop 10.0.1 respondeu HTTP 200 na API e no Connector. Foram
reexecutados `status --json`, `inventory --json`, `collections --json` e `tags --json`.
A biblioteca local correta contém 1.457 itens principais: 1.456 na raiz
`PE9UF4YN` e somente `FXC7ZY9R` na coleção controlada `EMHHKNTM`.
PMID `37415704` permanece associado à produção `8XVBQIYE`.
O grupo nativo documentado historicamente é `FXC7ZY9R` versus `8XVBQIYE`:
**DO NOT MERGE**. As identidades e associações foram reconfirmadas pela API;
não se afirma nova abertura da interface nativa de duplicados nesta execução.

Não houve divergências estruturais de PMID, DOI, título ou ano entre os conjuntos.
Permanecem dois pares candidatos por título com PMIDs/anos distintos, sem merge.
Os 35 registros de tipos diferentes de Journal Article conservam o tipo PubMed
original; a representação bibliográfica genérica JOUR não equivale à validação
individual do tipo documental. Os 156 DOI ausentes não foram inventados.

## Correções realizadas

O motivo calculado em EC controla conjuntamente Claim-Ready, semáforo e Dashboard.
Retração, expressão de preocupação e restrições de integridade impedem aprovação.
Integridade pendente, resultado ausente, localização da fonte ausente, avaliação
metodológica pendente ou revisão humana não documentada também impedem aprovação.
Datas, revisor, claim específico, resultado e página/seção ou tabela/figura são
exigidos; preenchimentos genéricos e espaços não satisfazem a revisão humana.
As regras completas e conservadoras estão em [PREANALYSIS_RULES.md](PREANALYSIS_RULES.md).

O sinal **importado** `Retracted Publication` do PMID `26159007`, EV-1171,
key `9UE7LEZP`, agora produz alerta vermelho e prioridade crítica. A linha foi
preservada. Isso não declara leitura do aviso de retração nem verificação individual.

Os 1.456 Evidence IDs passaram de fórmulas dependentes de ROW para valores estáveis.
As sete dimensões de transferência aceitam somente inteiros 0/1/2; a fórmula também
recusa valores inválidos colados, mesmo se a validação de entrada for contornada.
Cinco tabelas operacionais congelam as três linhas de cabeçalho. O indicador
Analysis pending usa total identificado menos datas de análise positivas e retorna
1.456 nos dois formatos. O contador de alertas vermelhos passou a contar EC
`BLOCKED — integrity or use restriction` por igualdade exata, eliminando divergência de cálculo de curingas no XLSX:
Na revalidação documental de 2026-09-15, após a triagem assistida, o estado
canônico passou a **10 vermelhos, 1.446 amarelos e zero verdes** em ambos os
formatos: a retração e as nove propostas de exclusão permanecem bloqueadas para
uso, e os demais registros continuam em cautela. Esta nota substitui a contagem
transitória desta seção como referência de status atual.
Foram preservados 14 abas, 10 tabelas e 2 gráficos no XLSX.
Os rótulos de família primária B/C distinguem 385/191 linhas dos retornos 391/194
das buscas, que têm sobreposição. O baseline histórico pré-execução continua
`912db0a4d3d6b9551fba228cd94d797b46370c50`; Search Provenance continua informando
PubMed A/B/C executado, importado e reconciliado, com triagem não iniciada.

## Backups e testes

Antes das alterações, foram preservados XLSX, mapa CSV e snapshot SQLite fora do
Git. O backup SQLite online ficou bloqueado e foi interrompido; o arquivo vazio
resultante é inválido e não foi usado. O snapshot alternativo copiou DB/WAL somente
com hashes estáveis antes, durante e depois da cópia. Recuperação ocorreu apenas
na cópia, seguida de `integrity_check=ok`, 1.457 itens principais e inclusão das
1.456 keys. O manifesto registra hashes e tamanhos; DB, WAL/SHM, anexos e arquivos
temporários não são versionados. O script recusa sobrescrever o backup já registrado.

Os 24 cenários sintéticos foram executados em cópias descartáveis, com cálculo real
do Artifact Tool para XLSX e do Google Sheets nativo. Incluem controles positivos,
claim manual sem rastreabilidade, retração, expressão de preocupação, sinal importado,
correção não resolvida, identificadores não verificados, ausência de resultado,
fonte, revisor ou data, texto pendente/espaços, avaliação metodológica pendente,
limitação genérica, restrição de segurança e escala decimal/negativa/acima de 2/vazia.
Ordenação decrescente por PMID e inserção de linha na cópia Sheets preservaram
1.456/1.456 associações. Nenhum dado sintético foi gravado na versão canônica.
Os testes automatizados de regressão verificam o contrato do arquivo publicado.

## Drive e autoridade

A [planilha canônica](https://docs.google.com/spreadsheets/d/1X6MerTU2oZYup6LMI0SVBxFg3FcH_smstrBOf_wSRDM/edit)
foi atualizada no mesmo ID e movida para `04_EXTRACAO`. A releitura confirmou as
mesmas permissões e ausência de compartilhamento público. O conector funcionou;
um limite temporário de quota na criação da cópia foi resolvido por nova tentativa.
A [cópia anterior](https://docs.google.com/spreadsheets/d/1C75aNKQPWVt4SRoKs0uaRo41p3Q78RMmMVBlxdW3KZM/edit)
está preservada em `10_ARQUIVO`. Um snapshot XLSX versionado foi enviado a
`04_EXTRACAO` sob ID `1igS_nn-bUFP2WTUdgaHdIMbMH3xIPVFV`.
Consulte [o índice de autoridade](../drive/CANONICAL_VERSION_INDEX.md).

## Limites, histórico e decisão

O checklist administrativo permanece 52/74 (70,27%): protocolo 12/12,
infraestrutura 16/18, teste histórico Zotero 21/21, identificação 3/14 e síntese 0/9.
Esses percentuais não representam aprovação científica. As marcações antigas de
OSF registram o histórico informado; URL pública da inscrição e DOI continuam
pendentes de verificação independente. As abas auxiliares têm capacidade inicial
500/200 linhas, não representam registros ausentes e devem ser expandidas conforme
o procedimento documentado antes do uso além desses limites.

Os controles locais e a sincronização canônica estão aprovados. **PUBMED PASS é
restrito à identificação/importação e às correções operacionais**, e só entra em
vigor quando o commit que contém este relatório estiver confirmado no remoto com
todos os jobs de CI aprovados. A confirmação do SHA e da execução de CI é entregue
no fechamento da execução; sem essa evidência, a decisão é BLOCKED por publicação
não comprovada. Aprovação científica dos 1.456 artigos permanece pendente.

Evidências: `reporting/preanalysis/2026-09-06/` (manifesto, mapa, testes dos dois
motores, reconciliação canônica e diagnósticos Zotero pós-correção).
