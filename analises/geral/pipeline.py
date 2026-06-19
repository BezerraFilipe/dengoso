"""Pipeline DENGUE/Recife (SINAN 2013-2025) — Tarefas 1, 2 e 3.

Tarefa 1: DataFrame único e coerente (renomeio p/ esquema único via ALL_MAPPINGS,
          dedup, coluna ano_csv, concatenação).
Tarefa 2: variável delta_dias = dt_internacao - dt_sintoma, com flag delta_invalido.
Tarefa 3: base limpa (remove investigação/ignorado/descartado; decodifica idade).

Gera reports/relatorio.md com todas as contagens. Encoding latin-1; delimitador
detectado por arquivo.
"""
from __future__ import annotations

import csv
import glob
import os
import re
from datetime import datetime

import pandas as pd

from mappings import ALL_MAPPINGS, COLUNAS_USADAS, semantic_key
from utils import decodifica_idade, normaliza_categoria, parse_datas

# raiz do projeto = dengoso/  (este arquivo está em dengoso/analises/geral/)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DENGUE_DIR = os.path.join(ROOT, "data", "dengue")
REPORTS = os.path.join(ROOT, "reports")
ENCODING = "latin-1"
os.makedirs(REPORTS, exist_ok=True)

# Códigos SINAN usados nos filtros da Tarefa 3.
CRITERIO_EM_INVESTIGACAO = "3"
EVOLUCAO_IGNORADO = "9"
CLASSIF_DESCARTADO = "5"


def detectar_delimitador(path: str) -> str:
    with open(path, encoding=ENCODING) as f:
        header = f.readline()
    try:
        return csv.Sniffer().sniff(header, delimiters=";,").delimiter
    except csv.Error:
        return ";" if header.count(";") >= header.count(",") else ","


def ano_do_arquivo(path: str) -> int:
    m = re.search(r"(\d{4})", os.path.basename(path))
    return int(m.group(1)) if m else -1


# ─────────────────────────── TAREFA 1 ────────────────────────────────────────
def tarefa1_dataframe_unico(log: dict):
    arquivos = sorted(glob.glob(os.path.join(DENGUE_DIR, "dengue-*.csv")),
                      key=ano_do_arquivo)
    partes = []
    t1 = []  # por-ano: contagens
    for path in arquivos:
        ano = ano_do_arquivo(path)
        delim = detectar_delimitador(path)
        df = pd.read_csv(path, sep=delim, encoding=ENCODING, dtype=str,
                         low_memory=False)
        n_lido = len(df)

        # Renomeio para chave semântica (esquema único).
        rename = {c: semantic_key(c) for c in df.columns if semantic_key(c)}
        df = df.rename(columns=rename)
        # Mantém só colunas mapeadas (evita colisões de nomes não mapeados).
        df = df.loc[:, [c for c in df.columns if c in set(ALL_MAPPINGS.values())]]
        df = df.loc[:, ~df.columns.duplicated()]

        # Dedup por tp_duplicidade onde a coluna existe (2013-2014).
        rem_dup_col = 0
        if "duplicidade" in df.columns:
            dup = normaliza_categoria(df["duplicidade"])
            # No SINAN, registro marcado com '1' indica duplicidade a remover.
            mask_dup = dup == "1"
            rem_dup_col = int(mask_dup.sum())
            df = df[~mask_dup]

        # Dedup por chave exata (notificação + data sintoma) nos demais anos.
        chave = [c for c in ("notificacao", "dt_sintoma") if c in df.columns]
        antes = len(df)
        if chave:
            df = df.drop_duplicates(subset=chave, keep="first")
        rem_dup_chave = antes - len(df)

        df["ano_csv"] = ano
        partes.append(df)
        t1.append({"ano": ano, "delimitador": delim, "n_lido": n_lido,
                   "rem_tp_duplicidade": rem_dup_col,
                   "rem_dup_chave": rem_dup_chave, "n_final": len(df)})

    full = pd.concat(partes, ignore_index=True)
    log["tarefa1"] = pd.DataFrame(t1)
    log["total_lido"] = sum(r["n_lido"] for r in t1)
    log["total_apos_dedup"] = len(full)
    log["t1_ncols"] = full.shape[1]  # esquema único + ano_csv (antes da Tarefa 2)
    return full


# ─────────────────────────── TAREFA 2 ────────────────────────────────────────
def tarefa2_delta_dias(df: pd.DataFrame, log: dict):
    df["dt_sintoma"] = parse_datas(df["dt_sintoma"])
    df["dt_internacao"] = parse_datas(df["dt_internacao"])
    df["delta_dias"] = (df["dt_internacao"] - df["dt_sintoma"]).dt.days

    tem_delta = df["delta_dias"].notna()
    df["delta_invalido"] = tem_delta & (df["delta_dias"] < 0)

    log["delta_internados"] = int(tem_delta.sum())     # têm dt_internacao válida
    log["delta_negativos"] = int(df["delta_invalido"].sum())
    log["delta_validos"] = int((tem_delta & ~df["delta_invalido"]).sum())
    log["delta_pct_base"] = round(100 * tem_delta.mean(), 2)
    # Descritiva sobre o subconjunto internado válido.
    validos = df.loc[tem_delta & ~df["delta_invalido"], "delta_dias"]
    log["delta_desc"] = validos.describe() if len(validos) else None
    return df


