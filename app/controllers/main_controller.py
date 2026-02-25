from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QFileInfo, QObject, Slot

from app.models.summary_sheet import SummarySheet
from app.views.components.summary_table_widget import SummaryTableWidget
from app.views.main_window import MainWindow

LEVELS = [1, 2, 3, 4]
logger = logging.getLogger(__name__)


class MainController(QObject):
    def __init__(self, main_window: MainWindow, data_dir: Path | None = None) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup()

        # 状態変数
        self.summary_sheet: SummarySheet | None = None

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

    def _get_table_widget(self, level: int) -> SummaryTableWidget:
        """レベル番号に対応するテーブルウィジェットを返す"""
        mapping = {
            1: self.main_window.level1TableWidget,
            2: self.main_window.level2TableWidget,
            3: self.main_window.level3TableWidget,
            4: self.main_window.level4TableWidget,
        }
        widget = mapping.get(level)
        if isinstance(widget, SummaryTableWidget):
            return widget

        raise RuntimeError(f"レベル{level} のテーブルが見つかりません。")

    def _init_table_widget(self, level: int) -> None:
        """テーブルを初期化"""
        table = self._get_table_widget(level)
        table.setRowCount(0)

    @Slot(str)
    def on_path_changed(self, filepath: str) -> None:
        """`FileSelector` のパス変更ハンドラ"""
        self._update_tables()
        logger.info("選択パスが変更されました: %s", filepath)

    def _update_tables(self) -> None:
        """テーブルを全て更新する"""
        csv_filepath = Path(self.filepath.absoluteFilePath())
        summary_sheet = SummarySheet.load_from_csv(csv_filepath)

        # レベル毎にシートをセット
        for level in LEVELS:
            summary_sheet.display_level = level
            csv_data = summary_sheet.csv_data
            table_widget = self._get_table_widget(level)
            table_widget.populate(csv_data)

    def set_initial_path(self, filepath: str) -> None:
        """外部から初期ファイルパスを設定する"""
        try:
            self.main_window.fileSelector.filepath = filepath
            logger.info("初期パスを設定しました: %s", filepath)
        except Exception:
            logger.exception("初期パスの適用に失敗しました: %s", filepath)

    @property
    def filepath(self) -> QFileInfo:
        return self.main_window.fileSelector.filepath
