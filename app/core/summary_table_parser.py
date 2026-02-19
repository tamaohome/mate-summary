from pathlib import Path

from app.core.csv_data_parser import CSVDataParser
from app.io.csv_handler import read_csv
from app.models.csv_data import CSVData
from app.models.summary_table import SummaryColumn, SummaryItem, SummaryTable


class SummaryTableParser:
    """CSVファイルから `SummaryTable` をパースするクラス"""

    def __init__(self, csv_path: Path):
        csv_data = read_csv(csv_path)
        self._csv_data_parser = CSVDataParser(csv_data)
        self._csv_tables = self._csv_data_parser.csv_tables

    def parse(self) -> dict[int, SummaryTable]:
        """
        CSVデータをパースして辞書形式で返す

        辞書のキーにレベル番号として `1~5` を指定すると、レベル毎の `SummaryTable` が取得される
        """
        # #1レベル〜#5レベルのテーブルを格納する辞書を用意
        table_dict: dict[int, SummaryTable] = {}

        for csv_table in self._csv_tables:
            name = self._parse_name(csv_table)
            level = self._parse_level(csv_table)
            new_table = SummaryTable(name=name, level=level)
            self._parse_columns(csv_table, new_table)

            if table := table_dict.get(level):
                table += new_table
            else:
                table_dict[level] = new_table

        return table_dict

    def _parse_name(self, csv_data: CSVData) -> str:
        name_cell = csv_data[0][0]
        return name_cell

    def _parse_level(self, csv_data: CSVData) -> int:
        level_name_cell = csv_data[0][0]
        return int(level_name_cell[1])

    def _parse_columns(self, csv_data: CSVData, parent: SummaryTable) -> None:
        for col in csv_data.cols:
            self._parse_column(col, parent)

    def _parse_column(self, csv_col: list[str], parent: SummaryTable) -> None:
        # ヘッダー列の場合
        if self._is_header_col(csv_col):
            header_name = csv_col[0]
            parent.header_cols[header_name] = csv_col[1:]
            return

        # 列が空の場合
        if self._is_empty_col(csv_col):
            return

        name = self._parse_column_name(csv_col)
        parent_name = self._parse_column_parent_name(parent)
        column = SummaryColumn(parent=parent, name=name, parent_name=parent_name)
        self._parse_items(csv_col, column)

    def _is_header_row(self, csv_row: list[str]) -> bool:
        return csv_row[0].endswith("レベル名")

    def _is_header_col(self, csv_col: list[str]) -> bool:
        header_name = csv_col[0]
        if header_name.endswith("レベル名"):
            return True
        if header_name in ["材質", "形状", "寸法", "合計"]:
            return True
        return False

    def _is_empty_col(self, csv_col: list[str]) -> bool:
        return all(cell == "" for cell in csv_col)

    def _parse_column_name(self, csv_col: list[str]) -> str:
        return csv_col[0]

    def _parse_column_parent_name(self, parent: SummaryTable) -> str:
        parent_name_col = next(v for k, v in parent.header_cols.items() if k.endswith("レベル名"))
        return parent_name_col[0]

    def _parse_items(self, csv_col: list[str], parent: SummaryColumn) -> None:
        cells = csv_col[1:]
        for i, cell in enumerate(cells):
            props = self._parse_item_props(parent, i)
            SummaryItem(parent=parent, value=cell, props=props)

    def _parse_item_props(self, col: SummaryColumn, index: int) -> dict[str, str]:
        return {
            "材質": col.parent.header_cols["材質"][index],
            "形状": col.parent.header_cols["形状"][index],
            "寸法": col.parent.header_cols["寸法"][index],
        }
