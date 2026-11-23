import pandas as pd


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa, padroniza e transforma os dados recebidos.

    Retorna um novo DataFrame sem modificar o original.
    """

    dados = df.copy()

    # Remover espaços extras dos textos
    colunas_texto = dados.select_dtypes(include=["object", "string"]).columns

    for coluna in colunas_texto:
        dados[coluna] = dados[coluna].apply(
            lambda valor: valor.strip() if isinstance(valor, str) else valor
        )

    # Padronizar nomes de produtos e categorias
    if "produto" in dados.columns:
        dados["produto"] = dados["produto"].apply(
            lambda valor: valor.title() if isinstance(valor, str) else valor
        )

    if "categoria" in dados.columns:
        dados["categoria"] = dados["categoria"].apply(
            lambda valor: valor.title() if isinstance(valor, str) else valor
        )

    # Converter colunas numéricas
    if "quantidade" in dados.columns:
        dados["quantidade"] = pd.to_numeric(dados["quantidade"], errors="coerce")

    if "preco_unitario" in dados.columns:
        dados["preco_unitario"] = pd.to_numeric(
            dados["preco_unitario"], errors="coerce"
        ).round(2)

    # Calcular valor total
    if {"quantidade", "preco_unitario"}.issubset(dados.columns):
        dados["valor_total"] = (dados["quantidade"] * dados["preco_unitario"]).round(2)

    return dados
