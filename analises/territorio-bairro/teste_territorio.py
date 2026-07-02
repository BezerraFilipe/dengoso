"""Teste de hipótese — desigualdade territorial do tempo até a internação (Fase 6).

Segunda pergunta do projeto: o tempo sintoma→internação (`delta_dias`) é
significativamente diferente entre regiões de Recife?

H₀: delta_dias médio é igual entre os grupos geográficos.

Enunciado pede comparar "as três zonas" com Kruskal-Wallis (3+ grupos,
não-paramétrico) e, se rejeitar H₀, post-hoc de Dunn. PORÉM `zona_residencia` é
**degenerada** em Recife (processo 7): 1.807 urbana × 1 rural × 2 periurbana — sem
massa rural/periurbana não há teste possível. A unidade geográfica testável (e a
pedida pelo DoD, "bairros de risco") é o **bairro**. Por isso:

  - a inviabilidade da zona é documentada (contagens), e
  - o teste é feito **entre bairros** com n ≥ 30 (35 elegíveis, processo 7).

Como a normalidade foi rejeitada (processo 9), usa-se Kruskal-Wallis; se rejeitar
H₀ → Dunn (scikit_posthocs.posthoc_dunn, ajuste de Holm). Lista os bairros de risco
(maior delta_dias). Subconjunto: delta_dias válidos (≥ 0), internados.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scikit_posthocs as sp
from scipy import stats

# --- bootstrap: encontra a infra compartilhada em analises/geral/ ---
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "comum"))
# --- fim bootstrap ---
from pipeline import REPORTS, ROOT, tarefa1_dataframe_unico, tarefa2_delta_dias
from utils import normaliza_categoria

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)

ALFA = 0.05
N_MIN = 30  # mínimo de casos por bairro para entrar no teste (processo 7)

ZONA_ROT = {"1": "Urbana", "2": "Rural", "3": "Periurbana", "9": "Ignorado"}


def carregar():
    log = {}
    full = tarefa1_dataframe_unico(log)
    full = tarefa2_delta_dias(full, log)
    val = full[full["delta_dias"].notna()
               & ~full["delta_invalido"].fillna(False)].copy()
    val["delta_dias"] = val["delta_dias"].astype(float)
    val["zona"] = normaliza_categoria(val["zona_residencia"])
    val["bairro"] = val["nome_bairro_residencia"].astype(str).str.upper().str.strip()
    val.loc[val["bairro"].isin(["NAN", "NONE", ""]), "bairro"] = np.nan
    return val


def diagnostico_zona(val: pd.DataFrame):
    """Mostra por que a zona não é testável (degenerescência)."""
    cont = val["zona"].value_counts(dropna=False)
    linhas = []
    for k, n in cont.items():
        rot = "Sem registro" if pd.isna(k) else ZONA_ROT.get(k, f"Código {k}")
        linhas.append({"zona": rot, "n": int(n)})
    return pd.DataFrame(linhas)


def epsilon2(H: float, n: int, k: int) -> float:
    """Tamanho de efeito de Kruskal-Wallis: ε² = (H − k + 1)/(N − k)."""
    return (H - k + 1) / (n - k)


def kruskal_bairros(val: pd.DataFrame, max_delta: float | None = None):
    d = val.dropna(subset=["bairro"]).copy()
    if max_delta is not None:
        d = d[d["delta_dias"] <= max_delta]
    cont = d.groupby("bairro")["delta_dias"].count()
    elegiveis = cont[cont >= N_MIN].index
    d = d[d["bairro"].isin(elegiveis)].copy()
    grupos = [g["delta_dias"].values for _, g in d.groupby("bairro")]
    H, p = stats.kruskal(*grupos)
    eps = epsilon2(H, len(d), len(grupos))
    return d, sorted(elegiveis), H, p, eps


def dunn(d: pd.DataFrame) -> pd.DataFrame:
    """Post-hoc de Dunn (Holm) entre bairros → matriz de p-valores ajustados."""
    return sp.posthoc_dunn(d, val_col="delta_dias", group_col="bairro",
                           p_adjust="holm")


def ranking_risco(d: pd.DataFrame) -> pd.DataFrame:
    """Bairros ordenados por tempo (posto médio = base do Dunn; + mediana/média)."""
    d = d.copy()
    d["posto"] = stats.rankdata(d["delta_dias"])  # posto global (como no Dunn/KW)
    ag = d.groupby("bairro").agg(
        n=("delta_dias", "size"),
        mediana=("delta_dias", "median"),
        media=("delta_dias", "mean"),
        posto_medio=("posto", "mean"),
    ).round(2)
    return ag.sort_values("posto_medio", ascending=False)


def pares_significativos(pmat: pd.DataFrame, bairro: str) -> int:
    """Quantos outros bairros diferem significativamente de `bairro` (Holm)."""
    s = pmat.loc[bairro].drop(labels=[bairro])
    return int((s < ALFA).sum())


def figura(rank: pd.DataFrame, p: float):
    top = rank.sort_values("mediana", ascending=False).head(15)[::-1]
    fig, ax = plt.subplots(figsize=(9, 7))
    y = np.arange(len(top))
    ax.barh(y, top["mediana"], color="#c44", label="mediana")
    ax.plot(top["media"].clip(upper=15), y, "ko", label="média (recortada ≤15)")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{b} (n={int(n)})" for b, n in zip(top.index, top["n"])],
                       fontsize=8)
    ax.set_xlabel("delta_dias (dias sintoma → internação)")
    ax.set_title("Bairros de risco — maior tempo até a internação (top-15 por mediana)\n"
                 f"Kruskal-Wallis entre bairros: p={p:.2e} → diferença significativa")
    ax.legend(loc="lower right")
    fig.tight_layout()
    out = os.path.join(FIGURAS, "teste_territorio_bairros.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def main():
    val = carregar()
    print(f"n (delta válidos): {len(val)}")

    print("\n=== Zona — diagnóstico de viabilidade (enunciado pede 'três zonas') ===")
    print(diagnostico_zona(val).to_string(index=False))
    print("→ Zona DEGENERADA (rural=1, periurbana=2): Kruskal-Wallis entre zonas é "
          "inviável. Unidade geográfica testável = BAIRRO (processo 7).")

    d, elig, H, p, eps = kruskal_bairros(val)
    print(f"\n=== Kruskal-Wallis entre bairros (n ≥ {N_MIN}) ===")
    print(f"bairros elegíveis: {len(elig)}  |  N usado: {len(d)}")
    print(f"H = {H:.3f}   p = {p:.3e}   ε² (efeito) = {eps:.3f}")
    decisao = "Rejeitar H₀" if p < ALFA else "Não rejeitar H₀"
    print(f">>> {decisao} (α={ALFA})")

    # robustez sem outliers de registro
    _, _, Hr, pr, epsr = kruskal_bairros(val, max_delta=60)
    print(f"robustez (delta ≤ 60 d): H={Hr:.2f}  p={pr:.3e}  ε²={epsr:.3f} "
          f"→ {'mantém' if pr < ALFA else 'cai'}")

    if p < ALFA:
        pmat = dunn(d)
        out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dunn_bairros.csv")
        pmat.round(4).to_csv(out_csv)
        n_pares = len(elig) * (len(elig) - 1) // 2
        sig = int(((pmat.values < ALFA) & ~np.eye(len(elig), dtype=bool)).sum() // 2)
        print(f"\n=== Post-hoc de Dunn (Holm) — {n_pares} pares ===")
        print(f"pares significativos (p_ajust < {ALFA}): {sig} de {n_pares} "
              f"({100*sig/n_pares:.0f}%)")
        print(f"matriz completa -> {os.path.relpath(out_csv, ROOT)}")

        rank = ranking_risco(d)
        rank["pares_difere"] = [pares_significativos(pmat, b) for b in rank.index]
        print("\n=== Bairros de RISCO (maior tempo até internação) — top-12 ===")
        print(rank.head(12).to_string())
        out_rank = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking_risco_bairros.csv")
        rank.to_csv(out_rank)
        print(f"\nranking completo -> {os.path.relpath(out_rank, ROOT)}")

        fig = figura(rank, p)
        print(f"figura -> {os.path.relpath(fig, ROOT)}")


if __name__ == "__main__":
    main()
