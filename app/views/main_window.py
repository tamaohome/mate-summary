from PySide6.QtWidgets import QMainWindow

from app.config import APP_NAME_JP, APP_VERSION
from app.ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QMainWindow | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(f"{APP_NAME_JP} - v{APP_VERSION}")
