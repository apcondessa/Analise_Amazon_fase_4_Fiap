// =============================================================================
// Consultas do Power Query (M) do dashboard "Amazon Product Performance & Customer Insights"
// Origem: powerbi/Tech_Challenge_Amazon_Fiap_Fase_4.pbix
//
// Todas as consultas leem os CSV do repositório público apcondessa/Amazon_dataset
// pelo parâmetro "Pasta" (Transformar dados > Gerenciar parâmetros):
//   "https://raw.githubusercontent.com/apcondessa/Amazon_dataset/main/" meta [IsParameterQuery = true, IsParameterQueryRequired = false, Type = type text]
// Credencial: Anônimo. Para ler CSV locais, use o caminho da pasta data/tratados/
// (terminado em barra) e troque Web.Contents por File.Contents.
// A cultura "en-US" nas conversões é obrigatória: em pt-BR o ponto decimal vira separador de milhar.
// =============================================================================

// ----- Consulta: palavras_grupos -----
let
    Fonte = Csv.Document(Web.Contents(Pasta & "palavras_grupos.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos,
        {{"palavra", type text}, {"%_bem_avaliados", type number},
         {"%_mal_avaliados", type number}, {"razao_mal_vs_bem", type number}}, "en-US"),
    SemVazios = Table.SelectRows(Tipos, each [palavra] <> null and [palavra] <> "")
in
    SemVazios

// ----- Consulta: palavras_por_categoria -----
let
    Fonte = Csv.Document(Web.Contents(Pasta & "palavras_por_categoria.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos,
        {{"categoria", type text}, {"palavra", type text}, {"pct_bem", type number},
         {"pct_mal", type number}, {"razao", type number}}, "en-US"),
    SemVazios = Table.SelectRows(Tipos, each [palavra] <> null and [palavra] <> "")
in
    SemVazios

// ----- Consulta: temas_grupos -----
let
    Fonte = Csv.Document(Web.Contents(Pasta & "temas_grupos.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos,
        {{"tema", type text}, {"alta", type number}, {"baixa", type number}, {"media", type number}}, "en-US")
in
    Tipos

// ----- Consulta: produtos_tratados -----
let
    Fonte = Csv.Document(
        Web.Contents(Pasta & "amazon_tratado.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),

    Tipos = Table.TransformColumnTypes(Cabecalho, {
        {"product_id", type text}, {"product_name", type text}, {"category", type text},
        {"discounted_price", type text}, {"actual_price", type text}, {"discount_percentage", type text},
        {"about_product", type text}, {"review_title", type text}, {"review_content", type text},
        {"product_link", type text}, {"txt", type text},
        {"cat_principal", type text}, {"cat_sub", type text}, {"cat_folha", type text},
        {"faixa_desconto", type text}, {"faixa_preco", type text}, {"faixa_avaliacao", type text},
        {"quadrante", type text}, {"grupo_nota", type text},
        {"rating", type number}, {"rating_count", Int64.Type},
        {"discounted_price_inr", type number}, {"actual_price_inr", type number},
        {"discount_pct", type number}, {"discount_value_inr", type number},
        {"tema_Qualidade/Durabilidade", type logical}, {"tema_Preço/Custo-benefício", type logical},
        {"tema_Bateria/Carga", type logical}, {"tema_Som/Áudio", type logical},
        {"tema_Defeito/Falha", type logical}, {"tema_Entrega/Embalagem", type logical},
        {"tema_Instalação/Uso", type logical}, {"tema_Desempenho", type logical}
    }, "en-US"),

    Ordenado = Table.Sort(Tipos, {{"rating_count", Order.Descending}, {"discounted_price_inr", Order.Descending}}),
    Buffer = Table.Buffer(Ordenado)
in
    Buffer
