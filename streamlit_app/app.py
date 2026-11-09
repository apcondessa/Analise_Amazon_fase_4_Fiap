"""Ponto de entrada. Rode com:  streamlit run streamlit_app/app.py"""
import streamlit as st

import utils

st.set_page_config(page_title="Amazon: Product Performance & Customer Insights", page_icon="📊", layout="wide")
utils.aplicar_estilo()  # fundo em degradê cinza, como no Power BI

# mesmas páginas e mesma ordem do Power BI; cada página desenha os próprios filtros.
# A pasta se chama "telas" (e não "pages") para o Streamlit não montar uma segunda navegação sozinho.
paginas = st.navigation([
    st.Page("telas/inicio.py", title="Início", icon="🏠", default=True),
    st.Page("telas/executiva.py", title="Visão Executiva", icon="📈"),
    st.Page("telas/engajamento.py", title="Engajamento × Satisfação", icon="🎯"),
    st.Page("telas/notas.py", title="Avaliações X Notas", icon="⭐"),
    st.Page("telas/produtos.py", title="Avaliações X Produtos", icon="🛒"),
    st.Page("telas/notas_baixas.py", title="Prod. Notas < 4", icon="⚠️"),
    st.Page("telas/notas_altas.py", title="Prod. Notas ≥ 4,3", icon="🏆"),
    st.Page("telas/precos.py", title="Preços e Estratégia Comercial", icon="💰"),
    st.Page("telas/clientes.py", title="Customer Insights", icon="💬"),
    st.Page("telas/temas.py", title="Avaliação X Temas", icon="🏷️"),
    st.Page("telas/recomendacoes.py", title="Oportunidades & Recomendações", icon="✅"),
])

paginas.run()
