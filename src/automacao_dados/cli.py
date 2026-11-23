import argparse
import logging
import sys
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from automacao_dados.config import settings
from automacao_dados.history import ExecutionRepository
from automacao_dados.logging_config import configure_logging
from automacao_dados.pipeline import run_pipeline

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="automacao-dados",
        description="Plataforma de automação e inteligência de dados.",
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    run = commands.add_parser(
        "run",
        help="Executa o pipeline de dados.",
    )

    run.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Arquivo CSV, Excel ou JSON.",
    )

    run.add_argument(
        "--output",
        type=Path,
        default=settings.reports_dir,
        help="Diretório dos relatórios.",
    )

    history = commands.add_parser(
        "history",
        help="Mostra execuções anteriores.",
    )

    history.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Quantidade de execuções exibidas.",
    )

    return parser


def execute_run(
    input_file: Path,
    output_dir: Path,
    repository: ExecutionRepository,
) -> int:
    execution_id = str(uuid4())
    start = perf_counter()

    try:
        repository.start(execution_id, str(input_file))
    except Exception:
        logger.exception("Não foi possível registrar a execução")
        return 1

    logger.info("Execução iniciada: %s", execution_id)

    try:
        result = run_pipeline(
            input_file,
            output_dir=output_dir,
            execution_id=execution_id,
        )

        duration = perf_counter() - start

        repository.finish(
            execution_id,
            status="SUCCESS",
            duration=duration,
            result=result,
        )

    except Exception as exc:
        duration = perf_counter() - start

        logger.exception("Falha na execução %s", execution_id)

        try:
            repository.finish(
                execution_id,
                status="FAILED",
                duration=duration,
                error=str(exc),
            )
        except Exception:
            logger.exception("Falha ao atualizar histórico")

        return 1

    logger.info("Status: SUCCESS")
    logger.info("Registros: %d", result["total_registros"])
    logger.info(
        "Faturamento: R$ %.2f",
        result["indicadores"]["faturamento_total"],
    )
    logger.info("Relatório: %s", result["arquivo_relatorio"])
    logger.info("Duração: %.3fs", duration)

    return 0


def show_history(
    repository: ExecutionRepository,
    limit: int,
) -> int:
    try:
        executions = repository.list_recent(limit)
    except (ValueError, OSError):
        logger.exception("Não foi possível consultar o histórico")
        return 1

    if not executions:
        print("Nenhuma execução registrada.")
        return 0

    print(f"{'ID':36}  {'STATUS':8}  {'REGISTROS':10}  ARQUIVO")

    for execution in executions:
        print(
            f"{execution['id']:36}  "
            f"{execution['status']:8}  "
            f"{str(execution['records_processed'] or 0):10}  "
            f"{execution['input_file']}"
        )

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    configure_logging()

    try:
        repository = ExecutionRepository()

        if args.command == "run":
            return execute_run(
                args.input,
                args.output,
                repository,
            )

        if args.command == "history":
            return show_history(repository, args.limit)

    except Exception:
        logger.exception("Erro ao inicializar a aplicação")
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
