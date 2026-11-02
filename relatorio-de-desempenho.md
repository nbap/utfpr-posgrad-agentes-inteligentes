# Relatório de desempenho da linha de base

<!--
Item 3 da N2. Este relatório tem as quatro informações que o slide 28 do
E4 cobra, mais a leitura de onde erra (slide 30) — a saída do medir.py já
traz quase tudo pronto: rode `python medir.py` na pasta do D2-06 (ou do
seu projeto) e cole no lugar marcado. Responda NOS COLCHETES, apagando
nada das seções.
-->

**Projeto:** AMS · Assistente de Manutenção Segura · **Data:** 02/11/2026

## 1. A métrica primária

Acerto do risco — casos em que o risco decidido pelo agente ("alto" ou
"baixo") é igual ao rótulo, sobre o total. O rótulo é "alto" quando o
registro do AI4I tem `Machine failure` = 1, e "baixo" nos demais. É a
parte de risco do parecer correto do PEAS: NR e LOTO ainda não têm
gabarito.

## 2. O valor

```
$ python medir.py
Métrica primária: acerto da decisão (casos com decisão igual à rotulada, sobre o total)
Valor: 23/30 = 0.7667
```

O mesmo número sai de `python -m ams.baseline`.

## 3. O conjunto

`data/casos-baseline.csv` — 30 registros da amostra versionada do AI4I
2020 (`data/amostra/ai4i2020.csv`, UCI ID 601), em ordem de UDI. Não usei
o conjunto de reserva do D2-06.

- Rótulos: 8 "alto" (todas as leituras com falha da amostra) e 22 "baixo".
- Dificuldade: 12 fáceis, 16 difíceis (as 3 falhas por desgaste e 13
  leituras sem falha perto de um limiar) e 2 atípicos (UDI 195, falha de
  potência a 2678 rpm; UDI 3944, dois modos de falha ao mesmo tempo).
- O dataset não tem data: o "período" é a ordem do UDI, e é nela que o
  estado interno se acumula. A seleção está descrita em `data/FONTE.md`.

## 4. Onde o agente erra

```
Onde erra (o rótulo que o agente não deu):
  caso UDI0593: decidiu alto, correto era baixo
  caso UDI0926: decidiu alto, correto era baixo
  caso UDI1252: decidiu alto, correto era baixo
  caso UDI2589: decidiu alto, correto era baixo
  caso UDI2758: decidiu alto, correto era baixo
  caso UDI2861: decidiu alto, correto era baixo
  caso UDI2941: decidiu alto, correto era baixo
```

**O padrão.** Os 7 erros são do mesmo tipo: alarme falso em máquina sem
falha com a ferramenta acima de 200 min (desgaste de 201 a 240 min), todos
disparados pela condição com estado interno — depois que o agente viu uma
falha em fim de vida, ele marca "alto" em todo desgaste ≥ 200 nos 10
casos seguintes. Não há nenhum falso negativo: as 8 falhas foram marcadas
"alto", e as de calor, potência e sobrecarga saíram certas pela regra
reativa dos limiares físicos.

**A hipótese.** A falha por desgaste (TWF) acontece em algum ponto entre
200 e 240 min, e a leitura do instante não diz quando: UDI 1088 (206 min)
falhou e UDI 0926 (210 min) não, com leituras parecidas. O agente não vê o
que separa os dois — o histórico de troca daquela ferramenta —, então só
pode escolher entre marcar todos (7 alarmes falsos, 8/8 falhas) ou nenhum
(27/30, mas 3 falhas por desgaste perdidas).

## 5. A tabela comparativa de busca (item 4 da N2)

Subproblema da seção 7 do `agent-spec.md`: a ordem de checar os itens de
segurança da OS-2026-0012 (`meu_problema.py`).

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

**A pergunta do item 4.** Sim: o A* com a heurística admissível manteve o
custo ótimo de 28 minutos e expandiu 117 nós, contra 201 do custo
uniforme — 84 a menos (42%). Economizou porque a heurística (o esforço
base dos itens por checar mais as pendências abertas) nunca passa do custo
real, mas não é zero: vale 17 no estado inicial, contra 28 reais. A
diferença vem das pendências que as checagens futuras ainda vão abrir, que
ela ignora — e por isso o A* ainda expande mais da metade do espaço. O
espaço é pequeno (204 nós gerados) e todo caminho tem 7 ações, o que
explica por que a largura e o custo uniforme expandem o mesmo número de
nós: a diferença entre eles está só no custo do caminho que devolvem.

**A ressalva de contagem.** A profundidade limitada é recursiva e não tem
fronteira; nela, `nos_expandidos` conta entradas na recursão, sem
repetidos. Os 8 nós dela não são comparáveis aos 201 da largura: parte da
vantagem é diferença de contagem, não eficiência.
