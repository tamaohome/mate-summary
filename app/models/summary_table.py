from __future__ import annotations

from collections.abc import Iterator
from typing import Final

from anytree import NodeMixin, RenderTree

from app.models.csv_data import CSVData


class SummaryTable(NodeMixin):
    """総括表クラス"""

    def __init__(self, name: str, level: int):
        self.name: Final = name
        self.level: Final = level
        self.header_cols: Final[dict[str, list[str]]] = {}

    # def __add__(self, other_table: "SummaryTable") -> "SummaryTable":
    #     if not isinstance(other_table, SummaryTable):
    #         return NotImplemented
    #     for col in other_table:
    #     return self

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
        rows: list[list[str]] = []

        # ヘッダー行を構築
        # header_colsの各エントリを行に変換
        for header_name, header_values in self.header_cols.items():
            rows.append([header_name] + header_values)

        # データ行を構築
        # 各SummaryColumnとその配下のSummaryItemを処理
        for col in self.cols:
            row = [col.name]
            for item in col.items:
                row.append(item.value)
            rows.append(row)

        # ステップ3: CSVDataオブジェクトを生成して返す
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


"""
SummaryTable
    parent = None
    name = "横桁"
    level = "#4"
    depth = 4
    columns: list[SummaryColumn]
    total_column: TotalColumn
    total_column.value = 960

SummaryColumn
    parent: SummaryTable
    parent.name = "横桁"
    parent.level = "#4"
    name = "端支点横桁"
    level = "#5"
    depth = 5
    items: list[SummaryItem]
    value: int = 642

TotalColumn extends SummaryColumn

SummaryItem
    parent: SummaryColumn
    parent.name = "端支点横桁"
    parent.level = "#5"
    parent.depth = 5
    parent.parent.name = "横桁"
    parent.parent.level = "#4"
    parent.parent.depth = 4
    props: dict[str, str] = {
        "材質": "SMA490BW",
        "形状": "PL",
        "寸法": " 19.0"
    }
    value: int = 166

#1レベル名,材質,形状,寸法,"合計","上部構造"
"サンプル橋","SMA490BW","PL"," 19.0",166,166
"サンプル橋",小計,,,166,166

SummaryCell
value: "166"
row_header: "上部構造"
col_headers: [
    "#1レベル名": "サンプル橋",
    "材質": "SMA490BW",
    "形状": "PL",
    "寸法": " 19.0"
]
"""

# class ColumnLevel:
#     """`SummaryColumn` の階層情報を保持するクラス"""

#     def __init__(self, level_depth_name: str, name: str):
#         self._validate_level_type(level_depth_name)
#         self._level_type_name = level_depth_name
#         self._name = name

#     def _validate_level_type(self, level_depth_name: str) -> None:
#         if level_depth_name not in LEVEL_LABELS:
#             raise ValueError(f"Invalid level type: {level_depth_name}")

#     @property
#     def depth(self) -> int:
#         return LEVEL_LABELS.index(self._level_type_name) + 1

#     @property
#     def name(self) -> str:
#         return self._name


# @dataclass
# class SummaryColumn:
#     table: "SummaryTable"
#     row_header: str
#     values: list[str]
#     hidden: bool = False
#     parent_level = ColumnLevel.get_level()
#     parent_level = ColumnLevel.get_parent_level(header)

#     @property
#     def is_header(self) -> bool:
#         """ヘッダー列の場合は `True` を返す"""
#         return self.row_header in [*LEVEL_LABELS, *COL_HEADER_LABELS]


# class SummaryTable:
#     def __init__(self, cols: list[SummaryColumn]):
#         self._cols: list[SummaryColumn] = [col for col in cols if not col.is_header]

#     def __getitem__(self, index: int) -> SummaryColumn:
#         return self._cols[index]

#     def __setitem__(self, index: int, value: SummaryColumn) -> None:
#         self._cols[index] = value

#     def __delitem__(self, index: int) -> None:
#         del self._cols[index]

#     def __len__(self) -> int:
#         return len(self._cols)

#     def insert(self, index: int, value: SummaryColumn) -> None:
#         self._cols.insert(index, value)

#     @property
#     def cols(self) -> list["SummaryColumn"]:
#         return self._cols
