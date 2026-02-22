from app.models.summary_sheet import SummarySheet


def test_SummarySheet(summary_sheet: SummarySheet):
    assert len(summary_sheet.cols) == 11


def test_SummaryColumn_properties(summary_sheet: SummarySheet):
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
