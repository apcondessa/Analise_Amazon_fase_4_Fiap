import pandas as pd
import plotly.express as px
import streamlit as st

import utils
from utils import AMBER, BLUE, GRAY, GREEN, RED, br

df = utils.filtros_pagina("notas", "categoria")
utils.titulo_pagina("Avaliações X Notas", "Onde se concentram as avaliações: em notas baixas, médias ou altas?")
utils.exige_dados(df)

base = utils.base()
total = utils.avaliacoes_unicas(base)  # % Avaliações da Categoria: sempre sobre o portfólio inteiro
rank = utils.ranking_categorias(df)

# Avaliações_Baixa/Média/Alta ignoram o filtro de categoria: o ranking é sempre do portfólio inteiro
rank_geral = utils.ranking_categorias(base)
top3 = list(rank_geral.index[:3])
linhas = {
    "Todos os produtos": list(rank_geral.index),
    "Top 3 categorias (juntas)": top3,
    "Top 1 categoria": top3[:1],
    "Top 2 categoria": top3[1:2],
    "Top 3 categoria": top3[2:3],
}
sel_linhas = utils.filtro("Agrupamento", list(linhas), "filtro_notas_linha")

c1, c2 = st.columns(2)
with c1:
    t = rank.head(3).reset_index()
    t.columns = ["categoria", "avaliacoes"]
    t["pct"] = t["avaliacoes"] / total * 100
    fig = px.bar(t, x="pct", y="categoria", orientation="h", text=t["pct"].map(lambda v: br(v, 1, sufixo="%")),
                 title="Top 3 categorias mais avaliadas (percentual)", color_discrete_sequence=[BLUE])
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="% do total de avaliações")
    st.plotly_chart(utils.estilo_fig(fig, 280, False), width="stretch")

    t = rank.tail(6).reset_index()
    t.columns = ["categoria", "avaliacoes"]
    t["pct"] = t["avaliacoes"] / total * 100
    fig = px.bar(t, x="pct", y="categoria", orientation="h", text=t["pct"].map(lambda v: br(v, 2, sufixo="%")),
                 title="Avaliações pelas demais categorias (percentual)", color_discrete_sequence=[AMBER])
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="% do total de avaliações")
    st.plotly_chart(utils.estilo_fig(fig, 300, False), width="stretch")

reg = [{"Linha": nome, **utils.avaliacoes_por_faixa(base, cats)}
       for nome, cats in linhas.items() if not sel_linhas or nome in sel_linhas]
tab = pd.DataFrame(reg)

with c2:
    m = tab.melt("Linha", var_name="Faixa de nota", value_name="Avaliações")
    m["Linha"] = m["Linha"].str.replace(" cat", "<br>cat").str.replace(" prod", "<br>prod")
    fig = px.bar(m, x="Linha", y="Avaliações", color="Faixa de nota", barmode="group", title="Quantidade de avaliações X rating (por agrupamentos)",
                 color_discrete_map={"Baixa (< 4,0)": RED, "Média (4,0 a < 4,3)": GRAY, "Alta (≥ 4,3)": GREEN})
    fig.update_xaxes(title="", tickangle=0)
    st.plotly_chart(utils.estilo_fig(fig, 380), width="stretch")

    st.markdown("**Tabela de avaliações por rating (por agrupamentos)**")
    show = tab.copy()
    for c in show.columns[1:]:
        show[c] = show[c].map(br)
    st.dataframe(show, hide_index=True, width="stretch")
    st.caption(f"Top 1 = {top3[0]}, Top 2 = {top3[1]}, Top 3 = {top3[2]} (ranking por avaliações). "
               "Como no Power BI, estes dois visuais não mudam com o filtro de categoria.")
utils.rodape()
