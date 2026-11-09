import plotly.graph_objects as go
import streamlit as st

import utils
from utils import AMBER, BLUE, br

utils.titulo_pagina("Prod. Notas ≥ 4,3", "Produtos com alta avaliação (notas ≥ 4,3): top 20 produtos de maior preço real")

# Top20_Preco_Real_Alta: nota ≥ 4,3, 1 linha por listagem, 20 maiores preços reais (empate: menor product_id)
top = utils.top20_preco_real(utils.base(), alta=True)

k = st.columns(3)
k[0].metric("Preço real médio (top 20)", utils.rs(top["actual_price_inr"].mean()))
k[1].metric("Soma de avaliações (top 20)", br(top["rating_count"].sum()))
k[2].metric("Em Electronics (Eletrônicos)", f"{br((top['cat_principal'] == 'Electronics').sum())} de {len(top)}")

fig = go.Figure()
fig.add_bar(x=top["posicao"], y=top["actual_price_inr"] / 1000, name="Preço real (₹)", marker_color=BLUE)
fig.add_bar(x=top["posicao"], y=top["rating_count"] / 1000, name="Número de avaliações", marker_color=AMBER)
fig.update_xaxes(title="Posição (1 = maior preço real)", dtick=1)
fig.update_yaxes(title_text="Milhares")
fig.update_layout(title="Preço real (milhares) e número de avaliações (milhares)", barmode="group")
st.plotly_chart(utils.estilo_fig(fig, 420), width="stretch")
st.caption("Alguns itens têm poucas avaliações (ex.: 7 ou 567); nesses casos a nota alta ainda não é conclusiva.")

c1, c2 = st.columns([1, 3])
with c1:
    pos = top[["posicao", "rating_count", "actual_price_inr"]].rename(columns={
        "posicao": "Posição", "rating_count": "Avaliações", "actual_price_inr": "Preço real (₹)"})
    st.dataframe(pos, hide_index=True, width="stretch", height=390)
with c2:
    tab = top[["nome_curto", "cat_principal", "cat_sub_lbl", "rating", "rating_count", "actual_price_inr"]].rename(columns={
        "nome_curto": "Produto", "cat_principal": "Categoria", "cat_sub_lbl": "Subcategoria",
        "rating": "Nota", "rating_count": "Avaliações", "actual_price_inr": "Preço real (₹)"})
    st.dataframe(tab, hide_index=True, width="stretch", height=390,
                 column_config={"Produto": st.column_config.TextColumn(width="medium")})
utils.rodape()
