from app.models.csv_summary_data import CSVSummaryData


def test_CSVSummaryData_load_from_csv_file(csv_summary_data: CSVSummaryData):
    assert isinstance(csv_summary_data, CSVSummaryData)


def test_CSVSummaryData_行数および列数(csv_summary_data: CSVSummaryData):
    # CSVデータの行数
    assert len(csv_summary_data.rows) == 102
    # CSVデータの列数
    assert len(csv_summary_data.cols) == 8
    # 自身の長さは行数を返す
    assert len(csv_summary_data) == len(csv_summary_data.rows)


def test_CSVSummaryData_分割したテーブルの取得(csv_summary_data: CSVSummaryData):
    sheets = csv_summary_data.sheets
    assert len(sheets) == 8  # 総括表シートの総数
    # 各シートの列数をチェック
    assert len(sheets[0].cols) == 6
    assert len(sheets[1].cols) == 7
    assert len(sheets[2].cols) == 8
