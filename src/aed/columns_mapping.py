# Mapeamento de variantes de nomes de colunas entre os CSVs
# Cada conjunto agrupa todas as variantes conhecidas de uma mesma coluna semântica.
# ── Identificação ────────────────────────────────────────────────────────────

COLUNA_NOTIFICACAO = {
    "nu_notificacao", "NU_NOTIFIC", "nu_notific",
}

COLUNA_TIPO_NOTIFICACAO = {
    "tp_notificacao", "TP_NOT", "tp_not",
}

COLUNA_CID = {
    "co_cid", "ID_AGRAVO", "id_agravo",
}

COLUNA_DT_NOTIFICACAO = {
    "dt_notificacao", "DT_NOTIFIC", "dt_notific",
}

COLUNA_SEMANA_NOTIFICACAO = {
    "ds_semana_notificacao", "SEM_NOT", "sem_not",
}

COLUNA_ANO = {
    "notificacao_ano", "ano_notificacao", "NU_ANO", "nu_ano",
}

COLUNA_UF_NOTIFICACAO = {
    "co_uf_notificacao", "SG_UF_NOT", "sg_uf_not",
}

COLUNA_MUNICIPIO_NOTIFICACAO = {
    "co_municipio_notificacao", "ID_MUNICIP", "id_municip",
}

COLUNA_REGIONAL = {
    "id_regional", "ID_REGIONA", "id_regiona",
}

COLUNA_UNIDADE_NOTIFICACAO = {
    "co_unidade_notificacao", "ID_UNIDADE", "id_unidade",
}

COLUNA_DT_INVESTIGACAO = {
    "dt_investigacao", "DT_INVEST", "dt_invest",
}

COLUNA_OCUPACAO = {
    "co_cbo_ocupacao", "ID_OCUPA_N", "id_ocupa_n",
}

# ── Sintomas / datas clínicas ────────────────────────────────────────────────

COLUNA_DT_SINTOMA = {
    "dt_diagnostico_sintoma", "DT_SIN_PRI", "dt_sin_pri",
}

COLUNA_SEMANA_SINTOMA = {
    "ds_semana_sintoma", "SEM_PRI", "sem_pri",
}

# ── Dados demográficos ───────────────────────────────────────────────────────

COLUNA_DT_NASCIMENTO = {
    "dt_nascimento", "DT_NASC", "dt_nasc",
}

COLUNA_IDADE = {
    "nu_idade", "NU_IDADE_N", "nu_idade_n",
}

COLUNA_SEXO = {
    "tp_sexo", "CS_SEXO", "cs_sexo",
}

COLUNA_GESTANTE = {
    "tp_gestante", "CS_GESTANT", "cs_gestant",
}

COLUNA_RACA_COR = {
    "tp_raca_cor", "CS_RACA", "cs_raca",
}

COLUNA_ESCOLARIDADE = {
    "tp_escolaridade", "CS_ESCOL_N", "cs_escol_n",
}

# ── Localização — residência ─────────────────────────────────────────────────

COLUNA_UF_RESIDENCIA = {
    "co_uf_residencia", "SG_UF", "sg_uf",
}

COLUNA_MUNICIPIO_RESIDENCIA = {
    "co_municipio_residencia", "ID_MN_RESI", "id_mn_resi",
}

COLUNA_REGIONAL_RESIDENCIA = {
    "co_regional_residencia", "ID_RG_RESI", "ID_RG_RESI",
    "id_rg_residencia", "id_rg_resi",
}

COLUNA_DISTRITO_RESIDENCIA = {
    "co_distrito_residencia", "ID_DISTRIT", "id_distrit",
}

COLUNA_BAIRRO_RESIDENCIA = {
    "co_bairro_residencia", "ID_BAIRRO", "id_bairro",
}

COLUNA_NOME_BAIRRO_RESIDENCIA = {
    "no_bairro_residencia", "NM_BAIRRO", "nm_bairro",
}

COLUNA_LOGRADOURO_RESIDENCIA = {
    "co_logradouro_residencia", "ID_LOGRADO", "id_logrado",
}

COLUNA_NOME_LOGRADOURO_RESIDENCIA = {
    "nome_logradouro_residencia", "NM_LOGRADO",
    "nm_logradouro_residencia", "nm_logrado",
}

