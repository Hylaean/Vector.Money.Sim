import pandas as pd

from src.data.io import read_inventory, read_io_table
from src.data.normalise import normalise_per_capita


def test_read_io_and_inventory(tmp_path):
    csv = tmp_path / "table.csv"
    csv.write_text("a,b\n1,2\n3,4\n")
    df_io = read_io_table(csv)
    df_inv = read_inventory(csv)
    assert df_io.equals(df_inv)
    assert df_io.shape == (2, 2)


def test_normalise_per_capita():
    df = pd.DataFrame({"a": [10, 20], "b": [30, 40]})
    result = normalise_per_capita(df, population=10)
    assert result.iloc[0, 0] == 1
    assert result.iloc[1, 1] == 4