# ─────────────────────────── TAREFA 3 ────────────────────────────────────────
def tarefa3_base_limpa(df: pd.DataFrame, log: dict):
    n0 = len(df)
    crit = normaliza_categoria(df.get("criterio", pd.Series(index=df.index, dtype=str)))
    evol = normaliza_categoria(df.get("evolucao", pd.Series(index=df.index, dtype=str)))
    clas = normaliza_categoria(df.get("classificacao", pd.Series(index=df.index, dtype=str)))

    mask_invest = crit == CRITERIO_EM_INVESTIGACAO
    mask_ignor = evol == EVOLUCAO_IGNORADO
    mask_descart = clas == CLASSIF_DESCARTADO
    mask_delta_inv = df["delta_invalido"].fillna(False)

    rem_total = mask_invest | mask_ignor | mask_descart | mask_delta_inv
    limpa = df[~rem_total].copy()

    # Decodifica idade -> anos.
    limpa["idade_anos"] = decodifica_idade(limpa["idade"])

    log["t3_inicial"] = n0
    log["t3_rem_investigacao"] = int(mask_invest.sum())
    log["t3_rem_ignorado"] = int(mask_ignor.sum())
    log["t3_rem_descartado"] = int(mask_descart.sum())
    log["t3_rem_delta_invalido"] = int(mask_delta_inv.sum())
    log["t3_rem_total_unico"] = int(rem_total.sum())
    log["t3_final"] = len(limpa)
    log["t3_idade_ok"] = int(limpa["idade_anos"].notna().sum())
    log["t3_idade_desc"] = limpa["idade_anos"].describe()
    return limpa


