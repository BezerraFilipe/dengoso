"""Análise COMPLEMENTAR — tempo do sintoma até a NOTIFICAÇÃO (delta_notif).

Motivação: a variável principal do trabalho (delta_dias = internação − sintoma) só
existe para os ~3% de casos internados. A data de NOTIFICAÇÃO, ao contrário, está
preenchida em ~99,9% dos casos — e marca quando o caso ENTROU no sistema de saúde
(proxy de "procurou/recebeu atendimento"). Por isso, refazemos as duas perguntas do
projeto usando delta_notif = dt_notificacao − dt_sintoma, agora sobre quase toda a
base de casos confirmados (base limpa), em vez de um subconjunto selecionado.

Mantém-se a variável original (internação) como pedido no enunciado; esta é uma
análise paralela, mais representativa.

Q1: o tempo até a notificação difere entre desfechos (cura × óbito)? → Mann-Whitney
Q2: o tempo até a notificação difere entre bairros? → Kruskal-Wallis
Métodos não-paramétricos (distribuição não-normal, igual à variável original).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "comum"))

from pipeline import (REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias,
                      tarefa3_base_limpa)
from utils import normaliza_categoria, parse_datas

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)
ALFA = 0.05
N_MIN = 30


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    limpa = tarefa3_base_limpa(full.copy(), log)
    s = parse_datas(limpa["dt_sintoma"])
    n = parse_datas(limpa["dt_notificacao"])
    limpa["delta_notif"] = (n - s).dt.days
    limpa["ev"] = normaliza_categoria(limpa["evolucao"])
    limpa["bairro"] = limpa["nome_bairro_residencia"].astype(str).str.upper().str.strip()
    limpa.loc[limpa["bairro"].isin(["NAN", "NONE", ""]), "bairro"] = np.nan
    val = limpa[limpa["delta_notif"].notna() & (limpa["delta_notif"] >= 0)].copy()
    return limpa, val


def descritiva(val):
    s = val["delta_notif"]
    print(f"delta_notif (sintoma→notificação): n={len(s)}  "
          f"mediana={s.median():.0f}  média={s.mean():.1f}  "
          f"IQR={s.quantile(.25):.0f}–{s.quantile(.75):.0f}  máx={s.max():.0f}")


def q1_desfecho(val):
    cura = val.loc[val["ev"] == "1", "delta_notif"].to_numpy(float)
    obito = val.loc[val["ev"].isin(["2", "3", "4"]), "delta_notif"].to_numpy(float)
    u, p = stats.mannwhitneyu(obito, cura, alternative="two-sided")
    rb = 2 * u / (len(obito) * len(cura)) - 1
    print("\n=== Q1 — tempo até notificação por desfecho (Mann-Whitney) ===")
    print(f"cura: n={len(cura)}, mediana={np.median(cura):.0f} d  |  "
          f"óbito: n={len(obito)}, mediana={np.median(obito):.0f} d")
    print(f"p={p:.4g}  efeito(rank-biserial)={rb:.3f}  → "
          f"{'Rejeitar H0' if p < ALFA else 'Não rejeitar H0'} (α={ALFA})")
    return cura, obito, p


def q2_bairro(val):
    d = val.dropna(subset=["bairro"])
    cont = d.groupby("bairro")["delta_notif"].count()
    elig = cont[cont >= N_MIN].index
    d = d[d["bairro"].isin(elig)]
    grupos = [g["delta_notif"].values for _, g in d.groupby("bairro")]
    H, p = stats.kruskal(*grupos)
    eps = (H - len(grupos) + 1) / (len(d) - len(grupos))
    print("\n=== Q2 — tempo até notificação por bairro (Kruskal-Wallis) ===")
    print(f"bairros (n≥{N_MIN}): {len(grupos)}  |  N={len(d)}")
    print(f"H={H:.2f}  p={p:.3e}  ε²={eps:.3f}  → "
          f"{'Rejeitar H0' if p < ALFA else 'Não rejeitar H0'} (α={ALFA})")
    ag = d.groupby("bairro")["delta_notif"].agg(["count", "median", "mean"]).round(2)
    ag = ag.sort_values("median", ascending=False)
    print("\nbairros que mais DEMORAM a notificar (top-8 por mediana):")
    print(ag.head(8).to_string())
    print("\nbairros mais RÁPIDOS (top-5):")
    print(ag.tail(5).to_string())
    return ag, p


def figura(val, cura, obito, p_q1):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    # painel A — distribuição geral
    ax1.hist(val["delta_notif"].clip(upper=30), bins=31, color="#69b", edgecolor="white")
    ax1.axvline(val["delta_notif"].median(), color="#c22", lw=2,
                label=f"mediana = {val['delta_notif'].median():.0f} dias")
    ax1.set_xlabel("Tempo do sintoma até a notificação (dias)")
    ax1.set_ylabel("Nº de casos")
    ax1.set_title(f"Distribuição em ~100% dos casos confirmados (n={len(val):,})\n"
                  "vs. apenas 3% pela internação")
    ax1.legend()
    # painel B — por desfecho
    ax2.boxplot([cura, obito], tick_labels=[f"Cura\n(n={len(cura):,})",
                f"Óbito\n(n={len(obito)})"], showfliers=False, widths=0.5)
    ax2.set_ylim(-1, 30)
    ax2.set_ylabel("Tempo até a notificação (dias)")
    ax2.set_title(f"Por desfecho — p={p_q1:.3f}\n"
                  f"{'sem diferença relevante' if p_q1 >= ALFA else 'ver tamanho de efeito'}")
    fig.suptitle("Análise complementar: tempo do sintoma até a NOTIFICAÇÃO "
                 "(mais representativo que a internação)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = os.path.join(FIGURAS, "viz_complementar_notificacao.png")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def main():
    limpa, val = carregar()
    print(f"base limpa: {len(limpa):,}  |  delta_notif válido: {len(val):,} "
          f"({100*len(val)/len(limpa):.1f}%)")
    descritiva(val)
    cura, obito, p1 = q1_desfecho(val)
    ag, p2 = q2_bairro(val)
    fig = figura(val, cura, obito, p1)
    print(f"\nfigura -> {os.path.relpath(fig, ROOT)}")


if __name__ == "__main__":
    main()
