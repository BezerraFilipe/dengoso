# Hipótese 1 — Tempo de internação × desfecho

**Pergunta:** o tempo entre o início dos sintomas e a internação (`delta_dias`) está
associado ao desfecho (cura × óbito)? **Vale só para os internados (~3% da base).**

**Conclusão:** **NÃO.** A mediana é ~4 dias em todos os desfechos; correlação de Spearman
desprezível (ρ = 0,040); o p = 0,034 do teste principal é artefato de n grande (efeito
desprezível, IC95% da diferença em [−1, +1] dia); comparação clínica (p = 0,18) e
Kruskal-Wallis (p = 0,072) não rejeitam H₀. **O tempo até internar não discrimina o desfecho.**

## Scripts (geram figuras em `figuras/`)
| Arquivo | Processo | Saída |
|---|---|---|
| `desc_delta.py` | P6 descritiva por desfecho | `delta_por_desfecho.png` |
| `dist_delta.py` | P8 distribuição/normalidade (KDE) | `dist_delta_por_desfecho.png` |
| `teste_normalidade.py` | P9 Shapiro/KS + QQ-plot | `qqplot_delta_por_desfecho.png` |
| `teste_correlacao.py` | P10 Spearman | `matriz_correlacao.png` |
| `teste_hipotese.py` | P11 Mann-Whitney + IC bootstrap + Kruskal | `teste_hipotese_cura_obito.png` |

## Como rodar (a partir de `dengoso/`)
```bash
python3 analises/comum/pipeline.py        # 1x: garante a base
python3 analises/internacao-desfecho/desc_delta.py
python3 analises/internacao-desfecho/dist_delta.py
python3 analises/internacao-desfecho/teste_normalidade.py
python3 analises/internacao-desfecho/teste_correlacao.py
python3 analises/internacao-desfecho/teste_hipotese.py
```
