# Fonte dos dados — AI4I 2020 Predictive Maintenance Dataset

- **URL:** https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip
  (UCI Machine Learning Repository, ID 601 — https://archive.ics.uci.edu/dataset/601)
- **Arquivo:** `data/amostra/ai4i2020.csv`
- **Citação**
AI4I 2020 Predictive Maintenance Dataset [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5HS5C.

## Colunas (dicionário resumido)

| Coluna | Significado |
|---|---|
| `UDI` | identificador do registro |
| `Product ID`, `Type` | produto (letra inicial = qualidade L/M/H) e tipo L/M/H |
| `Air temperature [K]`, `Process temperature [K]` | temperaturas de ar e processo |
| `Rotational speed [rpm]`, `Torque [Nm]` | rotação e torque do fuso |
| `Tool wear [min]` | minutos de desgaste da ferramenta |
| `Machine failure` | rótulo geral (0/1) |
| `TWF`, `HDF`, `PWF`, `OSF`, `RNF` | os cinco modos de falha (0/1) |

## Conjunto da linha de base — `data/casos-baseline.csv`

30 registros da amostra acima (D2, Laboratório 06), em ordem de UDI: as 8
leituras com falha e 22 sem falha. A D5, a D7 e a D10 reusam o mesmo
conjunto.

- **Rótulo:** `acao_correta` = `alto` quando `Machine failure` = 1, senão
  `baixo`; `falhou_depois` repete o `Machine failure`; `modo` lista os
  modos de falha do registro.
- **`categoria`** (escolha manual): `facil` — falhas de HDF/OSF e 9 leituras
  sem falha sorteadas (`random_state=42`) no miolo seguro; `dificil` — as 3
  falhas por desgaste (TWF) e 13 leituras sem falha perto de um limiar
  (diferença de temperatura, potência, sobrecarga ou desgaste ≥ 200 min);
  `atipico` — UDI 195 (falha de potência a 2678 rpm) e UDI 3944 (dois modos
  ao mesmo tempo, PWF e OSF).
