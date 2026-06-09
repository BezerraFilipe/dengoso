import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.aed.columns_mapping import ALL_MAPPINGS


BASE_DIR   = Path(__file__).resolve().parents[2] / "data"
DELIMITERS = [";", ","]

COL_TO_KEY = {
    variant: key
    for key, variants in ALL_MAPPINGS.items()
    for variant in variants
}

COLUNAS_CATEGORICAS = [
    "hospitalizacao", "evolucao", "classificacao", "criterio",
    "sexo", "gestante", "raca_cor", "escolaridade", "zona_residencia",
    "tipo_notificacao", "autoctone", "doenca_trabalho",
]


def _extract_year(filename: Path) -> str | None:
    for part in filename.stem.split("-"):
        if part.isdigit() and len(part) == 4:
            return part
    return None


def _read_csv(csv_file: Path) -> pd.DataFrame | None:
    for delimiter in DELIMITERS:
        try:
            df = pd.read_csv(csv_file, delimiter=delimiter, dtype=str, encoding="utf-8")
            if len(df.columns) > 1:
                return df
        except Exception:
            continue
    return None


def _normalizar_categorica(serie: pd.Series) -> pd.Series:
    return (
        serie
        .astype(str)
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace("nan", pd.NA)
        .replace("",    pd.NA)
    )


def build_master_df(base_dir: Path = BASE_DIR) -> pd.DataFrame:
    """Lê todos os CSVs de dengue, padroniza colunas e retorna o DataFrame mestre."""
    dfs = []

    for csv_file in sorted((base_dir / "dengue").glob("*.csv")):
        year = _extract_year(csv_file)
        if year is None:
            print(f"[AVISO] Não foi possível extrair ano de: {csv_file.name}")
            continue

        df = _read_csv(csv_file)
        if df is None:
            print(f"[AVISO] Não foi possível ler: {csv_file.name}")
            continue

        df.columns = [col.strip() for col in df.columns]
        df.rename(columns=COL_TO_KEY, inplace=True)
        df["arquivo"] = year
        dfs.append(df)

    master_df = pd.concat(dfs, ignore_index=True)

    for col in COLUNAS_CATEGORICAS:
        if col in master_df.columns:
            master_df[col] = _normalizar_categorica(master_df[col])

    master_df["dt_sintoma"]    = pd.to_datetime(master_df["dt_sintoma"],    dayfirst=True, errors="coerce")
    master_df["dt_internacao"] = pd.to_datetime(master_df["dt_internacao"], dayfirst=True, errors="coerce")
    master_df["delta_dias"]    = (master_df["dt_internacao"] - master_df["dt_sintoma"]).dt.days
    master_df["delta_invalido"] = (
        master_df["delta_dias"].isna() |
        (master_df["delta_dias"] < 0)  |
        (master_df["delta_dias"] > 365)
    )

    return master_df