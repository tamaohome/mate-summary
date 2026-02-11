from PySide6.QtWidgets import QMainWindow

from app.ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QMainWindow | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
