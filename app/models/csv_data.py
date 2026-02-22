from __future__ import annotations

from collections.abc import Sequence
from itertools import zip_longest
from pathlib import Path
from typing import Final

from app.io.csv_reader import CSVColumn, CSVReader, CSVRow


class CSVData(Sequence[CSVRow]):
    """CSVデータを格納するクラス"""

    def __init__(self, rows: list[CSVRow]):
        self.cols: Final = self._rows_to_cols(rows)
        self.rows: Final = self._cols_to_rows(self.cols)

    def __getitem__(self, index):
        return self.rows[index]

    def __len__(self) -> int:
        return len(self.rows)

    @staticmethod
    def load_from_csv(csv_path: str | Path) -> CSVData:
        """CSVファイルからインスタンスを生成する"""
        reader = CSVReader(csv_path)
        rows = reader.load()
        return CSVData(rows)

    def _rows_to_cols(self, rows: list[CSVRow]) -> list[CSVColumn]:
        cols: list[CSVColumn] = []
        for col in zip_longest(*rows, fillvalue=""):
            if not any(col):
                continue
            csv_col = CSVColumn(col)
            cols.append(csv_col)
        return cols

    def _cols_to_rows(self, cols: list[CSVColumn]) -> list[CSVRow]:
        rows = [CSVRow(row) for row in zip(*cols, strict=False)]
        return rows

    @property
    def header(self) -> CSVRow:
        """CSVデータのヘッダー"""
        if not self.rows:
            return CSVRow()
        return self.rows[0]

    @property
    def data(self) -> list[CSVRow]:
        """CSVデータの内容 (ヘッダーを除く)"""
        if not self.rows:
            return []
        return self.rows[1:]
