from pathlib import Path
from typing import Final

import pytest

from app.core.csv_data_parser import CSVDataParser
from app.core.summary_table_parser import SummaryTableParser
from app.io.csv_handler import read_csv
from app.models.csv_data import CSVData
from app.models.summary_table import SummaryTable

ENCODING: Final = "shift_jis"


@pytest.fixture(scope="module")
def sample_csv_path() -> Path:
    """テストで用いるサンプル CSV ファイルへのパスを返すフィクスチャ"""
    return Path("tests/data/鋼材重量総括表.csv")


@pytest.fixture(scope="module")
def csv_data(sample_csv_path: Path) -> CSVData:
    """CSVファイルから直接読み込んだCSVDataを返すフィクスチャ"""
    return read_csv(sample_csv_path)


@pytest.fixture(scope="module")
def parser(csv_data: CSVData) -> CSVDataParser:
    """CSVDataParserの共有インスタンスを返すフィクスチャ"""
    return CSVDataParser(csv_data)


@pytest.fixture(scope="module")
def csv_tables(parser: CSVDataParser) -> list[CSVData]:
    """parser.csv_tablesを返すフィクスチャ"""
    return parser.csv_tables


@pytest.fixture(scope="module")
def summary_table_parser(sample_csv_path: Path) -> SummaryTableParser:
    """SummaryTableParserの共有インスタンスを返すフィクスチャ"""
    return SummaryTableParser(sample_csv_path)


@pytest.fixture(scope="module")
def summary_tables(summary_table_parser: SummaryTableParser) -> dict[int, SummaryTable]:
    """パースされたSummaryTableの辞書を返すフィクスチャ"""
    return summary_table_parser.parse()
