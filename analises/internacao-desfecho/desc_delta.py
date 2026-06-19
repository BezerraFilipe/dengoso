"""Estatísticas descritivas de delta_dias estratificadas por desfecho (evolucao).

Posição (média, mediana, moda) e dispersão (desvio padrão, IQR, min, max) do tempo
sintoma→internação, por grupo de evolução:
    1=cura, 2=óbito por dengue, 3=óbito por outras causas, 4=óbito em investigação.

Usa groupby('evolucao')['delta_dias'].describe() + `statistics` (moda) + IQR manual.
Considera apenas delta_dias válidos (não-nulos e não-negativos, i.e. excluindo
delta_invalido). Gera tabela (markdown), boxplot e documento com interpretação.
"""
from __future__ import annotations

import os
import statistics

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- bootstrap: encontra a infra compartilhada em analises/geral/ ---
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "geral"))
# --- fim bootstrap ---
from pipeline import REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias
from utils import normaliza_categoria

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)

ROTULOS = {
    "1": "Cura",
    "2": "Óbito por dengue",
    "3": "Óbito por outras causas",
    "4": "Óbito em investigação",
}
ESTRATOS = ["1", "2", "3", "4"]


def moda(serie: pd.Series):
    vals = statistics.multimode(serie.tolist())
    return vals[0] if len(vals) == 1 else vals  # único valor ou lista (multimodal)


def construir_tabela(val: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for cod in ESTRATOS:
        s = val.loc[val["evolucao_n"] == cod, "delta_dias"].dropna()
        if s.empty:
            linhas.append({"desfecho": f"{cod} — {ROTULOS[cod]}", "n": 0})
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        linhas.append({
            "desfecho": f"{cod} — {ROTULOS[cod]}",
            "n": int(s.count()),
            "média": round(s.mean(), 2),
            "mediana": round(s.median(), 2),
            "moda": moda(s),
            "desvio_padrão": round(s.std(), 2),
            "IQR": round(q3 - q1, 2),
            "min": round(s.min(), 2),
            "max": round(s.max(), 2),
        })
    return pd.DataFrame(linhas)


def _md_table(df: pd.DataFrame) -> str:
    headers = [str(c) for c in df.columns]
    rows = ["| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, r in df.iterrows():
        rows.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(rows)


def boxplot(val: pd.DataFrame):
    dados = [val.loc[val["evolucao_n"] == c, "delta_dias"].dropna().values
             for c in ESTRATOS]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(dados, tick_labels=[f"{c}\n{ROTULOS[c]}" for c in ESTRATOS],
               showmeans=True, showfliers=False)
    ax.set_ylim(-0.5, 20)  # recorte para legibilidade (outliers omitidos)
    ax.set_ylabel("delta_dias (dias) — eixo recortado em 20")
    ax.set_title("Tempo sintoma→internação por desfecho — Dengue/Recife\n"
                 "(caixa=IQR, linha=mediana, ▲=média; outliers omitidos)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = os.path.join(FIGURAS, "delta_por_desfecho.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def main():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    full["evolucao_n"] = normaliza_categoria(full["evolucao"])
    val = full[full["delta_dias"].notna()
               & ~full["delta_invalido"].fillna(False)].copy()

    tab = construir_tabela(val)
    print("=== delta_dias por desfecho (válidos: não-nulos e ≥0) ===")
    print(tab.to_string(index=False))
    fig = boxplot(val)
    print(f"\nboxplot -> {os.path.relpath(fig, ROOT)}")
    return tab, val


if __name__ == "__main__":
    main()
