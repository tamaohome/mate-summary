import tempfile
from pathlib import Path

import pytest

from app.io import ENCODING
from app.io.csv_reader import CSVReader, CSVRow


@pytest.fixture(scope="module")
def sample_csv_path() -> Path:
    """サンプルCSVファイルへのパスを返すフィクスチャ"""
    return Path("tests/data/sample.csv")


@pytest.fixture(scope="module")
def sample_csv_rows(sample_csv_path: Path) -> list[CSVRow]:
    """サンプルCSVファイルを基に読み込んだCSVデータを返すフィクスチャ"""
    reader = CSVReader(sample_csv_path)
    return reader.load()


def test_CSVReader_セルの読み込み(sample_csv_rows: list[CSVRow]):
    header = sample_csv_rows[0]
    data = sample_csv_rows[1:]

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


def test_CSVReader_セルの空白削除() -> None:
    # 空白を含むCSVを作成してテスト
    with tempfile.NamedTemporaryFile(mode="w", encoding=ENCODING, suffix=".csv", delete=False) as f:
        f.write(" test , value ")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        csv_rows = reader.load()
        assert csv_rows[0][0] == "test"
        assert csv_rows[0][1] == "value"
    finally:
        temp_path.unlink()


def test_CSVReader_ファイルが見つからない場合() -> None:
    """ファイルが見つからない場合にFileNotFoundErrorが発生"""
    non_existent_path = Path("tests/data/non_existent.csv")
    with pytest.raises(FileNotFoundError):
        _ = CSVReader(non_existent_path)
