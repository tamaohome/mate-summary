from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QFileInfo, QObject, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.config import APP_NAME, APP_VERSION
from app.models.summary_sheet import SummarySheet
from app.views.components.summary_table_widget import SummaryTableWidget
from app.views.main_window import MainWindow
from app.views.settings import WindowSettings

LEVELS = [1, 2, 3, 4]
logger = logging.getLogger(__name__)


class MainController(QObject):
    def __init__(self, main_window: MainWindow, data_dir: Path | None = None) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.window_settings = WindowSettings()

        # ウィンドウ状態を復元
        self.restore_window()

        # 初期化処理
        self._setup()

        # 状態変数を宣言
        self.summary_sheet: SummarySheet | None = None

    @property
    def filepath(self) -> QFileInfo:
        return self.main_window.fileSelector.filepath

    def set_initial_path(self, filepath: str) -> None:
        """外部から初期ファイルパスを設定する"""
        try:
            self.main_window.fileSelector.filepath = filepath
            logger.info("初期パスを設定しました: %s", filepath)
        except Exception:
            logger.exception("初期パスの適用に失敗しました: %s", filepath)

    def save_window(self) -> None:
        """ウィンドウの位置と状態を保存"""
        self.window_settings.save_window_state(self.main_window)
        logger.info("ウィンドウ状態を保存しました")

    def restore_window(self) -> None:
        """ウィンドウの位置と状態を復元"""
        self.window_settings.restore_window_state(self.main_window)
        logger.info("ウィンドウ状態を復元しました")

    @Slot(str)
    def on_path_changed(self, filepath: str) -> None:
        """`FileSelector` のパス変更ハンドラ"""
        self._update_tables()
        logger.info("選択パスが変更されました: %s", filepath)

    @Slot()
    def on_open(self) -> None:
        """ファイル選択ダイアログを開く"""
        self.main_window.fileSelector.on_open()

    @Slot()
    def on_save_as(self) -> None:
        """名前を付けてCSVファイルを保存"""
        if self.summary_sheet is None:
            logger.warning("保存するデータがありません")
            return

        # 入力されたCSVファイルのファイル名 (拡張子を除く)
        input_csv_path = self.summary_sheet.csv_path
        if input_csv_path:
            input_file_stem = input_csv_path.stem
        else:
            input_file_stem = "summary"

        # レベル名称
        level = self.summary_sheet.display_level
        level_name = f"#{level}レベル名"  # 例: #3レベル

        # 保存先のファイル名 (例: 鋼材重量総括表_#3レベル.csv)
        output_filename = f"{input_file_stem}_{level_name}.csv"

        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "CSVファイルを保存",
            output_filename,
            "CSVファイル (*.csv);;すべてのファイル (*.*)",
        )
        if file_path:
            try:
                # 元のCSVデータを保存
                from app.io.csv_handler import write_csv

                write_csv(self.summary_sheet.csv_data, Path(file_path))
                logger.info("ファイルを保存しました: %s", file_path)
            except Exception:
                logger.exception("ファイル保存に失敗しました: %s", file_path)

    @Slot()
    def on_exit(self) -> None:
        """アプリケーションを終了"""
        self.save_window()
        self.main_window.close()

    @Slot()
    def on_show_version(self) -> None:
        """バージョン情報ダイアログを表示"""
        message = f"{APP_NAME}\nバージョン {APP_VERSION}"
        QMessageBox.information(self.main_window, "バージョン情報", message)

    def _setup(self) -> None:
        """シグナル接続と初期化処理を行う"""
        # シグナル接続
        self.main_window.fileSelector.pathChanged.connect(self.on_path_changed)

        # メニューアクション接続
        self.main_window.actionOpen.triggered.connect(self.on_open)
        self.main_window.actionSaveAs.triggered.connect(self.on_save_as)
        self.main_window.actionExit.triggered.connect(self.on_exit)
        self.main_window.actionShowVersion.triggered.connect(self.on_show_version)

        # ボタンアクション接続
        self.main_window.saveButton.clicked.connect(self.on_save_as)

        # ウィンドウ終了イベントにウィンドウ状態保存をフック
        self.main_window.closeEvent = self._handle_close_event

        # テーブルを全て初期化
        self._init_tables()

    def _handle_close_event(self, event: QCloseEvent) -> None:
        """ウィンドウ終了イベント"""
        self.save_window()
        event.accept()

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

    def _update_tables(self) -> None:
        """テーブルを全て更新する"""
        csv_filepath = Path(self.filepath.absoluteFilePath())
        self.summary_sheet = SummarySheet.load_from_csv(csv_filepath)

        # レベル毎にシートをセット
        for level in LEVELS:
            self.summary_sheet.display_level = level
            csv_data = self.summary_sheet.csv_data
            table_widget = self._get_table_widget(level)
            table_widget.populate(csv_data)
