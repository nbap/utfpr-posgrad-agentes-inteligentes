# agent-spec.md — modelo do meu agente

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:** AMS · Assistente de Manutenção Segura — parecer de risco, normas e 
LOTO para ordens de serviço industriais
**Autor(a):** Nicolas Baptista · **Última revisão:** 15/10/2026

---

## 1. PEAS

<!-- Perguntas que guiam o preenchimento:
  - Performance: o que conta como sucesso, em uma fórmula? Sobre o quê se
    conta, sobre qual conjunto, quanto é sucesso? Qual termo impede a
    trapaça mais óbvia (fechar rápido sem resolver)?
  - Environment: onde o agente opera? O que existe lá — sistemas, pessoas,
    documentos, ruído? Cite elementos concretos.
  - Actuators: o que o agente pode FAZER? Inclua comunicar e escalar:
    informar a decisão é uma ação, e passar adiante também é.
  - Sensors: o que o agente consegue PERCEBER? Só o que ele enxerga existe
    para ele.
  Um PEAS que menciona tecnologia de solução (banco vetorial, nome de modelo)
  está descrevendo a solução — o PEAS descreve o problema.
-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:**

    desempenho = ordens com parecer correto / total de ordens do conjunto

Acertar o parecer de risco, as NRs e a exigência de LOTO em mais de 80% de um 
lote de 30 ordens de serviço do AI4I 2020 (comparado ao gabarito do supervisor). 
Hoje o acerto é 0%. Trava de segurança: se o agente não marcar risco "alto" em 
pelo menos 90% das máquinas que realmente falharam, a nota final é zero.

**Environment:**

Fila de ordens da manutenção; máquinas de usinagem (tipos L/M/H) e seus sensores; 
histórico de 10.000 leituras (3,4% de falhas); normas NR-10, NR-12 e NR-35; 
técnicos (com pouco tempo) e o supervisor de segurança. Ruído: descrições vagas 
("trocar peça") e leituras digitadas erradas.

**Actuators:**

Classificar o risco (baixo, médio ou alto); indicar NRs aplicáveis; 
arcar se precisa de LOTO; enviar parecer com explicação curta ao técnico; 
pedir mais dados se a ordem for vaga; e escalar o caso ao supervisor se a 
confiança for baixa.

**Sensors:**

A ordem de serviço (máquina e serviço); dados atuais de temperatura, rotação, 
torque e desgaste; histórico de falhas; e o texto das NRs. O que não estiver 
nesses pontos o agente não vê (ex.: histórico da máquina, fadiga da equipe, etc).

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
**Quando se preenche:** no Laboratório 02, no sábado (encontro 2).

| Dimensão | Classificação | Justificativa | O que obriga no projeto |
|---|---|---|---|
| Observabilidade | Parcial | O histórico daquela máquina e a energia/instalação elétrica que a descrição não menciona mudam o parecer e não chegam na ordem | Estado interno; memória e contexto |
| Número de agentes | Único | O técnico decide depois do parecer e o supervisor só audita; nenhum dos dois muda o acerto do parecer | Sem protocolo de comunicação |
| Determinismo | Estocástico | A mesma leitura às vezes falha e às vezes não (falha aleatória, RNF), e a leitura da descrição livre por um modelo de linguagem varia entre execuções | Valor esperado, nova tentativa, tempo máximo |
| Episódico ou sequencial | Episódico | Cada ordem é avaliada individualmente e errar uma não muda a próxima | Avaliação por conjunto de ordens independentes |
| Estático ou dinâmico | Semidinâmico | A ordem não muda enquanto o agente decide, mas o técnico tem pouco tempo entre ordens e a resposta atrasada perde valor | Prazo de resposta e resposta parcial aceitável |
| Discreto ou contínuo | Contínuo | Temperatura, rotação, torque e desgaste variam; só o parecer (3 níveis, 3 NRs, LOTO sim/não) é contabilizavel | Discretização declarada: 3 níveis de risco = 3 condutas |
| Conhecido ou desconhecido | Conhecido | As NRs estão documentadas e os limiares de cada modo de falha estão descritos no dataset | Sem fase de exploração |

---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche:** no sábado (encontro 2, manhã).

[o tipo mais simples que resolve, justificado pela dimensão
do ambiente que o obriga]

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

**Fórmula (Laboratório 01):**

    desempenho = ordens com parecer correto / total de ordens do conjunto

[métrica primária e duas secundárias, cada uma com: como se
calcula, sobre qual conjunto, qual o limiar de sucesso e o
valor de hoje]

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

[latência aceitável, custo aceitável, o que o agente jamais
pode fazer sozinho, e a troca qualidade × custo que você
aceita — com um exemplo numérico]

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.

