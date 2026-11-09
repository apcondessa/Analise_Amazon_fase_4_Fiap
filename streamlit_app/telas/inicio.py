import streamlit as st

import utils
from utils import br

utils.titulo_pagina("Amazon: Product Performance & Customer Insights",
                    "Tech Challenge · Fase 4 · E-commerce · Portfólio · Desconto · Sentimento")
df = utils.base()

k = st.columns(4)
k[0].metric("Produtos analisados", br(df["product_id"].nunique()))
k[1].metric("Categorias", br(df["cat_principal"].nunique()))
k[2].metric("Avaliações totais", utils.milhoes(utils.avaliacoes_unicas(df)))
k[3].metric("Rating ponderado", br(utils.rating_ponderado(df), 2))

st.caption("Jornada analítica: Preço → Desconto → Engajamento → Satisfação")
st.subheader("Selecione uma página do dashboard")

PAGINAS = [
    ("telas/executiva.py", "📈 Visão Executiva", "A saúde do portfólio."),
    ("telas/engajamento.py", "🎯 Engajamento × Satisfação", "Onde a reputação se concentra."),
    ("telas/notas.py", "⭐ Avaliações X Notas", "Como as notas se distribuem."),
    ("telas/produtos.py", "🛒 Avaliações X Produtos", "Quem lidera em avaliações."),
    ("telas/notas_baixas.py", "⚠️ Prod. Notas < 4", "Caros e mal avaliados."),
    ("telas/notas_altas.py", "🏆 Prod. Notas ≥ 4,3", "Caros e bem avaliados."),
    ("telas/precos.py", "💰 Preços e Estratégia Comercial", "Desconto garante nota?"),
    ("telas/clientes.py", "💬 Customer Insights", "O que o cliente diz."),
    ("telas/temas.py", "🏷️ Avaliação X Temas", "Os temas por trás da nota."),
    ("telas/recomendacoes.py", "✅ Oportunidades & Recomendações", "Onde agir primeiro."),
]
cols = st.columns(3)
for i, (caminho, titulo, texto) in enumerate(PAGINAS):
    with cols[i % 3].container(border=True):
        st.page_link(caminho, label=titulo)
        st.caption(texto)

st.info("Os filtros de cada página ficam na barra lateral, os mesmos do Power BI. "
        "Os cálculos seguem as medidas DAX do dashboard.")
utils.rodape()