COLUNA_CEP_RESIDENCIA = {
    "nu_cep_residencia", "NU_CEP", "nu_cep",
}

COLUNA_PAIS_RESIDENCIA = {
    "co_pais_residencia", "ID_PAIS", "id_pais",
}

COLUNA_ZONA_RESIDENCIA = {
    "tp_zona_residencia", "CS_ZONA",
}

# ── Localização — infecção ───────────────────────────────────────────────────

COLUNA_AUTOCTONE = {
    "tp_autoctone_residencia", "TPAUTOCTO", "tpautocto",
}

COLUNA_UF_INFECCAO = {
    "co_uf_infeccao", "COUFINF", "coufinf",
}

COLUNA_PAIS_INFECCAO = {
    "co_pais_infeccao", "COPAISINF", "copaisinf",
}

COLUNA_MUNICIPIO_INFECCAO = {
    "co_municipio_infeccao", "COMUNINF", "comuninf",
}

COLUNA_DISTRITO_INFECCAO = {
    "co_distrito_infeccao", "CODISINF", "codisinf",
}

COLUNA_BAIRRO_INFECCAO = {
    "co_bairro_infeccao", "CO_BAINF", "CO_BAINFC", "co_bainf",
}

COLUNA_NOME_BAIRRO_INFECCAO = {
    "no_bairro_infeccao", "NOBAIINF", "nobaiinf",
}

# ── Classificação e critério ─────────────────────────────────────────────────

COLUNA_CLASSIFICACAO = {
    "tp_classificacao_final", "CLASSI_FIN", "classi_fin",
}

COLUNA_CRITERIO = {
    "tp_criterio_confirmacao", "CRITERIO", "criterio",
}

COLUNA_DOENCA_TRABALHO = {
    "st_doenca_trabalho", "DOENCA_TRA", "doenca_tra",
}

# ── Evolução e desfecho ──────────────────────────────────────────────────────

COLUNA_EVOLUCAO = {
    "tp_evolucao_caso", "EVOLUCAO", "evolucao",
}

COLUNA_DT_OBITO = {
    "dt_obito", "DT_OBITO",
}

COLUNA_DT_ENCERRAMENTO = {
    "dt_encerramento", "DT_ENCERRA", "dt_encerra",
}

# ── Hospitalização / internação ──────────────────────────────────────────────

COLUNA_HOSPITALIZACAO = {
    "st_ocorreu_hospitalizacao", "HOSPITALIZ", "hospitaliz",
}

COLUNA_DT_INTERNACAO = {
    "dt_internacao", "DT_INTERNA", "dt_interna",
}

COLUNA_UF_HOSPITAL = {
    "co_uf_hospital", "UF", "uf",
}

COLUNA_MUNICIPIO_HOSPITAL = {
    "co_municipio_hospital", "MUNICIPIO", "municipio",
}

COLUNA_UNIDADE_HOSPITAL = {
    "co_unidade_hospital", "HOSPITAL", "hospital",
}

COLUNA_DDD_HOSPITAL = {
    "nu_ddd_hospital", "DDD_HOSP", "ddd_hosp", "ddd_hospital",
}

COLUNA_TEL_HOSPITAL = {
    "nu_telefone_hospital", "TEL_HOSP", "tel_hosp", "tel_hospital",
}

# ── Exames laboratoriais ─────────────────────────────────────────────────────

COLUNA_DT_SORO_IGM_S1 = {
    "dt_chil_s1", "DT_CHIK_S1", "dt_chik_s1",
}

COLUNA_DT_SORO_IGM_S2 = {
    "dt_chil_s2", "DT_CHIK_S2", "dt_chik_s2",
}

COLUNA_DT_PRNT = {
    "dt_prnt", "DT_PRNT",
}

COLUNA_RES_CHIK_S1 = {
    "res_chiks1", "RES_CHIKS1",
}

COLUNA_RES_CHIK_S2 = {
    "res_chiks2", "RES_CHIKS2",
}

COLUNA_RES_PRNT = {
    "resul_prnt", "RESUL_PRNT",
}

COLUNA_DT_SORO = {
    "dt_coleta_exame", "DT_SORO", "dt_soro",
}

COLUNA_RES_SORO = {
    "tp_result_exame", "RESUL_SORO", "resul_soro",
}

