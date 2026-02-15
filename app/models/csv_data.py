from collections.abc import Sequence
from itertools import zip_longest
from typing import Final

type CSVDataType = list[CSVRowType]
type CSVRowType = list[str]


class CSVData(Sequence[CSVRowType]):
    """CSVデータを格納するクラス"""

    def __init__(self, rows: CSVDataType):
        self.cols: Final = self._rows_to_cols(rows)
        self.rows: Final = self._cols_to_rows(self.cols)

    def __getitem__(self, index):
        return self.rows[index]

    def __len__(self) -> int:
        return len(self.rows)

    def _rows_to_cols(self, rows: CSVDataType) -> CSVDataType:
        cols: CSVDataType = [list(col) for col in zip_longest(*rows, fillvalue="")]
        return cols

    def _cols_to_rows(self, cols: CSVDataType) -> CSVDataType:
        rows: CSVDataType = [list(row) for row in zip(*cols, strict=False)]
        return rows

    @property
    def header(self) -> CSVRowType:
        return self.rows[0]
