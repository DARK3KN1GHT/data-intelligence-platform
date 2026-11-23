from pathlib import Path

from automacao_dados.pipeline import run_pipeline


def main() -> None:
    diretorio = Path("data/raw")

    arquivos = [
        diretorio / "vendas.csv",
        diretorio / "vendas.xlsx",
        diretorio / "vendas.json",
    ]

    for arquivo in arquivos:
        print(f"\n{'=' * 55}")
        print(f"PROCESSANDO: {arquivo.name}")
        print(f"{'=' * 55}")

        try:
            resultado = run_pipeline(arquivo)

            indicadores = resultado["indicadores"]
            anomalias = resultado["anomalias"]

            print("\nPIPELINE EXECUTADO COM SUCESSO!")
            print(f"Registros: {resultado['total_registros']}")
            print(f"Erros de validação: {resultado['diagnostico']['total_erros']}")

            print("\nINDICADORES DE VENDAS")
            print("-" * 40)

            print(f"Faturamento total: R$ {indicadores['faturamento_total']:,.2f}")
            print(f"Quantidade vendida: {indicadores['quantidade_total_vendida']}")
            print(
                f"Ticket médio por unidade: "
                f"R$ {indicadores['ticket_medio_por_unidade']:,.2f}"
            )
            print(
                f"Produto com maior faturamento: "
                f"{indicadores['produto_maior_faturamento']['nome']}"
            )
            print(
                f"Produto mais vendido: {indicadores['produto_mais_vendido']['nome']}"
            )

            print("\nFATURAMENTO POR CATEGORIA")

            for categoria, valor in indicadores["faturamento_por_categoria"].items():
                print(f"{categoria}: R$ {valor:,.2f}")

            print("\nDETECÇÃO DE ANOMALIAS")
            print("-" * 40)
            print(f"Total de anomalias: {resultado['total_anomalias']}")

            if anomalias:
                for anomalia in anomalias:
                    produto = anomalia.get("produto", "Não identificado")

                    print(
                        f"Produto: {produto} | "
                        f"Campo: {anomalia['campo']} | "
                        f"Valor: {anomalia['valor']}"
                    )
            else:
                print("Nenhuma anomalia estatística identificada.")

            print("\nARQUIVOS GERADOS")
            print(f"CSV: {resultado['arquivo_saida']}")
            print(f"Excel: {resultado['arquivo_relatorio']}")

        except (FileNotFoundError, ValueError) as erro:
            print(f"Falha no processamento: {erro}")


if __name__ == "__main__":
    main()
