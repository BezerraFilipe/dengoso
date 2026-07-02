"""Spearman — tempo até a NOTIFICAÇÃO × gravidade do caso.

Pergunta: o tempo dos primeiros sintomas até a notificação no sistema de saúde
(delta_notif = dt_notificacao - dt_sintoma) tem relação com a gravidade com que o
caso chegou (1-Dengue, 2-Sinais de alarme, 3-Grave)?

Tempo medido até a NOTIFICAÇÃO (entrada no sistema, ~100% dos casos), não até a
internação. Gravidade é ordinal -> Spearman (não-paramétrico), coerente com a
distribuição assimétrica/não-normal do tempo.

Resultado esperado: rho = -0,0008, p = 0,84, n = 59.704 (sem associação).
"""
from __future__ import annotations

import os
import sys

import numpy as np
from scipy import stats

# --- infra compartilhada em analises/geral/ ---
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir, "comum"))
from pipeline import (tarefa1_dataframe_unico, tarefa2_delta_dias,  # noqa: E402
                      tarefa3_base_limpa)
from utils import normaliza_categoria, parse_datas  # noqa: E402

# CLASSI_FIN -> nível de gravidade (harmoniza códigos antigos 2013-14 e novos 2015+)
MAPA_GRAV = {"10": 1, "1": 1, "11": 2, "2": 2, "12": 3, "3": 3}
ROTULOS = {1: "1-Dengue", 2: "2-Sinais de alarme", 3: "3-Grave"}


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    limpa = tarefa3_base_limpa(full.copy(), log)

    grav = normaliza_categoria(limpa["classificacao"]).map(MAPA_GRAV)
    s = parse_datas(limpa["dt_sintoma"])
    n = parse_datas(limpa["dt_notificacao"])
    dnotif = (n - s).dt.days

    m = grav.notna() & dnotif.notna() & (dnotif >= 0)
    return dnotif[m].astype(float), grav[m].astype(float)


def main():
    dnotif, grav = carregar()
    r, p = stats.spearmanr(dnotif, grav)

    print("=== Spearman: tempo (sintoma -> notificacao) x gravidade (1-3) ===")
    print(f"n = {len(dnotif)}")
    print(f"rho = {r:.4f}   p = {p:.4g}")
    forca = ("desprezível" if abs(r) < 0.10 else "fraca" if abs(r) < 0.30 else
             "moderada" if abs(r) < 0.50 else "forte")
    print(f"força: {forca}  |  |r| > 0,5 (critério do grupo)? "
          f"{'Sim' if abs(r) > 0.5 else 'Não'}")

    print("\nmediana do tempo por nível de gravidade:")
    for k in (1, 2, 3):
        v = dnotif[grav == k]
        print(f"  {ROTULOS[k]:20s} n={len(v):6d}  "
              f"mediana={np.median(v):.0f}d  média={v.mean():.1f}d")


if __name__ == "__main__":
    main()
