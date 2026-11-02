"""Testes do Laboratório 06 — o baseline do AMS e a medição de pé.

Como usar (da raiz do projeto):
    python -m pytest teste.py -q

As quatro famílias do pacote, adaptadas aos limiares do AMS:

  1. AS REGRAS — cada limiar físico (HDF, PWF, OSF) dispara no caso que o
     define, e a condição reativa vem antes da que consulta o estado;
  2. O ESTADO INTERNO — uma falha com a ferramenta em fim de vida acende o
     alerta para desgaste ≥ 200 min, e ele sai da janela de 10 casos;
  3. O GABARITO — as 30 decisões sobre `data/casos-baseline.csv` e a
     métrica final: 23/30. Mudou uma regra, muda o gabarito e a análise;
  4. A TROCA — o mesmo medidor sobre OUTRO arquivo, sem tocar em código.
"""

import csv

from ams import baseline
from medir import medir

ERROS_ESPERADOS = ["UDI0593", "UDI0926", "UDI1252", "UDI2589", "UDI2758", "UDI2861", "UDI2941"]


def _registro(**mudancas) -> dict:
    """Uma leitura no miolo seguro: ΔT 10 K, 6283 W, 4000 min·Nm."""
    base = {
        "id_caso": "T0001",
        "tipo": "L",
        "temperatura_ar": 300.0,
        "temperatura_processo": 310.0,
        "rotacao": 1500,
        "torque": 40.0,
        "desgaste": 100,
        "falhou_depois": 0,
    }
    base.update(mudancas)
    return base


def _decidir(estado=None, **mudancas) -> str:
    return baseline.decidir(_registro(**mudancas), estado or baseline.EstadoDaPlanta())


# --- 1. as regras -----------------------------------------------------------


def test_leitura_no_miolo_seguro_e_risco_baixo():
    assert _decidir() == "baixo"


def test_hdf_pouca_diferenca_de_temperatura_e_rotacao_baixa():
    assert _decidir(temperatura_processo=308.0, rotacao=1350) == "alto"


def test_hdf_exige_as_duas_condicoes():
    assert _decidir(temperatura_processo=308.0, rotacao=1500) == "baixo"


def test_pwf_potencia_baixa_e_alta():
    assert _decidir(torque=10.0) == "alto"  # ~1571 W
    assert _decidir(torque=70.0, rotacao=1500) == "alto"  # ~10996 W


def test_osf_depende_do_tipo_de_produto():
    # 190 min × 60 Nm = 11400 min·Nm: passa do limite de L, não do de H
    assert _decidir(tipo="L", desgaste=190, torque=60.0, rotacao=1400) == "alto"
    assert _decidir(tipo="H", desgaste=190, torque=60.0, rotacao=1400) == "baixo"


def test_a_condicao_reativa_vem_antes_do_estado():
    estado = baseline.EstadoDaPlanta()
    assert _decidir(estado, torque=10.0, desgaste=50) == "alto"


# --- 2. o estado interno e a janela -----------------------------------------


def test_falha_em_fim_de_vida_acende_o_alerta_de_desgaste():
    estado = baseline.EstadoDaPlanta()
    assert _decidir(estado, desgaste=210) == "baixo"
    estado.registrar_desfecho(_registro(desgaste=205, falhou_depois=1))
    assert _decidir(estado, desgaste=210) == "alto"
    assert _decidir(estado, desgaste=150) == "baixo"


def test_falha_com_ferramenta_nova_nao_acende_o_alerta():
    estado = baseline.EstadoDaPlanta()
    estado.registrar_desfecho(_registro(desgaste=80, falhou_depois=1))
    assert _decidir(estado, desgaste=210) == "baixo"


def test_a_falha_sai_da_janela_de_dez_casos():
    estado = baseline.EstadoDaPlanta()
    estado.registrar_desfecho(_registro(desgaste=205, falhou_depois=1))
    for _ in range(baseline.JANELA_CASOS):
        estado.registrar_desfecho(_registro())
    assert _decidir(estado, desgaste=210) == "baixo"


def test_sem_falha_o_estado_nao_acende():
    estado = baseline.EstadoDaPlanta()
    estado.registrar_desfecho(_registro(desgaste=230, falhou_depois=0))
    assert estado.falhas_em_fim_de_vida() == 0


# --- 3. o gabarito dos 30 casos ----------------------------------------------


def test_a_metrica_final_e_23_de_30():
    resultado = medir(baseline.CAMINHO_DOS_CASOS, baseline.decidir, baseline.EstadoDaPlanta)
    assert resultado["total"] == 30
    assert resultado["distribuicao"] == {"alto": 8, "baixo": 22}
    assert (resultado["acertos"], round(resultado["valor"], 4)) == (23, 0.7667)
    assert [e["id_caso"] for e in resultado["erros"]] == ERROS_ESPERADOS, (
        "os erros são a matéria-prima da análise escrita — mudaram, muda a análise"
    )


def test_baseline_e_medir_do_pacote_dao_o_mesmo_numero():
    assert (
        baseline.medir()["acertos"]
        == medir(baseline.CAMINHO_DOS_CASOS, baseline.decidir, baseline.EstadoDaPlanta)["acertos"]
    )


# --- 4. a troca do conjunto é uma linha ---------------------------------------


def test_o_medidor_roda_sobre_outro_arquivo_sem_tocar_em_codigo(tmp_path):
    casos_novos = tmp_path / "meus_casos.csv"
    with casos_novos.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(
            [
                "id_caso",
                "product_id",
                "tipo",
                "temperatura_ar",
                "temperatura_processo",
                "rotacao",
                "torque",
                "desgaste",
                "categoria",
                "acao_correta",
                "falhou_depois",
                "modo",
            ]
        )
        escritor.writerow(
            ["M01", "L1", "L", 300.0, 308.0, 1350, 45.0, 50, "facil", "alto", 1, "HDF"]
        )
        escritor.writerow(["M02", "L2", "L", 300.0, 310.0, 1500, 40.0, 50, "facil", "baixo", 0, ""])
    resultado = baseline.medir(casos_novos)
    assert resultado["total"] == 2
    assert resultado["acertos"] == 2
