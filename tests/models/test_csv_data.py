from app.models.csv_data import CSVData


def test_CSVデータの読み込み(csv_data: CSVData):
    assert isinstance(csv_data, CSVData)


def test_CSVデータの行数および列数(csv_data: CSVData):
    # CSVデータの行数
    assert len(csv_data.rows) == 102
    # CSVデータの列数
    assert len(csv_data.cols) == 8
    # 自身の長さは行数を返す
    assert len(csv_data) == len(csv_data.rows)


def test_CSVデータのヘッダー(csv_data: CSVData):
    # CSVデータの列数はヘッダーの個数と同値
    assert len(csv_data.cols) == len(csv_data.header)


def test_CSVデータの内容(csv_data: CSVData):
    # 自身のインデックス参照は rows のインデックス参照を返す
    for i in range(len(csv_data)):
        assert csv_data[i] is csv_data.rows[i]

    # 0行目の内容
    assert csv_data.rows[0] == ["#1レベル名", "材質", "形状", "寸法", "合計", "上部構造", "", ""]
    # 42行目の内容
    assert csv_data.rows[42] == ["#3レベル名", "材質", "形状", "寸法", "合計", "主桁", "横桁", "横構"]


def test_CSVデータをテーブル毎に取得(csv_tables: list[CSVData]):
    # テーブルの総数
    assert len(csv_tables) == 8


def test_CSVデータの行列取得(csv_tables: list[CSVData]):
    assert csv_tables[2][0] == ["#3レベル名", "材質", "形状", "寸法", "合計", "主桁", "横桁", "横構"]
    assert csv_tables[-1].cols[1] == ["材質", "SS400", "加工鋼重中計", "SS400", "購入部品中計", "合計"]


def test_CSVテーブルリストのレベル名(csv_tables: list[CSVData]):
    level_names = [table.rows[0][0][:2] for table in csv_tables]
    assert level_names == ["#1", "#2", "#3", "#3", "#4", "#4", "#4", "#4"]