COLUNA_DT_NS1 = {
    "dt_coleta_NS1", "DT_NS1", "dt_ns1",
}

COLUNA_RES_NS1 = {
    "Tp_result_NS1", "RESUL_NS1", "resul_ns1",
}

COLUNA_DT_ISOLAMENTO = {
    "dt_coleta_isolamento", "DT_VIRAL", "dt_viral",
}

COLUNA_RES_ISOLAMENTO = {
    "tp_result_isolamento", "RESUL_VI_N", "resul_vi_n",
}

COLUNA_DT_PCR = {
    "dt_coleta_rtpcr", "DT_PCR", "dt_pcr",
}

COLUNA_RES_PCR = {
    "tp_result_rtpcr", "RESUL_PCR_", "resul_pcr_",
}

COLUNA_SOROTIPO = {
    "tp_sorotipo", "SOROTIPO", "sorotipo",
}

COLUNA_HISTOPATOLOGIA = {
    "tp_result_histopatologia", "HISTOPA_N", "histopa_n",
}

COLUNA_IMUNOHISTOQUIMICA = {
    "tp_result_imunohistoquimica", "IMUNOH_N", "imunoh_n",
}

# ── Sinais clínicos ──────────────────────────────────────────────────────────

COLUNA_FEBRE          = {"febre",        "FEBRE"}
COLUNA_MIALGIA        = {"mialgia",      "MIALGIA"}
COLUNA_CEFALEIA       = {"cefaleia",     "CEFALEIA"}
COLUNA_EXANTEMA       = {"exantema",     "EXANTEMA"}
COLUNA_VOMITO         = {"vomito",       "VOMITO"}
COLUNA_NAUSEA         = {"nausea",       "NAUSEA"}
COLUNA_DOR_COSTAS     = {"dor_costas",   "DOR_COSTAS"}
COLUNA_CONJUTIVITE    = {"conjutivite",  "CONJUNTVIT", "conjuntvit"}
COLUNA_ARTRITE        = {"artrite",      "ARTRITE"}
COLUNA_ARTRALGIA      = {"artralgia",    "ARTRALGIA"}
COLUNA_PETEQUIA_N     = {"petequia_n",   "PETEQUIA_N"}
COLUNA_LEUCOPENIA     = {"leucopenia",   "LEUCOPENIA"}
COLUNA_LACO           = {"laco",         "LACO"}
COLUNA_DOR_RETRO      = {"dor_retro",    "DOR_RETRO"}
COLUNA_DIABETES       = {"diabetes",     "DIABETES"}
COLUNA_HEMATOLOG      = {"hematolog",    "HEMATOLOG"}
COLUNA_HEPATOPAT      = {"hepatopat",    "HEPATOPAT"}
COLUNA_RENAL          = {"renal",        "RENAL"}
COLUNA_HIPERTENSAO    = {"hipertensao",  "HIPERTENSA", "hipertensa"}
COLUNA_ACIDO_PEPT     = {"acido_pept",   "ACIDO_PEPT"}
COLUNA_AUTO_IMUNE     = {"auto_imune",   "AUTO_IMUNE"}
COLUNA_CLINC_CHIK     = {"clinc_chik",   "CLINC_CHIK"}

# ── Sinais de alarme ─────────────────────────────────────────────────────────

COLUNA_ALRM_HIPOT  = {"alrm_hipot",  "ALRM_HIPOT"}
COLUNA_ALRM_PLAQ   = {"alrm_plaq",   "ALRM_PLAQ"}
COLUNA_ALRM_VOM    = {"alrm_vom",    "ALRM_VOM"}
COLUNA_ALRM_SANG   = {"alrm_sang",   "ALRM_SANG"}
COLUNA_ALRM_HEMAT  = {"alrm_hemat",  "ALRM_HEMAT"}
COLUNA_ALRM_ABDOM  = {"alrm_abdom",  "ALRM_ABDOM"}
COLUNA_ALRM_LETAR  = {"alrm_letar",  "ALRM_LETAR"}
COLUNA_ALRM_HEPAT  = {"alrm_hepat",  "ALRM_HEPAT"}
COLUNA_ALRM_LIQ    = {"alrm_liq",    "ALRM_LIQ"}
COLUNA_DT_ALARME   = {"dt_alrm",     "DT_ALRM"}

