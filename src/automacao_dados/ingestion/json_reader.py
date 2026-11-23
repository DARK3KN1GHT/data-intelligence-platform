from pathlib import Path

import pandas as pd


def read_json(file_path: str | Path) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    if not path.is_file():
        raise ValueError(f"O caminho não é um arquivo: {path}")

    if path.suffix.lower() != ".json":
        raise ValueError("Formato inválido. Esperado: .json")

    return pd.read_json(path)
