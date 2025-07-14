import json
from pathlib import Path
from typing import Dict, Union


def load_dist(filepath: Union[str, Path]) -> Dict[str, Dict]:
    path = Path(filepath)
    if not path.is_absolute():
        path = Path(__file__).parent / path

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to load JSON file: {path}") from e
