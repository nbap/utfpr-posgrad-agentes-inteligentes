# Análise

<!--
Item 5 da N2 — a única escrita genuinamente nova, e o tema é fixo:
quais propriedades do ambiente tornam o problema difícil, e que tipo de
agente o problema realmente exige. Um parágrafo por pergunta abaixo; a
meta é UMA página. O que separa o adequado do excelente é a EVIDÊNCIA:
citar o número que apareceu, o caso que errou, a linha da tabela — algo
que só quem rodou saberia. Responda NOS COLCHETES.
-->

## O que torna o problema difícil

O primeiro desafio real é a observabilidade parcial na prática: a falha por desgaste da ferramenta acontece em algum momento entre 200 e 240 minutos de uso, mas a leitura isolada dos sensores não avisa quando. Por exemplo, o caso UDI 1088 (206 min) falhou, enquanto o UDI 0926 (210 min) não falhou, mesmo tendo leituras muito parecidas. O que diferencia os dois é o histórico de troca daquela ferramenta específica, uma informação que não vem na ordem de serviço. É por isso que o nosso baseline erra sempre do mesmo jeito: todos os seus 7 erros são alarmes falsos em ferramentas que passaram dos 200 minutos.

A segunda dificuldade é que as falhas são raras (3,4% no dataset original e 8 em 30 no nosso recorte). Um agente inútil que chutasse "risco baixo" para tudo acertaria 22 de 30 casos (73%) sem detectar nenhum problema real — ficando a apenas 1 acerto de distância do nosso baseline (23/30). Sem a trava de cobertura mínima, a métrica principal acabaria premiando um agente que nunca dá alerta.

Por fim, o terceiro obstáculo está na etapa de busca: o caminho mais rápido (28 minutos, achado pelo custo uniforme e pelo A*) deixa o LOTO por último, empatando em tempo com rotas que fazem o bloqueio antes. Como não colocamos uma regra de precedência na modelagem, o cálculo de custo sozinho não sabe diferenciar uma sequência segura de uma perigosa.

## Que tipo de agente o problema realmente exige

Um agente reativo simples não dá conta do recado. Quando testamos a versão sem memória, a taxa geral de acerto até subiu para 27/30, mas ela deixou passar todas as 3 falhas por desgaste (UDI 1088, 4208 e 8358), detectando só 5 das 8 falhas reais (62,5% de cobertura, bem abaixo da trava de 90%). 

Por isso, o agente precisa ser **baseado em modelo** (com estado interno). O problema é que a memória que implementamos hoje — que olha apenas se houve falhas de fim de vida nos últimos 10 casos gerais da fábrica — ainda é muito rudimentar. Ela até recupera as 3 falhas de desgaste, mas gera 7 alarmes falsos em troca, porque monitora a planta inteira em vez de acompanhar a ferramenta específica. O estado interno ideal precisa ser rastreado por máquina (quantas horas se passaram desde a última troca naquela unidade). Já para definir a ordem da checagem de segurança, entra uma parte **baseada em objetivos** (busca), desde que a gente corrija o modelo para obrigar o LOTO a vir primeiro. Essa arquitetura tem a vantagem de ser enxuta: como é um agente único e cada ordem de serviço é avaliada de forma independente (seção 2), não precisamos nos preocupar com protocolos de comunicação entre múltiplos agentes nem com avaliação de trajetórias longas.

## O que isto muda no projeto

Para a próxima etapa (D10), mais do que criar regras novas, precisamos trazer um dado novo: o histórico de troca de ferramenta por máquina. Sem isso, nenhum agente — usando LLM ou não — vai conseguir diferenciar o caso UDI 1088 do UDI 0926. Também precisamos incluir a regra de precedência do LOTO na formulação da busca. Por outro lado, onde o baseline já resolve bem (nas falhas por calor, potência e sobrecarga, onde os limites físicos acertaram 100% dos casos), não faz sentido gastar com LLM para substituir o que já funciona. O modelo de linguagem deve entrar só onde as regras fixas não alcançam: na interpretação do texto livre da ordem para definir as NRs e o LOTO.
