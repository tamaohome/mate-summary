from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Final, overload, override

from anytree import NodeMixin

from app.io.csv_reader import CSVRowType
from app.models.csv_data import CSVColType
from app.models.csv_summary_data import CSVSummaryData

HEADER_COL_NAMES = ["材質", "形状", "寸法"]


class SummarySheet(NodeMixin):
    """総括表クラス"""

    def __init__(self, csv_summary_data: CSVSummaryData):
        self._csv_summary_data: Final = csv_summary_data
        self._parse_summary_columns()

    def __iter__(self) -> Iterator[SummaryColumn]:
        return iter(self.children)

    @overload
    def __getitem__(self, key: int) -> SummaryColumn: ...
    @overload
    def __getitem__(self, key: slice) -> tuple[SummaryColumn, ...]: ...
    @overload
    def __getitem__(self, key: str) -> list[str]: ...
    def __getitem__(self, key: int | slice | str):
        if isinstance(key, str):
            return self.header_cols[key]
        return self.cols[key]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @staticmethod
    def load_from_csv(csv_path: str | Path) -> SummarySheet:
        """CSVファイルからインスタンスを生成する"""
        csv_summary_data = CSVSummaryData.load_from_csv(csv_path)
        return SummarySheet(csv_summary_data)

    @property
    @override
    def children(self) -> tuple[SummaryColumn, ...]:
        return super().children

    @property
    def cols(self) -> tuple[SummaryColumn, ...]:
        """総括表列"""
        return self.children

    @property
    def columns(self) -> tuple[SummaryColumn, ...]:
        """総括表列"""
        return self.children

    @property
    def header_cols(self) -> dict[str, list[str]]:
        """総括表ヘッダー列"""
        result: dict[str, list[str]] = {}
        for header_name in HEADER_COL_NAMES:
            result[header_name] = [col[header_name] for col in self.cols]
        return result

    # def to_csvdata(self) -> CSVData:
    #     """`SummaryTable` を `CSVData` 形式に変換して返す"""
    #     cols: list[CSVColType] = []

    #     # ヘッダー列を構築
    #     # header_colsの各エントリを列に変換
    #     for header_name, header_values in self.header_cols.items():
    #         cols.append([header_name] + header_values)

    #     # データ列を構築
    #     # 各SummaryColumnとその配下のSummaryItemを処理
    #     for col in self.cols:
    #         row = [col.name]
    #         for item in col.items:
    #             row.append(item.value)
    #         cols.append(row)

    #     # 行列変換
    #     rows: list[CSVRowType] = []
    #     for row in zip(*cols, strict=False):
    #         rows.append(row)

    #     # CSVDataオブジェクトを生成して返す
    #     return CSVData(rows)

    def _parse_summary_columns(self) -> None:
        """総括表列を生成する"""
        # 分割したCSV総括表シートをループ
        for sheet in self._csv_summary_data.sheets:
            header_cols: list[CSVColType] = []
            # CSV総括表の列をループ
            for col in sheet.cols:
                # ヘッダー列の場合はヘッダー列リストに追加してスキップ
                if _is_header_col(col):
                    header_cols.append(col)
                    continue
                # 総括表列インスタンスを生成
                SummaryColumn(self, col, header_cols)


class SummaryColumn(NodeMixin):
    """総括表の列クラス"""

    def __init__(self, parent: SummarySheet, col: CSVColType, header_cols: list[CSVColType]):
        self.parent: SummarySheet = parent
        self._col = col
        self._header_cols = header_cols
        self.name: Final = self._get_name()
        self.level = self._get_level()
        self.level_name = self._get_level_name()
        self._parse_summary_items()

    def __getitem__(self, index):
        return self.children[index]

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        items_count = len(self.items)
        return f"SummaryColumn(name={self.name!r}, level_name={self.level_name!r}, items={items_count})"

    @property
    def children(self) -> tuple[SummaryItem]:
        return super().children

    @property
    def items(self) -> tuple[SummaryItem]:
        return self.children

    def _get_name(self) -> str:
        """CSV列データを基に列名を返す"""
        return self._col[0]

    def _get_level(self) -> int:
        """CSV列データを基にレベル番号を返す"""
        level_cell = self._header_cols[0][0]

        if "#" not in level_cell or "レベル名" not in level_cell:
            raise ValueError(f"不正なセル内容: {level_cell}")

        # "#" と "レベル名" の間の数字を抽出
        match = re.search(r"#(\d+)レベル名", level_cell)
        if not match:
            raise ValueError(f"不正なセル内容: {level_cell}")

        return int(match.group(1))

    def _get_level_name(self) -> str:
        """CSV列データを基にレベル名（列の上位階層名）を返す"""
        # TODO: CSVColType -> CSVColumn(list) クラス定義
        return self._header_cols[0][1]

    def _parse_summary_items(self) -> None:
        """総括表アイテムを生成する"""
        for i, cell in enumerate(self._col):
            header = [col[i] for col in self._header_cols]
            if _is_header_row(header):
                continue
            if _is_subtotal_row(header):
                continue
            props = SummaryProps(header)
            SummaryItem(self, cell, props)


class SummaryItem(NodeMixin):
    def __init__(self, parent: SummaryColumn, value: str, props: dict[str, str]):
        self.parent: SummaryColumn = parent
        self.value: Final = value
        self.props: Final = props

    def __repr__(self) -> str:
        return f"SummaryItem(value={self.value!r})"


class SummaryProps(dict):
    def __init__(self, header: list[str]):
        self["材質"] = header[1]
        self["形状"] = header[2]
        self["寸法"] = header[3]


def _is_header_row(row: CSVRowType) -> bool:
    """ヘッダー行の場合 `True` を返す"""
    if row[0].endswith("レベル名"):
        return True
    return False


def _is_header_col(col: CSVColType) -> bool:
    """ヘッダー列の場合 `True` を返す"""
    if col[0].endswith("レベル名"):
        return True
    if col[0] in HEADER_COL_NAMES:
        return True
    if col[0] == "合計":
        return True
    return False


def _is_subtotal_row(row: CSVRowType) -> bool:
    """小計行の場合 `True` を返す"""
    if "小計" in row:
        return True
    return False
