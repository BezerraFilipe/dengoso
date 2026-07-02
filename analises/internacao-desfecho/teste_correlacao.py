"""Grau de associação entre delta_dias e o desfecho (evolucao) — Fase 5.

Como a normalidade foi rejeitada (processo 9), usa-se **Spearman** (não Pearson).
Correlação entre delta_dias (numérica) e evolucao codificada ordinalmente
(cura=1, óbito=2+). Gera também uma matriz de correlação (Spearman) entre as
variáveis de interesse e avalia o critério de viabilidade |r| > 0,5.

Subconjunto: delta_dias válidos (≥ 0) e evolucao ∈ {1,2,3,4}.
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
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "comum"))
# --- fim bootstrap ---
from pipeline import REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias
from utils import decodifica_idade, normaliza_categoria

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)

LIMIAR = 0.5  # critério de viabilidade do grupo: |r| > 0,5


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    full["ev"] = normaliza_categoria(full["evolucao"])
    full["idade_anos"] = decodifica_idade(full["idade"])
    val = full[full["delta_dias"].notna()
               & ~full["delta_invalido"].fillna(False)].copy()
    sub = val[val["ev"].isin(["1", "2", "3", "4"])].copy()
    sub["evolucao_ord"] = sub["ev"].astype(int)           # 1..4 ordinal
    sub["obito"] = np.where(sub["evolucao_ord"] == 1, 1, 2)  # cura=1, óbito=2
    return sub


def forca(r: float) -> str:
    a = abs(r)
    if a < 0.10:
        return "desprezível"
    if a < 0.30:
        return "fraca"
    if a < 0.50:
        return "moderada"
    if a < 0.70:
        return "forte"
    return "muito forte"


def correlacoes(sub: pd.DataFrame):
    pares = [
        ("delta_dias × evolução (cura=1/óbito=2)", "delta_dias", "obito"),
        ("delta_dias × evolução (1–4 ordinal)", "delta_dias", "evolucao_ord"),
        ("delta_dias × idade (anos)", "delta_dias", "idade_anos"),
    ]
    linhas = []
    for nome, a, b in pares:
        d = sub[[a, b]].dropna()
        r, p = stats.spearmanr(d[a], d[b])
        linhas.append({"par": nome, "n": len(d), "r_spearman": round(r, 4),
                       "p_valor": f"{p:.2e}", "força": forca(r),
                       "|r|>0,5?": "Sim" if abs(r) > LIMIAR else "Não"})
    return pd.DataFrame(linhas)


def matriz(sub: pd.DataFrame):
    vars_ = ["delta_dias", "obito", "evolucao_ord", "idade_anos"]
    m = sub[vars_].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(m, annot=True, fmt=".3f", cmap="coolwarm", center=0,
                vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={"label": "ρ de Spearman"})
    ax.set_title("Matriz de correlação (Spearman) — variáveis de interesse")
    fig.tight_layout()
    out = os.path.join(FIGURAS, "matriz_correlacao.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return m, out


def main():
    sub = carregar()
    print(f"n (delta válidos, evolução 1–4): {len(sub)}")
    tab = correlacoes(sub)
    print("\n=== Correlações de Spearman ===")
    print(tab.to_string(index=False))
    m, fig = matriz(sub)
    print("\n=== Matriz de correlação (Spearman) ===")
    print(m.round(3).to_string())
    print(f"\nfigura -> {os.path.relpath(fig, ROOT)}")

    r_main = float(stats.spearmanr(sub["delta_dias"], sub["obito"])[0])
    print(f"\nCritério |r| > {LIMIAR}: r_principal={r_main:.4f} "
          f"({forca(r_main)}) -> {'ATENDE' if abs(r_main) > LIMIAR else 'NÃO ATENDE'}")


if __name__ == "__main__":
    main()
