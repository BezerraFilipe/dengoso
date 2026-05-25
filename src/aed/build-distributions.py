import csv
import re
import pandas as pd
from pathlib import Path
from columns_mapping import ALL_MAPPINGS

BASE_DIR = Path(__file__).resolve().parents[2] / "data"
ARBOVIROSES = ["dengue", "zika", "chikungunya"]
DELIMITERS = [";", ","]

COL_TO_KEY = {}
for key, variants in ALL_MAPPINGS.items():
    for variant in variants:
        COL_TO_KEY[variant] = key

def detect_delimiter(csv_file):
    for delimiter in DELIMITERS:
        try:
            with open(csv_file, encoding="utf-8", newline="") as f:
                reader = csv.reader(f, delimiter=delimiter)
                header = next(reader)
                columns = [col.strip() for col in header if col.strip()]
                if len(columns) > 1:
                    return delimiter
        except StopIteration:
            return None
        except Exception:
            continue
    return None

rows = []

for arbovirose in ARBOVIROSES:
    folder = BASE_DIR / arbovirose
    if not folder.exists():
        print(f"[AVISO] Pasta não encontrada: {folder}")
        continue

    for csv_file in sorted(folder.glob("*.csv")):
        match = re.search(r"(\d{4})", csv_file.name)
        if not match:
            print(f"[AVISO] Ano não encontrado no nome: {csv_file.name}")
            continue
        ano = int(match.group(1))

        delimiter = detect_delimiter(csv_file)
        if delimiter is None:
            print(f"[AVISO] Delimitador não detectado: {csv_file.name}")
            continue

        try:
            df = pd.read_csv(csv_file, delimiter=delimiter, dtype=str, encoding="utf-8")
        except Exception as e:
            print(f"[ERRO] {csv_file.name}: {e}")
            continue

        df.columns = [c.strip() for c in df.columns]
        df = df.replace("", pd.NA)

        casos = len(df)

        # mapeia coluna presente no df para sua chave semântica
        col_map = {}
        for col in df.columns:
            key = COL_TO_KEY.get(col)
            if key and key not in col_map:
                col_map[key] = col

        for variavel in ALL_MAPPINGS:
            if variavel in col_map:
                presenca_abs = int(df[col_map[variavel]].notna().sum())
            else:
                presenca_abs = 0

            presenca_rel = round(presenca_abs / casos * 100, 2) if casos > 0 else 0.0

            rows.append({
                "variavel":           variavel,
                "arbovirose":         arbovirose,
                "ano":                ano,
                "casos":              casos,
                "presenca-absoluta":  presenca_abs,
                "presenca-relativa":  presenca_rel,
            })

        print(f"  OK {csv_file.name} — {casos} casos")

output_path = Path(__file__).resolve().parent / "distribuicoes.csv"
fieldnames = ["variavel", "arbovirose", "ano", "casos", "presenca-absoluta", "presenca-relativa"]

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nCSV gerado em: {output_path}")
print(f"Total de linhas: {len(rows)}")