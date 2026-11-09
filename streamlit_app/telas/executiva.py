import plotly.express as px
import streamlit as st

import utils
from utils import QUAD_COLORS, QUAD_DESTAQUE, RISCO, br

df = utils.filtros_pagina("executiva", "preco", "desconto")
utils.titulo_pagina("Visão Executiva", "Como está o portfólio? Nota média boa, mas há produtos de alto engajamento com nota baixa.")
utils.exige_dados(df)

k = st.columns(6)
k[0].metric("Total de produtos", br(df["product_id"].nunique()))
k[1].metric("Categorias totais", br(df["cat_principal"].nunique()))
k[2].metric("Avaliações totais", utils.milhoes(utils.avaliacoes_unicas(df)))
k[3].metric("Rating ponderado", br(utils.rating_ponderado(df), 2))
k[4].metric("Desconto médio", br(df["discount_pct"].mean() * 100, 1, sufixo="%"))
k[5].metric("Produtos nota < 4", br(utils.pct_nota_menor_4(df) * 100, 1, sufixo="%"))

com_nota = df.dropna(subset=["rating"])
risco = df[df["quadrante"] == RISCO]
n_ele = (risco["cat_principal"] == "Electronics").sum()

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("**Segmentação dos produtos (quartis)**\n\n"
                    "- **Alto engajamento:** a partir do P75 (4º quartil), cerca de 16.000 avaliações.\n"
                    "- **Baixo engajamento:** até o P25 (1º quartil), cerca de 1.100 avaliações.")
    with st.container(border=True):
        st.markdown("**Notas de avaliação de produtos pelos clientes: intervalos**")
        a, b = st.columns(2)
        if len(com_nota):
            a.metric("Mal avaliados (< 4,0)", br((com_nota["rating"] < 4).mean() * 100, 1, sufixo="%"))
            b.metric("Bem avaliados (≥ 4,3)", br((com_nota["rating"] >= 4.3).mean() * 100, 1, sufixo="%"))
    with st.container(border=True):
        st.markdown(f"**{br(len(risco))} produtos de alto engajamento têm nota < 4,0.** "
                    f"{br(n_ele)} destes pertencem à categoria de Eletrônicos.")

with c2:
    q = df[df["quadrante"].isin(QUAD_DESTAQUE)]["quadrante"].value_counts(ascending=True).reset_index()
    q.columns = ["quadrante", "produtos"]
    fig = px.bar(q, x="produtos", y="quadrante", orientation="h", color="quadrante",
                 color_discrete_map=QUAD_COLORS, text="produtos", title="Produtos: Engajamento × Rating")
    fig.update_yaxes(title="")
    fig.update_xaxes(title="Produtos")
    st.plotly_chart(utils.estilo_fig(fig, 340, False), width="stretch")
    st.markdown("- **Produtos em risco:** alto engajamento e nota < 4,0.\n"
                "- **Joia escondida:** baixo engajamento e nota ≥ 4,3.\n"
                "- **Estrela:** alto engajamento e nota ≥ 4,3.")

utils.rodape()
