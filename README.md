# Dengoso


Uma abordagem estatística sobre a questão das arbovirores na cidade do Recife.

Esse repositório documenta decisões técnicas de projeto além da implementação de fato das análises feitas.

Para ver o resultado final, consulte o artigo ...

---

## Estrutura do repo

``` text
dengoso/
├──analises/ # códigos + gráficos, separados por tema
│  ├──geral/              # infra (pipeline/utils/mappings) + análises que servem às duas hipóteses
│  ├──internacao-desfecho/# Hipótese 1: tempo de internação × desfecho
│  ├──territorio-bairro/  # Hipótese 2: tempo até atendimento por bairro
│  └──riscos/             # gravidade e fatores de risco (em andamento)
├──docs/ # documentações diversas
├──data/ # base de dados csv utilizada
├──reports/ # saídas gerais (base_limpa.csv, distribuicoes.csv, relatorio.md)
└──src/aed/ # scripts antigos (legado, não usados)
```

Cada pasta de `analises/` tem um `README.md` próprio com a conclusão e como rodar. Os
scripts de cada tema importam a infra de `analises/geral/`, então rode sempre **a partir da
raiz `dengoso/`** (ex.: `python3 analises/geral/pipeline.py`).

Para anexar a base de dados, descompacte [esse arquivo](https://drive.google.com/file/d/1EUHq8jpjr3oKz9iFQr6bo4OvB6j_8aml/view?usp=sharing) e o copie para o diretório raiz com o nome "data"
