from pathlib import Path

import pandas as pd


def read_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Lê um arquivo CSV e retorna seus dados em um DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    if not path.is_file():
        raise ValueError(f"O caminho informado não é um arquivo: {path}")

    return pd.read_csv(path)
