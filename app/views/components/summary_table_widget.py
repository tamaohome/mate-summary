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
