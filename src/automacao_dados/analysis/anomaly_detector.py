import pandas as pd

COLUNAS_ANALISADAS = [
    "quantidade",
    "preco_unitario",
    "valor_total",
]

MINIMO_REGISTROS = 6
FATOR_IQR = 2.0


def detect_anomalies(df: pd.DataFrame) -> list[dict]:
    """
    Identifica valores estatisticamente atípicos usando IQR.

    Utiliza limites mais conservadores para reduzir falsos positivos.

    As anomalias são alertas para investigação, não erros confirmados.
    """

    if df.empty:
        return []

    anomalias = []

    for coluna in COLUNAS_ANALISADAS:
        if coluna not in df.columns:
            continue

        valores = pd.to_numeric(df[coluna], errors="coerce").dropna()

        if len(valores) < MINIMO_REGISTROS:
            continue

        q1 = valores.quantile(0.25)
        q3 = valores.quantile(0.75)

        intervalo_interquartil = q3 - q1

        if intervalo_interquartil == 0:
            continue

        limite_inferior = q1 - FATOR_IQR * intervalo_interquartil

        limite_superior = q3 + FATOR_IQR * intervalo_interquartil

        indices_atipicos = valores[
            (valores < limite_inferior) | (valores > limite_superior)
        ].index

        for indice in indices_atipicos:
            registro = {
                "indice": (int(indice) if isinstance(indice, int) else str(indice)),
                "campo": coluna,
                "valor": float(valores.loc[indice]),
                "limite_inferior": round(float(limite_inferior), 2),
                "limite_superior": round(float(limite_superior), 2),
            }

            if "produto" in df.columns:
                registro["produto"] = str(df.loc[indice, "produto"])

            anomalias.append(registro)

    return anomalias