[tabela: nome · entrada · saída · é reversível? · risco se
errar — ações de leitura e de escrita]

---

## 7. Formulação por busca

<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

**O que é busca:** definir a melhor ordem para checar os itens de segurança antes de liberar o trabalho (exemplo da OS-2026-0012: troca do rolamento do mancal dianteiro, com NR-12 e LOTO).

| Componente | Neste domínio |
|---|---|
| **Estado inicial** | Nada checado e nenhuma pendência em aberto. |
| **Ações** | Checar um item pendente ou resolver uma pendência da lista. |
| **Transição** | Checar um item marca ele como concluído e abre novas tarefas necessárias (ex.: LOTO exige colocar cadeado e etiqueta); resolver uma tarefa a remove da lista. |
| **Teste de objetivo** | Todos os 5 itens checados e nenhuma pendência sobrando. |
| **Custo** | Tempo em minutos (tentar checar algo sem resolver as pendências antes custa o dobro de tempo por causa de retrabalho). |

* **O estado do sistema** é apenas a foto atual: `(itens checados, pendências abertas)`.
* **O que NÃO é busca:** calcular o nível de risco e definir quais NRs se aplicam são tarefas de classificação, não de montagem de sequência.

**Medições das buscas (Laboratórios 04 e 05):**

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 35.0 | 7 | 201 | 204 | 7 | 0.0004 |
| custo_uniforme | 28.0 | 7 | 201 | 204 | 7 | 0.0004 |
| profundidade_limitada(limite=32) | 35.0 | 7 | 8 | 7 | 7 | 0.0 |
| aprofundamento_iterativo(limite=32) | 35.0 | 7 | 260 | 619 | 7 | 0.0012 |
| gulosa[admissivel] | 28.0 | 7 | 8 | 18 | 7 | 0.0001 |
| a_estrela[admissivel] | 28.0 | 7 | 117 | 176 | 7 | 0.0005 |
| gulosa[inadmissivel] | 28.0 | 7 | 8 | 18 | 7 | 0.0001 |
| a_estrela[inadmissivel] | 28.0 | 7 | 19 | 35 | 7 | 0.0001 |

**Conclusão:** sim, o custo uniforme achou um caminho mais barato que a
largura: 28 contra 35 minutos, com as mesmas 7 ações. Todo caminho tem 7
ações (5 itens + 2 pendências), então a largura não tem como distinguir
um do outro e devolve o primeiro: checa os 5 itens e só depois fecha as
pendências, pagando o retrabalho em dobro nos itens checados com
pendência aberta (+7 min). O custo uniforme fecha cada pendência logo
depois do item que a abriu e deixa o LOTO por último, pagando só os 28
minutos de esforço base. A profundidade limitada e o aprofundamento
iterativo também ficam em 35, porque só olham profundidade, não custo.

**O limite da formulação:** o caminho mais barato é inseguro. Ele checa
as proteções e a energia residual e drena o ar comprimido antes de
bloquear e etiquetar a chave geral — na prática, o LOTO vem primeiro,
porque sem ele a energia pode voltar durante a intervenção. A busca não
errou: a formulação só tem custo de retrabalho e nenhuma regra de
precedência, então nada obriga o LOTO a vir antes. O ótimo pelo custo
não é o ótimo pela segurança enquanto essa precedência não estiver na
formulação.

**Ressalva de contagem:** a profundidade limitada é recursiva e não tem
fronteira; nela, `nos_expandidos` conta entradas na recursão, sem
repetidos. Os 8 nós dela não são comparáveis aos 201 da largura: parte da
vantagem é diferença de contagem, não eficiência.

**Dominância (Laboratório 05):** entre duas heurísticas admissíveis,
a que estima mais alto em todo estado é a que domina, e a dominada nunca expande
menos. A admissível (o esforço base do que falta: itens por checar mais
pendências abertas) domina a heurística zero do custo uniforme: vale 17
no estado inicial contra 0, e nunca passa do custo real (28) porque
ignora as pendências que as checagens futuras vão abrir e o retrabalho
só aumenta o custo. A evidência: o A* com ela expandiu 117 nós contra 201
do custo uniforme, com o mesmo custo ótimo de 28. A inadmissível (o dobro
da admissível) estima mais alto em todo estado e expandiu só 19, mas não
entra na dominância: tem valor 34 no estado inicial que é acima dos 28, então
a garantia de ótimo caiu.

As duas gulosas saem idênticas (8 expandidos, custo 28) porque a gulosa
só usa a ordem dos valores de h e dobrar h não muda a ordem. O 28 delas
também não é garantido.

Os dois A* acharam caminhos diferentes com o mesmo custo de 28: o da
admissível deixa o LOTO por último; o da inadmissível bloqueia antes de
eliminar a energia residual. 
