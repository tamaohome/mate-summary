from __future__ import annotations

from pathlib import Path

from app.io.csv_reader import CSVReader, CSVRowType
from app.models.csv_data import CSVData


class CSVSummaryData(CSVData):
    """CSV総括表データを格納するクラス"""

    def __init__(self, rows: list[CSVRowType]):
        super().__init__(rows)
        self.tables = self._parse_tables()

    @staticmethod
    def load_from_csv_file(csv_path: str | Path) -> CSVSummaryData:
        """CSVファイルからインスタンスを生成する"""
        reader = CSVReader(csv_path)
        rows = reader.load()
        return CSVSummaryData(rows)

    def _parse_tables(self) -> dict[int, list[CSVRowType]]:
        tables: dict[int, list[CSVRowType]] = {}
        return tables
