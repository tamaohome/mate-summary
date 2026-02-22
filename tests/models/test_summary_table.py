import pytest

from app.models.summary_table import SummarySheet


@pytest.mark.skip
def test_SummaryTableの読み込み(summary_sheets: list[SummarySheet]):
    assert len(summary_sheets) == 4
    # 辞書のキー 1, 2, 3, 4 は値が存在する
    assert all([summary_sheets[1], summary_sheets[2], summary_sheets[3], summary_sheets[4]])
    # それ以外のキーには値が存在しない
    with pytest.raises(KeyError):
        _ = summary_sheets[0]
    with pytest.raises(KeyError):
        _ = summary_sheets[5]


@pytest.mark.skip
def test_SummaryTableの名称(summary_sheets: list[SummarySheet]):
    assert summary_sheets[1].name == "#1レベル名"
    assert summary_sheets[2].name == "#2レベル名"
    assert summary_sheets[3].name == "#3レベル名"
    assert summary_sheets[4].name == "#4レベル名"


@pytest.mark.skip
def test_SummaryTableのヘッダー列(summary_sheets: list[SummarySheet]):
    table = summary_sheets[1]
    assert len(table.header_cols) == 5

    assert {"#1レベル名", "材質", "形状", "寸法", "合計"}.issubset(table.header_cols)

    assert len(table.header_cols["#1レベル名"]) == 20
    assert len(table.header_cols["材質"]) == 20
    assert len(table.header_cols["形状"]) == 20
    assert len(table.header_cols["寸法"]) == 20
    assert len(table.header_cols["合計"]) == 20


@pytest.mark.skip
def test_SummaryTableをCSVDataに変換(summary_sheets: list[SummarySheet]):
    table = summary_sheets[3]
    csvdata = table.to_csvdata()

    # ヘッダー行の内容をテスト
    header = csvdata.rows[0]
    header_names = ["#3レベル名", "材質", "形状", "寸法", "合計", "主桁", "横桁", "横構", "排水装置"]
    assert header_names == header

    # データ行の個数をテスト
    assert all(len(header_names) == len(row) for row in csvdata.data)


@pytest.mark.skip
def test_SummaryTableの列数(summary_sheets: list[SummarySheet]):
    table = summary_sheets[1]
    assert len(table.cols) == 1


@pytest.mark.skip
def test_SummaryColumnの内容(summary_sheets: list[SummarySheet]):
    summary_column = summary_sheets[1].cols[0]
    assert len(summary_column) == 20
    assert summary_column.name == "上部構造"
    assert summary_column.parent_name == "サンプル橋"


@pytest.mark.skip
def test_SummaryItemの内容(summary_sheets: list[SummarySheet]):
    summary_item = summary_sheets[1].cols[0].items[0]
    assert summary_item.value == "166"
    assert summary_item.props["材質"] == "SMA490BW"
    assert summary_item.props["形状"] == "PL"
    assert summary_item.props["寸法"] == "19.0"
