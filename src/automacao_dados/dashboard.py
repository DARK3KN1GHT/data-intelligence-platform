
from pathlib import Path

import pandas as pd
import streamlit as st

from automacao_dados.history import ExecutionRepository

st.set_page_config(
    page_title="Data Intelligence | Monitoramento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_executions() -> pd.DataFrame:
    repository = ExecutionRepository()
    records = repository.list_recent(limit=10000)

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    df["started_at"] = pd.to_datetime(
        df["started_at"],
        utc=True,
        errors="coerce",
    )

    df["duration_seconds"] = pd.to_numeric(
        df["duration_seconds"],
        errors="coerce",
    )

    return df


def show_metrics(df: pd.DataFrame) -> None:
    total = len(df)
    success = int((df["status"] == "SUCCESS").sum())
    failed = int((df["status"] == "FAILED").sum())

    success_rate = success / total * 100 if total else 0

    finished = df.loc[
        df["status"].isin(["SUCCESS", "FAILED"]),
        "duration_seconds",
    ]

    avg_duration = finished.mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Execuções", f"{total:,}")
    col2.metric("Sucesso", f"{success_rate:.1f}%")
    col3.metric("Falhas", failed)
    col4.metric(
        "Tempo médio",
        f"{avg_duration:.3f} s"
        if pd.notna(avg_duration)
        else "—",
    )


def show_charts(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Execuções por status")

        status_counts = (
            df["status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Quantidade")
        )

        st.bar_chart(
            status_counts,
            x="Status",
            y="Quantidade",
            color="#38BDF8",
        )

    with col2:
        st.subheader("Atividade diária")

        daily = (
            df.dropna(subset=["started_at"])
            .assign(
                data=lambda data: data[
                    "started_at"
                ].dt.date
            )
            .groupby("data")
            .size()
            .rename("Execuções")
        )

        st.line_chart(daily)


def show_history(df: pd.DataFrame) -> None:
    st.subheader("Histórico de processamento")

    status_options = [
        "Todos",
        "SUCCESS",
        "FAILED",
        "RUNNING",
    ]

    selected_status = st.selectbox(
        "Filtrar por status",
        status_options,
    )

    filtered = df.copy()

    if selected_status != "Todos":
        filtered = filtered[
            filtered["status"] == selected_status
        ]

    columns = [
        "started_at",
        "id",
        "status",
        "input_file",
        "records_processed",
        "revenue",
        "duration_seconds",
    ]

    st.dataframe(
        filtered[columns].rename(
            columns={
                "started_at": "Início (UTC)",
                "id": "Execução",
                "status": "Status",
                "input_file": "Arquivo",
                "records_processed": "Registros",
                "revenue": "Faturamento",
                "duration_seconds": "Duração (s)",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "O faturamento corresponde a cada execução. "
        "Processamentos repetidos podem conter as "
        "mesmas vendas."
    )


def show_execution_details(df: pd.DataFrame) -> None:
    st.subheader("Detalhes da execução")

    execution_id = st.selectbox(
        "Selecione uma execução",
        df["id"].tolist(),
        format_func=lambda value: value[:8],
    )

    execution = df.loc[df["id"] == execution_id].iloc[0]

    st.write("**Status:**", execution["status"])
    st.write("**Arquivo:**", execution["input_file"])
    st.write("**UUID:**", execution["id"])

    error = execution.get("error_message")

    if pd.notna(error) and error:
        st.error(str(error))

    report = execution.get("report_file")

    if pd.notna(report) and report:
        path = Path(str(report))

        if path.is_file():
            with path.open("rb") as file:
                st.download_button(
                    label="Baixar relatório Excel",
                    data=file.read(),
                    file_name=path.name,
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                    ),
                )


def main() -> None:
    st.title("Data Intelligence")
    st.caption("Plataforma de Automação e Inteligência de Dados")

    with st.sidebar:
        st.header("Monitoramento")
        st.write("Histórico de execuções registrado no SQLite.")

        if st.button("Atualizar dados", use_container_width=True):
            st.rerun()

        st.divider()
        st.caption("Versão 0.3.0")

    try:
        df = load_executions()
    except Exception as exc:
        st.error(f"Não foi possível consultar o histórico: {exc}")
        st.stop()

    if df.empty:
        st.info(
            "Nenhuma execução registrada. "
            "Execute o pipeline pelo terminal."
        )
        st.stop()

    show_metrics(df)

    st.divider()
    show_charts(df)

    st.divider()
    show_history(df)

    st.divider()
    show_execution_details(df)


if __name__ == "__main__":
    main()

