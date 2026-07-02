# Dengoso


Uma abordagem estatística sobre a questão das arbovirores na cidade do Recife.

Esse repositório documenta decisões técnicas de projeto além da implementação de fato das análises feitas.

Para ver o resultado final, consulte o artigo ...

---

## Estrutura do repo

``` text
dengoso/
├──analises/ # códigos + gráficos, separados por tema
│  ├──comum/              # infra compartilhada: pipeline, utils, mappings, diagnostico
│  ├──panorama/           # análises transversais: presença/escopo + síntese visual final
│  ├──internacao-desfecho/# Hipótese 1: tempo de internação × desfecho
│  ├──territorio-bairro/  # Hipótese 2: tempo até atendimento por bairro
│  └──complementares/     # iniciativas do grupo: tempo até notificação + gravidade graduada
├──docs/ # documentações diversas
├──data/ # base de dados csv utilizada
├──reports/ # saídas gerais (base_limpa.csv, distribuicoes.csv, relatorio.md)
└──src/aed/ # scripts antigos (legado, não usados)
```

Cada pasta de `analises/` tem um `README.md` próprio com a conclusão e como rodar. Os
scripts de cada tema importam a infra de `analises/comum/`, então rode sempre **a partir da
raiz `dengoso/`** (ex.: `python3 analises/comum/pipeline.py`).

A base de dados (SINAN — dengue, zika e chikungunya do Recife) já acompanha o repositório
em `data/`, então basta clonar; nenhum download adicional é necessário.
