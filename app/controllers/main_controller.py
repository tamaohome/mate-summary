from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QFileInfo, QObject, Slot
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from app.core.summary_table_parser import SummaryTableParser
from app.models.csv_data import CSVData
from app.models.summary_table import SummaryTable
from app.views.main_window import MainWindow

LEVELS = [1, 2, 3, 4, 5]
logger = logging.getLogger(__name__)


class MainController(QObject):
    def __init__(self, main_window: MainWindow, data_dir: Path | None = None) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup()

        # 状態変数
        self.summary_table: SummaryTable | None = None

    def _setup(self) -> None:
        """シグナル接続と初期化処理を行う"""
        # シグナル接続
        self.main_window.fileSelector.pathChanged.connect(self.on_path_changed)

        # テーブルを全て初期化
        self._init_tables()

    def _init_tables(self) -> None:
        """テーブルを全て初期化"""
        for level in LEVELS:
            self._init_table_widget(level)

    def _get_table_widget(self, level: int) -> QTableWidget:
        """レベル番号に対応する `QTableWidget` を返す"""
        mapping = {
            1: self.main_window.level1TableWidget,
            2: self.main_window.level2TableWidget,
            3: self.main_window.level3TableWidget,
            4: self.main_window.level4TableWidget,
            5: self.main_window.level5TableWidget,
        }
        widget = mapping.get(level)
        if widget:
            return widget

        raise RuntimeError(f"レベル{level} のテーブルが見つかりません。")

    def _init_table_widget(self, level: int) -> None:
        """テーブルを初期化"""
        table = self._get_table_widget(level)
        table.setColumnCount(5)
        header = [f"#{level}レベル名", "材質", "形状", "寸法", "合計"]
        table.setHorizontalHeaderLabels(header)
        table.setRowCount(0)

    @Slot(str)
    def on_path_changed(self, filepath: str) -> None:
        """`FileSelector` のパス変更ハンドラ"""
        self._update_tables()
        logger.info("選択パスが変更されました: %s", filepath)

    def _update_tables(self) -> None:
        """テーブルを全て更新する"""
        csv_filepath = Path(self.filepath.absoluteFilePath())
        summary_table_parser = SummaryTableParser(csv_filepath)
        summary_tables = summary_table_parser.parse()

        for index, summary_table in summary_tables.items():
            self._populate_table(index, summary_table.to_csvdata())

    def _populate_table(self, level: int, csv_data: CSVData) -> None:
        """指定されたレベルのテーブルにデータをセットする"""
        table = self._get_table_widget(level)
        # Sequence なので長さを事前に設定して直接書き込む
        table.setRowCount(len(csv_data))
        for r, row in enumerate(csv_data):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table.setItem(r, c, item)

    @property
    def filepath(self) -> QFileInfo:
        return self.main_window.fileSelector.filepath