# ── Sinais de gravidade ──────────────────────────────────────────────────────

COLUNA_GRAV_PULSO  = {"grav_pulso",  "GRAV_PULSO"}
COLUNA_GRAV_CONV   = {"grav_conv",   "GRAV_CONV"}
COLUNA_GRAV_ENCH   = {"grav_ench",   "GRAV_ENCH"}
COLUNA_GRAV_INSUF  = {"grav_insuf",  "GRAV_INSUF"}
COLUNA_GRAV_TAQUI  = {"grav_taqui",  "GRAV_TAQUI"}
COLUNA_GRAV_EXTRE  = {"grav_extre",  "GRAV_EXTRE"}
COLUNA_GRAV_HIPOT  = {"grav_hipot",  "GRAV_HIPOT"}
COLUNA_GRAV_HEMAT  = {"grav_hemat",  "GRAV_HEMAT"}
COLUNA_GRAV_MELEN  = {"grav_melen",  "GRAV_MELEN"}
COLUNA_GRAV_METRO  = {"grav_metro",  "GRAV_METRO"}
COLUNA_GRAV_SANG   = {"grav_sang",   "GRAV_SANG"}
COLUNA_GRAV_AST    = {"grav_ast",    "GRAV_AST"}
COLUNA_GRAV_MIOC   = {"grav_mioc",   "GRAV_MIOC"}
COLUNA_GRAV_CONSC  = {"grav_consc",  "GRAV_CONSC"}
COLUNA_GRAV_ORGAO  = {"grav_orgao",  "GRAV_ORGAO"}
COLUNA_DT_GRAV     = {"dt_grav",     "DT_GRAV"}

# ── Manifestações hemorrágicas ───────────────────────────────────────────────

# Nota: "mami_hemor" (freq 6) parece typo de "mani_hemor" — agrupado aqui
COLUNA_MANI_HEMOR  = {"mani_hemor",  "MANI_HEMOR", "mami_hemor"}
COLUNA_EPISTAXE    = {"epistaxe",    "EPISTAXE"}
COLUNA_GENGIVO     = {"gengivo",     "GENGIVO"}
COLUNA_METRO       = {"metro",       "METRO"}
COLUNA_PETEQUIAS   = {"petequias",   "PETEQUIAS"}
COLUNA_HEMATURA    = {"hematura",    "HEMATURA"}
COLUNA_SANGRAM     = {"sangram",     "SANGRAM"}
COLUNA_LACO_N      = {"laco_n",      "LACO_N"}
COLUNA_PLASMATICO  = {"plasmatico",  "PLASMATICO"}
COLUNA_EVIDENCIA   = {"evidencia",   "EVIDENCIA"}
COLUNA_PLAQ_MENOR  = {"plaq_menor",  "PLAQ_MENOR"}
COLUNA_CON_FHD     = {"con_fhd",     "CON_FHD", "conf_fhd"}

# ── Complicações e observações ───────────────────────────────────────────────

COLUNA_COMPLICA    = {"complica",    "COMPLICA"}
COLUNA_DS_OBS      = {"ds_obs",      "DS_OBS"}

# ── Controle / duplicidade ───────────────────────────────────────────────────

COLUNA_DUPLICIDADE = {"tp_duplicidade", "NDUPLIC_N"}

# ── Aggregado para uso programático ─────────────────────────────────────────

