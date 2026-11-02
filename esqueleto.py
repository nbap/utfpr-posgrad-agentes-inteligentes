"""Laboratório 06 — o agente de linha de base do AMS.

As regras, o estado interno e a leitura dos casos moram em
`src/ams/baseline.py`, o caminho que a entrega final cobra. Este arquivo só
os expõe com os nomes que o `medir.py` e o `teste.py` do pacote esperam.

    python medir.py
"""

from ams.baseline import CAMINHO_DOS_CASOS, carregar_casos, decidir
from ams.baseline import EstadoDaPlanta as EstadoDaFrota

__all__ = ["CAMINHO_DOS_CASOS", "EstadoDaFrota", "carregar_casos", "decidir"]

if __name__ == "__main__":
    from medir import medir_e_imprimir

    medir_e_imprimir(CAMINHO_DOS_CASOS, decidir, EstadoDaFrota)
