import plotly.express as px
import streamlit as st

import utils
from utils import BLUE, RISCO, br

df = utils.filtros_pagina("produtos", "produto")
utils.titulo_pagina("Avaliações X Produtos", "Quais produtos concentram as avaliações e como está a nota deles?")
utils.exige_dados(df)

quad = df["quadrante"].value_counts()
k = st.columns(3)
k[0].metric("Estrela", br(quad.get("Estrela", 0)), help="Alto engajamento e nota ≥ 4,3")
k[1].metric("Joia escondida", br(quad.get("Joia escondida", 0)), help="Baixo engajamento e nota ≥ 4,3")
k[2].metric("Produtos em risco", br(quad.get(RISCO, 0)), help="Alto engajamento e nota < 4,0")

# listagens únicas: variantes de um mesmo produto (cores) não aparecem duas vezes.
# Como no Power BI, agrupa por nome curto e usa a média de avaliações do nome.
top = (utils.listagens_unicas(df).dropna(subset=["rating_count"]).groupby("nome_curto", as_index=False)
       .agg(rating_count=("rating_count", "mean"), rating=("rating", "first"), cat_sub_lbl=("cat_sub_lbl", "first"))
       .nlargest(10, "rating_count"))
fig = px.bar(top, x="rating_count", y="nome_curto", orientation="h", color_discrete_sequence=[BLUE],
             text=top["rating_count"].map(br), title="Top 10 produtos com maior número de avaliações",
             hover_data={"rating": True, "cat_sub_lbl": True})
fig.update_yaxes(title="", autorange="reversed")
fig.update_xaxes(title="Avaliações")
fig.update_traces(textposition="outside")
st.plotly_chart(utils.estilo_fig(fig, 420, False), width="stretch")

st.subheader("Todos os produtos")
st.caption("Uma linha por listagem: variantes (cores) com a mesma nota e número de avaliações aparecem uma vez.")
tab = utils.listagens_unicas(df)[["nome_curto", "cat_sub_lbl", "actual_price_inr", "discounted_price_inr", "rating", "rating_count"]].rename(columns={
    "nome_curto": "Produto", "cat_sub_lbl": "Subcategoria", "actual_price_inr": "Preço real (₹)",
    "discounted_price_inr": "Preço com desconto (₹)", "rating": "Nota", "rating_count": "Avaliações"})
st.dataframe(tab.sort_values("Avaliações", ascending=False), hide_index=True, width="stretch")

with st.expander("Detalhe de um produto"):
    nome = st.selectbox("Produto", df["product_name"].sort_values().unique(), index=None, placeholder="Escolha um produto")
    if nome:
        p = df[df["product_name"] == nome].iloc[0]
        st.write(f"**{p['product_name']}**")
        st.write(f"Categoria: {p['cat_principal']} · Nota {br(p['rating'], 1)} · {br(p['rating_count'])} avaliações · "
                 f"Preço {utils.rs(p['discounted_price_inr'])} (de {utils.rs(p['actual_price_inr'])})")
        if isinstance(p["product_link"], str):
            st.link_button("Abrir na Amazon", p["product_link"])
utils.rodape()
