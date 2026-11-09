import plotly.express as px
import streamlit as st

import utils
from utils import QUAD_COLORS, QUAD_DESTAQUE, RISCO, br

df = utils.base()  # sem filtros, como no Power BI
utils.titulo_pagina("Oportunidades & Recomendações", "O que fazer com o que o painel mostra?")

q = df["quadrante"].value_counts()
k = st.columns(3)
k[0].metric("Produtos em risco", br(q.get(RISCO, 0)), help="Alto engajamento e nota < 4,0")
k[1].metric("Estrelas", br(q.get("Estrela", 0)), help="Alto engajamento e nota ≥ 4,3")
k[2].metric("Joias escondidas", br(q.get("Joia escondida", 0)), help="Baixo engajamento e nota ≥ 4,3")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Respostas às perguntas do desafio")
    with st.container(border=True):
        st.markdown(
            "- **Relevância:** Electronics (Eletrônicos), Computers & Accessories (Computadores e Acessórios) e "
            "Home & Kitchen (Casa e Cozinha) somam 98,6% das avaliações.\n"
            "- **Engajamento:** o cabo HDMI Amazon Basics lidera, com 427 mil avaliações.\n"
            "- **Desconto e nota:** correlação fraca e negativa (−0,16).\n"
            "- **Alto engajamento, nota baixa:** 49 produtos. Dos 20 mais caros com nota < 4,0, 14 são de Electronics (Eletrônicos).\n"
            "- **Pouca visibilidade, boa nota:** 81 joias escondidas.\n"
            "- **Voz do cliente:** elogiam qualidade, facilidade e recomendação. Criticam bateria, ruído e graves.\n"
            "- **Risco e oportunidade:** reputação em fones, eletroportáteis e eletrônicos caros. "
            "Dar visibilidade às joias escondidas e testar descontos com controle.")
with c2:
    qq = df[df["quadrante"].isin(QUAD_DESTAQUE)]["quadrante"].value_counts(ascending=True).reset_index()
    qq.columns = ["quadrante", "produtos"]
    fig = px.bar(qq, x="produtos", y="quadrante", orientation="h", color="quadrante", color_discrete_map=QUAD_COLORS,
                 text="produtos", title="Produtos por quadrante")
    fig.update_yaxes(title="")
    st.plotly_chart(utils.estilo_fig(fig, 340, False), width="stretch")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Mensagens finais para a liderança")
    with st.container(border=True):
        st.markdown(
            "1. **Risco concentrado:** a nota média de 4,16 esconde 49 produtos de alto engajamento (nota < 4,0). "
            "30 são de Electronics (Eletrônicos).\n"
            "2. **Desconto não eleva a satisfação:** testar com grupo de controle.\n"
            "3. **Os clientes apontam o que corrigir:** bateria, ruído e graves nos fones; "
            "aquecimento, potência e recebimento nos eletroportáteis.\n"
            "4. **Ganho de baixo custo:** dar visibilidade aos 81 produtos bem avaliados e com baixo engajamento.\n"
            "5. **Monitoramento:** acompanhar todo mês os 112 produtos Estrela.")
with c2:
    # Top 10 por número de avaliações, 1 linha por listagem (variantes/cores não repetem)
    risco = utils.listagens_unicas(df[df["quadrante"] == RISCO]).nlargest(10, "rating_count")
    st.markdown("**Top 10 produtos em risco** (alto engajamento, nota < 4)")
    st.dataframe(
        risco[["nome_curto", "rating", "rating_count", "discount_pct"]].rename(columns={
            "nome_curto": "Produto", "rating": "Nota", "rating_count": "Avaliações", "discount_pct": "Desconto"}),
        hide_index=True, width="stretch",
        column_config={"Desconto": st.column_config.NumberColumn(format="percent")})

st.subheader("Plano de ação")
with st.container(border=True):
    st.markdown("**Reputação: proteger quem já vende.** Revisar o portfólio de fones. "
                "Quem: gerência de Eletrônicos e Qualidade. O quê: auditar os fones de ouvido (nota média 3,9) antes de novos descontos. "
                "Por quê: maior volume de avaliações com nota abaixo da média; 30 dos 49 produtos em risco estão em Eletrônicos.")
with st.container(border=True):
    st.markdown("**Estratégia de desconto: testar antes de mudar.** Quem: Precificação. "
                "O quê: testar descontos entre 20% e 60% com grupo de controle. "
                "Por quê: a nota cai de 4,17 para 3,97, mas a correlação é fraca (−0,16): é associação, não causa. "
                "Acompanhamento: Analytics acompanha todo mês a % de produtos com nota < 4.")
with st.container(border=True):
    st.markdown("**Visibilidade: dar espaço a quem merece.** Joias escondidas: Marketing e anúncios fazem banners, recomendações cruzadas "
                "e anúncios patrocinados, começando por 20 itens (81 produtos com nota ≥ 4,3 e poucas avaliações). "
                "Estrelas: gerência de categorias e Qualidade monitoram a nota para não perder a posição.")
st.caption("Os textos desta página usam os números do dashboard completo (sem filtros).")
utils.rodape()
