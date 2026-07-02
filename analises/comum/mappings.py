"""Mapeamento de colunas dos CSVs do SINAN (dengue/Recife) para um esquema único.

Os CSVs vêm em dois vocabulários:
  - descritivo minúsculo (snake_case), p.ex. ``dt_diagnostico_sintoma``;
  - código SINAN maiúsculo, p.ex. ``DT_SIN_PRI``.

``ALL_MAPPINGS`` mapeia *nome original de coluna* -> *chave semântica única*.
A correspondência é feita de forma case-insensitive (ver ``semantic_key``),
de modo que variantes maiúsculas/minúsculas do mesmo código caem na mesma chave.
"""

# Grupos: chave semântica -> conjunto de nomes originais conhecidos.
# Cobre as colunas usadas pelas Tarefas 1-3 e o essencial de identificação.
_GROUPS = {
    # Identificação / tempo
    "notificacao":        {"nu_notificacao", "NU_NOTIFIC"},
    "tipo_notificacao":   {"tp_notificacao", "TP_NOT"},
    "cid":                {"co_cid", "ID_AGRAVO"},
    "dt_notificacao":     {"dt_notificacao", "DT_NOTIFIC"},
    "ano":                {"notificacao_ano", "ano_notificacao", "NU_ANO"},
    "uf_notificacao":     {"co_uf_notificacao", "SG_UF_NOT"},
    "municipio_notificacao": {"co_municipio_notificacao", "ID_MUNICIP"},
    "dt_investigacao":    {"dt_investigacao", "DT_INVEST"},
    # Sintomas / datas clínicas
    "dt_sintoma":         {"dt_diagnostico_sintoma", "DT_SIN_PRI"},
    # Demográficos
    "dt_nascimento":      {"dt_nascimento", "DT_NASC"},
    "idade":              {"nu_idade", "NU_IDADE_N"},
    "sexo":               {"tp_sexo", "CS_SEXO"},
    "gestante":           {"tp_gestante", "CS_GESTANT"},
    "raca_cor":           {"tp_raca_cor", "CS_RACA"},
    # Residência
    "municipio_residencia": {"co_municipio_residencia", "ID_MN_RESI"},
    "distrito_residencia":  {"co_distrito_residencia", "ID_DISTRIT"},
    "bairro_residencia":    {"co_bairro_residencia", "ID_BAIRRO"},
    "nome_bairro_residencia": {"no_bairro_residencia", "NM_BAIRRO"},
    "zona_residencia":    {"tp_zona_residencia", "CS_ZONA"},
    # Classificação / critério / desfecho
    "classificacao":      {"tp_classificacao_final", "CLASSI_FIN"},
    "criterio":           {"tp_criterio_confirmacao", "CRITERIO"},
    "evolucao":           {"tp_evolucao_caso", "EVOLUCAO"},
    "dt_obito":           {"dt_obito", "DT_OBITO"},
    "dt_encerramento":    {"dt_encerramento", "DT_ENCERRA"},
    # Hospitalização / internação
    "hospitalizacao":     {"st_ocorreu_hospitalizacao", "HOSPITALIZ"},
    "dt_internacao":      {"dt_internacao", "DT_INTERNA"},
    # Comorbidades (existem apenas em 2015–2025; ausentes em 2013–2014).
    # Codificação SINAN: 1=Sim, 2=Não, 9=Ignorado, vazio=sem registro.
    "comorb_diabetes":    {"diabetes", "DIABETES"},
    "comorb_hipertensao": {"hipertensao", "HIPERTENSA"},
    "comorb_hematologica": {"hematolog", "HEMATOLOG"},
    "comorb_hepatopatia": {"hepatopat", "HEPATOPAT"},
    "comorb_autoimune":   {"auto_imune", "AUTO_IMUNE"},
    # Controle / duplicidade
    "duplicidade":        {"tp_duplicidade", "NDUPLIC_N"},
}

# ALL_MAPPINGS: nome original (em minúsculas) -> chave semântica.
# Indexamos por lower() para casar tanto a variante maiúscula quanto a minúscula.
ALL_MAPPINGS = {}
for _semantic, _variants in _GROUPS.items():
    for _orig in _variants:
        ALL_MAPPINGS[_orig.lower()] = _semantic

# Conjunto de chaves semânticas conhecidas (para validação).
SEMANTIC_KEYS = set(_GROUPS)


def semantic_key(col: str):
    """Retorna a chave semântica para um nome de coluna original, ou None."""
    return ALL_MAPPINGS.get(str(col).strip().lower())


# Colunas que as Tarefas 1-3 efetivamente usam (para checagem de preenchimento).
COLUNAS_USADAS = [
    "duplicidade",      # Tarefa 1 (dedup)
    "dt_sintoma",       # Tarefa 2 (delta_dias)
    "dt_internacao",    # Tarefa 2 (delta_dias)
    "criterio",         # Tarefa 3 (remove "em investigação")
    "evolucao",         # Tarefa 3 (remove "ignorado"/"descartado")
    "classificacao",    # Tarefa 3 (remove "descartado")
    "idade",            # Tarefa 3 (decodificar idade)
]
