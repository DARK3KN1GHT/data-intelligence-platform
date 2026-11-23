import pytest

from automacao_dados.history import ExecutionRepository


@pytest.fixture
def repository(tmp_path):
    return ExecutionRepository(tmp_path / "test.sqlite3")


def test_registra_execucao_em_andamento(repository):
    repository.start("exec-001", "vendas.csv")

    history = repository.list_recent()

    assert len(history) == 1
    assert history[0]["status"] == "RUNNING"
    assert history[0]["input_file"] == "vendas.csv"


def test_finaliza_execucao_com_sucesso(repository):
    repository.start("exec-002", "vendas.csv")

    repository.finish(
        "exec-002",
        status="SUCCESS",
        duration=0.25,
        result={
            "total_registros": 5,
            "total_anomalias": 0,
            "arquivo_relatorio": "relatorio.xlsx",
            "indicadores": {
                "faturamento_total": 11150.0,
            },
        },
    )

    execution = repository.list_recent()[0]

    assert execution["status"] == "SUCCESS"
    assert execution["records_processed"] == 5
    assert execution["revenue"] == 11150.0
    assert execution["duration_seconds"] == 0.25


def test_registra_execucao_com_falha(repository):
    repository.start("exec-003", "inexistente.csv")

    repository.finish(
        "exec-003",
        status="FAILED",
        duration=0.01,
        error="Arquivo não encontrado",
    )

    execution = repository.list_recent()[0]

    assert execution["status"] == "FAILED"
    assert "não encontrado" in execution["error_message"]


def test_impede_finalizacao_duplicada(repository):
    repository.start("exec-004", "vendas.csv")
    repository.finish(
        "exec-004",
        status="SUCCESS",
        duration=0.1,
    )

    with pytest.raises(ValueError):
        repository.finish(
            "exec-004",
            status="SUCCESS",
            duration=0.2,
        )
