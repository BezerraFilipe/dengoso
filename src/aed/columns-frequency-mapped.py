import csv
from pathlib import Path
from collections import defaultdict
from columns_mapping import ALL_MAPPINGS

BASE_DIR = Path(__file__).resolve().parents[2] / "data"
ARBOVIROSES = ["dengue", "zika", "chikungunya"]
DELIMITERS = [";", ","]

COL_TO_KEY = {}
for key, variants in ALL_MAPPINGS.items():
    for variant in variants:
        COL_TO_KEY[variant] = key

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

key_files = defaultdict(set)   # chave semântica -> arquivos
raw_files = defaultdict(set)   # coluna bruta (sem mapeamento) -> arquivos
file_columns = {}
files_found = []

for arbovirose in ARBOVIROSES:
    folder = BASE_DIR / arbovirose
    if not folder.exists():
        print(f"[AVISO] Pasta não encontrada: {folder}")
        continue

    for csv_file in sorted(folder.glob("*.csv")):
        columns, _ = detect_header(csv_file)
        if columns is None:
            print(f"[AVISO] Não foi possível ler: {csv_file.name}")
            continue
        file_columns[csv_file.name] = set(columns)
        files_found.append(csv_file.name)
        for col in columns:
            key = COL_TO_KEY.get(col)
            if key:
                key_files[key].add(csv_file.name)
            else:
                raw_files[col].add(csv_file.name)

total = len(files_found)

# Unifica tudo numa lista para ordenar
entries = []
for key, files in key_files.items():
    variants = sorted(ALL_MAPPINGS[key])
    label = f"{key}  {variants}"
    entries.append((label, key, len(files)))

for col, files in raw_files.items():
    entries.append((col, col, len(files)))

entries.sort(key=lambda x: x[2], reverse=True)

print(f"\nArquivos lidos ({total}):")
for name in files_found:
    print(f"  {name}")

print(f"\nFrequência de colunas (de {total} arquivos), ordem decrescente:\n")
for label, _, count in entries:
    print(f"  {label}: {count}")

print("\n" + "-" * 50)
print("Digite o nome semântico ou o nome exato de uma coluna para ver em quais arquivos ela aparece.")

print("Digite 'exit' para sair.")
print("-" * 50)

while True:
    query = input("\n> ").strip()

    if query.lower() == "exit":
        print("Encerrando.")
        break

    if not query:
        continue

    if query in key_files:
        files = sorted(key_files[query])
        missing = sorted(set(files_found) - key_files[query])
        print(f"\n'{query}' aparece em {len(files)}/{total} arquivo(s):")
        for f in files:
            print(f"  + {f}")
        if missing:
            print(f"\n  Ausente em {len(missing)} arquivo(s):")
            for f in missing:
                print(f"  - {f}")
    elif query in raw_files:
        files = sorted(raw_files[query])
        missing = sorted(set(files_found) - raw_files[query])
        print(f"\n'{query}' aparece em {len(files)}/{total} arquivo(s):")
        for f in files:
            print(f"  + {f}")
        if missing:
            print(f"\n  Ausente em {len(missing)} arquivo(s):")
            for f in missing:
                print(f"  - {f}")
    else:
        candidates = [k for k in list(ALL_MAPPINGS.keys()) + list(raw_files.keys())
                      if query.lower() in k.lower()]
        print(f"  '{query}' não encontrada.")
        if candidates:
            print(f"  Similares: {', '.join(candidates)}")