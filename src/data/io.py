"""Functions to load input-output tables and ecological inventories."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _read_file(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def read_io_table(path: str | Path) -> pd.DataFrame:
    """Return an input-output table located at ``path``."""
    return _read_file(path)


def read_inventory(path: str | Path) -> pd.DataFrame:
    """Return an ecological inventory located at ``path``."""
    return _read_file(path)
