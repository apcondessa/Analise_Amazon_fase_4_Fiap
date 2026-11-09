# Amazon Product Performance & Customer Insights

Tech Challenge · Fase 4 · POSTECH/FIAP. Análise de 1.351 produtos do *Amazon Sales Dataset* para responder: **quais produtos e categorias merecem atenção, como desconto e preço se relacionam com a nota, e o que os clientes dizem?**

| Entregável | Onde está |
|---|---|
| Notebook de tratamento e análise | `notebooks/TECH_CHALLENGE__FASE_4_AMAZON.ipynb` |
| Dashboard Power BI (11 páginas) | `powerbi/Tech_Challenge_Amazon_Fiap_Fase_4.pbix` |
| Medidas DAX (medidas, colunas e tabelas calculadas) | `powerbi/medidas.dax` |
| Consultas do Power Query (M) | `powerbi/consultas_power_query.pq` |
| Dashboard online (Streamlit, mesmas 11 páginas) | `streamlit_app/.(https://amazon-fase4-fiap.streamlit.app)|
| Relatório executivo (Google Docs) | [Abrir o relatório](https://docs.google.com/document/d/1nJ6-IzIBC5tEF3M564fA08emyZh-X_lt-B6tJHeiHjE/edit?usp=sharing) |
| Apresentação (Google Slides) | [Abrir os slides](https://docs.google.com/presentation/d/1Utp5Bee0UqbSHt3OzNIuMrp_cH8OD9uVWmhEA0f41BQ/edit?usp=sharing) |
| Vídeo executivo (YouTube) | [Assistir ao vídeo](https://www.youtube.com/watch?v=pTv3qIHMpzY) |
| Base de dados usada pelo Power BI | [apcondessa/Amazon_dataset](https://github.com/apcondessa/Amazon_dataset) |

## Base e metodologia

- **Fonte:** [Amazon Sales Dataset (Kaggle)](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset). Preços em rupias (₹).
- **Tratamento:** limpeza de preços e percentuais, separação das categorias (principal, subcategoria e folha), faixas de preço e de desconto, temas extraídos das avaliações e palavras mais frequentes por grupo de nota.
- **Avaliações únicas:** variantes (cores) do mesmo produto repetem a nota e o número de avaliações. O painel conta cada combinação de nota e número de avaliações uma vez (coluna `Flag Listagem`). A soma simples daria 23,8 milhões, 30,5% a mais que as **18,2 milhões** reais.
- **Rating ponderado:** média das notas ponderada pelo número de avaliações (4,16). O rating médio simples é 4,09.
- **Grupos de nota:** bem avaliados (≥ 4,3: 419 produtos, 31,0%), mal avaliados (< 4,0: 340, 25,2%) e intermediários (591, 43,8%), sobre os 1.350 produtos com nota.
- **Segmentação por quartis de avaliações:** alto engajamento a partir do P75 (~16.000 avaliações) e baixo engajamento até o P25 (~1.100).
  - **Em risco:** alto engajamento e nota < 4,0.
  - **Estrela:** alto engajamento e nota ≥ 4,3.
  - **Joia escondida:** baixo engajamento e nota ≥ 4,3.
- Produtos sem nota ou sem avaliações ficam na base, mas fora dos cálculos de satisfação (3 produtos).

## Páginas do dashboard

| # | Página | O que responde |
|---|---|---|
| 1 | Início | Navegação entre as páginas. |
| 2 | Visão Executiva | Cartões principais (inclui desconto médio), intervalos de nota e segmentação em quartis. |
| 3 | Engajamento × Satisfação | Concentração das avaliações, dispersão avaliações × nota por quadrante e nota por categoria. |
| 4 | Avaliações X Notas | Distribuição das avaliações por faixa de nota nas 3 maiores categorias. |
| 5 | Avaliações X Produtos | Top 10 produtos por avaliações e lista completa. |
| 6 | Prod. Notas < 4 | Os 20 produtos de maior preço real com nota abaixo de 4. |
| 7 | Prod. Notas ≥ 4,3 | Os 20 produtos de maior preço real com nota de 4,3 ou mais. |
| 8 | Preços e Estratégia Comercial | Relação entre desconto e nota (correlação de −0,16). |
| 9 | Customer Insights | Palavras que diferenciam mal e bem avaliados, geral e em Electronics. |
| 10 | Avaliação X Temas | Temas citados por grupo de nota. |
| 11 | Oportunidades & Recomendações | Quadrantes, top 10 em risco, respostas às perguntas do desafio e mensagens finais (no Streamlit, também o plano de ação). |

## Principais resultados

- **Portfólio:** 1.351 produtos, 9 categorias, 18,2 milhões de avaliações únicas, rating ponderado de 4,16. Um em cada quatro produtos (25,2%) tem nota < 4.
- **Risco concentrado:** 49 produtos de alto engajamento têm nota < 4,0. 30 deles são de Electronics (14 fones, 7 wearables, 6 celulares e acessórios, entre outros). O portfólio de fones tem 63 produtos e nota média de 3,92.
- **Concentração:** 23% dos produtos somam 80% das avaliações. As 112 estrelas (8% dos produtos) concentram 25% das avaliações.
- **Oportunidade:** 112 estrelas e 81 joias escondidas, que têm nota ≥ 4,3, mas só 0,2% das avaliações.
- **Desconto:** o desconto médio é 46,7% e 49% dos produtos têm desconto de 50% ou mais. A nota cai de 4,17 (0–20%) para 3,97 (acima de 80%), mas a correlação é fraca (−0,16; Spearman −0,15). É associação, não causa.
- **Temas (bem − mal avaliados):** Instalação/Uso +14,2 pp, Entrega/Embalagem +11,0 pp, Desempenho +5,8 pp e Qualidade +5,2 pp. Bateria/Carga aparece 7,7 pp mais entre os mal avaliados.
- **Preço alto e nota baixa:** dos 20 produtos mais caros com nota < 4, 14 são de Electronics. O preço real médio é ₹17.599 e eles somam 96.613 avaliações.
- **Preço alto e nota alta:** dos 20 produtos mais caros com nota ≥ 4,3, 15 são de Electronics. O preço real médio é ₹49.712 (quase 3 vezes o do grupo de nota baixa) e eles somam 189.070 avaliações: a faixa premium, em geral, é bem avaliada.

## Recomendações

1. **Reputação:** auditar os fones de ouvido antes de novos descontos (gerência de Eletrônicos e Qualidade).
2. **Desconto:** testar faixas de 20% a 60% com grupo de controle antes de mudar a política (Precificação).
3. **Visibilidade:** dar espaço às joias escondidas com banners, recomendações cruzadas e anúncios patrocinados, começando por 20 itens (Marketing).
4. **Estrelas:** monitorar a nota para não perder a posição (categorias e Qualidade).
5. **Acompanhamento:** medir todo mês a % de produtos com nota < 4 (Analytics).

## Estrutura do repositório

```
.
├── data/
│   ├── raw_amazon.csv                 # dados originais
│   └── tratados/                      # CSV usados pelo Power BI e pelo Streamlit
│       ├── amazon_tratado.csv
│       ├── palavras_grupos.csv
│       ├── palavras_por_categoria.csv
│       ├── temas_grupos.csv
│       └── produtos_tratados.csv
├── imagens/                           # gráficos do notebook
├── notebooks/TECH_CHALLENGE__FASE_4_AMAZON.ipynb
├── powerbi/
│   ├── Tech_Challenge_Amazon_Fiap_Fase_4.pbix
│   ├── medidas.dax
│   └── consultas_power_query.pq
├── streamlit_app/
│   ├── app.py                         # navegação (11 páginas)
│   ├── utils.py                       # dados, filtros de cada página, cálculos equivalentes às medidas DAX e estilo
│   └── telas/                         # inicio, executiva, engajamento, notas, produtos, notas_baixas, notas_altas,
│                                      # precos, clientes, temas, recomendacoes
├── .streamlit/config.toml             # tema do app (tons de cinza do dashboard)
├── requirements.txt
└── README.md
```

## Como abrir o dashboard no Power BI

1. Abra o arquivo `.pbix` em `powerbi/` no Power BI Desktop.
2. Clique em **Atualizar**. Os dados são carregados automaticamente do repositório público [apcondessa/Amazon_dataset](https://github.com/apcondessa/Amazon_dataset), sem precisar configurar caminho no computador.
3. Se o Power BI pedir credencial, escolha **Anônimo** → **Conectar**. Se aparecer aviso de privacidade, marque as fontes como **Público**.

> O parâmetro `Pasta` (Transformar dados → Gerenciar parâmetros) aponta para `https://raw.githubusercontent.com/apcondessa/Amazon_dataset/main/`. Para usar os CSV locais de `data/tratados/`, troque o valor pelo caminho da pasta, terminado em barra (ex.: `C:\projeto\data\tratados\`), e troque `Web.Contents` por `File.Contents` nas consultas.

