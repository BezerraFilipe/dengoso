"""Teste formal de normalidade de delta_dias por grupo de desfecho.

Regra (do enunciado): Shapiro-Wilk para grupos com n < 5.000; Kolmogorov-Smirnov
(kstest) para grupos maiores. α = 0,05. Aplicado a delta_dias dentro de cada grupo de
evolucao (1=cura, 2=óbito dengue, 3=óbito outras causas, 4=óbito em investigação).

Complementos: checagem de robustez (sem outliers, delta ≤ 60 dias) e QQ-plots.
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
ALFA = 0.05
N_CORTE = 5000  # < N_CORTE → Shapiro; ≥ → KS


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    full["ev"] = normaliza_categoria(full["evolucao"])
    return full[full["delta_dias"].notna()
                & ~full["delta_invalido"].fillna(False)].copy()


def testar(s: pd.Series):
    """Retorna (nome_teste, estatística, p_valor) conforme o n."""
    n = len(s)
    if n < 3:
        return ("n insuficiente", np.nan, np.nan)
    if n < N_CORTE:
        W, p = stats.shapiro(s)
        return ("Shapiro-Wilk", float(W), float(p))
    # KS contra normal com média/desvio estimados (Lilliefors — conservador).
    st, p = stats.kstest(s, "norm", args=(s.mean(), s.std(ddof=1)))
    return ("Kolmogorov-Smirnov", float(st), float(p))


def tabela(val: pd.DataFrame) -> pd.DataFrame:
    linhas = []
    for c in ESTRATOS:
        s = val.loc[val["ev"] == c, "delta_dias"].astype(float)
        nome, st, p = testar(s)
        if np.isnan(p):
            concl = "indeterminado (n insuficiente)"
        else:
            concl = "Normal" if p >= ALFA else "Não-normal"
        linhas.append({
            "desfecho": f"{c} — {ROTULOS[c]}", "n": len(s), "teste": nome,
            "estatística": round(st, 4) if not np.isnan(st) else None,
            "p_valor": f"{p:.2e}" if not np.isnan(p) else None,
            "conclusão (α=0,05)": concl,
        })
    return pd.DataFrame(linhas)


def tabela_robustez(val: pd.DataFrame) -> pd.DataFrame:
    """Repete o teste excluindo outliers (delta ≤ 60 dias)."""
    linhas = []
    for c in ESTRATOS:
        s = val.loc[(val["ev"] == c) & (val["delta_dias"] <= 60),
                    "delta_dias"].astype(float)
        nome, st, p = testar(s)
        concl = ("indeterminado" if np.isnan(p)
                 else ("Normal" if p >= ALFA else "Não-normal"))
        linhas.append({"desfecho": f"{c} — {ROTULOS[c]}", "n (≤60d)": len(s),
                       "p_valor": f"{p:.2e}" if not np.isnan(p) else None,
                       "conclusão": concl})
    return pd.DataFrame(linhas)


def qqplots(val: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for ax, c in zip(axes.ravel(), ESTRATOS):
        s = val.loc[val["ev"] == c, "delta_dias"].astype(float)
        if len(s) >= 3:
            stats.probplot(s, dist="norm", plot=ax)
            ax.get_lines()[0].set_markersize(3)
        ax.set_title(f"{c} — {ROTULOS[c]} (n={len(s)})")
    fig.suptitle("QQ-plots de delta_dias por desfecho (vs. normal)\n"
                 "desvios da reta = afastamento da normalidade", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = os.path.join(FIGURAS, "qqplot_delta_por_desfecho.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def _print(df):
    print(df.to_string(index=False))


def main():
    val = carregar()
    print("=== Teste de normalidade de delta_dias por desfecho (α=0,05) ===")
    _print(tabela(val))
    print("\n=== Robustez: mesmo teste sem outliers (delta ≤ 60 dias) ===")
    _print(tabela_robustez(val))
    fig = qqplots(val)
    print(f"\nQQ-plots -> {os.path.relpath(fig, ROOT)}")


if __name__ == "__main__":
    main()
