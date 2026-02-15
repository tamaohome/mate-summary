from __future__ import annotations

from collections.abc import Iterator
from typing import Final

from anytree import NodeMixin, RenderTree

from app.models.csv_data import CSVData, CSVDataType


class SummaryTable(NodeMixin):
    """総括表クラス"""

    def __init__(self, name: str, level: int):
        self.name: Final = name
        self.level: Final = level
        self.header_cols: Final[dict[str, list[str]]] = {}

    def __iadd__(self, other_table) -> SummaryTable:
        if not isinstance(other_table, SummaryTable):
            return NotImplemented
        for col in other_table:
            col.parent = self
        return self

    def __iter__(self) -> Iterator[SummaryColumn]:
        return iter(self.children)

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
        return self.children

    def to_csvdata(self) -> CSVData:
        """`SummaryTable` を `CSVData` 形式に変換して返す"""
        cols: CSVDataType = []

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
        rows = [list(row) for row in zip(*cols, strict=False)]

        # CSVDataオブジェクトを生成して返す
        return CSVData(rows)


class SummaryColumn(NodeMixin):
    """総括表の列クラス"""

    def __init__(self, parent: SummaryTable, name: str, parent_name: str):
        self.parent: SummaryTable = parent
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
