"""Funções compartilhadas: leitura dos dados, filtros, cálculos e estilo.

Os cálculos em Python reproduzem as medidas DAX de powerbi/medidas.dax
(a correspondência está indicada em cada função).
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------------ cores
NAVY, BLUE, RED, GREEN, AMBER, GRAY = "#14213D", "#3B6FB6", "#D64545", "#3FA34D", "#E8A33D", "#9AA0A6"
RISCO = "Alto engajamento, baixa nota"  # mesmo rótulo da coluna quadrante2 do Power BI
QUAD_COLORS = {RISCO: RED, "Estrela": GREEN, "Joia escondida": AMBER, "Demais": GRAY}
QUAD_DESTAQUE = [RISCO, "Estrela", "Joia escondida"]  # filtro dos gráficos de quadrante do Power BI

TOP3_CATS = ["Electronics", "Computers&Accessories", "Home&Kitchen"]

# ------------------------------------------------------------------ dados
_RAIZ = Path(__file__).resolve().parents[1]
_CANDIDATAS = [
    _RAIZ / "data" / "tratados",
    _RAIZ / "data" / "tratado",
    Path(__file__).resolve().parent / "data" / "tratados",
    Path(__file__).resolve().parent / "data",
]


def pasta_dados() -> Path:
    for p in _CANDIDATAS:
        if (p / "amazon_tratado.csv").exists():
            return p
    st.error("Não encontrei `amazon_tratado.csv`. Coloque os CSV tratados em `data/tratados/` na raiz do repositório.")
    st.stop()


TEMAS = [
    "Qualidade/Durabilidade", "Preço/Custo-benefício", "Bateria/Carga", "Som/Áudio",
    "Defeito/Falha", "Entrega/Embalagem", "Instalação/Uso", "Desempenho",
]
COLUNAS = [
    "product_id", "product_name", "product_link", "discounted_price_inr", "actual_price_inr",
    "discount_pct", "discount_value_inr", "rating", "rating_count", "cat_principal", "cat_sub",
    "faixa_desconto", "faixa_preco",
] + [f"tema_{t}" for t in TEMAS]


def _limpa_faixa(s: pd.Series) -> pd.Series:
    """'2. 20-40%' -> '20-40%' (o prefixo numérico serve só para ordenar no Power BI)."""
    return s.astype(str).str.replace(r"^\d+\.\s*", "", regex=True)


def _ordenada(s: pd.Series) -> pd.Series:
    """Texto sem prefixo, mas com a ordem original (1., 2., 3. ...)."""
    ordem = [_limpa_faixa(pd.Series([x]))[0] for x in sorted(s.dropna().unique())]
    return pd.Categorical(_limpa_faixa(s), categories=ordem, ordered=True)


@st.cache_data(show_spinner="Carregando dados...")
def carregar_produtos() -> pd.DataFrame:
    # utf-8-sig: os CSV do Colab/Power BI começam com BOM
    df = pd.read_csv(pasta_dados() / "amazon_tratado.csv", encoding="utf-8-sig", usecols=COLUNAS)

    # --- colunas calculadas do modelo (powerbi/medidas.dax, parte 2)
    df["cat_grupo"] = np.where(df["cat_principal"].isin(TOP3_CATS), df["cat_principal"], "Outras")
    df["cat_sub_lbl"] = df["cat_sub"].astype(str).str.replace(r"(?<=[a-z])(?=[A-Z])", " ", regex=True)
    nome = df["product_name"].astype(str)
    df["nome_curto"] = np.where(nome.str.len() > 45, nome.str.slice(0, 45) + "...", nome)
    df["faixa_desconto"] = _ordenada(df["faixa_desconto"])
    df["faixa_preco"] = _ordenada(df["faixa_preco"])

    # Flag Listagem: 1 linha por combinação (rating, rating_count); variantes (cores) não contam duas vezes
    menor_id = df.groupby(["rating", "rating_count"], dropna=False)["product_id"].transform("min")
    df["flag_listagem"] = (df["product_id"] == menor_id).astype(int)

    # quadrante2: quartis de avaliações calculados sobre todos os produtos
    p75, p25 = df["rating_count"].quantile(0.75), df["rating_count"].quantile(0.25)
    r, n = df["rating"], df["rating_count"]
    quad = np.select(
        [r.isna() | n.isna(), (n >= p75) & (r < 4), (n >= p75) & (r >= 4.3), (n <= p25) & (r >= 4.3)],
        ["Sem dados", RISCO, "Estrela", "Joia escondida"], default="Demais")
    df["quadrante"] = quad

    # Grupo de Nota
    df["grupo_nota"] = np.select(
        [r.isna(), r >= 4.3, r < 4.0], ["Sem nota", "Bem avaliados (≥ 4,3)", "Mal avaliados (< 4,0)"],
        default="Intermediários")
    return df


@st.cache_data(show_spinner=False)
def carregar_palavras():
    p = pasta_dados()
    pg = pd.read_csv(p / "palavras_grupos.csv", encoding="utf-8-sig")
    pg["dif_pp"] = (pg["%_mal_avaliados"] - pg["%_bem_avaliados"]) * 100
    pc = pd.read_csv(p / "palavras_por_categoria.csv", encoding="utf-8-sig")
    pc["dif_pp"] = (pc["pct_mal"] - pc["pct_bem"]) * 100
    return pg, pc


# ------------------------------------------------------------------ cálculos (equivalem às medidas DAX)
def listagens_unicas(df: pd.DataFrame) -> pd.DataFrame:
    """Linhas com Flag Listagem = 1."""
    return df[df["flag_listagem"] == 1]


def avaliacoes_unicas(df: pd.DataFrame) -> float:
    """[Total Avaliações]: SUMMARIZE por (rating, rating_count) dentro da seleção atual."""
    return float(df.drop_duplicates(["rating", "rating_count"])["rating_count"].sum())


def rating_ponderado(df: pd.DataFrame) -> float:
    """[Rating Ponderado]: média das notas ponderada por rating_count."""
    d = df.dropna(subset=["rating", "rating_count"])
    return float(np.average(d["rating"], weights=d["rating_count"])) if len(d) and d["rating_count"].sum() else np.nan


def pct_nota_menor_4(df: pd.DataFrame) -> float:
    """[% Produtos Nota < 4]: produtos distintos com nota < 4 / produtos distintos com nota."""
    d = df.dropna(subset=["rating"])
    n = d["product_id"].nunique()
    return d.loc[d["rating"] < 4, "product_id"].nunique() / n if n else np.nan


def pct_avaliacoes_quadrante(df: pd.DataFrame, quadrante: str) -> float:
    """[% Avaliações nas Estrelas] / [% Avaliações nas Joias]: parcela das avaliações da seleção."""
    total = avaliacoes_unicas(df)
    return avaliacoes_unicas(df[df["quadrante"] == quadrante]) / total if total else np.nan


def pct_produtos_80(df: pd.DataFrame) -> float:
    """[% Produtos p/ 80% das Avaliações]: menor fatia de produtos (os mais avaliados) que soma 80%."""
    av = df["rating_count"].dropna().sort_values(ascending=False)
    if av.empty:
        return np.nan
    # produtos empatados entram juntos, como no SUMX com [@av] >= a
    acumulado = av.cumsum().groupby(av, sort=False).transform("max")
    return float((acumulado <= 0.8 * av.sum()).sum() / len(av))


def correlacao(df: pd.DataFrame) -> float:
    """[Correlação Desconto x Rating] (Pearson)."""
    d = df.dropna(subset=["rating", "discount_pct"])
    return float(d["discount_pct"].corr(d["rating"])) if len(d) > 2 else np.nan


def avaliacoes_por_faixa(df: pd.DataFrame, cats=None) -> dict:
    """[Avaliações_Baixa/Média/Alta]: avaliações únicas por faixa de nota, opcionalmente só em `cats`."""
    d = listagens_unicas(df).dropna(subset=["rating", "rating_count"])
    if cats is not None:
        d = d[d["cat_principal"].isin(cats)]
    return {
        "Baixa (< 4,0)": float(d.loc[d["rating"] < 4, "rating_count"].sum()),
        "Média (4,0 a < 4,3)": float(d.loc[(d["rating"] >= 4) & (d["rating"] < 4.3), "rating_count"].sum()),
        "Alta (≥ 4,3)": float(d.loc[d["rating"] >= 4.3, "rating_count"].sum()),
    }


def top20_preco_real(df: pd.DataFrame, alta: bool = False) -> pd.DataFrame:
    """Tabelas Top20_Preco_Real_Baixa (nota < 4) e Top20_Preco_Real_Alta (nota >= 4,3): 1 linha por listagem,
    20 maiores preços reais (empate: menor product_id), com a coluna `posicao`."""
    nota = (df["rating"] >= 4.3) if alta else (df["rating"] < 4)
    base = df[nota & (df["flag_listagem"] == 1) & df["rating_count"].notna()]
    top = base.sort_values(["actual_price_inr", "product_id"], ascending=[False, True]).head(20).copy()
    top["posicao"] = range(1, len(top) + 1)
    return top


def ranking_categorias(df: pd.DataFrame) -> pd.Series:
    """Avaliações únicas por categoria, em ordem decrescente (base do RANKX da tabela Linhas)."""
    return pd.Series({c: avaliacoes_unicas(g) for c, g in df.groupby("cat_principal")}).sort_values(ascending=False)


# ------------------------------------------------------------------ formatação pt-BR
def br(x, casas=0, prefixo="", sufixo="") -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    s = f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{prefixo}{s}{sufixo}"


def rs(x, casas=0) -> str:
    return br(x, casas, prefixo="₹")


def milhoes(x) -> str:
    return br(x / 1e6, 1, sufixo=" mi")


# ------------------------------------------------------------------ filtros de cada página
_CAMPOS = {
    "categoria": ("cat_principal", "Categoria"),
    "preco": ("faixa_preco", "Faixa de preço"),
    "desconto": ("faixa_desconto", "Faixa de desconto"),
    "produto": ("nome_curto", "Produtos"),
}


def base() -> pd.DataFrame:
    """Todos os produtos. Lê do cache, então funciona mesmo abrindo direto o link de uma página."""
    return carregar_produtos()


def _guarda(chave: str):
    st.session_state[f"_{chave}"] = st.session_state[chave]


def filtro(rotulo: str, opcoes: list, chave: str) -> list:
    """Multiselect na barra lateral que mantém a seleção ao trocar de página, como um slicer."""
    if f"_{chave}" in st.session_state:
        st.session_state[chave] = st.session_state[f"_{chave}"]
    return st.sidebar.multiselect(rotulo, opcoes, key=chave, placeholder="Todas", on_change=_guarda, args=(chave,))


def filtros_pagina(pagina: str, *campos: str, categoria_compartilhada: bool = False) -> pd.DataFrame:
    """Mostra na barra lateral só os slicers que a página tem no Power BI e devolve os dados filtrados.
    categoria_compartilhada: slicer de categoria sincronizado entre páginas (syncGroup cat_principal)."""
    df = base()
    f = df
    st.sidebar.markdown("### Filtros desta página")
    for campo in campos:
        coluna, rotulo = _CAMPOS[campo]
        s = df[coluna]
        opcoes = list(s.cat.categories) if hasattr(s, "cat") else sorted(s.unique())
        compartilhada = campo == "categoria" and categoria_compartilhada
        sel = filtro(rotulo, opcoes, "filtro_categoria" if compartilhada else f"filtro_{pagina}_{campo}")
        if sel:
            f = f[f[coluna].isin(sel)]
    st.sidebar.caption(f"{br(len(f))} de {br(len(df))} produtos selecionados")
    return f


def exige_dados(df: pd.DataFrame):
    if df.empty:
        st.warning("Nenhum produto para esta combinação de filtros. Ajuste os filtros na barra lateral.")
        st.stop()


# ------------------------------------------------------------------ estilo
def estilo_fig(fig: go.Figure, altura=380, legenda=True) -> go.Figure:
    fig.update_layout(
        height=altura, template="plotly_white", margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.35)", font_color="#1f2228",
        font=dict(family="Segoe UI, system-ui, sans-serif", size=13), showlegend=legenda,
        legend=dict(orientation="h", y=-0.2, title_text=""), separators=",.",
    )
    # textos dos eixos mais escuros para o fundo cinza
    escuro = "#2b2e33"
    fig.update_xaxes(tickfont_color=escuro, title_font_color=escuro, gridcolor="rgba(255,255,255,0.7)")
    fig.update_yaxes(tickfont_color=escuro, title_font_color=escuro, gridcolor="rgba(255,255,255,0.7)")
    fig.update_layout(legend_font_color=escuro, coloraxis_colorbar_tickfont_color=escuro)
    return fig


_CSS = """
<style>
/* fundo em degradê cinza, nos mesmos tons da página inicial do Power BI */
[data-testid="stApp"] {
    background: linear-gradient(135deg, #cfd0d3 0%, #bcbec1 45%, #a4a7ab 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #b3b5b8 0%, #96989b 100%); }
/* cartões e caixas: cinza translúcido com borda clara, como os cartões do dashboard */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {
    background: rgba(255, 255, 255, 0.22);
    border-color: rgba(255, 255, 255, 0.55) !important;
}
/* textos de apoio mais escuros, para manter o contraste no fundo cinza */
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: #33363c !important; }
[data-testid="stMetricLabel"] p { color: #2b2e33; }
[data-testid="stSidebarNavLink"] span { color: #1f2228; }
</style>
"""


def aplicar_estilo():
    st.markdown(_CSS, unsafe_allow_html=True)


def titulo_pagina(titulo: str, pergunta: str):
    st.title(titulo)
    st.caption(pergunta)


def rodape():
    st.divider()
    st.caption("Fonte: Amazon Sales Dataset (Kaggle) · preços em rupias (₹) · "
               "avaliações contadas uma vez por listagem · os resultados mostram associações, não causas.")