Para recriar o modelo do zero, use `powerbi/consultas_power_query.pq` (consultas) e `powerbi/medidas.dax` (28 medidas, 11 colunas calculadas e 3 tabelas calculadas). O arquivo `.dax` explica onde cada item é usado. As conversões usam a cultura `en-US`, necessária para ler os decimais dos CSV.

## Como rodar o dashboard Streamlit

🔗 **App publicado:** _adicionar link (`https://amazon-fase4-fiap.streamlit.app`)_

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

O app abre em `http://localhost:8501`. Ele lê os CSV de `data/tratados/` (na raiz do repositório, ao lado de `streamlit_app/`). A barra lateral mostra os filtros de cada página, os mesmos do Power BI. As páginas sem filtro no Power BI também não têm filtro no app.

### Publicar no Streamlit Community Cloud

1. Suba o repositório para o GitHub, incluindo `data/tratados/` e `requirements.txt`.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e entre com sua conta do GitHub.
3. Clique em **Create app**, escolha o repositório e a branch.
4. Em **Main file path**, informe `streamlit_app/app.py` e clique em **Deploy**.

### Problemas comuns

| Sintoma | Solução |
|---|---|
| "Não encontrei `amazon_tratado.csv`" | Confirme que `data/tratados/` está na raiz do repositório. |
| `st.navigation` não existe | Atualize: `pip install -U "streamlit>=1.50"`. |
| Porta 8501 ocupada | `streamlit run streamlit_app/app.py --server.port 8502`. |
| Números diferentes do Power BI | O app usa os mesmos filtros e fórmulas. Confira se os filtros da página na barra lateral estão vazios. |

## Limitações

- O dataset é uma amostra do catálogo. Os resultados valem para esta base, não para a Amazon inteira.
- Desconto, preço e nota mostram **associações, não causas**.
- As palavras e os temas vêm de uma amostra de avaliações por produto.
- Subcategorias e categorias pequenas têm poucos produtos e exigem cuidado na leitura.
- Preços em rupias (₹), sem conversão cambial.

## Tecnologias

Python (pandas, numpy, plotly), Streamlit, Power BI (DAX e Power Query), Google Colab.

## Equipe

_**Ana Paula Machado Condessa - rm373492**_  
_**Jhennifer Aparecida Oliveira Freitas - rm370853**_  
_**Lucas Henrique da Silva Cruz - rm374131**_  
_**Pedro Paulo Goes Alves - rm370771**_  
_**João Vicente da Rosa da Silveira - rm372552**_
