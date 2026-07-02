"""Funções utilitárias de normalização para os CSVs do SINAN.

Trata as 'realidades da base':
  - datas em 3+ formatos misturados (AAAA-MM-DD, AAAA/MM/DD 00:00:00, DD/MM/AAAA)
    e, em alguns anos, número de série do Excel (p.ex. '45742');
  - categóricos como '2' e '2.0' misturados;
  - idade com codificação composta (1=hora, 2=dia, 3=mês, 4=ano no 1º dígito).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

_NULOS = {"", "nan", "none", "nat", "null"}


def _limpa_serie_str(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.strip()
    return s.mask(s.str.lower().isin(_NULOS))


def normaliza_categoria(serie: pd.Series) -> pd.Series:
    """Normaliza categóricos: '2.0' -> '2', remove espaços, nulos -> NaN.

    Mantém como string para comparação consistente (evita '2' vs 2 vs 2.0).
    """
    s = _limpa_serie_str(serie)
    # '2.0' -> '2'  (apenas quando é número com parte decimal só zeros)
    s = s.str.replace(r"^(\d+)\.0+$", r"\1", regex=True)
    return s


def parse_datas(serie: pd.Series) -> pd.Series:
    """Converte uma série de strings em datetime, tratando os formatos mistos.

    Detecta o formato por padrão (regex) e aplica máscara a máscara, somando
    também o caso de número de série do Excel (origem 1899-12-30).
    """
    s = _limpa_serie_str(serie)
    out = pd.Series(pd.NaT, index=serie.index, dtype="datetime64[ns]")

    # 1) ISO: AAAA-MM-DD (com ou sem hora)
    m = s.str.match(r"^\d{4}-\d{2}-\d{2}") == True  # noqa: E712
    out.loc[m] = pd.to_datetime(s[m], format="%Y-%m-%d", errors="coerce",
                                exact=False)

    # 2) AAAA/MM/DD (com ou sem ' 00:00:00')
    m = (s.str.match(r"^\d{4}/\d{2}/\d{2}") == True) & out.isna()  # noqa: E712
    out.loc[m] = pd.to_datetime(s[m], format="%Y/%m/%d", errors="coerce",
                                exact=False)

    # 3) DD/MM/AAAA (com ou sem hora)
    m = (s.str.match(r"^\d{2}/\d{2}/\d{4}") == True) & out.isna()  # noqa: E712
    out.loc[m] = pd.to_datetime(s[m], format="%d/%m/%Y", errors="coerce",
                                exact=False)

    # 4) Número de série do Excel (p.ex. '45742' -> 2025-03-xx)
    m = (s.str.match(r"^\d{4,6}(\.0+)?$") == True) & out.isna()  # noqa: E712
    if m.any():
        nums = pd.to_numeric(s[m].str.replace(r"\.0+$", "", regex=True),
                             errors="coerce")
        # faixa plausível de datas (1990-2035): seriais ~32874 a ~49700
        ok = nums.between(32000, 50000)
        out.loc[m & ok.reindex(out.index, fill_value=False)] = (
            pd.to_datetime(nums[ok], unit="D", origin="1899-12-30",
                           errors="coerce")
        )
    return out


def decodifica_idade(serie: pd.Series) -> pd.Series:
    """Decodifica nu_idade (codificação SINAN) para idade em ANOS (float).

    1º dígito = unidade: 1=hora, 2=dia, 3=mês, 4=ano. Dígitos restantes =
    quantidade. Ex.: 4025 -> 25 anos; 3011 -> 11 meses ~ 0.92 anos.
    """
    s = normaliza_categoria(serie)
    cod = pd.to_numeric(s, errors="coerce")
    unidade = (cod // 1000).astype("Int64")
    qtd = (cod % 1000).astype("Int64")
    qtd_f = qtd.astype("float64")

    anos = pd.Series(np.nan, index=serie.index, dtype="float64")
    anos[unidade == 4] = qtd_f[unidade == 4]              # anos
    anos[unidade == 3] = qtd_f[unidade == 3] / 12.0       # meses
    anos[unidade == 2] = qtd_f[unidade == 2] / 365.25     # dias
    anos[unidade == 1] = qtd_f[unidade == 1] / 8760.0     # horas
    # idades implausíveis viram NaN
    anos[(anos < 0) | (anos > 120)] = np.nan
    return anos
