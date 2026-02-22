from pathlib import Path

from app.models.csv_data import CSVData


def test_CSVData_load_from_csv(summary_csv_path: Path):
    csv_data = CSVData.load_from_csv(summary_csv_path)
    assert isinstance(csv_data, CSVData)


def test_CSVData_行数および列数(csv_data: CSVData):
    # CSVデータの行数
    assert len(csv_data.rows) == 102
    # CSVデータの列数
    assert len(csv_data.cols) == 8
    # 自身の長さは行数を返す
    assert len(csv_data) == len(csv_data.rows)


def test_CSVData_ヘッダーの列数(csv_data: CSVData):
    # CSVデータの列数はヘッダーの個数と同値
    assert len(csv_data.cols) == len(csv_data.header)


def test_CSVデータの内容(csv_data: CSVData):
    # 自身のインデックス参照は rows のインデックス参照を返す
    for i in range(len(csv_data)):
        assert csv_data[i] is csv_data.rows[i]

    # 0行目の内容 (最大列数に満たない行は空文字列でフィルされる)
    assert csv_data.rows[0] == ["#1レベル名", "材質", "形状", "寸法", "合計", "上部構造", "", ""]
    # 42行目の内容
    assert csv_data.rows[42] == ["#3レベル名", "材質", "形状", "寸法", "合計", "主桁", "横桁", "横構"]
