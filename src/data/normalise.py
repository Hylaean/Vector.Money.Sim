"""Data normalisation helpers."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def normalise_per_capita(
    data: pd.DataFrame, population: float, columns: Iterable[str] | None = None
) -> pd.DataFrame:
    """Return a per-capita normalised copy of ``data``."""
    if population == 0:
        raise ValueError("population must be non-zero")

    df = data.copy()
    cols = list(columns) if columns is not None else df.select_dtypes("number").columns
    df[cols] = df[cols].div(population)
    return df
