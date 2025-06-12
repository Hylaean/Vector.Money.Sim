from __future__ import annotations

from pathlib import Path
import csv
from typing import Iterable, List, Dict

class DataFrame:
    def __init__(self, data: Dict[str, Iterable]):
        self._data = {k: list(v) for k, v in data.items()}
        self.columns = list(data.keys())

    def equals(self, other: 'DataFrame') -> bool:
        return self._data == getattr(other, '_data', None)

    @property
    def shape(self) -> tuple[int, int]:
        rows = len(next(iter(self._data.values()), []))
        return (rows, len(self.columns))

    def copy(self) -> 'DataFrame':
        return DataFrame({k: v[:] for k, v in self._data.items()})

    def select_dtypes(self, _type: str) -> 'DataFrame':
        return DataFrame({k: v[:] for k, v in self._data.items()})

    def div(self, value: float) -> 'DataFrame':
        for k in self.columns:
            self._data[k] = [x / value for x in self._data[k]]
        return self

    def __getitem__(self, key):
        if isinstance(key, list):
            return DataFrame({k: self._data[k][:] for k in key})
        return self._data[key]

    def __setitem__(self, key, value):
        if isinstance(key, list) and isinstance(value, DataFrame):
            for k in key:
                self._data[k] = value._data[k]
        else:
            self._data[key] = value

    @property
    def iloc(self):
        df = self

        class _ILoc:
            def __getitem__(self, idx):
                i, j = idx
                col = df.columns[j]
                return df._data[col][i]

        return _ILoc()

def read_csv(path: str | Path) -> DataFrame:
    with open(Path(path)) as f:
        reader = csv.DictReader(f)
        data: Dict[str, List] = {field: [] for field in reader.fieldnames or []}
        for row in reader:
            for field in data:
                val = row[field]
                try:
                    data[field].append(float(val))
                except ValueError:
                    data[field].append(val)
    return DataFrame(data)

def read_excel(path: str | Path) -> DataFrame:
    return read_csv(path)
