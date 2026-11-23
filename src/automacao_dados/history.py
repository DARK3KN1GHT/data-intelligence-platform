import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from automacao_dados.config import settings


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class ExecutionRepository:
    def __init__(self, database: Path | None = None):
        self.database = database or (settings.data_dir / "executions.sqlite3")
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS executions (
                    id TEXT PRIMARY KEY,
                    input_file TEXT NOT NULL,
                    status TEXT NOT NULL
                        CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    duration_seconds REAL,
                    records_processed INTEGER,
                    revenue REAL,
                    anomalies INTEGER,
                    report_file TEXT,
                    error_message TEXT
                )
                """
            )

    def start(self, execution_id: str, input_file: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO executions
                    (id, input_file, status, started_at)
                VALUES (?, ?, 'RUNNING', ?)
                """,
                (execution_id, input_file, utc_now()),
            )

    def finish(
        self,
        execution_id: str,
        *,
        status: str,
        duration: float,
        result: dict | None = None,
        error: str | None = None,
    ) -> None:
        if status not in {"SUCCESS", "FAILED"}:
            raise ValueError(f"Status final inválido: {status}")

        result = result or {}
        indicadores = result.get("indicadores", {})

        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE executions
                SET status = ?,
                    finished_at = ?,
                    duration_seconds = ?,
                    records_processed = ?,
                    revenue = ?,
                    anomalies = ?,
                    report_file = ?,
                    error_message = ?
                WHERE id = ? AND status = 'RUNNING'
                """,
                (
                    status,
                    utc_now(),
                    duration,
                    result.get("total_registros"),
                    indicadores.get("faturamento_total"),
                    result.get("total_anomalias"),
                    result.get("arquivo_relatorio"),
                    error,
                    execution_id,
                ),
            )

            if cursor.rowcount != 1:
                raise ValueError(f"Execução inexistente ou finalizada: {execution_id}")

    def list_recent(self, limit: int = 10) -> list[dict]:
        if limit < 1:
            raise ValueError("O limite deve ser maior que zero.")

        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM executions
                ORDER BY started_at DESC, rowid DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [dict(row) for row in rows]
