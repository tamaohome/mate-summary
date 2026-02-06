import tempfile
from pathlib import Path

from app.io.csv_handler import write_csv
from app.models.summary_table import SummaryTable


def test_CSVの書き出し(summary_tables: list[SummaryTable]) -> None:
    table = summary_tables[1]
    output_csvdata = table.to_csvdata()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_csv_path = Path(tmpdir) / "output.csv"
        write_csv(output_csvdata, output_csv_path)
        assert output_csv_path.exists()
