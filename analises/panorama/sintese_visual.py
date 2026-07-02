"""Síntese e visualização final — figuras para o relatório e a apresentação.

Transforma os resultados das fases anteriores em três visualizações de alta
resolução (dpi=200), cada uma autoexplicativa (título + legenda):

  (1) boxplot de delta_dias por desfecho            → diferença central entre grupos
  (2) top-20 bairros por delta_dias médio           → desigualdade territorial
  (3) série temporal de casos e óbitos por ano       → contexto do período 2013–2025

Narrativa: o tempo até a internação é estável entre desfechos (processo 11) mas
varia entre bairros (processo 12), num período com surtos marcados (2015–2016).
Subconjunto de delta_dias: válidos (≥ 0), internados.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "comum"))

from pipeline import REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias
from utils import normaliza_categoria

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)
DPI = 200  # alta resolução p/ relatório e slides

ROTULOS = {"1": "Cura", "2": "Óbito\npor dengue",
           "3": "Óbito por\noutras causas", "4": "Óbito em\ninvestigação"}
sns.set_theme(style="whitegrid")


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    full["ev"] = normaliza_categoria(full["evolucao"])
    val = full[full["delta_dias"].notna()
               & ~full["delta_invalido"].fillna(False)].copy()
    val["delta_dias"] = val["delta_dias"].astype(float)
    val["bairro"] = val["nome_bairro_residencia"].astype(str).str.upper().str.strip()
    val.loc[val["bairro"].isin(["NAN", "NONE", ""]), "bairro"] = np.nan
    return full, val


# (1) ------------------------------------------------------------------ boxplot
def fig_desfecho(val: pd.DataFrame):
    estratos = ["1", "2", "3"]  # grupo 4 (n=4) omitido por falta de significância
    dados = [val.loc[val["ev"] == c, "delta_dias"].values for c in estratos]
    fig, ax = plt.subplots(figsize=(9, 6))
    bp = ax.boxplot(dados, showfliers=False, widths=0.55, patch_artist=True,
                    medianprops=dict(color="black", lw=2))
    for patch, cor in zip(bp["boxes"], ["#4c9", "#e76", "#e9a"]):
        patch.set_facecolor(cor)
    ax.set_xticklabels([f"{ROTULOS[c]}\n(n={len(d)})" for c, d in zip(estratos, dados)])
    ax.set_ylim(-1, 25)  # recorte: outliers de registro (máx 1.116 d) achatariam tudo
    ax.set_ylabel("delta_dias — dias do sintoma até a internação")
    for i, d in enumerate(dados, 1):
        ax.text(i, np.median(d) + 0.4, f"md={np.median(d):.0f}", ha="center",
                fontsize=9, fontweight="bold")
    ax.set_title("Tempo até a internação por desfecho\n"
                 "medianas iguais (~4 dias): o tempo NÃO discrimina o desfecho "
                 "(Mann-Whitney, processo 11)")
    fig.text(0.5, 0.01, "Eixo y recortado em 25 dias (outliers de registro fora da "
             "vista). Grupo 'óbito em investigação' (n=4) omitido.",
             ha="center", fontsize=8, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = os.path.join(FIGURAS, "viz_final_1_desfecho.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


# (2) -------------------------------------------------------------- top bairros
def fig_bairros(val: pd.DataFrame):
    d = val.dropna(subset=["bairro"])
    ag = d.groupby("bairro")["delta_dias"].agg(["count", "mean", "median"])
    ag = ag[ag["count"] >= 30].sort_values("mean", ascending=False).head(20)[::-1]
    CAP = 15.0  # recorte do eixo: CORDEIRO (média 284) é outlier de registro
    fig, ax = plt.subplots(figsize=(10, 8))
    y = np.arange(len(ag))
    ax.barh(y, ag["mean"].clip(upper=CAP), color="#c0504d", label="média")
    ax.plot(ag["median"], y, "o", color="black", label="mediana (robusta)")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{b}  (n={int(n)})" for b, n in zip(ag.index, ag["count"])],
                       fontsize=8)
    ax.set_xlim(0, CAP + 0.5)
    ax.set_xlabel("delta_dias médio (dias) — barra recortada em 15")
    # anota o valor real dos que estouram o recorte (CORDEIRO)
    for yi, (b, r) in zip(y, ag.iterrows()):
        if r["mean"] > CAP:
            ax.text(CAP - 0.2, yi, f"média real = {r['mean']:.0f} d (outlier) →",
                    ha="right", va="center", fontsize=8, color="white",
                    fontweight="bold")
    ax.set_title("Top-20 bairros por tempo médio até a internação (n ≥ 30)\n"
                 "desigualdade territorial significativa, mas modesta "
                 "(Kruskal-Wallis p≈2,7e-22, processo 12)")
    ax.legend(loc="lower right")
    fig.text(0.5, 0.01, "Média recortada em 15 d; CORDEIRO (média 284) é artefato de um "
             "registro impossível de 19.100 d — sua mediana é 4 d, típica. "
             "Comparar pela MEDIANA.", ha="center", fontsize=8, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = os.path.join(FIGURAS, "viz_final_2_bairros.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


# (3) --------------------------------------------------------- série temporal
def fig_serie(full: pd.DataFrame):
    g = full.groupby("ano_csv")
    casos = g.size()
    obitos = full[full["ev"] == "2"].groupby("ano_csv").size().reindex(
        casos.index, fill_value=0)
    anos = casos.index.astype(int)

    fig, ax1 = plt.subplots(figsize=(11, 6))
    ax1.fill_between(anos, casos.values, color="#9cf", alpha=0.6, zorder=1)
    ax1.plot(anos, casos.values, color="#27c", marker="o", lw=2,
             label="Casos notificados", zorder=2)
    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Casos notificados de dengue", color="#27c")
    ax1.tick_params(axis="y", labelcolor="#27c")
    ax1.set_xticks(anos)
    ax1.set_ylim(0, casos.max() * 1.12)

    ax2 = ax1.twinx()
    ax2.grid(False)
    ax2.plot(anos, obitos.values, color="#c22", marker="s", lw=2,
             label="Óbitos por dengue", zorder=3)
    ax2.set_ylabel("Óbitos por dengue (evolução = 2)", color="#c22")
    ax2.tick_params(axis="y", labelcolor="#c22")
    ax2.set_ylim(0, max(obitos.max() * 1.6, 5))
    for x, v in zip(anos, obitos.values):
        if v > 0:
            ax2.annotate(str(int(v)), (x, v), textcoords="offset points",
                         xytext=(0, 6), ha="center", fontsize=8, color="#c22")

    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc="upper right")
    ax1.set_title("Casos e óbitos por dengue em Recife por ano (2013–2025)\n"
                  "surtos marcados em 2015–2016; base do estudo")
    fig.text(0.5, 0.01, "Casos = base unificada (110.385). Óbitos por dengue = evolução 2 "
             "(total 58); a codificação de óbito é esparsa em alguns anos (limitação "
             "do SINAN).", ha="center", fontsize=8, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = os.path.join(FIGURAS, "viz_final_3_serie_temporal.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return out


def main():
    full, val = carregar()
    print(f"delta válidos: {len(val)}  |  base unificada: {len(full)}")
    f1 = fig_desfecho(val)
    f2 = fig_bairros(val)
    f3 = fig_serie(full)
    print("Figuras finais (dpi=200):")
    for f in (f1, f2, f3):
        print("  ->", os.path.relpath(f, ROOT))


if __name__ == "__main__":
    main()
