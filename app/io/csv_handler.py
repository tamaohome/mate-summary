import csv
from pathlib import Path

from app.io import ENCODING
from app.models.csv_data import CSVData


def write_csv(csv_data: CSVData, output_path: Path) -> None:
    """`CSVData` をCSVファイルに書き込む"""
    with output_path.open("w", encoding=ENCODING, newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in csv_data:
            writer.writerow(row)
