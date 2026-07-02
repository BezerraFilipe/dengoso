# Complementares — iniciativas do grupo

Análises que vão além do que o enunciado pedia, para reforçar as duas hipóteses por
outros caminhos. Importam a infra de `../comum/`.

## Tempo até a notificação (~100% dos casos)
A variável do enunciado (`delta_dias = internação − sintoma`) só cobre ~3% dos casos.
`delta_notif = notificação − sintoma` está em ~99,9% da base e refaz Q1 (desfecho) e
Q2 (bairro):
- **Q1:** cura × óbito sem diferença (Mann-Whitney, p = 0,83) — confirma a Hipótese 1.
- **Q2:** diferença entre bairros ainda mais nítida (Kruskal-Wallis, medianas 3–12 dias)
  — reforça a leitura de desigualdade de acesso.

## Gravidade graduada (além do óbito)
Ir além do óbito binário e olhar a gravidade em 3 níveis (dengue / sinais de alarme / grave):
- **Gravidade ≠ óbito:** letalidade sobe 0,07% → 3,72% → 34,29%, validando a escala. O tempo
  até a notificação **não** varia com a gravidade (Kruskal-Wallis) — coerente com a conclusão central.
- **Tempo × gravidade (Spearman):** ρ = −0,0008 (p = 0,84; n = 59.704) — sem associação
  entre o tempo sintoma→notificação e a gravidade com que o caso chegou.

## Scripts e saídas
| Arquivo | Processo | Saída |
|---|---|---|
| `delta_notificacao.py` | P14 tempo até notificação (Q1 desfecho + Q2 bairro) | `figuras/viz_complementar_notificacao.png` |
| `gravidade.py` | P15 gravidade graduada (letalidade + tempo por nível, Kruskal-Wallis) | `figuras/viz_gravidade.png` |
| `spearman_tempo_gravidade.py` | Spearman tempo (sintoma→notificação) × gravidade | (impresso no terminal; texto em `spearman_tempo_gravidade.md`) |

## Como rodar (a partir de `dengoso/`)
```bash
python3 analises/comum/pipeline.py        # 1x: garante a base
python3 analises/complementares/delta_notificacao.py
python3 analises/complementares/gravidade.py
python3 analises/complementares/spearman_tempo_gravidade.py
```
