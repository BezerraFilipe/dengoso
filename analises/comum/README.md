# Comum — infraestrutura compartilhada

Código importado por **todos** os temas de análise. Não produz resultado próprio; é a
base que lê, limpa e disponibiliza os dados.

| Arquivo | Papel |
|---|---|
| `pipeline.py` | Tarefas 1–3: DataFrame único, `delta_dias`, base limpa. Resolve `ROOT = dengoso/`. Gera `../../reports/relatorio.md` e `base_limpa.csv`. |
| `utils.py` | `parse_datas`, `normaliza_categoria`, `decodifica_idade`. |
| `mappings.py` | `ALL_MAPPINGS`, `COLUNAS_USADAS`. |
| `diagnostico.py` | Diagnóstico de preenchimento por ano. |

Os scripts dos demais temas adicionam esta pasta ao `sys.path` e importam
`pipeline`/`utils`/`mappings`. Rode sempre **a partir da raiz `dengoso/`**.

## Como rodar (a partir de `dengoso/`)
```bash
python3 analises/comum/pipeline.py       # base: reports/relatorio.md, base_limpa.csv
python3 analises/comum/diagnostico.py    # (opcional) preenchimento por ano
```
