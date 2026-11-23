import logging
from pathlib import Path

import pandas as pd

from automacao_dados.analysis.anomaly_detector import detect_anomalies
from automacao_dados.analysis.sales_analyzer import analyze_sales
from automacao_dados.config import settings
from automacao_dados.exceptions import (
    DataValidationError,
    IngestionError,
    ProcessingError,
    ReportGenerationError,
)
from automacao_dados.ingestion.csv_reader import read_csv
from automacao_dados.ingestion.excel_reader import read_excel
from automacao_dados.ingestion.json_reader import read_json
from automacao_dados.processing.data_processor import process_dataframe
from automacao_dados.reporting.excel_report import generate_excel_report
from automacao_dados.validation.data_validator import validate_dataframe

logger = logging.getLogger(__name__)


def load_data(file_path: Path) -> pd.DataFrame:
    readers = {
        ".csv": read_csv,
        ".xlsx": read_excel,
        ".json": read_json,
    }

    reader = readers.get(file_path.suffix.lower())

    if reader is None:
        raise IngestionError(f"Formato não suportado: {file_path.suffix}")

    try:
        return reader(file_path)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        raise IngestionError(f"Falha ao importar {file_path}: {exc}") from exc


def run_pipeline(
    file_path: str | Path,
    output_dir: str | Path | None = None,
    execution_id: str | None = None,
) -> dict:
    origem = Path(file_path)

    if not origem.is_file():
        raise IngestionError(f"Arquivo não encontrado: {origem}")

    destino = Path(output_dir) if output_dir is not None else settings.reports_dir

    logger.info("Importando dados")
    dados = load_data(origem)

    logger.info("Validando %d registros", len(dados))
    diagnostico = validate_dataframe(dados)

    if not diagnostico["valido"]:
        raise DataValidationError(f"Validação falhou: {diagnostico['erros']}")

    logger.info("Processando dados")

    try:
        dados_processados = process_dataframe(dados)
        indicadores = analyze_sales(dados_processados)
        anomalias = detect_anomalies(dados_processados)
    except (ValueError, TypeError, KeyError) as exc:
        raise ProcessingError(str(exc)) from exc

    settings.processed_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    nome_base = f"{origem.stem}_{origem.suffix.lstrip('.').lower()}"

    if execution_id is not None:
        nome_base = f"{nome_base}_{execution_id}"

    arquivo_csv = settings.processed_dir / f"{nome_base}_processado.csv"

    arquivo_excel = destino / f"{nome_base}_relatorio.xlsx"

    try:
        dados_processados.to_csv(arquivo_csv, index=False)

        generate_excel_report(
            df=dados_processados,
            indicadores=indicadores,
            output_path=arquivo_excel,
        )
    except (OSError, ValueError, TypeError) as exc:
        raise ReportGenerationError(f"Falha ao gerar arquivos: {exc}") from exc

    logger.info("Análise concluída")
    logger.info(
        "Faturamento: %.2f",
        indicadores["faturamento_total"],
    )

    return {
        "execution_id": execution_id,
        "arquivo_origem": str(origem),
        "arquivo_saida": str(arquivo_csv),
        "arquivo_relatorio": str(arquivo_excel),
        "total_registros": len(dados_processados),
        "diagnostico": diagnostico,
        "indicadores": indicadores,
        "anomalias": anomalias,
        "total_anomalias": len(anomalias),
    }
