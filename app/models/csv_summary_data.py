from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from app.io.csv_reader import CSVReader, CSVRow
from app.models.csv_data import CSVData


class CSVSummaryData(CSVData):
    """CSV総括表データを格納するクラス"""

    def __init__(self, rows: list[CSVRow]):
        super().__init__(rows)
        self.sheets = self._parse_sheets()

    @staticmethod
    def load_from_csv(csv_path: str | Path) -> CSVSummaryData:
        """CSVファイルからインスタンスを生成する"""
        reader = CSVReader(csv_path)
        rows = reader.load()
        return CSVSummaryData(rows)

    def _parse_sheets(self) -> list[CSVData]:
        """`CSVData` をヘッダーごとに分割したシートを生成"""
        csv_sheets = self._split_sheets_by_level()
        return list(csv_sheets)

    def _split_sheets_by_level(self) -> Iterator[CSVData]:
        current_rows: list[CSVRow] = []
        for row in self.rows:
            # 新しいシートを生成
            if is_header_row(row) and current_rows:
                yield CSVData(current_rows)
                current_rows = []
            # 現在のシートに行を追加
            current_rows.append(row)

        if current_rows:
            yield CSVData(current_rows)


def is_header_row(csv_row: CSVRow) -> bool:
    """ヘッダー行の場合 `True` を返す"""
    if csv_row[0].endswith("レベル名"):
        return True
    return False
