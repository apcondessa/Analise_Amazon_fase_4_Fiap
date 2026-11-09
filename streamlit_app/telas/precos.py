import plotly.express as px
import streamlit as st

import utils
from utils import BLUE, br

df = utils.base()
utils.titulo_pagina("Preços e Estratégia Comercial", "Dar mais desconto melhora a nota? Os dados mostram uma relação fraca.")

k = st.columns(6)
k[0].metric("Desconto médio", br(df["discount_pct"].mean() * 100, 1, sufixo="%"))
k[1].metric("Economia média", utils.rs(df["discount_value_inr"].mean()))
k[2].metric("Preço médio com desconto", utils.rs(df["discounted_price_inr"].mean()))
k[3].metric("Desconto ≥ 50%", br((df["discount_pct"] >= 0.5).mean() * 100, 0, sufixo="%"),
            help="Parcela dos produtos com desconto de 50% ou mais")
k[4].metric("Rating médio", br(df["rating"].mean(), 2))
k[5].metric("Correlação", br(utils.correlacao(df), 2), help="Correlação de Pearson entre desconto e nota")

c1, c2 = st.columns([1, 1.7])
with c1:
    d = df.dropna(subset=["rating"])
    fig = px.scatter(d, x="discount_pct", y="rating", opacity=0.45, hover_name="nome_curto",
                     color_discrete_sequence=[BLUE], title="Desconto × nota (um ponto por produto)")
    fig.update_xaxes(title="Desconto", tickformat=".0%")
    fig.update_yaxes(title="Nota")
    st.plotly_chart(utils.estilo_fig(fig, 480, False), width="stretch")
    with st.container(border=True):
        st.markdown("**Descontos maiores não correspondem a notas melhores.**\n\n"
                    "- A nota cai de 4,17 (descontos de 0–20%) para 3,97 (descontos acima de 80%).\n"
                    "- O gráfico de dispersão apresenta correlação fraca (−0,16): é associação, não causa.")
with c2:
    g = df.groupby("faixa_desconto", observed=True)["rating"].mean().reset_index(name="mean")
    fig = px.bar(g, x="faixa_desconto", y="mean", text=g["mean"].map(lambda v: br(v, 2)),
                 title="Rating médio por faixa de desconto", color_discrete_sequence=[BLUE])
    fig.update_yaxes(title="Rating médio (eixo de 3,8 a 4,3)", range=[3.8, 4.3])
    fig.update_xaxes(title="Faixa de desconto")
    st.plotly_chart(utils.estilo_fig(fig, 340, False), width="stretch")

    h = df.pivot_table(index="cat_grupo", columns="faixa_desconto", values="rating", aggfunc="mean", observed=True)
    fig = px.imshow(h, text_auto=".2f", aspect="auto", color_continuous_scale="Blues", zmin=3.75, zmax=4.35,
                    title="Rating médio X faixa de desconto e categoria dos grupos")
    fig.update_xaxes(title="Faixa de desconto")
    fig.update_yaxes(title="")
    st.plotly_chart(utils.estilo_fig(fig, 340, False), width="stretch")
utils.rodape()
