import pandas as pd
from masterdf import build_master_df


# ── Etapa 1.1 — Análise exploratória inicial ────────────────────────────────

def aed(df: pd.DataFrame) -> None:
    print(f"DataFrame com {len(df)} linhas e {len(df.columns)} colunas.")

    print("\nColunas disponíveis e sua presença")
    for col in df.columns:
        print(f" - {col} - {df[col].notna().sum()} valores não nulos")

    for col in ["arquivo", "classificacao", "hospitalizacao", "evolucao"]:
        if col not in df.columns:
            continue
        print(f"\n Distribuição de frequência da variável '{col}'")
        for value in df[col].unique():
            count = (df[col] == value).sum()
            print(f" - {value}: {count} registros")


def filtrar_confirmados_hospitalizados(df: pd.DataFrame) -> pd.DataFrame:
    """Casos confirmados de dengue (excluindo classificações 5 e 8), hospitalizados e com critério != 3."""
    return df[
        (~df["classificacao"].isin(["5", "8"])) &
        (df["hospitalizacao"] == "1") &
        (df["criterio"] != "3")
    ]


def relatorio_delta_dias(df: pd.DataFrame) -> None:
    total     = len(df)
    invalidos = df["delta_invalido"].sum()
    validos   = (~df["delta_invalido"] & df["delta_dias"].notna()).sum()
    sem_data  = df["delta_dias"].isna().sum()

    print(f"\n── delta_dias ──────────────────────────────")
    print(f"   Registros totais:           {total:>10}")
    print(f"   Com delta válido:           {validos:>10}")
    print(f"   Sinalizados como inválidos: {invalidos:>10}")
    print(f"     └ sem data suficiente:    {sem_data:>10}")
    print(f"     └ delta negativo:         {(df['delta_dias'] < 0).sum():>10}")
    print(f"     └ delta > 365 dias:       {(df['delta_dias'] > 365).sum():>10}")


if __name__ == "__main__":
    master_df = build_master_df()

    print("\n── Análise exploratória inicial ────────────────────────────────")
    aed(master_df)

    print("\n── Apenas casos confirmados de dengue hospitalizados ────────────")
    df_confirmados = filtrar_confirmados_hospitalizados(master_df)
    aed(df_confirmados)

    print("\n Distribuição por ano nos casos confirmados de dengue hospitalizados:")
    for year in df_confirmados["arquivo"].unique():
        total_ano     = (master_df["arquivo"] == year).sum()
        filtrados_ano = (df_confirmados["arquivo"] == year).sum()
        print(f" - {year}: {filtrados_ano} registros, {total_ano} totais ({filtrados_ano/total_ano:.2%})")

    total_geral    = len(master_df)
    total_filtrado = len(df_confirmados)
    print(f"\n Total: {total_filtrado} registros confirmados hospitalizados de {total_geral} ({total_filtrado/total_geral:.2%})")

    relatorio_delta_dias(master_df)