import pandas as pd

from automacao_dados.processing.data_processor import process_dataframe


def test_processamento_de_dados():
    dados = pd.DataFrame(
        [
            {
                "id": 1,
                "produto": " notebook ",
                "categoria": " ELETRONICOS ",
                "quantidade": 2,
                "preco_unitario": 3500,
            }
        ]
    )

    resultado = process_dataframe(dados)

    assert resultado.loc[0, "produto"] == "Notebook"
    assert resultado.loc[0, "categoria"] == "Eletronicos"
    assert resultado.loc[0, "valor_total"] == 7000


def test_original_nao_e_modificado():
    dados = pd.DataFrame(
        [
            {
                "id": 1,
                "produto": " notebook ",
                "categoria": " ELETRONICOS ",
                "quantidade": 2,
                "preco_unitario": 3500,
            }
        ]
    )

    original = dados.copy()

    process_dataframe(dados)

    pd.testing.assert_frame_equal(dados, original)
