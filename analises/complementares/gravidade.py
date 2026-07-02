"""Análise da GRAVIDADE graduada (além do óbito).

Motivação: usar apenas cura × óbito torna o desfecho quase binário e ignora os casos
que ficaram graves mas sobreviveram. O SINAN classifica a gravidade do caso no campo
CLASSI_FIN, permitindo uma escala em 3 níveis:

  1-Dengue            (códigos 10 novo / 1 antigo "clássico")
  2-Sinais de alarme  (códigos 11 novo / 2 antigo "com complicações")
  3-Grave             (códigos 12 novo / 3 antigo "febre hemorrágica")

(5 = descartado e 8 = inconclusivo não são níveis de gravidade e ficam de fora.)

Investigamos: (a) a gravidade é mesmo diferente do óbito? (letalidade por nível);
(b) o tempo até o atendimento (notificação) e até a internação varia com a gravidade?
Métodos não-paramétricos (Kruskal-Wallis), sobre a base limpa (casos confirmados).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

# --- bootstrap: encontra a infra compartilhada em analises/geral/ ---
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "comum"))
# --- fim bootstrap ---
from pipeline import (REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias,
                      tarefa3_base_limpa)
from utils import normaliza_categoria, parse_datas

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)
ALFA = 0.05

# CLASSI_FIN → nível de gravidade (harmoniza códigos antigos 2013-14 e novos 2015+)
MAPA_GRAV = {
    "10": "1-Dengue", "1": "1-Dengue",
    "11": "2-Sinais de alarme", "2": "2-Sinais de alarme",
    "12": "3-Grave", "3": "3-Grave",
}
NIVEIS = ["1-Dengue", "2-Sinais de alarme", "3-Grave"]


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    limpa = tarefa3_base_limpa(full.copy(), log)
    c = normaliza_categoria(limpa["classificacao"])
    limpa["grav"] = c.map(MAPA_GRAV)
    ev = normaliza_categoria(limpa["evolucao"])
    limpa["morreu"] = np.where(ev.isin(["2", "3", "4"]), 1.0,
                               np.where(ev == "1", 0.0, np.nan))
    s = parse_datas(limpa["dt_sintoma"])
    n = parse_datas(limpa["dt_notificacao"])
    limpa["dnotif"] = (n - s).dt.days
    return limpa


def letalidade(d):
    print("\n=== (a) Gravidade ≠ óbito: letalidade por nível ===")
    linhas = []
    for niv in NIVEIS:
        sub = d[(d["grav"] == niv) & (d["morreu"].notna())]
        ob = int(sub["morreu"].sum())
        linhas.append({"nível": niv, "n": len(sub), "óbitos": ob,
                       "sobreviveram": len(sub) - ob,
                       "letalidade_%": round(sub["morreu"].mean() * 100, 2)})
    tab = pd.DataFrame(linhas)
    print(tab.to_string(index=False))
    return tab


def tempo_por_gravidade(d, col, rotulo):
    sub = d[d["grav"].notna() & d[col].notna() & (d[col] >= 0)]
    if col == "delta_dias":
        sub = sub[~sub["delta_invalido"].fillna(False)]
    ag = sub.groupby("grav")[col].agg(["count", "median", "mean"]).round(2)
    grupos = [g[col].values for _, g in sub.groupby("grav") if len(g) >= 5]
    H, p = stats.kruskal(*grupos)
    print(f"\n=== (b) Tempo até {rotulo} por gravidade ===")
    print(ag.to_string())
    print(f"Kruskal-Wallis: H={H:.2f}  p={p:.3e}  → "
          f"{'difere' if p < ALFA else 'NÃO difere'} (α={ALFA})")
    return ag, p


def figura(letal, d):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    # painel A — letalidade por gravidade
    cores = ["#4c9", "#e9a", "#c22"]
    ax1.bar(letal["nível"], letal["letalidade_%"], color=cores)
    for i, (v, n) in enumerate(zip(letal["letalidade_%"], letal["n"])):
        ax1.text(i, v + 0.6, f"{v:.1f}%\n(n={n:,})", ha="center", fontsize=9)
    ax1.set_ylabel("Letalidade (% de óbitos no nível)")
    ax1.set_ylim(0, 40)
    ax1.set_title("A gravidade É diferente do óbito\n"
                  "a letalidade cresce muito do nível leve ao grave")
    ax1.tick_params(axis="x", labelsize=8)
    # painel B — tempo até notificação por gravidade
    sub = d[d["grav"].notna() & d["dnotif"].notna() & (d["dnotif"] >= 0)]
    dados = [sub.loc[sub["grav"] == niv, "dnotif"].values for niv in NIVEIS]
    ax2.boxplot(dados, tick_labels=[f"{niv}\n(n={len(x):,})"
                for niv, x in zip(NIVEIS, dados)], showfliers=False, widths=0.55)
    ax2.set_ylim(-1, 30)
    ax2.set_ylabel("Tempo do sintoma até a notificação (dias)")
    ax2.set_title("Mas o TEMPO até o atendimento não muda\n"
                  "medianas iguais (~6 dias) nos três níveis")
    ax2.tick_params(axis="x", labelsize=8)
    fig.suptitle("Gravidade graduada da dengue (além do óbito)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = os.path.join(FIGURAS, "viz_gravidade.png")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def main():
    d = carregar()
    print("=== Níveis de gravidade (base limpa, confirmados) ===")
    print(d["grav"].value_counts(dropna=False).to_string())
    letal = letalidade(d)
    tempo_por_gravidade(d, "dnotif", "NOTIFICAÇÃO (~100% dos casos)")
    tempo_por_gravidade(d, "delta_dias", "INTERNAÇÃO (~3%, internados)")
    fig = figura(letal, d)
    print(f"\nfigura -> {os.path.relpath(fig, ROOT)}")


if __name__ == "__main__":
    main()
