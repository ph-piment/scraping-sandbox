import json
import tempfile
from pathlib import Path

import pytest

from rss_fetch_from_search.reader import load_dist


def test_load_dist_success():
    sample_data = {"react": {"name": "react"}}
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tmp:
        json.dump(sample_data, tmp)
        tmp_path = Path(tmp.name)

    result = load_dist(tmp_path)
    assert result == sample_data

    tmp_path.unlink()


def test_load_dist_file_not_found():
    nonexistent_path = Path("nonexistent_file.json")
    with pytest.raises(RuntimeError) as exc_info:
        load_dist(nonexistent_path)
    assert "Failed to load JSON file" in str(exc_info.value)


def test_load_dist_invalid_json():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tmp:
        tmp.write("not a valid json")
        tmp_path = Path(tmp.name)

    with pytest.raises(RuntimeError) as exc_info:
        load_dist(tmp_path)
    assert "Failed to load JSON file" in str(exc_info.value)

    tmp_path.unlink()
