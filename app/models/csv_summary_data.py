from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from app.io.csv_reader import CSVReader, CSVRowType
from app.models.csv_data import CSVData


class CSVSummaryData(CSVData):
    """CSV総括表データを格納するクラス"""

    def __init__(self, rows: list[CSVRowType]):
        super().__init__(rows)
        self.sheets = self._parse_sheets()

    @staticmethod
    def load_from_csv(csv_path: str | Path) -> CSVSummaryData:
        """CSVファイルからインスタンスを生成する"""
        reader = CSVReader(csv_path)
        rows = reader.load()
        return CSVSummaryData(rows)

    def _parse_sheets(self) -> list[list[CSVRowType]]:
        """`CSVData` をヘッダーごとに分割したシートを生成"""
        csv_sheets = self._split_sheets_by_level()
        return list(csv_sheets)

    def _split_sheets_by_level(self) -> Iterator[list[CSVRowType]]:
        current_sheet: list[CSVRowType] = []
        for row in self.rows:
            # 新しいシートを生成
            if is_header_row(row) and current_sheet:
                yield current_sheet
                current_sheet = []
            # 現在のシートに行を追加
            current_sheet.append(row)

        if current_sheet:
            yield current_sheet


def is_header_row(csv_row: CSVRowType) -> bool:
    """ヘッダー行の場合 `True` を返す"""
    if csv_row[0].endswith("レベル名"):
        return True
    return False
