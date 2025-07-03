import csv
from minkabu_timeline_scraper.writer import save_csv

def test_save_csv_default_fieldnames(tmp_path):
    data = [
        {"Date": "2025-07-01", "Open": "100", "High": "110", "Low": "90", "Close": "105", "Volume": "123456"},
        {"Date": "2025-07-02", "Open": "101", "High": "111", "Low": "91", "Close": "106", "Volume": "123000"},
    ]
    output_file = tmp_path / "test_output.csv"

    save_csv(data, output_file)

    with open(output_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows == data

def test_save_csv_explicit_fieldnames(tmp_path):
    data = [
        {"foo": "1", "bar": "2"},
        {"foo": "3", "bar": "4"},
    ]
    output_file = tmp_path / "custom_output.csv"
    fieldnames = ["bar", "foo"]

    save_csv(data, output_file, fieldnames=fieldnames)

    with open(output_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        lines = list(reader)

    assert lines[0] == ["bar", "foo"]
    assert lines[1] == ["2", "1"]
    assert lines[2] == ["4", "3"]

