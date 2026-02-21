import csv
from pathlib import Path
from typing import override

from app.io import ENCODING
from app.io.file_reader import BaseFileReader

type CSVRowType = list[str]
type CSVColType = list[str]


class CSVReader(BaseFileReader):
    """CSVファイルを2次元リストに読み込むクラス"""

    def __init__(self, csv_path: str | Path):
        super().__init__(csv_path)

    def load(self) -> list[CSVRowType]:
        """CSVファイルを読み込んで検証する"""
        csv_data: list[CSVRowType] = []
        with self.csv_path.open("r", encoding=ENCODING) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                csv_data.append(self._strip_cells(row))

        self._validate_csv_data(csv_data)
        return csv_data

    def _validate_csv_data(self, csv_data: list[CSVRowType]) -> None:
        """読み込んだCSVデータを検証"""
        if not csv_data:
            raise ValueError("CSVファイルが空です")

    def _strip_cells(self, row: CSVRowType) -> CSVRowType:
        """各セルの前後の空白を削除して返す"""
        return [cell.strip() for cell in row]

    @property
    @override
    def supported_extensions(self) -> list[str]:
        return [".csv"]

    @property
    def csv_path(self) -> Path:
        """CSVファイルパス"""
        return self.file_path
