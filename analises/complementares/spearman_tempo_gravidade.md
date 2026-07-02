# Spearman — tempo até a notificação × gravidade do caso

**Pergunta:** o tempo dos **primeiros sintomas até a notificação no sistema de saúde**
(`delta_notif = dt_notificacao − dt_sintoma`) tem relação com a **gravidade com que o caso
chegou** (1-Dengue comum, 2-Dengue com sinais de alarme, 3-Dengue grave)?

> Observação: aqui o tempo é medido até a **notificação** (entrada no sistema, ~100% dos
> casos), **não** até a internação (`delta_dias`, que só existe em ~3% dos casos).

## Método

- **Coeficiente:** Spearman (ρ) — não-paramétrico, escolhido porque a distribuição do tempo
  é assimétrica / não-normal (Shapiro rejeitado nos processos anteriores). Adequado também
  porque a gravidade é uma variável **ordinal** (1 < 2 < 3).
- **População:** base limpa (casos confirmados); `delta_notif` válido (≥ 0) e gravidade
  classificada em 1–3. Códigos SINAN harmonizados: `10/1 → 1-Dengue`, `11/2 → 2-Sinais de
  alarme`, `12/3 → 3-Grave` (5-descartado e 8-inconclusivo ficam de fora).

## Resultado

| | valor |
|---|---|
| **ρ de Spearman** | **−0,0008** |
| **p-valor** | **0,84** |
| **n** | **59.704** |

Tempo mediano do sintoma até a notificação, por nível de gravidade:

| nível | n | mediana | média |
|---|--:|--:|--:|
| 1-Dengue | 59.281 | 6 dias | 15,5 dias |
| 2-Sinais de alarme | 387 | 6 dias | 9,0 dias |
| 3-Grave | 36 | 6 dias | 9,8 dias |

## Interpretação

**ρ = −0,0008 é praticamente zero** (numa escala de −1 a +1; o critério de viabilidade do
grupo era |r| > 0,5, ~625 vezes maior). O **p = 0,84** também não é significativo (bem acima
de α = 0,05) — ou seja, nem sequer há indício de associação. **Não existe relação entre o
tempo que a pessoa levou para entrar no sistema de saúde e a gravidade com que o caso
chegou.** As medianas idênticas (6 dias nos três níveis) reforçam a conclusão.

Isso é coerente com o restante do trabalho: o tempo de acesso ao atendimento **não distingue**
a evolução clínica do paciente (nem o desfecho cura × óbito, nem a gravidade) — o que varia é
**onde** a pessoa mora (diferença territorial entre bairros).

## Código

Script reprodutível em [`spearman_tempo_gravidade.py`](spearman_tempo_gravidade.py). Trecho central:

```python
from scipy import stats

# grav: gravidade 1..3 (de CLASSI_FIN); dnotif: dt_notificacao - dt_sintoma (em dias)
r, p = stats.spearmanr(dnotif, grav)
# -> rho = -0.0008, p = 0.84, n = 59.704
```
