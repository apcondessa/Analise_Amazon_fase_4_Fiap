import plotly.express as px
import streamlit as st

import utils
from utils import BLUE, RED, br

pg, pc = utils.carregar_palavras()
# como no Power BI: o filtro "Palavras" só age no gráfico por categoria (tabela palavras_por_categoria)
st.sidebar.markdown("### Filtros desta página")
sel_palavras = utils.filtro("Palavras", sorted(pc["palavra"].dropna().unique()), "filtro_clientes_palavras")
utils.titulo_pagina("Customer Insights", "O que os clientes dizem quando avaliam mal e quando avaliam bem?")

n = st.slider("Quantidade de palavras", 5, 20, 10)
c1, c2, c3 = st.columns([1.2, 1.2, 0.8])
with c1:
    m = pg.nlargest(n, "dif_pp")
    fig = px.bar(m, x="dif_pp", y="palavra", orientation="h", color_discrete_sequence=[RED],
                 text=m["dif_pp"].map(lambda v: "+" + br(v, 1)), title="Palavras mais citadas em produtos mal avaliados")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Diferença (pontos percentuais)")
    st.plotly_chart(utils.estilo_fig(fig, 460, False), width="stretch")
with c2:
    b = pg.assign(dif_bem=-pg["dif_pp"]).nlargest(n, "dif_bem")
    fig = px.bar(b, x="dif_bem", y="palavra", orientation="h", color_discrete_sequence=[BLUE],
                 text=b["dif_bem"].map(lambda v: "+" + br(v, 1)), title="Palavras mais citadas em produtos bem avaliados")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Diferença (pontos percentuais)")
    st.plotly_chart(utils.estilo_fig(fig, 460, False), width="stretch")
with c3:
    with st.container(border=True):
        st.markdown("Quem avalia mal fala de **bateria**, **ruído** e **graves** (noise +9,5, battery +9,2, bass +8,6).\n\n"
                    "Os clientes que avaliam bem falam de **qualidade**, **facilidade** e **recomendação**.")

c1, c2 = st.columns([0.8, 2])
with c1:
    with st.container(border=True):
        st.markdown("Os temas **Instalação** e **Entrega** aparecem mais entre os bem avaliados.\n\n"
                    "Já o tema **Bateria**, mais entre os mal avaliados.")
    categorias = sorted(pc["categoria"].unique())
    cat = st.selectbox("Categoria do gráfico", categorias, index=categorias.index("Electronics"))
with c2:
    x = pc[pc["categoria"] == cat].copy()
    if sel_palavras:
        x = x[x["palavra"].isin(sel_palavras)]
    if x.empty:
        st.info("Nenhuma das palavras escolhidas aparece nesta categoria.")
        st.stop()
    x = x.reindex(x["dif_pp"].abs().sort_values(ascending=False).index).head(n).sort_values("dif_pp", ascending=False)
    x["lado"] = x["dif_pp"].map(lambda v: "Mal avaliados" if v > 0 else "Bem avaliados")
    fig = px.bar(x, x="dif_pp", y="palavra", orientation="h", color="lado",
                 color_discrete_map={"Mal avaliados": RED, "Bem avaliados": BLUE},
                 title=f"Palavras que mais diferenciam em {cat}")
    fig.update_xaxes(title="Diferença (pontos percentuais)")
    fig.update_yaxes(title="", categoryorder="array", categoryarray=list(x["palavra"]), autorange="reversed")
    st.plotly_chart(utils.estilo_fig(fig, 460), width="stretch")

st.caption("Palavras das avaliações (amostra por produto).")
utils.rodape()
