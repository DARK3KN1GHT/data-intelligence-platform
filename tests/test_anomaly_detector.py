import pandas as pd

from automacao_dados.analysis.anomaly_detector import detect_anomalies


def test_identifica_valor_atipico():
    dados = pd.DataFrame(
        {
            "produto": [
                "Produto A",
                "Produto B",
                "Produto C",
                "Produto D",
                "Produto E",
                "Produto F",
            ],
            "quantidade": [10, 11, 9, 10, 12, 100],
            "preco_unitario": [20, 21, 19, 20, 22, 20],
            "valor_total": [200, 231, 171, 200, 264, 2000],
        }
    )

    resultado = detect_anomalies(dados)

    assert any(
        item["campo"] == "quantidade" and item["produto"] == "Produto F"
        for item in resultado
    )

    assert any(
        item["campo"] == "valor_total" and item["produto"] == "Produto F"
        for item in resultado
    )


def test_dados_sem_anomalias():
    dados = pd.DataFrame(
        {
            "quantidade": [10, 11, 9, 10, 12, 10],
            "preco_unitario": [20, 21, 19, 20, 22, 20],
            "valor_total": [200, 231, 171, 200, 264, 200],
        }
    )

    resultado = detect_anomalies(dados)

    assert resultado == []


def test_dataframe_vazio():
    dados = pd.DataFrame()

    resultado = detect_anomalies(dados)

    assert resultado == []


def test_coluna_com_poucos_registros():
    dados = pd.DataFrame(
        {
            "quantidade": [10, 100, 20],
        }
    )

    resultado = detect_anomalies(dados)

    assert resultado == []
