# Panorama — análises transversais

Análises que **não** pertencem a uma só hipótese: descrevem a base como um todo e
fecham o trabalho em visualizações. Importam a infra de `../comum/`.

| Arquivo | Processo | Saída |
|---|---|---|
| `distribuicoes.py` | P4–5 presença/escopo | `figuras/presenca_relativa.png`, `../../reports/distribuicoes.csv` |
| `sintese_visual.py` | P13 síntese | `figuras/viz_final_{1_desfecho,2_bairros,3_serie_temporal}.png` |

## Como rodar (a partir de `dengoso/`)
```bash
python3 analises/comum/pipeline.py        # 1x: garante a base
python3 analises/panorama/distribuicoes.py
python3 analises/panorama/sintese_visual.py
```
