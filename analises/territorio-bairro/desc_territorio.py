"""Análise descritiva territorial de delta_dias (bairro e zona).

- Ranking dos bairros por delta_dias médio, filtrando bairros com < 30 casos.
- Histograma de delta_dias por zona (urbana/rural/periurbana) com contagem por grupo.

Subconjunto: delta_dias válidos (não-nulos e ≥ 0) — os internados (~3% da base).
Gera tabelas (markdown), CSV do ranking e figuras. Documenta os outliers de registro
e a degenerescência da variável zona em Recife.
"""
from __future__ import annotations

import os

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- bootstrap: encontra a infra compartilhada em analises/geral/ ---
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "comum"))
# --- fim bootstrap ---
from pipeline import REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias
from utils import normaliza_categoria

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)

N_MIN = 30
# Janela dos dados (2013–2025) ≈ 13 anos; delta acima disso é impossível (erro de data).
DELTA_IMPOSSIVEL = 365 * 13  # ~4745 dias

ZONA_ROTULO = {"1": "Urbana", "2": "Rural", "3": "Periurbana",
               "9": "Ignorado", "0": "Não informado"}


def carregar_validos() -> pd.DataFrame:
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    val = full[full["delta_dias"].notna()
               & ~full["delta_invalido"].fillna(False)].copy()
    val["bairro_norm"] = (val["nome_bairro_residencia"].astype(str)
                          .str.strip().str.upper()
                          .mask(lambda s: s.isin(["", "NAN", "NONE"])))
    val["zona_norm"] = normaliza_categoria(val["zona_residencia"])
    return val


def _md(df: pd.DataFrame, index=True) -> str:
    cols = ([df.index.name or ""] if index else []) + [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |",
           "| " + " | ".join(["---"] * len(cols)) + " |"]
    for idx, r in df.iterrows():
        cells = ([str(idx)] if index else []) + [str(v) for v in r]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def ranking_bairros(val: pd.DataFrame):
    g = (val.dropna(subset=["bairro_norm"])
            .groupby("bairro_norm")["delta_dias"]
            .agg(["mean", "median", "count"]))
    elegiveis = g[g["count"] >= N_MIN].copy()
    elegiveis = elegiveis.round({"mean": 2, "median": 2})
    elegiveis.index.name = "bairro"
    top_mean = elegiveis.sort_values("mean", ascending=False).head(10)
    top_median = elegiveis.sort_values("median", ascending=False).head(10)

    # salva ranking completo dos elegíveis
    out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking_bairros.csv")
    elegiveis.sort_values("mean", ascending=False).to_csv(out_csv, encoding="utf-8")

    print(f"Bairros distintos: {g.shape[0]} | com n>={N_MIN}: {len(elegiveis)}")
    print("\nTOP-10 por delta_dias MÉDIO (n>=30):")
    print(top_mean.to_string())
    return elegiveis, top_mean, top_median, out_csv


def grafico_top_bairros(top_mean: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(11, 6))
    d = top_mean.iloc[::-1]  # maior no topo
    ax.barh(d.index, d["mean"], color="#c44e52")
    for y, (m, n) in enumerate(zip(d["mean"], d["count"])):
        ax.text(m, y, f"  média={m:.0f} (n={n})", va="center", fontsize=8)
    ax.set_xlabel("delta_dias médio (dias)")
    ax.set_title("Top-10 bairros por delta_dias MÉDIO — internados, Dengue/Recife\n"
                 "(atenção: a média é inflada por outliers de registro; ver mediana)")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    out = os.path.join(FIGURAS, "top_bairros_delta.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def histograma_por_zona(val: pd.DataFrame):
    cont = (val["zona_norm"].map(ZONA_ROTULO).fillna("Sem registro")
            .value_counts())
    print("\nContagem de casos por zona (delta válidos):")
    print(cont.to_string())

    fig, ax = plt.subplots(figsize=(10, 6))
    cores = {"Urbana": "#4c72b0", "Rural": "#55a868", "Periurbana": "#dd8452"}
    bins = range(0, 31, 1)  # recorte 0–30 dias p/ legibilidade
    for z in ("Urbana", "Rural", "Periurbana"):
        s = val.loc[val["zona_norm"] == {v: k for k, v in ZONA_ROTULO.items()}[z],
                    "delta_dias"]
        n = len(s)
        ax.hist(s.clip(upper=30), bins=bins, alpha=0.6, label=f"{z} (n={n})",
                color=cores[z])
    ax.set_xlabel("delta_dias (dias) — recortado em 30")
    ax.set_ylabel("nº de casos")
    ax.set_title("Distribuição de delta_dias por zona — internados, Dengue/Recife")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = os.path.join(FIGURAS, "delta_por_zona.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return cont, out


def main():
    val = carregar_validos()
    print(f"delta válidos: {len(val)}")
    n_imp = int((val["delta_dias"] > DELTA_IMPOSSIVEL).sum())
    n_long = int((val["delta_dias"] > 60).sum())
    print(f"delta > 60 dias (clinicamente implausível): {n_long} | "
          f"delta impossível (> {DELTA_IMPOSSIVEL} dias): {n_imp}")
    elegiveis, top_mean, top_median, csv = ranking_bairros(val)
    fig1 = grafico_top_bairros(top_mean)
    cont, fig2 = histograma_por_zona(val)
    print(f"\nfiguras -> {os.path.relpath(fig1, ROOT)} | {os.path.relpath(fig2, ROOT)}")
    print(f"ranking csv -> {os.path.relpath(csv, ROOT)}")
    return val, elegiveis, top_mean, top_median, cont


if __name__ == "__main__":
    main()
