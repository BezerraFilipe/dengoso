# Geral — infraestrutura e análises que servem às duas hipóteses

Código compartilhado e análises que **não** pertencem a uma só hipótese (cruzam desfecho
e bairro, ou são base para tudo).

## Infraestrutura (importada por todos os temas)
| Arquivo | Papel |
|---|---|
| `pipeline.py` | Tarefas 1–3: DataFrame único, `delta_dias`, base limpa. Resolve `ROOT = dengoso/`. Gera `../../reports/relatorio.md` e `base_limpa.csv`. |
| `utils.py` | `parse_datas`, `normaliza_categoria`, `decodifica_idade`. |
| `mappings.py` | `ALL_MAPPINGS`, `COLUNAS_USADAS`. |
| `diagnostico.py` | Diagnóstico de preenchimento por ano. |

## Análises gerais (geram figuras em `figuras/`)
| Arquivo | Processo | Saída |
|---|---|---|
| `distribuicoes.py` | P4–5 presença/escopo | `figuras/presenca_relativa.png`, `../../reports/distribuicoes.csv` |
| `sintese_visual.py` | P13 síntese | `figuras/viz_final_{1_desfecho,2_bairros,3_serie_temporal}.png` |
| `delta_notificacao.py` | P14 tempo até notificação (Q1 desfecho + Q2 bairro, ~100% dos casos) | `figuras/viz_complementar_notificacao.png` |

## Como rodar (a partir de `dengoso/`)
```bash
python3 analises/geral/pipeline.py        # base (relatorio.md, base_limpa.csv em reports/)
python3 analises/geral/distribuicoes.py
python3 analises/geral/sintese_visual.py
python3 analises/geral/delta_notificacao.py
```
Os scripts dos demais temas dependem desta pasta (importam `pipeline`/`utils`/`mappings`).
