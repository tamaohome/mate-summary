from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget

from app.models.csv_data import CSVData


class SummaryTableWidget(QTableWidget):
    """総括表を表示するテーブルウィジェット"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def populate(self, csv_data: CSVData) -> None:
        """CSVデータをテーブルに設定する"""
        self.setColumnCount(len(csv_data.header))
        self.setHorizontalHeaderLabels(csv_data.header)
        self.setRowCount(len(csv_data))
        for r, row in enumerate(csv_data.data):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                # 4列目以降（インデックス3以上）は右揃えにする
                if c >= 3:
                    alignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    item.setTextAlignment(alignment)
                self.setItem(r, c, item)

        # 列幅の設定
        self._configure_column_widths([100, 50, 120], 60)

        # 行の高さを設定
        self._configure_row_heights(22)

    def _configure_column_widths(self, widths: list[int], default_width: int | None = None) -> None:
        """列幅を設定する"""
        # 指定された列幅を個別に設定
        for col_index, width in enumerate(widths):
            if col_index < self.columnCount():
                self.setColumnWidth(col_index, width)

        # デフォルト列幅を一括設定
        if not default_width:
            return
        for col_index in range(len(widths), self.columnCount()):
            self.setColumnWidth(col_index, default_width)

    def _configure_row_heights(self, height: int) -> None:
        """行の高さを設定する"""
        for row_index in range(self.rowCount()):
            self.setRowHeight(row_index, height)
