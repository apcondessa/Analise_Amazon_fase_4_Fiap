import math

import plotly.express as px
import streamlit as st

import utils
from utils import BLUE, QUAD_COLORS, RED, RISCO, br

df = utils.filtros_pagina("engajamento", "categoria", "preco")
utils.titulo_pagina("Engajamento × Satisfação", "A reputação do portfólio depende de poucos produtos?")
utils.exige_dados(df)

k = st.columns(4)
k[0].metric("Produtos que somam 80% das avaliações", br(utils.pct_produtos_80(df) * 100, 1, sufixo="%"))
k[1].metric("Avaliações nos produtos Estrela", br(utils.pct_avaliacoes_quadrante(df, "Estrela") * 100, 1, sufixo="%"))
k[2].metric("Avaliações em produtos de risco", utils.milhoes(utils.avaliacoes_unicas(df[df["quadrante"] == RISCO])))
k[3].metric("Avaliações nas Joias escondidas", br(utils.pct_avaliacoes_quadrante(df, "Joia escondida") * 100, 1, sufixo="%"))

c1, c2 = st.columns([1.5, 1])
with c1:
    d = df[df["quadrante"].isin(QUAD_COLORS)]
    fig = px.scatter(d, x="rating_count", y="rating", color="quadrante", log_x=True, opacity=0.5,
                     color_discrete_map=QUAD_COLORS, category_orders={"quadrante": list(QUAD_COLORS)},
                     hover_name="product_name", title="Avaliações × nota (um ponto por produto)",
                     labels={"rating_count": "Avaliações", "rating": "Nota", "quadrante": "Quadrante"})
    fig.update_xaxes(title="Nº de avaliações (escala logarítmica)")
    fig.update_yaxes(title="Nota", range=[2, 5])
    # no eixo log, a linha usa o valor real e o texto usa o log10 do valor
    for x, nome in [(1100, "P25 ≈ 1,1 mil"), (16000, "P75 ≈ 16 mil")]:
        fig.add_shape(type="line", x0=x, x1=x, yref="paper", y0=0, y1=1,
                      line=dict(color="#555555", dash="dash", width=2))
        fig.add_annotation(x=math.log10(x), yref="paper", y=1, text=nome, showarrow=False,
                           xanchor="left", yanchor="top", font=dict(color="#555555"))
    for y, nome, cor in [(4.0, "Nota 4,0", RED), (4.3, "Nota 4,3", QUAD_COLORS["Estrela"])]:
        fig.add_hline(y=y, line_dash="dash", line_color=cor, line_width=2,
                      annotation_text=nome, annotation_position="bottom left")
    st.plotly_chart(utils.estilo_fig(fig, 500), width="stretch")
    st.caption("Linhas tracejadas: cortes P25/P75 de avaliações e notas 4,0 / 4,3 que definem os quadrantes.")

with c2:
    g = df.dropna(subset=["rating"]).groupby("cat_grupo")
    t = g.apply(utils.pct_nota_menor_4, include_groups=False).mul(100).sort_values(ascending=False).reset_index(name="pct")
    fig = px.bar(t, x="pct", y="cat_grupo", orientation="h", color_discrete_sequence=[RED],
                 text=t["pct"].map(lambda v: br(v, 1, sufixo="%")), title="% de produtos com nota < 4 por categoria")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="")
    fig.update_traces(textposition="auto")
    st.plotly_chart(utils.estilo_fig(fig, 245, False), width="stretch")

    t = g.apply(utils.rating_ponderado, include_groups=False).sort_values(ascending=False).reset_index(name="nota")
    fig = px.bar(t, x="nota", y="cat_grupo", orientation="h", color_discrete_sequence=[BLUE],
                 text=t["nota"].map(lambda v: br(v, 2)), title="Rating ponderado por categoria")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Eixo começa em 3,8", range=[3.8, max(4.4, t["nota"].max() + 0.05)])
    fig.update_traces(textposition="auto")
    st.plotly_chart(utils.estilo_fig(fig, 245, False), width="stretch")

with st.container(border=True):
    st.markdown(
        "- **Concentração:** 23% dos produtos somam 80% das avaliações. A reputação do portfólio depende de poucos itens.\n"
        "- **Estrelas × Joias:** as 112 Estrelas (8% dos produtos) concentram 25% das avaliações; as 81 Joias escondidas "
        "têm nota ≥ 4,3, mas quase nenhuma visibilidade (0,2%).\n"
        "- **Categorias:** Home & Kitchen tem a maior fatia de produtos com nota < 4 (32%), acima de Electronics (26%) "
        "e Computers & Accessories (17%).")
st.caption("Leitura do portfólio completo (sem filtros).")
utils.rodape()