ALL_MAPPINGS = {
    # Identificação
    "notificacao":                  COLUNA_NOTIFICACAO,
    "tipo_notificacao":             COLUNA_TIPO_NOTIFICACAO,
    "cid":                          COLUNA_CID,
    "dt_notificacao":               COLUNA_DT_NOTIFICACAO,
    "semana_notificacao":           COLUNA_SEMANA_NOTIFICACAO,
    "ano":                          COLUNA_ANO,
    "uf_notificacao":               COLUNA_UF_NOTIFICACAO,
    "municipio_notificacao":        COLUNA_MUNICIPIO_NOTIFICACAO,
    "regional":                     COLUNA_REGIONAL,
    "unidade_notificacao":          COLUNA_UNIDADE_NOTIFICACAO,
    "dt_investigacao":              COLUNA_DT_INVESTIGACAO,
    "ocupacao":                     COLUNA_OCUPACAO,
    # Sintomas / datas clínicas
    "dt_sintoma":                   COLUNA_DT_SINTOMA,
    "semana_sintoma":               COLUNA_SEMANA_SINTOMA,
    # Demográficos
    "dt_nascimento":                COLUNA_DT_NASCIMENTO,
    "idade":                        COLUNA_IDADE,
    "sexo":                         COLUNA_SEXO,
    "gestante":                     COLUNA_GESTANTE,
    "raca_cor":                     COLUNA_RACA_COR,
    "escolaridade":                 COLUNA_ESCOLARIDADE,
    # Localização — residência
    "uf_residencia":                COLUNA_UF_RESIDENCIA,
    "municipio_residencia":         COLUNA_MUNICIPIO_RESIDENCIA,
    "regional_residencia":          COLUNA_REGIONAL_RESIDENCIA,
    "distrito_residencia":          COLUNA_DISTRITO_RESIDENCIA,
    "bairro_residencia":            COLUNA_BAIRRO_RESIDENCIA,
    "nome_bairro_residencia":       COLUNA_NOME_BAIRRO_RESIDENCIA,
    "logradouro_residencia":        COLUNA_LOGRADOURO_RESIDENCIA,
    "nome_logradouro_residencia":   COLUNA_NOME_LOGRADOURO_RESIDENCIA,
    "cep_residencia":               COLUNA_CEP_RESIDENCIA,
    "pais_residencia":              COLUNA_PAIS_RESIDENCIA,
    "zona_residencia":              COLUNA_ZONA_RESIDENCIA,
    # Localização — infecção
    "autoctone":                    COLUNA_AUTOCTONE,
    "uf_infeccao":                  COLUNA_UF_INFECCAO,
    "pais_infeccao":                COLUNA_PAIS_INFECCAO,
    "municipio_infeccao":           COLUNA_MUNICIPIO_INFECCAO,
    "distrito_infeccao":            COLUNA_DISTRITO_INFECCAO,
    "bairro_infeccao":              COLUNA_BAIRRO_INFECCAO,
    "nome_bairro_infeccao":         COLUNA_NOME_BAIRRO_INFECCAO,
    # Classificação e critério
    "classificacao":                COLUNA_CLASSIFICACAO,
    "criterio":                     COLUNA_CRITERIO,
    "doenca_trabalho":              COLUNA_DOENCA_TRABALHO,
    # Evolução e desfecho
    "evolucao":                     COLUNA_EVOLUCAO,
    "dt_obito":                     COLUNA_DT_OBITO,
    "dt_encerramento":              COLUNA_DT_ENCERRAMENTO,
    # Hospitalização / internação
    "hospitalizacao":               COLUNA_HOSPITALIZACAO,
    "dt_internacao":                COLUNA_DT_INTERNACAO,
    "uf_hospital":                  COLUNA_UF_HOSPITAL,
    "municipio_hospital":           COLUNA_MUNICIPIO_HOSPITAL,
    "unidade_hospital":             COLUNA_UNIDADE_HOSPITAL,
    "ddd_hospital":                 COLUNA_DDD_HOSPITAL,
    "tel_hospital":                 COLUNA_TEL_HOSPITAL,
    # Exames laboratoriais
    "dt_soro_igm_s1":               COLUNA_DT_SORO_IGM_S1,
    "dt_soro_igm_s2":               COLUNA_DT_SORO_IGM_S2,
    "dt_prnt":                      COLUNA_DT_PRNT,
    "res_chik_s1":                  COLUNA_RES_CHIK_S1,
    "res_chik_s2":                  COLUNA_RES_CHIK_S2,
    "res_prnt":                     COLUNA_RES_PRNT,
    "dt_soro":                      COLUNA_DT_SORO,
    "res_soro":                     COLUNA_RES_SORO,
    "dt_ns1":                       COLUNA_DT_NS1,
    "res_ns1":                      COLUNA_RES_NS1,
    "dt_isolamento":                COLUNA_DT_ISOLAMENTO,
    "res_isolamento":               COLUNA_RES_ISOLAMENTO,
    "dt_pcr":                       COLUNA_DT_PCR,
    "res_pcr":                      COLUNA_RES_PCR,
    "sorotipo":                     COLUNA_SOROTIPO,
    "histopatologia":               COLUNA_HISTOPATOLOGIA,
    "imunohistoquimica":            COLUNA_IMUNOHISTOQUIMICA,
    # Sinais clínicos
    "febre":                        COLUNA_FEBRE,
    "mialgia":                      COLUNA_MIALGIA,
    "cefaleia":                     COLUNA_CEFALEIA,
    "exantema":                     COLUNA_EXANTEMA,
    "vomito":                       COLUNA_VOMITO,
    "nausea":                       COLUNA_NAUSEA,
    "dor_costas":                   COLUNA_DOR_COSTAS,
    "conjutivite":                  COLUNA_CONJUTIVITE,
    "artrite":                      COLUNA_ARTRITE,
    "artralgia":                    COLUNA_ARTRALGIA,
    "petequia_n":                   COLUNA_PETEQUIA_N,
    "leucopenia":                   COLUNA_LEUCOPENIA,
    "laco":                         COLUNA_LACO,
    "dor_retro":                    COLUNA_DOR_RETRO,
    "diabetes":                     COLUNA_DIABETES,
    "hematolog":                    COLUNA_HEMATOLOG,
    "hepatopat":                    COLUNA_HEPATOPAT,
    "renal":                        COLUNA_RENAL,
    "hipertensao":                  COLUNA_HIPERTENSAO,
    "acido_pept":                   COLUNA_ACIDO_PEPT,
    "auto_imune":                   COLUNA_AUTO_IMUNE,
    "clinc_chik":                   COLUNA_CLINC_CHIK,
    # Sinais de alarme
    "alrm_hipot":                   COLUNA_ALRM_HIPOT,
    "alrm_plaq":                    COLUNA_ALRM_PLAQ,
    "alrm_vom":                     COLUNA_ALRM_VOM,
    "alrm_sang":                    COLUNA_ALRM_SANG,
    "alrm_hemat":                   COLUNA_ALRM_HEMAT,
    "alrm_abdom":                   COLUNA_ALRM_ABDOM,
    "alrm_letar":                   COLUNA_ALRM_LETAR,
    "alrm_hepat":                   COLUNA_ALRM_HEPAT,
    "alrm_liq":                     COLUNA_ALRM_LIQ,
    "dt_alarme":                    COLUNA_DT_ALARME,
    # Sinais de gravidade
    "grav_pulso":                   COLUNA_GRAV_PULSO,
    "grav_conv":                    COLUNA_GRAV_CONV,
    "grav_ench":                    COLUNA_GRAV_ENCH,
    "grav_insuf":                   COLUNA_GRAV_INSUF,
    "grav_taqui":                   COLUNA_GRAV_TAQUI,
    "grav_extre":                   COLUNA_GRAV_EXTRE,
    "grav_hipot":                   COLUNA_GRAV_HIPOT,
    "grav_hemat":                   COLUNA_GRAV_HEMAT,
    "grav_melen":                   COLUNA_GRAV_MELEN,
    "grav_metro":                   COLUNA_GRAV_METRO,
    "grav_sang":                    COLUNA_GRAV_SANG,
    "grav_ast":                     COLUNA_GRAV_AST,
    "grav_mioc":                    COLUNA_GRAV_MIOC,
    "grav_consc":                   COLUNA_GRAV_CONSC,
    "grav_orgao":                   COLUNA_GRAV_ORGAO,
    "dt_grav":                      COLUNA_DT_GRAV,
    # Manifestações hemorrágicas
    "mani_hemor":                   COLUNA_MANI_HEMOR,
    "epistaxe":                     COLUNA_EPISTAXE,
    "gengivo":                      COLUNA_GENGIVO,
    "metro_hemor":                  COLUNA_METRO,
    "petequias":                    COLUNA_PETEQUIAS,
    "hematura":                     COLUNA_HEMATURA,
    "sangram":                      COLUNA_SANGRAM,
    "laco_n":                       COLUNA_LACO_N,
    "plasmatico":                   COLUNA_PLASMATICO,
    "evidencia":                    COLUNA_EVIDENCIA,
    "plaq_menor":                   COLUNA_PLAQ_MENOR,
    "con_fhd":                      COLUNA_CON_FHD,
    # Complicações e observações
    "complica":                     COLUNA_COMPLICA,
    "ds_obs":                       COLUNA_DS_OBS,
    # Controle
    "duplicidade":                  COLUNA_DUPLICIDADE,
}