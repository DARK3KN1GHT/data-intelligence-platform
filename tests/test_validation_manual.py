import pandas as pd

from automacao_dados.validation.data_validator import validate_dataframe

# Criando dados propositalmente defeituosos
dados_teste = pd.DataFrame(
    [
        {
            "id": 1,
            "produto": "Notebook",
            "categoria": "Eletronicos",
            "quantidade": 2,
            "preco_unitario": 3500.00,
        },
        {
            "id": 1,  # ID duplicado
            "produto": "Mouse",
            "categoria": None,  # Categoria ausente
            "quantidade": -5,  # Quantidade negativa
            "preco_unitario": 80.00,
        },
        {
            "id": 3,
            "produto": "Teclado",
            "categoria": "Perifericos",
            "quantidade": 3,
            "preco_unitario": "abc",  # Preço inválido
        },
    ]
)


# Executando a validação
resultado = validate_dataframe(dados_teste)

print("\n===== TESTE DE VALIDAÇÃO =====")
print(f"Registros analisados: {resultado['total_registros']}")
print(f"Dados válidos: {resultado['valido']}")
print(f"Total de erros: {resultado['total_erros']}")

print("\nProblemas encontrados:")

for erro in resultado["erros"]:
    print(f"- [{erro['tipo']}] {erro['mensagem']}")
