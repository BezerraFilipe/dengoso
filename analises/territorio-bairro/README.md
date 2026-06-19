# Hipótese 2 — Tempo até atendimento por bairro

**Pergunta:** o tempo até o atendimento/internação varia conforme o bairro de residência?
(`zona_residencia` é degenerada em Recife — 1 rural, 2 periurbanas — então a unidade
geográfica é o **bairro**.)

**Conclusão:** **SIM.** Kruskal-Wallis entre os 35 bairros com n ≥ 30:
**H = 182,87; p = 2,69 × 10⁻²²** → rejeita H₀, e a rejeição **resiste à remoção de outliers**
(p = 2,13 × 10⁻²²). O efeito é pequeno (ε² = 0,064) e o intervalo de medianas é estreito
(0–5 d). Dunn: 49/595 pares (8%) significativos. **Bairros de risco** (mediana 5 d):
Jardim São Paulo, Afogados, Santo Amaro, Imbiribeira (+ Areias/Cohab/Ibura). CORDEIRO sai do
ranking real (mediana 4; a média 284 é o outlier de 19.100 dias).
**Contraste com a H1:** o tempo discrimina bairro, mas não desfecho → ligado a acesso/logística.

## Scripts e saídas
| Arquivo | Processo | Saída |
|---|---|---|
| `desc_territorio.py` | P7 descritiva territorial | `figuras/top_bairros_delta.png`, `figuras/delta_por_zona.png`, `ranking_bairros.csv` |
| `teste_territorio.py` | P12 Kruskal-Wallis + Dunn (Holm) | `figuras/teste_territorio_bairros.png`, `dunn_bairros.csv`, `ranking_risco_bairros.csv` |

## Como rodar (a partir de `dengoso/`)
```bash
python3 analises/geral/pipeline.py        # 1x: garante a base
python3 analises/territorio-bairro/desc_territorio.py
python3 analises/territorio-bairro/teste_territorio.py
```
