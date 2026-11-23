from pathlib import Path

import pandas as pd


def generate_excel_report(
    df: pd.DataFrame,
    indicadores: dict,
    output_path: str | Path,
) -> Path:
    """
    Gera um relatório Excel com indicadores,
    dados processados e gráficos.
    """

    caminho = Path(output_path)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        workbook = writer.book

        # Formatos
        formato_titulo = workbook.add_format(
            {
                "bold": True,
                "font_size": 18,
                "font_color": "#FFFFFF",
                "bg_color": "#17365D",
                "align": "center",
                "valign": "vcenter",
            }
        )

        formato_subtitulo = workbook.add_format(
            {
                "bold": True,
                "font_size": 12,
                "font_color": "#FFFFFF",
                "bg_color": "#4472C4",
            }
        )

        formato_moeda = workbook.add_format(
            {
                "num_format": "R$ #,##0.00",
            }
        )

        formato_destaque = workbook.add_format(
            {
                "bold": True,
                "font_size": 12,
                "bg_color": "#D9EAF7",
                "num_format": "R$ #,##0.00",
            }
        )

        # Aba de indicadores
        resumo = workbook.add_worksheet("Resumo")

        resumo.merge_range(
            "A1:D1",
            "RELATÓRIO EXECUTIVO DE VENDAS",
            formato_titulo,
        )

        resumo.set_row(0, 35)

        resumo.write("A3", "Indicador", formato_subtitulo)
        resumo.write("B3", "Resultado", formato_subtitulo)

        indicadores_excel = [
            ("Faturamento total", indicadores["faturamento_total"]),
            (
                "Quantidade vendida",
                indicadores["quantidade_total_vendida"],
            ),
            (
                "Ticket médio por unidade",
                indicadores["ticket_medio_por_unidade"],
            ),
            (
                "Maior faturamento por produto",
                indicadores["produto_maior_faturamento"]["nome"],
            ),
            (
                "Produto mais vendido",
                indicadores["produto_mais_vendido"]["nome"],
            ),
        ]

        for linha, (nome, valor) in enumerate(
            indicadores_excel,
            start=3,
        ):
            resumo.write(linha, 0, nome)

            if isinstance(valor, (int, float)):
                formato = (
                    formato_destaque
                    if "faturamento" in nome.lower() or "ticket" in nome.lower()
                    else None
                )

                resumo.write(linha, 1, valor, formato)
            else:
                resumo.write(linha, 1, valor)

        resumo.set_column("A:A", 34)
        resumo.set_column("B:B", 25)

        # Faturamento por categoria
        categorias = indicadores["faturamento_por_categoria"]

        linha_categoria = 10

        resumo.write(
            linha_categoria,
            0,
            "Categoria",
            formato_subtitulo,
        )

        resumo.write(
            linha_categoria,
            1,
            "Faturamento",
            formato_subtitulo,
        )

        for linha, (categoria, valor) in enumerate(
            categorias.items(),
            start=linha_categoria + 1,
        ):
            resumo.write(linha, 0, categoria)
            resumo.write(linha, 1, valor, formato_moeda)

        # Gráfico de faturamento por categoria
        if categorias:
            grafico = workbook.add_chart({"type": "column"})

            primeira_linha = linha_categoria
            ultima_linha = linha_categoria + len(categorias)

            grafico.add_series(
                {
                    "name": "Faturamento",
                    "categories": [
                        "Resumo",
                        primeira_linha + 1,
                        0,
                        ultima_linha,
                        0,
                    ],
                    "values": [
                        "Resumo",
                        primeira_linha + 1,
                        1,
                        ultima_linha,
                        1,
                    ],
                    "fill": {"color": "#4472C4"},
                }
            )

            grafico.set_title({"name": "Faturamento por categoria"})

            grafico.set_y_axis({"name": "Faturamento (R$)"})

            grafico.set_legend({"none": True})

            resumo.insert_chart("D3", grafico)

        # Aba de dados processados
        df.to_excel(
            writer,
            sheet_name="Dados",
            index=False,
        )

        dados_aba = writer.sheets["Dados"]

        dados_aba.freeze_panes(1, 0)
        dados_aba.autofilter(
            0,
            0,
            len(df),
            len(df.columns) - 1,
        )

        dados_aba.set_column(
            0,
            len(df.columns) - 1,
            20,
        )

    return caminho
