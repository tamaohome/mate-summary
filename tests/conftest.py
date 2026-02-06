from pathlib import Path
from typing import Final

import pytest

ENCODING: Final = "shift_jis"


@pytest.fixture(scope="module")
def sample_csv_path() -> Path:
    """テストで用いるサンプル CSV ファイルへのパスを返すフィクスチャ"""
    return Path("tests/data/鋼材重量総括表.csv")
