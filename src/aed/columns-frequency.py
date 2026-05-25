"""
    Esse script extrai todas os cabeçalhos dos CSVs de casos das arboviroses por ano e os armazena em um dicionário.
    O objetivo é mapear os diferentes nomes de um mesmo campo, por exemplo, dt_internacao = dt_interna = DT_INTERNA.
    E a partir disso, quais colunas (campos) ocorrem em todos os arquivos.
"""

import csv
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[2] / "data"
ARBOVIROSES = ["dengue", "zika", "chikungunya"]
DELIMITERS = [";", ","]

def detect_header(csv_file):
    for delimiter in DELIMITERS:
        try:
            with open(csv_file, encoding="utf-8", newline="") as f:
                reader = csv.reader(f, delimiter=delimiter)
                header = next(reader)
                columns = [col.strip() for col in header if col.strip()]
                if len(columns) > 1:
                    return columns, delimiter
        except StopIteration:
            return None, None
        except Exception:
            continue
    return None, None

column_counter = Counter()
file_columns = {}
files_found = []

for arbovirose in ARBOVIROSES:
    folder = BASE_DIR / arbovirose
    if not folder.exists():
        print(f"[AVISO] Pasta não encontrada: {folder}")
        continue

    for csv_file in sorted(folder.glob("*.csv")):
        columns, delimiter = detect_header(csv_file)
        if columns is None:
            print(f"[AVISO] Não foi possível ler: {csv_file.name}")
            continue
        column_counter.update(columns)
        file_columns[csv_file.name] = set(columns)
        files_found.append(csv_file.name)

print(f"\nArquivos lidos ({len(files_found)}):")
for name in files_found:
    print(f"  {name}")

print(f"\nFrequência de colunas ({len(column_counter)} distintas), ordem decrescente:\n")
for column, count in column_counter.most_common():
    print(f"  {column}: {count}")

print("\n" + "-" * 50)
print("Digite o nome de uma coluna para ver em quais arquivos ela aparece.")
print("Digite 'exit' para sair.")
print("-" * 50)

while True:
    query = input("\n> ").strip()

    if query.lower() == "exit":
        print("Encerrando.")
        break

    if not query:
        continue

    matches = [f for f, cols in file_columns.items() if query in cols]

    if matches:
        print(f"\n'{query}' aparece em {len(matches)} arquivo(s):")
        for f in sorted(matches):
            print(f"  {f}")
    else:
        candidates = [col for col in column_counter if query.lower() in col.lower()]
        print(f"  Coluna '{query}' não encontrada.")
        if candidates:
            print(f"  Colunas similares: {', '.join(candidates)}")