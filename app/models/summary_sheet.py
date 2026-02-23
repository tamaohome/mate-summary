from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path
from typing import Final, overload, override

from anytree import NodeMixin

from app.io.csv_reader import CSVColumn, CSVRow
from app.models.csv_summary_data import CSVSummaryData

HEADER_COL_NAMES = ["材質", "形状", "寸法"]


class SummarySheet(NodeMixin):
    """総括表クラス"""

    def __init__(self, csv_summary_data: CSVSummaryData):
        self._csv_summary_data: Final = csv_summary_data
        self._csv_sheets = self._csv_summary_data.sheets

        # 総括表列データをレベル毎に格納する
        # 格納処理は SummaryColumn のコンストラクタで行う
        self.cols_by_level: defaultdict[int, list[SummaryColumn]]
        self.cols_by_level: Final = defaultdict(list)

        self._parse_summary_columns()
        self.total_col: Final = self._parse_total_column()

    def __iter__(self) -> Iterator[SummaryColumn]:
        return iter(self.children)

    @overload
    def __getitem__(self, key: int) -> SummaryColumn: ...
    @overload
    def __getitem__(self, key: slice) -> tuple[SummaryColumn, ...]: ...
    def __getitem__(self, key: int | slice):
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
    @override
    def descendants(self) -> tuple[SummaryColumn, ...]:
        return super().descendants

    @property
    def cols(self) -> tuple[SummaryColumn, ...]:
        """総括表列"""
        return self.descendants

    @property
    def columns(self) -> tuple[SummaryColumn, ...]:
        """総括表列"""
        return self.cols

    @property
    def props_group(self) -> tuple[SummaryProps, ...]:
        """
        材片種別一覧

        最上位レベルの `SummaryColumn` から取得する
        """
        return self.children[0].props_group

    @property
    def header_rows(self) -> list[CSVRow]:
        """総括表の行ヘッダーリスト"""
        csv_rows: list[CSVRow] = []
        # 各行を追加
        for props in self.props_group:
            # 初回はヘッダー行を追加
            if not csv_rows:
                header_row = props.csv_header_row
                csv_rows.append(header_row)
            props_row = props.csv_row
            csv_rows.append(props_row)
        return csv_rows

    # def to_csvdata(self) -> CSVData:
    #     """`SummaryTable` を `CSVData` 形式に変換して返す"""
    #     cols: list[CSVColumn] = []

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
    #     rows: list[CSVRow] = []
    #     for row in zip(*cols, strict=False):
    #         rows.append(row)

    #     # CSVDataオブジェクトを生成して返す
    #     return CSVData(rows)

    def _parse_summary_columns(self) -> None:
        """総括表列を生成する"""
        # 分割したCSV総括表シートをループ
        for sheet in self._csv_sheets:
            header_cols: list[CSVColumn] = []
            # CSV総括表の列をループ
            for col in sheet.cols:
                # ヘッダー列の場合はヘッダー列リストに追加してスキップ
                if _is_header_col(col):
                    header_cols.append(col)
                    continue
                # 総括表列インスタンスを生成
                SummaryColumn(self, col, header_cols)

    def _parse_total_column(self) -> SummaryTotalColumn:
        """総括表合計列を生成する"""
        # 最上位レベルのCSVシートを取得
        sheet = self._csv_sheets[0]
        # CSVデータの "合計" 列を取得
        total_col = sheet.cols[4]
        return SummaryTotalColumn(total_col)


class SummaryColumn(NodeMixin):
    """総括表列クラス"""

    def __init__(self, summary_sheet: SummarySheet, col: CSVColumn, header_cols: list[CSVColumn]):
        self.summary_sheet: Final = summary_sheet
        self._col = col
        self._header_cols = header_cols
        self.name: Final = self._get_name()
        self.level: Final = self._get_level()
        self.level_name: Final = self._get_level_name()
        self.items: Final = self._parse_summary_items()

        # 親階層の更新
        self.parent: Final = self._get_parent()

        # レベル毎の辞書に自ノードを追加
        self.summary_sheet.cols_by_level[self.level].append(self)

    def __getitem__(self, index):
        return self.children[index]

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        items_count = len(self.items)
        return f"SummaryColumn(name={self.name!r}, level_name={self.level_name!r}, items={items_count})"

    @property
    def children(self) -> tuple[SummaryColumn, ...]:
        return super().children

    @property
    def props_group(self) -> tuple[SummaryProps, ...]:
        """材片種別一覧"""
        return tuple(item.props for item in self.items)

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
        return self._header_cols[0][1]

    def _parse_summary_items(self) -> tuple[SummaryItem, ...]:
        """総括表アイテムを生成する"""
        items: list[SummaryItem] = []
        for i, cell in enumerate(self._col):
            header = CSVRow(col[i] for col in self._header_cols)
            if _is_header_row(header):
                continue
            if _is_subtotal_row(header):
                continue
            props = SummaryProps(header)
            item = SummaryItem(self, cell, props)
            items.append(item)
        return tuple(items)

    def _get_parent(self) -> SummaryColumn | SummarySheet:
        """レベル名と一致するノードを走査し、親階層を返す"""
        # 自ノードのレベルが1の場合、ルート階層
        if self.level == 1:
            return self.summary_sheet

        # 親ノードの候補一覧を取得
        parent_level = self.level - 1
        parent_nodes = self.summary_sheet.cols_by_level[parent_level]
        for parent_node in parent_nodes:
            if self.level_name == parent_node.name:
                return parent_node

        # 親階層が存在しない場合エラー
        raise ValueError(f"親階層が存在しません: {self.level_name} | {self.name}")


class SummaryTotalColumn:
    """総括表合計列クラス"""

    def __init__(self, col: CSVColumn):
        self.col: Final = col
        self.name: Final = self.col[0]
        self.data: Final = self.col[1:]


class SummaryItem:
    """総括表アイテムクラス"""

    def __init__(self, parent: SummaryColumn, value: str, props: SummaryProps):
        self.parent: Final = parent
        self.value: Final = value
        self.props: Final = props

    def __repr__(self) -> str:
        return f"SummaryItem(value={self.value!r})"


class SummaryProps(dict):
    """総括表アイテムプロパティクラス"""

    def __init__(self, props: list[str]):
        self["材質"] = props[1]
        self["形状"] = props[2]
        self["寸法"] = props[3]

    def __eq__(self, other: object) -> bool:
        """材質、形状、寸法が全て同じなら同値と判定"""
        if not isinstance(other, SummaryProps):
            return False
        return self["材質"] == other["材質"] and self["形状"] == other["形状"] and self["寸法"] == other["寸法"]

    @property
    def csv_row(self) -> CSVRow:
        """材片種別をCSV行データとして返す"""
        row = list(self.values())
        return CSVRow(row)

    @property
    def csv_header_row(self) -> CSVRow:
        """材片種別ヘッダーをCSV行データとして返す"""
        header_row = list(self.keys())
        return CSVRow(header_row)


def _is_header_row(row: CSVRow) -> bool:
    """ヘッダー行の場合 `True` を返す"""
    if row[0].endswith("レベル名"):
        return True
    return False


def _is_header_col(col: CSVColumn) -> bool:
    """ヘッダー列の場合 `True` を返す"""
    if col[0].endswith("レベル名"):
        return True
    if col[0] in HEADER_COL_NAMES:
        return True
    if col[0] == "合計":
        return True
    return False


def _is_subtotal_row(row: CSVRow) -> bool:
    """小計行の場合 `True` を返す"""
    if "小計" in row:
        return True
    return False
