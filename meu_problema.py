"""Laboratório 03 — o subproblema do AMS formulado como busca.

Caminho padrão: o subproblema 3 do catálogo (roteiro de conformidade), com
os dados trocados pelos do AMS. A classe `Conformidade` fica intacta em
`comum/problemas/conformidade.py`; aqui só moram os dados.

O caso: antes de liberar a OS-2026-0012 (substituição do rolamento do
mancal dianteiro, NR-12, exige LOTO), em que ordem conferir os itens de
segurança e fechar as pendências que eles abrem? Esforço em minutos.

    python verificar-formulacao.py meu_problema.py:MEU_PROBLEMA
"""

from comum.problemas.conformidade import Conformidade, Item

ITENS: tuple[Item, ...] = (
    Item("leitura dos sensores dentro da faixa física", 2.0),
    Item("NRs aplicáveis identificadas", 3.0),
    Item("máquina bloqueada e etiquetada (LOTO)", 5.0,
         ("aplicar cadeado e etiqueta na chave geral",)),
    Item("energia residual eliminada", 4.0,
         ("drenar o ar comprimido do circuito",)),
    Item("proteções fixas da NR-12 conferidas", 3.0),
)
PENDENCIAS: dict[str, float] = {
    "aplicar cadeado e etiqueta na chave geral": 6.0,
    "drenar o ar comprimido do circuito": 5.0,
}

MEU_PROBLEMA = Conformidade(ITENS, PENDENCIAS)
