# Gate 1 — consistência documental

**Data:** 2026-09-15

**Escopo:** somente Gate 1

**Decisão:** PASS condicionado à publicação do commit e à CI verde

**Aprovação científica humana:** 0/1.456

## Resultado

GitHub, o XLSX local e a Google Sheet canônica apresentam o mesmo semáforo:
**10 vermelhos, 1.446 amarelos e zero verdes**. O conjunto continua com 1.456
registros, Claim-Ready 0/1.456 e nenhuma confirmação humana. A triagem assistida
não constitui aprovação científica dos artigos.

## Causa e correção

Uma frase no relatório pré-análise de 2026-09-06 preservava uma contagem
transitória anterior à triagem controlada. O Dashboard local, a Sheet canônica,
o relatório atual, o checklist e os testes já refletiam a classificação vigente:
uma retração e nove propostas de exclusão em vermelho, com os 1.446 registros
restantes em amarelo.

A frase foi atualizada para declarar o estado vigente e sua causa. README,
checklist e changelog receberam referência explícita a esta reconciliação. Não
houve alteração em planilha, Google Sheets, Zotero, decisões de triagem ou
metadados bibliográficos.

## Auditoria antes da alteração

| Controle | Evidência observada |
|---|---|
| Git | checkout limpo; `HEAD` e `origin/main` em `e9bf3c74fc709ee1b34a3b487ce003e4a3e0b480` |
| CI do commit inicial | GitHub Actions `Security baseline`, execução 34119367182, sucesso |
| XLSX local | 10 vermelhos; 1.446 amarelos; zero verdes; 1.456 linhas |
| Google Sheets | mesma contagem, mesmo ID canônico e permissão privada somente do proprietário |
| Master Evidence | 1.456 Evidence IDs, PMIDs e Zotero keys únicos; zero vazios nesses identificadores |
| Zotero | API/Connector HTTP 200; produção 1.456; controlado 1; biblioteca 1.457 |
| Par controlado | `FXC7ZY9R` isolado; PMID 37415704 em `8XVBQIYE`; `DO NOT MERGE` |
| Reconciliação bibliográfica | 44/44 controles estruturais aprovados em execução temporária |

## Backup e hashes de entrada

O backup externo verificável foi criado antes da correção no diretório adjacente
`outputs/gate1-documentary-backups/2026-09-15T-GATE1`, fora do checkout do
repositório.

| Arquivo | SHA-256 antes |
|---|---|
| `README.md` | `6174d444c3711218f90472413f2f2cfb015e6195af338c86a4207bfa4c4f1530` |
| `CHANGELOG.md` | `26189fd00c696fdc1b8d034d2624fcc8bbf77283b4643164b37da0eccd058794` |
| `reporting/CHECKLIST.md` | `72722a430e79f762a17e44f978eb23347d1e12f0a6e5ae6102e8600c5af230d5` |
| `docs/PUBMED_PREANALYSIS_GATE_2026-09-06.md` | `51b8d93df56df9c499f66a75308d9f8424f5f80c587d204eb420ab9f581fbf65` |
| XLSX canônico local, preservado | `2177618b04536e5a9c7b0feffe601b9847826b8fbb283715e2c071a1f604427b` |

Os hashes finais dos arquivos alterados constam no manifesto versionado
`reporting/gates/2026-09-15/gate1-manifest.json`.

## Revisão cruzada

As funções de metodologia, integridade científica, biblioteconomia biomédica,
epidemiologia, risco de viés, ciência de dados, rastreabilidade, Zotero,
planilhas e revisão editorial verificaram seus respectivos domínios. Essa
revisão é técnica e assistida; nenhuma revisão por pares humana foi registrada.

## Teste de regressão

O teste `analysis/test_gate1_documentary_consistency.py` exige 0/1.446/10 no
Dashboard local, rejeita a frase numérica superada nos documentos correntes e
confirma no registro de sincronização do Drive 1.456 linhas, identificadores
únicos, dez bloqueios de uso, zero Claim-Ready e zero campos humanos preenchidos.
O conjunto documental, estrutural, de fórmulas e de triagem concluiu 19/19
testes com sucesso. A primeira invocação, fora do diretório esperado pelos
módulos legados, falhou apenas na descoberta de imports; a execução corrigida
em `analysis/` foi integralmente aprovada.

## Limites e próximo gate

Gate 2 não foi iniciado. A fila de 18 relações editoriais continua exigindo
adjudicação humana identificável. Não houve avaliação individual de texto
completo, qualidade ou risco de viés, e não existe aprovação científica global.
