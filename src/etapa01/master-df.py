import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.aed.columns_mapping import ALL_MAPPINGS

BASE_DIR = Path(__file__).resolve().parents[2] / "data"
DELIMITERS = [";", ","]

COL_TO_KEY = {}
for key, variants in ALL_MAPPINGS.items():
    for variant in variants:
        COL_TO_KEY[variant] = key

def extract_year(filename):
    for part in filename.stem.split("-"):
        if part.isdigit() and len(part) == 4:
            return part
    return None

dfs = []

for csv_file in sorted((BASE_DIR / "dengue").glob("*.csv")):
    year = extract_year(csv_file)
    if year is None:
        print(f"[AVISO] Não foi possível extrair ano de: {csv_file.name}")
        continue

    df = None
    for delimiter in DELIMITERS:
        try:
            tmp = pd.read_csv(csv_file, delimiter=delimiter, dtype=str, encoding="utf-8")
            if len(tmp.columns) > 1:
                df = tmp
                break
        except Exception:
            continue

    if df is None:
        print(f"[AVISO] Não foi possível ler: {csv_file.name}")
        continue

    df.columns = [col.strip() for col in df.columns]
    df.rename(columns=COL_TO_KEY, inplace=True)
    df["arquivo"] = year
    dfs.append(df)

master_df = pd.concat(dfs, ignore_index=True)

print(f"DataFrame mestre criado com {len(master_df)} linhas e {len(master_df.columns)} colunas.")

print("\nColunas disponíveis e sua presença")
for col in master_df.columns:
    print(f" - {col} - {master_df[col].notna().sum()} valores não nulos")

print("\n Arquivos contemplados e quantidade de registros por arquivo")
for year in master_df["arquivo"].unique():
    print(f" - {year}: {len(master_df[master_df['arquivo'] == year])} registros")

print("\n Classificações contempladas e quantidade de registros por classificação")
for c in master_df["classificacao"].unique():
    print(f" - {c}: {len(master_df[master_df['classificacao'] == c])} registros")

# ── Etapa 1.2 — Variável derivada delta_dias ─────────────────────────────────

master_df["dt_sintoma"]    = pd.to_datetime(master_df["dt_sintoma"],    dayfirst=True, errors="coerce")
master_df["dt_internacao"] = pd.to_datetime(master_df["dt_internacao"], dayfirst=True, errors="coerce")

master_df["delta_dias"] = (master_df["dt_internacao"] - master_df["dt_sintoma"]).dt.days

master_df["delta_invalido"] = (
    master_df["delta_dias"].isna() |
    (master_df["delta_dias"] < 0)  |
    (master_df["delta_dias"] > 365)
)

total       = len(master_df)
invalidos   = master_df["delta_invalido"].sum()
validos     = (~master_df["delta_invalido"] & master_df["delta_dias"].notna()).sum()
sem_data    = master_df["delta_dias"].isna().sum()

print(f"\n── delta_dias ──────────────────────────────")
print(f"   Registros totais:           {total:>10}")
print(f"   Com delta válido:           {validos:>10}")
print(f"   Sinalizados como inválidos: {invalidos:>10}")
print(f"     └ sem data suficiente:    {sem_data:>10}")
print(f"     └ delta negativo:         {(master_df['delta_dias'] < 0).sum():>10}")
print(f"     └ delta > 365 dias:       {(master_df['delta_dias'] > 365).sum():>10}")