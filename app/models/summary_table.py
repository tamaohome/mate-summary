from __future__ import annotations

from collections.abc import Iterator
from typing import Final, overload

from anytree import NodeMixin, RenderTree

from app.io.csv_reader import CSVRowType
from app.models.csv_data import CSVColType, CSVData

HEADER_COL_NAMES = ["材質", "形状", "寸法"]


class SummarySheet(NodeMixin):
    """総括表クラス"""

    def __init__(self, name: str, level: int):
        self.name: Final = name
        self.level: Final = level

    def __iadd__(self, other_table) -> SummarySheet:
        if not isinstance(other_table, SummarySheet):
            return NotImplemented
        for col in other_table:
            col.parent = self
        return self

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
        if not self.cols:
            return f"SummaryTable(name={self.name!r}, level={self.level}, cols=[])"

        lines = [f"SummaryTable(name={self.name!r}, level={self.level})"]
        # RenderTree で SummaryColumn 一覧を表示
        for pre, _, node in RenderTree(self, maxlevel=2):
            if node is self:
                continue  # ルートノード（SummaryTable自身）はスキップ
            if isinstance(node, SummaryColumn):
                lines.append(f"{pre}{repr(node)}")
        return "\n".join(lines)

    @property
    def children(self) -> tuple[SummaryColumn]:
        return super().children

    @property
    def cols(self) -> tuple[SummaryColumn]:
        """総括表列"""
        return self.children

    @property
    def header_cols(self) -> dict[str, list[str]]:
        """総括表ヘッダー列"""
        result: dict[str, list[str]] = {}
        for header_name in HEADER_COL_NAMES:
            result[header_name] = [col[header_name] for col in self.cols]
        return result

    def to_csvdata(self) -> CSVData:
        """`SummaryTable` を `CSVData` 形式に変換して返す"""
        cols: list[CSVColType] = []

        # ヘッダー列を構築
        # header_colsの各エントリを列に変換
        for header_name, header_values in self.header_cols.items():
            cols.append([header_name] + header_values)

        # データ列を構築
        # 各SummaryColumnとその配下のSummaryItemを処理
        for col in self.cols:
            row = [col.name]
            for item in col.items:
                row.append(item.value)
            cols.append(row)

        # 行列変換
        rows: list[CSVRowType] = []
        for row in zip(*cols, strict=False):
            rows.append(row)

        # CSVDataオブジェクトを生成して返す
        return CSVData(rows)


class SummaryColumn(NodeMixin):
    """総括表の列クラス"""

    def __init__(self, parent: SummarySheet, name: str, parent_name: str):
        self.parent: SummarySheet = parent
        self.name: Final = name
        self.parent_name: Final = parent_name

    def __getitem__(self, index):
        return self.children[index]

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        items_count = len(self.items)
        return f"SummaryColumn(name={self.name!r}, parent_name={self.parent_name!r}, items={items_count})"

    @property
    def children(self) -> tuple[SummaryItem]:
        return super().children

    @property
    def items(self) -> tuple[SummaryItem]:
        return self.children


class SummaryItem(NodeMixin):
    def __init__(self, parent: SummaryColumn, value: str, props: dict[str, str]):
        self.parent: SummaryColumn = parent
        self.value: Final = value
        self.props: Final = props

    def __repr__(self) -> str:
        return f"SummaryItem(value={self.value!r})"
