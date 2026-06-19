"""Presença-relativa por (variável, ano) — base empírica da decisão de escopo.

Para cada arquivo de dengue: lê (latin-1, delimitador detectado), mapeia as
colunas para o esquema único e calcula, por variável:

    presenca_relativa = nao_nulos / total_linhas * 100

Gera:
  - reports/distribuicoes.csv  (schema: variavel, arbovirose, ano, casos,
                                presenca-absoluta, presenca-relativa)
  - reports/figuras/presenca_relativa.png  (barras agrupadas por ano das
                                            variáveis-chave)
  - imprime a tabela presença-relativa (variáveis-chave × ano).
"""
from __future__ import annotations

import glob
import os

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mappings import ALL_MAPPINGS, semantic_key
from pipeline import ENCODING, DENGUE_DIR, REPORTS, ROOT, ano_do_arquivo, \
    detectar_delimitador

FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(FIGURAS, exist_ok=True)
os.makedirs(FIGURAS, exist_ok=True)

# Variáveis-chave da decisão de escopo (nomes semânticos).
VARS_CHAVE = ["dt_internacao", "evolucao", "bairro_residencia", "zona_residencia"]
LIMIAR = 85.0


def gerar_distribuicoes() -> pd.DataFrame:
    """Calcula presença por (variável, ano) e salva reports/distribuicoes.csv."""
    todas_chaves = sorted(set(ALL_MAPPINGS.values()))
    rows = []
    for path in sorted(glob.glob(os.path.join(DENGUE_DIR, "dengue-*.csv")),
                       key=ano_do_arquivo):
        ano = ano_do_arquivo(path)
        delim = detectar_delimitador(path)
        df = pd.read_csv(path, sep=delim, encoding=ENCODING, dtype=str,
                         low_memory=False)
        df = df.replace(r"^\s*$", pd.NA, regex=True)  # vazios -> NA
        # Mapeia df para chaves semânticas (1ª ocorrência de cada chave).
        col_map = {}
        for col in df.columns:
            key = semantic_key(col)
            if key and key not in col_map:
                col_map[key] = col
        casos = len(df)
        for var in todas_chaves:
            if var in col_map:
                abs_ = int(df[col_map[var]].notna().sum())
            else:
                abs_ = 0
            rel = round(abs_ / casos * 100, 2) if casos else 0.0
            rows.append({"variavel": var, "arbovirose": "dengue", "ano": ano,
                         "casos": casos, "presenca-absoluta": abs_,
                         "presenca-relativa": rel})
    dist = pd.DataFrame(rows)
    out = os.path.join(REPORTS, "distribuicoes.csv")
    dist.to_csv(out, index=False, encoding="utf-8")
    print(f"distribuicoes.csv -> {os.path.relpath(out, ROOT)} ({len(dist)} linhas)")
    return dist


def tabela_chave(dist: pd.DataFrame) -> pd.DataFrame:
    """Pivot presença-relativa (linhas=ano, colunas=variáveis-chave)."""
    sub = dist[dist["variavel"].isin(VARS_CHAVE)]
    piv = sub.pivot(index="ano", columns="variavel",
                    values="presenca-relativa")[VARS_CHAVE]
    return piv


def grafico_barras(piv: pd.DataFrame):
    """Barras agrupadas: presença-relativa por variável-chave em cada ano."""
    anos = list(piv.index)
    n_var = len(piv.columns)
    largura = 0.8 / n_var
    fig, ax = plt.subplots(figsize=(13, 6))
    for i, var in enumerate(piv.columns):
        pos = [x + (i - n_var / 2) * largura + largura / 2 for x in range(len(anos))]
        ax.bar(pos, piv[var].values, width=largura, label=var)
    ax.axhline(LIMIAR, color="red", linestyle="--", linewidth=1,
               label=f"limiar {LIMIAR:.0f}%")
    ax.set_xticks(range(len(anos)))
    ax.set_xticklabels(anos, rotation=45)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Presença relativa (%)")
    ax.set_xlabel("Ano")
    ax.set_title("Presença relativa das variáveis-chave por ano — Dengue/Recife")
    ax.legend(ncol=3, fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = os.path.join(FIGURAS, "presenca_relativa.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print(f"figura -> {os.path.relpath(out, ROOT)}")
    return out


def main():
    dist = gerar_distribuicoes()
    piv = tabela_chave(dist)
    print("\n=== Presença-relativa (%) — variáveis-chave × ano ===")
    print(piv.round(1).to_string())
    print(f"\nVariáveis ≥{LIMIAR:.0f}% em TODOS os anos:")
    for var in piv.columns:
        ok = (piv[var] >= LIMIAR).all()
        anos_falha = list(piv.index[piv[var] < LIMIAR])
        print(f"  - {var:22s}: {'SIM' if ok else 'NÃO'}"
              + ("" if ok else f"  (falha em {anos_falha})"))
    grafico_barras(piv)


if __name__ == "__main__":
    main()
