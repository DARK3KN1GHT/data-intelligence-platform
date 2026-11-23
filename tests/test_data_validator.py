import pandas as pd

from automacao_dados.validation.data_validator import validate_dataframe


def criar_dados_validos():
    return pd.DataFrame(
        [
            {
                "id": 1,
                "produto": "Notebook",
                "categoria": "Eletronicos",
                "quantidade": 2,
                "preco_unitario": 3500.00,
            },
            {
                "id": 2,
                "produto": "Mouse",
                "categoria": "Perifericos",
                "quantidade": 5,
                "preco_unitario": 80.00,
            },
        ]
    )


def test_dados_validos():
    dados = criar_dados_validos()

    resultado = validate_dataframe(dados)

    assert resultado["valido"] is True
    assert resultado["total_erros"] == 0


def test_id_duplicado():
    dados = criar_dados_validos()
    dados.loc[1, "id"] = 1

    resultado = validate_dataframe(dados)

    assert resultado["valido"] is False
    assert any(erro["tipo"] == "ids_duplicados" for erro in resultado["erros"])


def test_quantidade_negativa():
    dados = criar_dados_validos()
    dados.loc[0, "quantidade"] = -10

    resultado = validate_dataframe(dados)

    assert any(erro["tipo"] == "valores_negativos" for erro in resultado["erros"])


def test_preco_nao_numerico():
    dados = criar_dados_validos()

    # Converte a coluna para aceitar diferentes tipos de valores
    dados["preco_unitario"] = dados["preco_unitario"].astype(object)

    # Insere um valor inválido propositalmente
    dados.loc[0, "preco_unitario"] = "abc"

    resultado = validate_dataframe(dados)

    assert any(erro["tipo"] == "valores_nao_numericos" for erro in resultado["erros"])


def test_coluna_obrigatoria_ausente():
    dados = criar_dados_validos()
    dados = dados.drop(columns=["categoria"])

    resultado = validate_dataframe(dados)

    assert resultado["valido"] is False
    assert any(erro["tipo"] == "colunas_ausentes" for erro in resultado["erros"])
