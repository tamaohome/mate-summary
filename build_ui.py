import logging
import shutil
import subprocess
import sys

from app import UI_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def build_all_ui() -> None:
    if shutil.which("pyside6-uic") is None:
        logger.error("pyside6-uic が見つかりません。インストールし PATH に追加してください。")
        sys.exit(2)

    ui_files = list(UI_DIR.rglob("*.ui"))
    if not ui_files:
        raise FileNotFoundError("変換対象の .ui ファイルが見つかりません")

    failures = []
    for ui_file in ui_files:
        py_file = ui_file.with_name(f"ui_{ui_file.stem}.py")

        # 既に現在のuiファイルを生成済みの場合はスキップ
        if py_file.exists() and py_file.stat().st_mtime >= ui_file.stat().st_mtime:
            logger.info("スキップ: %s は最新ファイル更新済み", ui_file.name)
            continue

        command = ["pyside6-uic", str(ui_file), "-o", str(py_file)]
        try:
            subprocess.run(command, check=True)
            logger.info("成功: %s -> %s", ui_file.name, py_file.name)
        except subprocess.CalledProcessError as e:
            logger.error("失敗: %s エラー: %s", ui_file.name, e.stderr or e)
            failures.append(ui_file)

    if failures:
        logger.error("変換に失敗したファイル数: %d", len(failures))
        sys.exit(1)


if __name__ == "__main__":
    build_all_ui()
