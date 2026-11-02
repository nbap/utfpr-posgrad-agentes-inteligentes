"""Agente de linha de base do AMS (Laboratório 06 da D2).

O agente mais simples que decide o risco de falha de uma ordem de serviço,
sem modelo de linguagem: percepção (a leitura dos sensores), decisão
(regras explícitas), ação (risco "alto" ou "baixo") e medida (acerto do
risco sobre os 30 casos de `data/casos-baseline.csv`).

As regras usam os limiares físicos documentados no AI4I 2020 (Matzka,
2020), um por modo de falha:

- HDF (dissipação de calor): diferença processo − ar < 8,6 K e rotação
  < 1380 rpm;
- PWF (potência): torque × rotação fora de 3500–9000 W;
- OSF (sobrecarga): desgaste × torque acima de 11000 (L), 12000 (M) ou
  13000 (H) min·Nm;
- TWF (desgaste da ferramenta): a ferramenta falha em algum ponto entre
  200 e 240 min — a leitura sozinha não diz quando. É a condição com
  estado interno.

Uso:  python -m ams.baseline
"""

import csv
import math
from collections import Counter, deque
from pathlib import Path

RAIZ_DO_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_DOS_CASOS = RAIZ_DO_PROJETO / "data" / "casos-baseline.csv"

LIMITE_DIFERENCA_TEMPERATURA = 8.6  # K   — HDF abaixo disso...
LIMITE_ROTACAO_HDF = 1380  # rpm — ...e abaixo desta rotação
POTENCIA_MINIMA = 3500.0  # W   — PWF fora da faixa
POTENCIA_MAXIMA = 9000.0  # W
LIMITE_SOBRECARGA = {"L": 11000.0, "M": 12000.0, "H": 13000.0}  # min·Nm
DESGASTE_FIM_DE_VIDA = 200  # min — início da faixa de TWF
JANELA_CASOS = 10  # "recente" = nos últimos 10 casos


class EstadoDaPlanta:
    """O que o agente já observou: os desfechos dos últimos casos.

    Guarda, para cada um dos últimos `JANELA_CASOS` casos, se houve falha
    com a ferramenta já em fim de vida. A janela é a política de
    esquecimento: uma falha antiga não deixa a planta em alerta para sempre.
    """

    def __init__(self, janela_casos: int = JANELA_CASOS) -> None:
        self._recentes: deque[bool] = deque(maxlen=janela_casos)

    def falhas_em_fim_de_vida(self) -> int:
        """Quantas falhas com desgaste ≥ 200 min o agente viu na janela."""

        return sum(self._recentes)

    def registrar_desfecho(self, registro: dict) -> None:
        """O ambiente revela se a máquina falhou depois da ordem."""

        self._recentes.append(
            registro["falhou_depois"] == 1 and registro["desgaste"] >= DESGASTE_FIM_DE_VIDA
        )


def _potencia(registro: dict) -> float:
    return registro["torque"] * registro["rotacao"] * 2 * math.pi / 60


def decidir(registro: dict, estado: EstadoDaPlanta) -> str:
    """Uma ordem: a leitura entra, o nível de risco sai."""

    diferenca = registro["temperatura_processo"] - registro["temperatura_ar"]
    hdf = diferenca < LIMITE_DIFERENCA_TEMPERATURA and registro["rotacao"] < LIMITE_ROTACAO_HDF
    pwf = not POTENCIA_MINIMA <= _potencia(registro) <= POTENCIA_MAXIMA
    osf = registro["desgaste"] * registro["torque"] > LIMITE_SOBRECARGA[registro["tipo"]]

    if hdf or pwf or osf:
        return "alto"
    if estado.falhas_em_fim_de_vida() >= 1 and registro["desgaste"] >= DESGASTE_FIM_DE_VIDA:
        return "alto"

    return "baixo"


def carregar_casos(caminho: str | Path = CAMINHO_DOS_CASOS) -> list[dict]:
    """Lê os casos rotulados na ordem do UDI — o estado se acumula caso a
    caso, então a ordem importa."""

    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        casos = list(csv.DictReader(arquivo))
    casos.sort(key=lambda registro: registro["id_caso"])

    for registro in casos:
        for coluna in ("temperatura_ar", "temperatura_processo", "torque"):
            registro[coluna] = float(registro[coluna])
        for coluna in ("rotacao", "desgaste", "falhou_depois"):
            registro[coluna] = int(registro[coluna])

    return casos


def medir(caminho: str | Path = CAMINHO_DOS_CASOS) -> dict:
    """Roda o agente sobre os casos e devolve a métrica primária."""
    casos = carregar_casos(caminho)
    estado = EstadoDaPlanta()
    acertos = 0
    erros: list[dict] = []

    for registro in casos:
        decisao = decidir(registro, estado)
        if decisao == registro["acao_correta"]:
            acertos += 1
        else:
            erros.append(
                {
                    "id_caso": registro["id_caso"],
                    "decidiu": decisao,
                    "correta": registro["acao_correta"],
                    "modo": registro["modo"],
                }
            )
        estado.registrar_desfecho(registro)

    total = len(casos)

    return {
        "caminho": str(caminho),
        "total": total,
        "acertos": acertos,
        "valor": acertos / total if total else 0.0,
        "distribuicao": dict(Counter(r["acao_correta"] for r in casos)),
        "erros": erros,
    }


if __name__ == "__main__":
    resultado = medir()

    print("Métrica primária: acerto do risco (casos com risco igual ao rotulado, sobre o total)")
    print(f"Valor: {resultado['acertos']}/{resultado['total']} = {round(resultado['valor'], 4)}")
    print(
        f"Conjunto: {resultado['caminho']} — {resultado['total']} casos "
        f"rotulados {resultado['distribuicao']}"
    )
    print("Onde erra:")

    for erro in resultado["erros"]:
        print(
            f"  {erro['id_caso']}: decidiu {erro['decidiu']}, correto era "
            f"{erro['correta']} (modo: {erro['modo'] or 'sem falha'})"
        )
