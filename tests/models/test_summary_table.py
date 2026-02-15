import pytest

from app.models.summary_table import SummaryTable


def test_SummaryTableの読み込み(summary_tables: list[SummaryTable]):
    assert len(summary_tables) == 4
    # 辞書のキー 1, 2, 3, 4 は値が存在する
    assert all([summary_tables[1], summary_tables[2], summary_tables[3], summary_tables[4]])
    # それ以外のキーには値が存在しない
    with pytest.raises(KeyError):
        _ = summary_tables[0]
    with pytest.raises(KeyError):
        _ = summary_tables[5]


def test_SummaryTableの内容(summary_tables: list[SummaryTable]):
    assert summary_tables[1].name == "#1レベル名"
    assert summary_tables[2].name == "#2レベル名"


def test_SummaryTableのヘッダー列(summary_tables: list[SummaryTable]):
    table = summary_tables[1]
    assert len(table.header_cols) == 5
    assert "#1レベル名" in table.header_cols
    assert "材質" in table.header_cols
    assert "形状" in table.header_cols
    assert "寸法" in table.header_cols
    assert "合計" in table.header_cols
    assert len(table.header_cols["#1レベル名"]) == 20
    assert len(table.header_cols["材質"]) == 20
    assert len(table.header_cols["形状"]) == 20
    assert len(table.header_cols["寸法"]) == 20
    assert len(table.header_cols["合計"]) == 20


def test_SummaryTableの列数(summary_tables: list[SummaryTable]):
    table = summary_tables[1]
    assert len(table.cols) == 1


def test_SummaryColumnの内容(summary_tables: list[SummaryTable]):
    summary_column = summary_tables[1].cols[0]
    assert len(summary_column) == 20
    assert summary_column.name == "上部構造"
    assert summary_column.parent_name == "サンプル橋"


def test_SummaryItemの内容(summary_tables: list[SummaryTable]):
    summary_item = summary_tables[1].cols[0].items[0]
    assert summary_item.value == "166"
    assert summary_item.props["材質"] == "SMA490BW"
    assert summary_item.props["形状"] == "PL"
    assert summary_item.props["寸法"] == "19.0"
