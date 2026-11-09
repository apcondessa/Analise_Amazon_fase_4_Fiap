import pandas as pd
import plotly.express as px
import streamlit as st

import utils
from utils import BLUE, GREEN, RED, TEMAS, br

df = utils.base()
utils.titulo_pagina("Avaliação X Temas", "Quais temas aparecem mais entre bem e mal avaliados, e onde estão as avaliações desses temas?")

bem, mal = df[df["grupo_nota"] == "Bem avaliados (≥ 4,3)"], df[df["grupo_nota"] == "Mal avaliados (< 4,0)"]

linhas = []
for t in TEMAS:
    c = f"tema_{t}"
    linhas.append({"Tema": t, "Bem avaliados": bem[c].mean() * 100, "Mal avaliados": mal[c].mean() * 100})
tb = pd.DataFrame(linhas).sort_values("Bem avaliados", ascending=False)
tb["Diferença (pp)"] = tb["Bem avaliados"] - tb["Mal avaliados"]


def grafico_tema(tema: str, titulo: str, so_top3: bool = False):
    """Conta os produtos que citam o tema, por categoria, como no dashboard."""
    d = df[df[f"tema_{tema}"].fillna(False).astype(bool)]
    if so_top3:
        d = d[d["cat_grupo"] != "Outras"]
    d = d.groupby("cat_principal").size().sort_values(ascending=False)
    st.markdown(f"**{titulo}**")
    fig = px.bar(d.reset_index(name="produtos"), x="cat_principal", y="produtos", text="produtos",
                 color_discrete_sequence=[BLUE])
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Produtos", range=[0, d.max() * 1.15])
    fig.update_traces(textposition="outside")
    st.plotly_chart(utils.estilo_fig(fig, 340, False), width="stretch")


c1, c2 = st.columns(2)
with c1:
    grafico_tema("Qualidade/Durabilidade", "Número de produtos por categoria que mencionam o tema qualidade")
    grafico_tema("Preço/Custo-benefício", "Número de produtos por categoria que mencionam o tema preço/custo-benefício", so_top3=True)
with c2:
    m = tb.melt("Tema", ["Bem avaliados", "Mal avaliados"], var_name="Grupo", value_name="% dos produtos")
    fig = px.bar(m, x="% dos produtos", y="Tema", color="Grupo", barmode="group", orientation="h",
                 text=m["% dos produtos"].map(lambda v: br(v, 0, sufixo="%")),
                 color_discrete_map={"Bem avaliados": GREEN, "Mal avaliados": RED},
                 title="% de produtos que citam cada tema, por grupo de nota")
    fig.update_yaxes(title="", autorange="reversed")
    st.plotly_chart(utils.estilo_fig(fig, 620), width="stretch")
    mais = tb.sort_values("Diferença (pp)", ascending=False)
    st.caption(f"Mais frequentes entre os bem avaliados: {mais.iloc[0]['Tema']} ({br(mais.iloc[0]['Diferença (pp)'], 1, '+')} pp) e "
               f"{mais.iloc[1]['Tema']} ({br(mais.iloc[1]['Diferença (pp)'], 1, '+')} pp). "
               f"Mais frequente entre os mal avaliados: {mais.iloc[-1]['Tema']} ({br(-mais.iloc[-1]['Diferença (pp)'], 1)} pp a mais).")

show = tb.copy()
for c in show.columns[1:]:
    show[c] = show[c].map(lambda v: br(v, 1))
with st.expander("Ver tabela dos temas"):
    st.dataframe(show, hide_index=True, width="stretch")
utils.rodape()
