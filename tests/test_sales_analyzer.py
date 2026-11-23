import pandas as pd
import pytest

from automacao_dados.analysis.sales_analyzer import analyze_sales


@pytest.fixture
def dados_vendas():
    return pd.DataFrame(
        {
            "produto": ["Notebook", "Mouse", "Teclado"],
            "categoria": ["Eletronicos", "Perifericos", "Perifericos"],
            "quantidade": [2, 5, 3],
            "preco_unitario": [3500.00, 80.00, 150.00],
            "valor_total": [7000.00, 400.00, 450.00],
        }
    )


def test_faturamento_total(dados_vendas):
    resultado = analyze_sales(dados_vendas)

    assert resultado["faturamento_total"] == 7850.00


def test_quantidade_total_vendida(dados_vendas):
    resultado = analyze_sales(dados_vendas)

    assert resultado["quantidade_total_vendida"] == 10


def test_ticket_medio_por_unidade(dados_vendas):
    resultado = analyze_sales(dados_vendas)

    assert resultado["ticket_medio_por_unidade"] == 785.00


def test_produto_maior_faturamento(dados_vendas):
    resultado = analyze_sales(dados_vendas)

    assert resultado["produto_maior_faturamento"]["nome"] == "Notebook"
    assert resultado["produto_maior_faturamento"]["valor"] == 7000.00


def test_produto_mais_vendido(dados_vendas):
    resultado = analyze_sales(dados_vendas)

    assert resultado["produto_mais_vendido"]["nome"] == "Mouse"
    assert resultado["produto_mais_vendido"]["quantidade"] == 5


def test_faturamento_por_categoria(dados_vendas):
    resultado = analyze_sales(dados_vendas)

    assert resultado["faturamento_por_categoria"] == {
        "Eletronicos": 7000.00,
        "Perifericos": 850.00,
    }


def test_dataframe_vazio():
    dados = pd.DataFrame(
        columns=[
            "produto",
            "categoria",
            "quantidade",
            "preco_unitario",
            "valor_total",
        ]
    )

    with pytest.raises(ValueError, match="Não existem dados"):
        analyze_sales(dados)


def test_coluna_obrigatoria_ausente(dados_vendas):
    dados = dados_vendas.drop(columns=["valor_total"])

    with pytest.raises(ValueError, match="Colunas necessárias"):
        analyze_sales(dados)
