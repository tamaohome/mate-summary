import pytest
from app.models.summary_sheet import SummarySheet, SummaryTotalColumn


def test_SummarySheet(summary_sheet: SummarySheet):
    assert len(summary_sheet.cols) == 11


def test_SummarySheet_レベル毎の列リストを取得(summary_sheet: SummarySheet):
    # レベル毎の列リストを取得
    level_1_cols = summary_sheet.cols_by_level[1]
    level_2_cols = summary_sheet.cols_by_level[2]
    level_3_cols = summary_sheet.cols_by_level[3]
    level_4_cols = summary_sheet.cols_by_level[4]

    # レベル毎の列名リストを取得
    level_1_col_names = [col.name for col in level_1_cols]
    level_2_col_names = [col.name for col in level_2_cols]
    level_3_col_names = [col.name for col in level_3_cols]
    level_4_col_names = [col.name for col in level_4_cols]

    assert level_1_col_names == ["上部構造"]
    assert level_2_col_names == ["主構造", "附属物"]
    assert level_3_col_names == ["主桁", "横桁", "横構", "排水装置"]
    assert level_4_col_names == ["G1", "端支点横桁", "下横構", "取付金具"]


def test_SummaryColumn_列番号を基に総括表列を取得(summary_sheet: SummarySheet):
    # 最初の総括表行をチェック
    col_1 = summary_sheet.cols[0]
    assert col_1.name == "上部構造"
    assert col_1.level == 1
    assert col_1.level_name == "サンプル橋"
    # 小計5行を除外したアイテム数
    assert len(col_1.items) == 20 - 5

    # 最後の総括表行をチェック
    col_2 = summary_sheet.cols[-1]
    assert col_2.name == "取付金具"
    assert col_2.level == 4
    assert col_2.level_name == "排水装置"
    assert len(col_2.items) == 5


def test_SummaryColumn_階層関係を基に総括表列を取得(summary_sheet: SummarySheet):
    # 最上位レベルの総括表列を取得
    root_col = summary_sheet.children[0]

    # 子レベルの総括表列リストを取得
    child_cols = root_col.children
    assert len(child_cols) == 2
    assert child_cols[0].name == "主構造"
    assert child_cols[1].name == "附属物"

    # 更に子レベルの総括表列リストを取得
    grandchild_cols = child_cols[0].children
    assert len(grandchild_cols) == 3
    assert grandchild_cols[0].name == "主桁"
    assert grandchild_cols[1].name == "横桁"
    assert grandchild_cols[2].name == "横構"


def test_SummaryProps_等価性のチェック(summary_sheet: SummarySheet):
    item_1 = summary_sheet.descendants[0].items[0]  # SMA490BW, PL, 19.0
    item_2 = summary_sheet.descendants[1].items[0]  # SMA490BW, PL, 19.0
    item_3 = summary_sheet.descendants[1].items[1]  # SMA490AW, PL, 16.0

    assert item_1.props == item_2.props
    assert item_1.props != item_3.props


def test_SummarySheet_総括表の行ヘッダーリストを取得(summary_sheet: SummarySheet):
    header_rows = summary_sheet.header_rows
    assert len(header_rows) == 16
    assert header_rows[0] == ["材質", "形状", "寸法"]
    assert header_rows[1] == ["SMA490BW", "PL", "19.0"]
    # 小計の行は取得しない
    assert header_rows[2] == ["SMA490AW", "PL", "16.0"]
    # 最後の行
    assert header_rows[-1] == ["合計", "", ""]


def test_SummaryTotalColumn_合計列を取得(summary_sheet: SummarySheet):
    total_col = summary_sheet.total_col
    assert len(total_col) == 16
    assert isinstance(total_col, SummaryTotalColumn)
    assert total_col.name == "合計"
    assert total_col.data[0] == "166"
    # 小計の行は取得しない
    assert total_col.data[1] == "38"
    # 最後の行
    assert total_col.data[-1] == "960"
