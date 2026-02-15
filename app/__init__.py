from pathlib import Path

# app/
APP_ROOT = Path(__file__).resolve().parent

# /
PROJECT_ROOT = APP_ROOT.parent

# app/ui/
UI_DIR = APP_ROOT / "ui"

# tests/data/
TEST_DATA_DIR = PROJECT_ROOT / "tests" / "data"
