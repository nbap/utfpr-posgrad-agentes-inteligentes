# Sete dimensões — perguntas para o meu ambiente

<!--
Este arquivo é o formulário do Laboratório 02: preencha DENTRO dele, na
seção do seu domínio, no fim. As perguntas por dimensão estão em comentário
como este — aparecem no editor, não na pré-visualização.

Em cada dimensão, a resposta tem duas partes obrigatórias: a classificação
e UMA FRASE de justificativa. A justificativa é o que a rubrica pontua — a
etiqueta sozinha não vale nada (slide 32). Quando a resposta honesta for
"depende", escreva de que depende e em que situação cada resposta se
aplica: isso é caracterização melhor, não pior.

Copie a tabela preenchida para a seção 2 do seu agent-spec.md ao terminar.
-->

## As sete perguntas (as mesmas do slide 22)

| Dimensão | A pergunta que ela faz |
|---|---|
| Observabilidade | O agente enxerga tudo o que precisa para decidir? |
| Número de agentes | Existe outro agente cujas ações afetam o resultado? |
| Determinismo | A mesma ação no mesmo estado dá sempre o mesmo efeito? |
| Episódico ou sequencial | A decisão de agora afeta as decisões seguintes? |
| Estático ou dinâmico | O ambiente muda enquanto o agente delibera? |
| Discreto ou contínuo | Estados e ações são contáveis ou variam sem degraus? |
| Conhecido ou desconhecido | O agente sabe de antemão as regras do ambiente? |

## O que prestar atenção em cada uma

- **Observabilidade** — o teste que decide: existe algo que muda a decisão
  correta e que o agente não mede? Se existe, é parcialmente observável,
  e o projeto precisa de estado interno. Quase todo domínio real é
  parcialmente observável; a resposta honesta aqui costuma ser "parcial".
- **Número de agentes** — um humano operador conta, se ele reage ao que o
  agente faz. Se a sua resposta for multiagente, a D11 será central para
  o seu projeto, e não periférica.
- **Determinismo** — é sobre o efeito das ações, não sobre a observação.
  E atenção: qualquer sistema que chame um modelo de linguagem tem uma
  ação estocástica no meio.
- **Episódico ou sequencial** — classificar um lote é episódico; conduzir
  um atendimento é sequencial. A consequência prática é o custo de
  avaliação: episódico avalia casos independentes, sequencial exige
  avaliar trajetórias inteiras.
- **Estático ou dinâmico** — dinâmico impõe prazo: resposta tardia é
  resposta errada. O caso do meio tem nome: semidinâmico, quando o
  ambiente não muda mas a nota do agente cai com a espera.
- **Discreto ou contínuo** — busca funciona sobre enumeração; contínuo
  precisa ser discretizado antes, e toda discretização perde informação.
  Se você discretizar, a granularidade é decisão declarada, com custo dos
  dois lados.
- **Conhecido ou desconhecido** — a distinção que mais confunde: trata do
  que o agente SABE sobre as regras, e não do que ele VÊ. Sistema legado
  sem documentação é ambiente desconhecido, mesmo que se enxergue tudo
  nele.

## As respostas do meu domínio

**Domínio:** AMS · Assistente de Manutenção Segura

| Dimensão | Minha classificação | Justificativa (uma frase) |
|---|---|---|
| Observabilidade | Parcial | O histórico daquela máquina e a energia/instalação elétrica que a descrição não menciona mudam o parecer e não chegam na ordem. |
| Número de agentes | Único | O técnico decide depois do parecer e o supervisor só audita; nenhum dos dois muda o acerto do parecer. |
| Determinismo | Estocástico | A mesma leitura às vezes falha e às vezes não (falha aleatória, RNF), e a leitura da descrição livre por um modelo de linguagem varia entre execuções. |
| Episódico ou sequencial | Episódico | Cada ordem é avaliada individualmente e errar uma não muda a próxima. |
| Estático ou dinâmico | Semidinâmico | A ordem não muda enquanto o agente decide, mas o técnico tem pouco tempo entre ordens e a resposta atrasada perde valor. |
| Discreto ou contínuo | Contínuo | Temperatura, rotação, torque e desgaste variam; só o parecer (3 níveis, 3 NRs, LOTO sim/não) é contabilizavel. |
| Conhecido ou desconhecido | Conhecido | As NRs estão documentadas e os limiares de cada modo de falha estão descritos no dataset. |

**O que a tabela de consequências obriga no meu projeto** (conferir no
`tabela-de-consequencias.pdf` e colar aqui as linhas que se aplicam):

- **Parcialmente observável → estado interno; memória e contexto:** guardar
  o que já se sabe da máquina e o que foi perguntado ao técnico.
- **Estocástico → valor esperado, nova tentativa, tempo máximo:** o risco
  sai de uma probabilidade; parecer inválido é pedido de novo; cada
  chamada tem tempo máximo.
- **Semidinâmico → prazo de resposta e resposta parcial aceitável:** se
  não houver tempo, entregar o risco e escalar as normas ao supervisor.
- **Contínuo → discretização declarada:** os três níveis de risco são a
  discretização; a granularidade são três condutas (segue, agenda
  inspeção, para antes de intervir).

O que **não** se aplica:

- **Agente único:** sem protocolo de comunicação; escalar é só passar o
  caso adiante.
- **Episódico:** avaliação por conjunto de ordens independentes (as 30 do
  Performance), sem trajetória inteira.
- **Conhecido:** sem fase de exploração.
