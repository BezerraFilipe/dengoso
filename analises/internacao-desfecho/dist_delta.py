"""Distribuição de delta_dias por desfecho — normalidade, assimetria e curtose.

Para cada grupo de evolução (1=cura, 2=óbito dengue, 3=óbito outras causas,
4=óbito em investigação):
  - histograma com curva KDE (seaborn `histplot(kde=True)`);
  - assimetria (skewness) e curtose (excesso) via `scipy.stats`.

Orienta a escolha entre testes paramétricos e não-paramétricos nas fases seguintes.
Subconjunto: delta_dias válidos (não-nulos e ≥ 0) — internados.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# --- bootstrap: encontra a infra compartilhada em analises/geral/ ---
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "geral"))
# --- fim bootstrap ---
from pipeline import REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias
from utils import normaliza_categoria

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)

ROTULOS = {"1": "Cura", "2": "Óbito por dengue",
           "3": "Óbito por outras causas", "4": "Óbito em investigação"}
ESTRATOS = ["1", "2", "3", "4"]
XLIM = 30  # janela de exibição (dias); outliers além ficam fora da vista


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    full["ev"] = normaliza_categoria(full["evolucao"])
    return full[full["delta_dias"].notna()
                & ~full["delta_invalido"].fillna(False)].copy()


def tabela_forma(val: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for c in ESTRATOS:
        s = val.loc[val["ev"] == c, "delta_dias"].dropna()
        n = len(s)
        # skew/kurtosis amostrais (bias=False) quando há n suficiente.
        if n >= 3:
            sk = stats.skew(s, bias=False)
            ku = stats.kurtosis(s, fisher=True, bias=False)  # excesso de curtose
        else:
            sk = ku = np.nan
        linhas.append({
            "desfecho": f"{c} — {ROTULOS[c]}", "n": n,
            "assimetria": round(float(sk), 2) if pd.notna(sk) else None,
            "curtose_excesso": round(float(ku), 2) if pd.notna(ku) else None,
            "mediana": round(float(s.median()), 1) if n else None,
            "max": int(s.max()) if n else None,
        })
    return pd.DataFrame(linhas)


def figura_kde(val: pd.DataFrame):
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, c in zip(axes.ravel(), ESTRATOS):
        s = val.loc[val["ev"] == c, "delta_dias"].dropna()
        n = len(s)
        sdisp = s[s <= XLIM]
        # KDE só faz sentido com n suficiente.
        usar_kde = n >= 5 and sdisp.nunique() > 1
        sns.histplot(sdisp, bins=range(0, XLIM + 1), kde=usar_kde,
                     ax=ax, color="#4c72b0",
                     line_kws={"color": "#c44e52", "lw": 2})
        skew_txt = (f"assimetria={stats.skew(s, bias=False):.2f}\n"
                    f"curtose={stats.kurtosis(s, bias=False):.2f}" if n >= 3
                    else "n insuficiente")
        ax.set_title(f"{c} — {ROTULOS[c]} (n={n})")
        ax.set_xlabel(f"delta_dias (dias) — janela 0–{XLIM}")
        ax.set_ylabel("nº de casos")
        ax.text(0.97, 0.95, skew_txt, transform=ax.transAxes, ha="right",
                va="top", fontsize=9,
                bbox=dict(boxstyle="round", fc="white", alpha=0.8))
    fig.suptitle("Distribuição de delta_dias por desfecho — internados, Dengue/Recife\n"
                 "(histograma + KDE; janela 0–30 dias, outliers omitidos da vista)",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    out = os.path.join(FIGURAS, "dist_delta_por_desfecho.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def main():
    val = carregar()
    tab = tabela_forma(val)
    print("=== Forma da distribuição de delta_dias por desfecho ===")
    print(tab.to_string(index=False))
    # Referência: normal tem assimetria 0 e curtose-excesso 0.
    fig = figura_kde(val)
    print(f"\nfigura -> {os.path.relpath(fig, ROOT)}")
    return tab


if __name__ == "__main__":
    main()
