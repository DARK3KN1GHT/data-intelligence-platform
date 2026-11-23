import pandas as pd

COLUNAS_OBRIGATORIAS = [
    "id",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
]


def validate_dataframe(df: pd.DataFrame) -> dict:
    """
    Verifica a qualidade de um DataFrame sem modificar os dados originais.
    """

    erros = []
    avisos = []

    # 1. Verificar se todas as colunas obrigatórias existem
    colunas_ausentes = [
        coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in df.columns
    ]

    if colunas_ausentes:
        erros.append(
            {
                "tipo": "colunas_ausentes",
                "mensagem": f"Colunas obrigatórias ausentes: {colunas_ausentes}",
            }
        )

    # 2. Verificar valores ausentes
    for coluna in df.columns:
        valores_ausentes = df[coluna].isna().sum()

        if valores_ausentes > 0:
            erros.append(
                {
                    "tipo": "valores_ausentes",
                    "mensagem": (
                        f"A coluna '{coluna}' possui "
                        f"{valores_ausentes} valor(es) ausente(s)."
                    ),
                }
            )

    # 3. Verificar IDs duplicados
    if "id" in df.columns:
        ids_duplicados = df["id"].duplicated().sum()

        if ids_duplicados > 0:
            erros.append(
                {
                    "tipo": "ids_duplicados",
                    "mensagem": (
                        f"Foram encontrados {ids_duplicados} ID(s) duplicado(s)."
                    ),
                }
            )

    # 4. Verificar campos numéricos
    colunas_numericas = ["quantidade", "preco_unitario"]

    for coluna in colunas_numericas:
        if coluna not in df.columns:
            continue

        valores = pd.to_numeric(df[coluna], errors="coerce")

        valores_invalidos = valores.isna() & df[coluna].notna()

        if valores_invalidos.sum() > 0:
            erros.append(
                {
                    "tipo": "valores_nao_numericos",
                    "mensagem": (
                        f"A coluna '{coluna}' possui "
                        f"{valores_invalidos.sum()} valor(es) não numérico(s)."
                    ),
                }
            )

        valores_negativos = (valores < 0).sum()

        if valores_negativos > 0:
            erros.append(
                {
                    "tipo": "valores_negativos",
                    "mensagem": (
                        f"A coluna '{coluna}' possui "
                        f"{valores_negativos} valor(es) negativo(s)."
                    ),
                }
            )

    # 5. Resultado final
    return {
        "valido": len(erros) == 0,
        "total_registros": len(df),
        "total_erros": len(erros),
        "erros": erros,
        "avisos": avisos,
    }
