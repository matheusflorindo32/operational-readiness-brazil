# Rubrica de triagem por título e resumo — 2026-09-07

## Função e limite

Esta é uma triagem primária assistida por IA para priorizar leitura integral no
ensaio conceitual. Não é uma seleção PRISMA, avaliação de qualidade, síntese de
evidência ou aprovação de claim. O revisor registrado é `OpenAI Codex —
AI-assisted primary screen`; confirmação humana e adjudicação continuam
obrigatórias antes de qualquer uso científico substantivo.

## Unidade e fontes

Cada PMID é avaliado individualmente por título e resumo do PubMed corrente,
recuperado por NCBI Entrez EFetch em 2026-09-07. A ausência de resumo não é
interpretada como ausência de relevância. O PMID, DOI, título, autores, fonte,
ano, tipos documentais e `CommentsCorrectionsList` são comparados com o registro
preservado. O item controlado `FXC7ZY9R` não integra a triagem.

## Decisões

- `INCLUDE_FULL_TEXT`: relação explícita entre uma população/contexto tático ou
  de segurança pública e um domínio de prontidão; relação operacional explícita
  com APHT/TEMS/TCCC/TECC; ou papel explícito de implementation science.
- `EXCLUDE_TITLE_ABSTRACT`: título/resumo permitem concluir, com baixa
  ambiguidade, que o registro não trata população/contexto tático, domínio de
  prontidão, APHT operacional nem implementation science pertinente.
- `PENDING_ADJUDICATION`: resumo ausente ou relação potencial, indireta ou
  ambígua. Nenhuma exclusão é inferida da falta de DOI.
- `BLOCKED_INTEGRITY`: sinal explícito de retração ou equivalente impede uso
  científico, mantendo o registro e a trilha de auditoria.

Os termos computacionais apenas tornam o primeiro passe reproduzível. Eles não
substituem leitura humana. Registros incluídos seguem para texto completo;
excluídos e pendentes exigem confirmação humana. Correções/erratas permanecem
pendentes de revisão específica. Nenhuma decisão produz `Claim-Ready`.

## Prioridades

Prioridade de auditoria: PMID 26159007; 156 registros originalmente sem DOI;
pares de mesmo título 38280817/36368814 e 33721322/11469036; conflitos atuais de
metadados e qualquer sinal de correção, retração ou expressão de preocupação.

## Limitação obrigatória

Em toda linha triada, `What this article does NOT allow us to claim` registra
que título/resumo não sustentam eficácia, causalidade, qualidade metodológica,
transferibilidade ao Brasil nem recomendação institucional. Para retração, a
fonte não pode sustentar conclusão científica no projeto.
