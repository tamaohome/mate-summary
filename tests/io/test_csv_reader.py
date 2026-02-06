import csv
import tempfile
from pathlib import Path

import pytest

from app.io.csv_handler import read_csv
from app.models.csv_data import CSVData

ENCODING = "shift-jis"


def test_CSVセルの読み込み():
    def strip_cells(cells: list[str]) -> list[str]:
        return [cell.strip() for cell in cells]

    csv_path = Path("tests/data/sample.csv")
    with csv_path.open("r", encoding=ENCODING) as f:
        reader = csv.reader(f)
        header = strip_cells(next(reader))
        data = [strip_cells(cells) for cells in reader]

    assert header == ["id", "value", "note"]
    assert len(data) == 20
    assert len(data[0]) == 3
    assert data[0][1] == "200"
    assert data[1][1] == "0012"
    assert data[2][1] == "1.923"
    assert data[14][1] == ""
    assert data[15][1] == ""
    assert data[16][1] == ""
    assert data[17][1] == "ABC"
    assert data[19][1] == "A1,B2"


def test_CSVファイルの読み込み(sample_csv_path: Path) -> None:
    csv_data = read_csv(sample_csv_path)
    assert isinstance(csv_data, CSVData)


def test_読み込まれたCSVDataの内容(sample_csv_path: Path) -> None:
    csv_data = read_csv(sample_csv_path)
    assert len(csv_data) > 0
    assert csv_data[0][0] == "#1レベル名"


def test_セルの空白削除() -> None:
    # 空白を含むCSVを作成してテスト
    with tempfile.NamedTemporaryFile(mode="w", encoding="shift_jis", suffix=".csv", delete=False) as f:
        f.write(" test , value ")
        temp_path = Path(f.name)

    try:
        csv_data = read_csv(temp_path)
        assert csv_data[0][0] == "test"
        assert csv_data[0][1] == "value"
    finally:
        temp_path.unlink()


def test_ファイルが見つからない場合() -> None:
    """ファイルが見つからない場合にFileNotFoundErrorが発生"""
    non_existent_path = Path("tests/data/non_existent.csv")
    with pytest.raises(FileNotFoundError):
        read_csv(non_existent_path)
