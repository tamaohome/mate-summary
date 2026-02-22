import tempfile
from pathlib import Path

import pytest

from app.io.csv_handler import write_csv
from app.models.summary_table import SummarySheet


@pytest.mark.skip
def test_CSVの書き出し(summary_sheets: list[SummarySheet]) -> None:
    sheet = summary_sheets[1]
    output_csvdata = sheet.to_csvdata()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_csv_path = Path(tmpdir) / "output.csv"
        write_csv(output_csvdata, output_csv_path)
        assert output_csv_path.exists()
