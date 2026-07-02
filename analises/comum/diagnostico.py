"""Diagnóstico dos CSVs de dengue ANTES de qualquer cálculo.

Para cada arquivo (um por ano):
  - detecta o delimitador pelo cabeçalho (";" vs ",");
  - identifica o vocabulário (descritivo vs código SINAN);
  - mapeia colunas para o esquema único e reporta presença + % de preenchimento
    das colunas usadas pelas Tarefas 1-3.

Não modifica nada; apenas imprime um resumo. Encoding latin-1.
"""
from __future__ import annotations

import csv
import glob
import os
import re

import pandas as pd

from mappings import COLUNAS_USADAS, semantic_key

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DENGUE_DIR = os.path.join(ROOT, "data", "dengue")
ENCODING = "latin-1"


def detectar_delimitador(path: str) -> str:
    """Detecta ';' ou ',' pela primeira linha (cabeçalho)."""
    with open(path, encoding=ENCODING) as f:
        header = f.readline()
    # csv.Sniffer pode falhar com aspas; fallback por contagem.
    try:
        dialect = csv.Sniffer().sniff(header, delimiters=";,")
        return dialect.delimiter
    except csv.Error:
        return ";" if header.count(";") >= header.count(",") else ","


def ano_do_arquivo(path: str) -> int:
    m = re.search(r"(\d{4})", os.path.basename(path))
    return int(m.group(1)) if m else -1


def main():
    arquivos = sorted(glob.glob(os.path.join(DENGUE_DIR, "dengue-*.csv")),
                      key=ano_do_arquivo)
    print(f"Arquivos de dengue encontrados: {len(arquivos)}\n")

    # Tabela de preenchimento: linhas = ano, colunas = COLUNAS_USADAS.
    fill_rows = {}
    meta_rows = {}

    for path in arquivos:
        ano = ano_do_arquivo(path)
        delim = detectar_delimitador(path)
        # Lê cabeçalho para identificar vocabulário.
        with open(path, encoding=ENCODING) as f:
            header_line = f.readline()
        cols_orig = [c.strip().strip('"') for c in header_line.rstrip("\n").split(delim)]
        # Vocabulário: maiúsculo (código SINAN) vs minúsculo (descritivo).
        upper = sum(1 for c in cols_orig if c.isupper())
        vocab = "codigo_SINAN" if upper > len(cols_orig) / 2 else "descritivo"

        # Lê o arquivo inteiro como string para medir preenchimento real.
        df = pd.read_csv(path, sep=delim, encoding=ENCODING, dtype=str,
                         keep_default_na=True, low_memory=False)
        n = len(df)
        # Renomeia para chave semântica.
        rename = {c: semantic_key(c) for c in df.columns if semantic_key(c)}
        df = df.rename(columns=rename)

        meta_rows[ano] = {"delimitador": delim, "vocab": vocab,
                          "n_colunas": len(cols_orig), "n_linhas": n}
        fill = {}
        for key in COLUNAS_USADAS:
            if key not in df.columns:
                fill[key] = None  # coluna ausente
            else:
                s = df[key].astype(str).str.strip()
                vazio = s.isin(["", "nan", "None", "NaN"]) | df[key].isna()
                fill[key] = round(100 * (~vazio).mean(), 1)
        fill_rows[ano] = fill

    # Imprime metadados.
    print("=== Metadados por ano ===")
    meta_df = pd.DataFrame(meta_rows).T
    print(meta_df.to_string())
    print()
    print("=== % de preenchimento das colunas usadas (Tarefas 1-3) ===")
    fill_df = pd.DataFrame(fill_rows).T  # index=ano
    fill_df.index.name = "ano"
    print(fill_df.to_string())
    print("\n(None = coluna AUSENTE no arquivo; número = % de linhas preenchidas)")

    return meta_df, fill_df


if __name__ == "__main__":
    main()
