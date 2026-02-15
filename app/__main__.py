from __future__ import annotations

import logging
import sys
from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

from app.controllers.main_controller import MainController
from app.views.main_window import MainWindow

logger = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO)

    argv = list(argv) if argv is not None else sys.argv[1:]

    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        _controller = MainController(window)
        window.show()

        # コマンドライン引数が存在する場合、ファイルパスとして読み込む
        if argv:
            try:
                window.fileSelector.filepath = argv[0]
            except Exception:
                logger.exception("コマンドライン引数で渡されたパスの設定に失敗しました: %s", argv[0])
        window.show()

        return app.exec()
    except Exception as exc:
        logger.exception("アプリケーションの起動に失敗しました: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
