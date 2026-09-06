# Controles de pré-análise

As fórmulas são controles operacionais de liberação. Não avaliam artigos nem
substituem revisão humana. Identificação/importação aprovada não significa
aprovação científica das 1.456 fontes.

## Regra única de liberação

`Master Evidence!EC` contém o motivo do gate. `EB` só retorna `Yes` quando EC
é `READY`; o semáforo C só fica verde quando EB é `Yes`. O Dashboard conta EB.

Todos os requisitos precisam estar atendidos:

1. Metadados, identificadores e checagem de integridade explicitamente `Yes`.
2. Estado de integridade `Clear` / `Verified — clear`. Retração, EoC e sinais
   importados de `Retracted Publication` bloqueiam a liberação. Correções
   documentadas ainda exigem uma futura resolução específica, sem aprovação
   automática por esta versão conservadora.
3. Instrumento de avaliação indicado, qualidade High/Moderate e risco de viés
   Low/Some concerns/Not applicable. A adequação da escolha é responsabilidade
   do revisor identificado; o preenchimento não comprova adequação científica.
4. Transferibilidade HIGH/CONDITIONAL, justificativa específica e safety
   override `No`. A escala aceita somente inteiros 0, 1 ou 2. Os limiares
   são regras do projeto, não uma escala psicometricamente validada.
5. Claim, localização no manuscrito, resultado exato e página/seção ou
   tabela/figura da fonte preenchidos.
6. Decisão Claim-ready, força Strong/Moderate, justificativa de uso, limitação
   específica, revisor identificado e data de análise numérica positiva.

Vazios, espaços e textos iniciados por Pending não satisfazem os campos
textuais exigidos. A limitação e a justificativa genéricas da importação não
substituem justificativas específicas. As 1.456 linhas reais continuam sem
análise, sem metadados individualmente verificados e sem claims liberados.

## Alerta de origem

PMID `26159007`, `EV-1171`, Zotero `9UE7LEZP`: a fonte preservada já contém
`Retracted Publication`. O alerta deriva exclusivamente desse rótulo importado.
O registro é mantido, com prioridade P1 e instrução de conferir o aviso antes
de qualquer uso. CJ/CK/CL/CM/CN não recebem verificações inventadas.

## Identidade e navegação

Os IDs existentes são valores estáveis, preservados no mapa
`reporting/preanalysis/2026-09-06/evidence-identity-map.csv`.
Nunca renumerar após ordenação ou inserir uma fórmula baseada em `ROW()`.
Novas fontes, se autorizadas em outra execução, precisam de IDs inéditos e de
extensão explícita do mapa. Inserir uma linha vazia não cria uma fonte.

Os cabeçalhos das tabelas longas permanecem congelados nas três primeiras
linhas. As tabelas auxiliares preservam as capacidades atuais: Full Text
Control 500, Claim Links e Gaps Future 200. São tabelas expansíveis, não limites
de evidências. Antes de ultrapassar a capacidade, inserir linhas completas na
tabela e estender fórmulas/validações e verificar referências no XLSX e Sheets.
Não houve preenchimento ou expansão artificial dessas tabelas nesta fase.

## Indicadores

`Analysis pending (undated)` é o total de IDs menos as datas de análise
positivas. Conta ausência de análise datada, não aprovação científica. O valor
atual é 1.456. A fórmula não usa `COUNTIFS(..., "")`.

`Primary family B (identified)` e `Primary family C (identified)` contam as
famílias primárias após reconciliação (385 e 191). Não contam relevância
científica avaliada e não substituem os totais recuperados de 391 e 194.

## Testes

Os cenários sintéticos são definidos em `analysis/preanalysis_rules.mjs` e
executados exclusivamente em cópias descartáveis. Incluem os três defeitos P0
da auditoria, campos essenciais ausentes, EoC, retração importada, revisão
humana ausente, safety override e escala decimal/fora dos limites.
Os controles precisam concordar entre EC, EB, C e Dashboard.
