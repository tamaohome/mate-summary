from PySide6.QtCore import QFileInfo, Signal
from PySide6.QtWidgets import QFileDialog, QWidget

from app.ui.ui_file_selector import Ui_FileSelector


class FileSelector(QWidget, Ui_FileSelector):
    """ファイルパス選択ウィジェット"""

    pathChanged = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # シグナル接続
        self.browsePushButton.clicked.connect(self._on_browse_clicked)
        self.pathLineEdit.textChanged.connect(lambda text: self.pathChanged.emit(text))

    def _on_browse_clicked(self) -> None:
        """ファイル選択ダイアログを表示し、結果を反映させる"""
        fp, _ = QFileDialog.getOpenFileName(self, "ファイルを選択", "", "CSV Files (*.csv)")
        if fp:
            self.filepath = fp

    @property
    def filepath(self) -> QFileInfo:
        """選択中のパスを返す"""
        return QFileInfo(self.pathLineEdit.text())

    @filepath.setter
    def filepath(self, value: QFileInfo | str) -> None:
        """パスを設定し、外部へシグナルを通知する"""
        fi = value if isinstance(value, QFileInfo) else QFileInfo(value)
        filepath = fi.filePath()
        # 変更がない場合はシグナルを発行しない
        if self.pathLineEdit.text() == filepath:
            return
        self.pathLineEdit.setText(filepath)
