"""Teste de hipótese — tempo (delta_dias) vs desfecho (Fase 6).

Pergunta central do projeto: pacientes com desfecho grave (óbito) esperaram mais
dias para ser internados do que os que se curaram?

H₀: delta_dias médio é igual entre os grupos de desfecho.
H₁: difere.

Seleção do teste (do enunciado):
  - se ambos os grupos forem normais (Shapiro, α=0,05) → scipy.stats.ttest_ind;
  - se não → scipy.stats.mannwhitneyu.
Como o processo 9 já rejeitou a normalidade, a seleção recai sobre Mann-Whitney;
a verificação é refeita aqui para deixar a escolha explícita e auditável.

Reporta: p-valor (bilateral), decisão sobre H₀ (α=0,05), tamanho de efeito
(r de rank-biserial), medianas/médias por grupo e **IC 95% para a diferença de
medianas** (bootstrap, coerente com teste não-paramétrico). Complemento:
Kruskal-Wallis entre os grupos com n adequado.

Subconjunto: delta_dias válidos (≥ 0), internados (~3% da base).
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

ALFA = 0.05
N_BOOT = 10000
SEED = 42

ROTULOS = {"1": "Cura", "2": "Óbito por dengue",
           "3": "Óbito por outras causas", "4": "Óbito em investigação"}


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    full["ev"] = normaliza_categoria(full["evolucao"])
    val = full[full["delta_dias"].notna()
               & ~full["delta_invalido"].fillna(False)].copy()
    val["delta_dias"] = val["delta_dias"].astype(float)
    return val


def serie(val: pd.DataFrame, codigos) -> np.ndarray:
    """delta_dias dos registros cujo `ev` está em `codigos`."""
    return val.loc[val["ev"].isin(codigos), "delta_dias"].to_numpy(dtype=float)


def normal(s: np.ndarray) -> bool:
    """Shapiro-Wilk: True se NÃO rejeita normalidade (p ≥ α)."""
    if len(s) < 3:
        return False
    return stats.shapiro(s)[1] >= ALFA


def ic_boot_diff_medianas(a: np.ndarray, b: np.ndarray):
    """IC 95% (percentil) da diferença de medianas (a − b), por bootstrap."""
    rng = np.random.default_rng(SEED)
    difs = np.empty(N_BOOT)
    na, nb = len(a), len(b)
    for i in range(N_BOOT):
        ra = a[rng.integers(0, na, na)]
        rb = b[rng.integers(0, nb, nb)]
        difs[i] = np.median(ra) - np.median(rb)
    lo, hi = np.percentile(difs, [2.5, 97.5])
    return float(lo), float(hi)


def rank_biserial(u: float, n1: int, n2: int) -> float:
    """Tamanho de efeito de Mann-Whitney: r = 2U/(n1·n2) − 1  (∈ [-1, 1]).

    U é o de Mann-Whitney do 1º grupo (óbito). Sinal positivo = óbito tende a
    esperar MAIS que cura; |r| pequeno = efeito desprezível.
    """
    return (2.0 * u) / (n1 * n2) - 1.0


def comparar(nome: str, a: np.ndarray, b: np.ndarray,
             rotulo_a: str, rotulo_b: str) -> dict:
    """Compara o grupo `a` (óbito) com `b` (cura). a é o 'grave'."""
    na, nb = len(a), len(b)
    amb_normais = normal(a) and normal(b)
    if amb_normais:
        teste = "t de Student (ttest_ind)"
        stat, p = stats.ttest_ind(a, b, equal_var=False)
    else:
        teste = "Mann-Whitney U"
        u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
        stat = float(u)
    # p unilateral (H₁: óbito espera MAIS que cura) — responde à pergunta direta.
    if amb_normais:
        _, p_um = stats.ttest_ind(a, b, equal_var=False, alternative="greater")
    else:
        _, p_um = stats.mannwhitneyu(a, b, alternative="greater")
    u_ab = stats.mannwhitneyu(a, b, alternative="two-sided")[0]
    rb = rank_biserial(u_ab, na, nb)
    prob_sup = u_ab / (na * nb)  # P(óbito ≥ cura): 0,5 = indistinguível
    lo, hi = ic_boot_diff_medianas(a, b)
    return {
        "comparação": nome,
        "n_óbito": na, "n_cura": nb,
        "mediana_óbito": float(np.median(a)), "mediana_cura": float(np.median(b)),
        "média_óbito": round(float(np.mean(a)), 2),
        "média_cura": round(float(np.mean(b)), 2),
        "ambos_normais": amb_normais, "teste": teste,
        "estatística": round(float(stat), 2),
        "p_bilateral": p, "p_unilateral_óbito>cura": p_um,
        "rank_biserial": round(rb, 3),
        "prob_superioridade (óbito≥cura)": round(prob_sup, 3),
        "dif_medianas (óbito−cura)": float(np.median(a) - np.median(b)),
        "IC95_dif_medianas": (round(lo, 2), round(hi, 2)),
        "decisão_H0": "Rejeitar H₀" if p < ALFA else "Não rejeitar H₀",
    }


def kruskal(val: pd.DataFrame):
    """Complemento: Kruskal-Wallis entre os grupos com n adequado (1,2,3)."""
    grupos, rotulos = [], []
    for c in ["1", "2", "3"]:
        s = serie(val, [c])
        grupos.append(s)
        rotulos.append(f"{c}-{ROTULOS[c]} (n={len(s)})")
    h, p = stats.kruskal(*grupos)
    return rotulos, float(h), float(p)


def figura(comps, val):
    """Boxplot cura × óbito (agregado) com medianas e IC da diferença anotado."""
    cura = serie(val, ["1"])
    obito = serie(val, ["2", "3", "4"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([cura, obito], tick_labels=[f"Cura\n(n={len(cura)})",
               f"Óbito (2+3+4)\n(n={len(obito)})"],
               showfliers=False, widths=0.5)
    ax.set_ylim(-1, 25)  # recorte: outliers de registro (máx 1.116 d) achatariam tudo
    ax.set_ylabel("delta_dias (dias sintoma → internação)")
    c = comps[0]
    ax.set_title("Tempo até a internação: cura × óbito\n"
                 f"{c['teste']} — p={c['p_bilateral']:.3f} → {c['decisão_H0']} "
                 f"(α={ALFA})")
    ax.text(0.5, 0.95,
            f"medianas: cura={np.median(cura):.0f} d, óbito={np.median(obito):.0f} d  |  "
            f"IC95% da diferença: {c['IC95_dif_medianas']} d",
            transform=ax.transAxes, ha="center", va="top", fontsize=9,
            bbox=dict(boxstyle="round", fc="#eef", ec="#99c"))
    fig.tight_layout()
    out = os.path.join(FIGURAS, "teste_hipotese_cura_obito.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def _fmt(c: dict) -> str:
    return (
        f"\n### {c['comparação']}\n"
        f"  n: óbito={c['n_óbito']}, cura={c['n_cura']}\n"
        f"  medianas: óbito={c['mediana_óbito']:.1f} d, cura={c['mediana_cura']:.1f} d "
        f"(dif={c['dif_medianas (óbito−cura)']:+.1f} d)\n"
        f"  médias:   óbito={c['média_óbito']} d, cura={c['média_cura']} d\n"
        f"  ambos normais? {c['ambos_normais']}  →  teste: {c['teste']}\n"
        f"  estatística={c['estatística']}  p_bilateral={c['p_bilateral']:.4g}  "
        f"p_unilateral(óbito>cura)={c['p_unilateral_óbito>cura']:.4g}\n"
        f"  tamanho de efeito (rank-biserial)={c['rank_biserial']}  |  "
        f"P(óbito≥cura)={c['prob_superioridade (óbito≥cura)']}\n"
        f"  IC95% da diferença de medianas (óbito−cura)={c['IC95_dif_medianas']} dias\n"
        f"  >>> {c['decisão_H0']} (α={ALFA})"
    )


def main():
    val = carregar()
    cura = serie(val, ["1"])
    obito_agg = serie(val, ["2", "3", "4"])
    obito_dengue = serie(val, ["2"])

    print(f"n (delta válidos): {len(val)}  |  cura={len(cura)}  "
          f"óbito(2+3+4)={len(obito_agg)}  óbito_dengue(2)={len(obito_dengue)}")

    comps = [
        comparar("Cura × Óbito (agregado 2+3+4) — principal",
                 obito_agg, cura, "óbito", "cura"),
        comparar("Cura × Óbito por dengue (grupo 2) — complemento clínico",
                 obito_dengue, cura, "óbito dengue", "cura"),
    ]
    print("\n===== TESTE DE HIPÓTESE: delta_dias entre desfechos =====")
    for c in comps:
        print(_fmt(c))

    rot, h, p = kruskal(val)
    print("\n### Complemento — Kruskal-Wallis entre grupos 1, 2, 3")
    print(f"  grupos: {', '.join(rot)}")
    print(f"  H={h:.3f}  p={p:.4g}  →  "
          f"{'Rejeitar H₀' if p < ALFA else 'Não rejeitar H₀'} (α={ALFA})")

    fig = figura(comps, val)
    print(f"\nfigura -> {os.path.relpath(fig, ROOT)}")


if __name__ == "__main__":
    main()
