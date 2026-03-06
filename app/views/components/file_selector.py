from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFileDialog, QWidget

from app.ui.ui_file_selector import Ui_FileSelector


class FileSelector(QWidget, Ui_FileSelector):
    """ファイルパス選択ウィジェット"""

    pathChanged = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self._initial_dir = ""

        # シグナル接続
        self.browsePushButton.clicked.connect(self.on_open)
        self.pathLineEdit.textChanged.connect(lambda text: self.pathChanged.emit(text))

    def set_initial_dir(self, initial_dir: str) -> None:
        """ファイル選択ダイアログの初期ディレクトリを設定する"""
        self._initial_dir = initial_dir

    @Slot()
    def on_open(self) -> None:
        """ファイル選択ダイアログを開く"""
        fp, _ = QFileDialog.getOpenFileName(self, "CSVファイルを選択", self._initial_dir, "CSV Files (*.csv)")
        if fp:
            self.filepath = fp

    @property
    def filepath(self) -> Path:
        """選択中のパスを返す"""
        return Path(self.pathLineEdit.text())

    @filepath.setter
    def filepath(self, value: Path | str) -> None:
        """パスを設定し、外部へシグナルを通知する"""
        path_str = str(value)
        # 変更がない場合はシグナルを発行しない
        if self.pathLineEdit.text() == path_str:
            return
        self.pathLineEdit.setText(path_str)
