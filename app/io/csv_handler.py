import csv
from pathlib import Path

from app.models.csv_data import CSVData, CSVDataType

ENCODING = "shift_jis"


def write_csv(csv_data: CSVData, output_path: Path) -> None:
    """`CSVData` をCSVファイルに書き込む"""
    with output_path.open("w", encoding=ENCODING, newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in csv_data:
            writer.writerow(row)


def read_csv(csv_path: Path) -> CSVData:
    """CSVファイルを読み込み、CSVDataを返す"""
    csv_rows: CSVDataType = []
    with csv_path.open("r", encoding=ENCODING) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            csv_rows.append(_strip_cells(row))
    return CSVData(csv_rows)


def _strip_cells(cells: list[str]) -> list[str]:
    """各セルの前後の空白を削除"""
    return [cell.strip() for cell in cells]
