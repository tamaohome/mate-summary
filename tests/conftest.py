from pathlib import Path

import pytest

from app.models.csv_data import CSVData
from app.models.csv_summary_data import CSVSummaryData


@pytest.fixture(scope="module")
def summary_csv_path() -> Path:
    """総括表CSVファイルのパスを返すフィクスチャ"""
    return Path("tests/data/鋼材重量総括表.csv")


@pytest.fixture(scope="module")
def csv_data(summary_csv_path: Path) -> CSVData:
    """総括表CSVファイルから `CSVData` を返すフィクスチャ"""
    data = CSVData.load_from_csv_file(summary_csv_path)
    return data


@pytest.fixture(scope="module")
def csv_summary_data(summary_csv_path: Path) -> CSVSummaryData:
    """総括表CSVファイルから `CSVSummaryData` を返すフィクスチャ"""
    data = CSVSummaryData.load_from_csv_file(summary_csv_path)
    return data
