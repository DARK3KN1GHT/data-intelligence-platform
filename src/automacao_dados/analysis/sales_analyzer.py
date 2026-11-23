import pandas as pd


def analyze_sales(df: pd.DataFrame) -> dict:
    """
    Analisa os dados de vendas e retorna indicadores empresariais.

    Recebe um DataFrame processado e calcula:
    - Faturamento total
    - Quantidade total vendida
    - Ticket médio por unidade
    - Produto com maior faturamento
    - Produto mais vendido
    - Faturamento por categoria
    - Estatísticas gerais
    """

    colunas_obrigatorias = {
        "produto",
        "categoria",
        "quantidade",
        "preco_unitario",
        "valor_total",
    }

    colunas_ausentes = colunas_obrigatorias - set(df.columns)

    if colunas_ausentes:
        raise ValueError(
            f"Colunas necessárias para análise ausentes: {sorted(colunas_ausentes)}"
        )

    if df.empty:
        raise ValueError("Não existem dados para analisar.")

    faturamento_total = round(df["valor_total"].sum(), 2)

    quantidade_total = df["quantidade"].sum()

    total_produtos = len(df)

    ticket_medio = (
        round(faturamento_total / quantidade_total, 2) if quantidade_total > 0 else 0
    )

    faturamento_por_produto = (
        df.groupby("produto")["valor_total"].sum().sort_values(ascending=False)
    )

    quantidade_por_produto = (
        df.groupby("produto")["quantidade"].sum().sort_values(ascending=False)
    )

    faturamento_por_categoria = (
        df.groupby("categoria")["valor_total"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_dict()
    )

    return {
        "faturamento_total": faturamento_total,
        "quantidade_total_vendida": quantidade_total,
        "total_registros": total_produtos,
        "ticket_medio_por_unidade": ticket_medio,
        "produto_maior_faturamento": {
            "nome": faturamento_por_produto.index[0],
            "valor": round(faturamento_por_produto.iloc[0], 2),
        },
        "produto_mais_vendido": {
            "nome": quantidade_por_produto.index[0],
            "quantidade": quantidade_por_produto.iloc[0],
        },
        "faturamento_por_categoria": faturamento_por_categoria,
    }
