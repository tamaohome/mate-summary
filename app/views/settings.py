from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QSettings, QSize
from PySide6.QtWidgets import QMainWindow

INI_FILENAME = "matecon.ini"
DEFAULT_WINDOW_SIZE = QSize(680, 420)


class WindowSettings(QSettings):
    """ウィンドウ設定クラス"""

    def __init__(self, filename=INI_FILENAME):
        # 実行環境に合わせて保存パスを決定
        if getattr(sys, "frozen", False):
            app_dir = Path(sys.executable).parent
        else:
            app_dir = Path(__file__).parents[1].resolve()

        settings_path = str(app_dir / filename)

        # 親クラス QSettings の初期化（INI形式を指定）
        super().__init__(settings_path, QSettings.Format.IniFormat)

    def save_window_state(self, window: QMainWindow) -> None:
        """ウィンドウの配置と状態を保存する"""
        self.setValue("window/geometry", window.saveGeometry())
        self.setValue("window/window_state", window.saveState())

        self.sync()  # INIファイルに保存

    def restore_window_state(self, window: QMainWindow) -> None:
        """ウィンドウの配置と状態を復元する"""
        geometry = self.value("window/geometry")
        if geometry:
            window.restoreGeometry(geometry)
        else:
            # デフォルトサイズを使用
            window.resize(DEFAULT_WINDOW_SIZE)

        window_state = self.value("window/window_state")
        if window_state:
            window.restoreState(window_state)