# ─────────────────────────── Diagnóstico de preenchimento ────────────────────
def preenchimento_por_ano(full: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for ano, g in full.groupby("ano_csv"):
        n = len(g)
        rows[ano] = {k: (round(100 * g[k].notna().mean(), 1)
                         if k in g.columns else None)
                     for k in COLUNAS_USADAS}
    out = pd.DataFrame(rows).T
    out.index.name = "ano"
    return out


# ─────────────────────────── Relatório markdown ──────────────────────────────
def _md_table(df: pd.DataFrame, index: bool = True, index_label: str = "") -> str:
    """Converte um DataFrame em tabela markdown (sem depender de `tabulate`)."""
    df = df.copy()
    headers = ([index_label or (df.index.name or "")] if index else []) + \
        [str(c) for c in df.columns]

    def fmt(v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return ""
        if isinstance(v, float):
            return f"{v:.2f}".rstrip("0").rstrip(".")
        return str(v)

    rows = []
    for idx, row in df.iterrows():
        cells = ([fmt(idx)] if index else []) + [fmt(v) for v in row]
        rows.append("| " + " | ".join(cells) + " |")
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    return "\n".join(["| " + " | ".join(headers) + " |", sep] + rows)


def _md_series(s: pd.Series, name: str, index_label: str = "métrica") -> str:
    return _md_table(s.to_frame(name), index=True, index_label=index_label)


def gerar_relatorio(log: dict, full: pd.DataFrame, limpa: pd.DataFrame):
    t1 = log["tarefa1"]
    L = []
    L.append("# Relatório — Análise de DENGUE em Recife (SINAN, 2013–2025)\n")
    L.append(f"_Gerado em {datetime.now():%Y-%m-%d %H:%M}._\n")
    L.append("Pipeline: `src/mappings.py`, `src/utils.py`, `src/pipeline.py`. "
             "Encoding `latin-1`; delimitador detectado por arquivo.\n")

    # --- Tarefa 1 ---
    L.append("## Tarefa 1 — DataFrame único e coerente\n")
    L.append("Cada CSV foi lido, teve as colunas renomeadas para o esquema único "
             "(`ALL_MAPPINGS`: nome original → chave semântica), deduplicado e "
             "concatenado com a coluna `ano_csv`.\n")
    L.append("**Dedup:** `tp_duplicidade==1` onde a coluna existe (2013–2014); "
             "duplicatas exatas por chave (`notificacao` + `dt_sintoma`) nos demais "
             "anos.\n")
    cols = ["ano", "delimitador", "n_lido", "rem_tp_duplicidade",
            "rem_dup_chave", "n_final"]
    L.append(_md_table(t1[cols], index=False))
    L.append("")
    L.append(f"- **Total lido (todos os anos):** {log['total_lido']:,} registros")
    L.append(f"- **Removidos por `tp_duplicidade`:** "
             f"{int(t1['rem_tp_duplicidade'].sum()):,}")
    L.append(f"- **Removidos por duplicata de chave:** "
             f"{int(t1['rem_dup_chave'].sum()):,}")
    L.append(f"- **DataFrame único final:** {log['total_apos_dedup']:,} registros, "
             f"{log['t1_ncols']} colunas (esquema único + `ano_csv`)\n")

    # --- Preenchimento ---
    L.append("## Preenchimento das colunas usadas (após Tarefa 1)\n")
    L.append("% de linhas preenchidas por ano (None = coluna ausente no arquivo "
             "original).\n")
    L.append(_md_table(log["fill"], index=True, index_label="ano"))
    L.append("")
    L.append("> ⚠️ **`dt_internacao` é estruturalmente esparsa** (~3% da base): o "
             "campo só é preenchido em internações, e a maioria dos casos de dengue "
             "não interna. Isso limita a Tarefa 2 (ver abaixo).\n")
    L.append("> ⚠️ **`duplicidade` só existe em 2013–2014**; por isso a dedup nos "
             "demais anos usa chave exata.\n")

    # --- Tarefa 2 ---
    L.append("## Tarefa 2 — `delta_dias`\n")
    L.append("`delta_dias = dt_internacao − dt_sintoma` (ambas convertidas com "
             "`pd.to_datetime`, tratando os formatos AAAA-MM-DD, AAAA/MM/DD "
             "00:00:00, DD/MM/AAAA e nº de série do Excel). Valores negativos "
             "(erro de registro) recebem `delta_invalido=True` e são excluídos.\n")
    L.append(f"- **Registros com `dt_internacao` válida (internados):** "
             f"{log['delta_internados']:,} ({log['delta_pct_base']}% da base)")
    L.append(f"- **`delta_dias` válidos (≥ 0):** {log['delta_validos']:,}")
    L.append(f"- **`delta_invalido` (negativos, excluídos):** "
             f"{log['delta_negativos']:,}\n")
    if log["delta_desc"] is not None:
        d = log["delta_desc"]
        L.append("Distribuição de `delta_dias` (dias, subconjunto internado válido):\n")
        L.append(_md_series(d.round(2), "delta_dias"))
        L.append("")
    L.append("> A coluna `delta_dias` existe na base inteira (cumpre o DoD), mas a "
             "análise descritiva é feita sobre o subconjunto internado, pois ~97% "
             "da base não tem `dt_internacao`.\n")
    L.append("> Nota: o enunciado pede sinalizar apenas negativos. Há também alguns "
             "positivos extremos (máx ~19.100 dias) — erros de registro de data que "
             "inflam o desvio-padrão; por isso a **mediana (~4 dias)** é a medida "
             "central mais confiável.\n")

    # --- Tarefa 3 ---
    L.append("## Tarefa 3 — Base limpa\n")
    L.append("Filtros aplicados (contagem de registros atingidos por cada motivo; "
             "um registro pode cair em mais de um motivo):\n")
    L.append(f"- Início (DataFrame único): **{log['t3_inicial']:,}**")
    L.append(f"- `criterio == 3` (em investigação): **{log['t3_rem_investigacao']:,}**")
    L.append(f"- `evolucao == 9` (ignorado): **{log['t3_rem_ignorado']:,}**")
    L.append(f"- `classificacao == 5` (descartado): **{log['t3_rem_descartado']:,}**")
    L.append(f"- `delta_invalido` (delta negativo): **{log['t3_rem_delta_invalido']:,}**")
    L.append(f"- **Total de registros únicos removidos:** {log['t3_rem_total_unico']:,}")
    L.append(f"- **Base limpa final:** {log['t3_final']:,} registros\n")
    L.append("Idade decodificada (`nu_idade` → anos; 1=hora, 2=dia, 3=mês, 4=ano "
             "no 1º dígito):\n")
    L.append(f"- Idade válida (0–120 anos): **{log['t3_idade_ok']:,}** registros\n")
    L.append(_md_series(limpa["idade_anos"].describe().round(2), "idade_anos"))
    L.append("")

    path = os.path.join(REPORTS, "relatorio.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return path


def main():
    log: dict = {}
    print("Tarefa 1: construindo DataFrame único...")
    full = tarefa1_dataframe_unico(log)
    log["fill"] = preenchimento_por_ano(full)
    print(f"  -> {len(full):,} registros, {full.shape[1]} colunas")

    print("Tarefa 2: calculando delta_dias...")
    full = tarefa2_delta_dias(full, log)
    print(f"  -> internados={log['delta_internados']:,} | "
          f"válidos={log['delta_validos']:,} | "
          f"inválidos(neg)={log['delta_negativos']:,}")

    print("Tarefa 3: base limpa...")
    limpa = tarefa3_base_limpa(full, log)
    print(f"  -> removidos: invest={log['t3_rem_investigacao']:,} "
          f"ignor={log['t3_rem_ignorado']:,} descart={log['t3_rem_descartado']:,} "
          f"delta_inv={log['t3_rem_delta_invalido']:,} | "
          f"base limpa={log['t3_final']:,}")

    # Persiste a base limpa para análises posteriores.
    out_csv = os.path.join(REPORTS, "base_limpa.csv")
    limpa.to_csv(out_csv, index=False, encoding="utf-8")
    path = gerar_relatorio(log, full, limpa)
    print(f"\nRelatório: {os.path.relpath(path, ROOT)}")
    print(f"Base limpa: {os.path.relpath(out_csv, ROOT)}")


if __name__ == "__main__":
    main()
