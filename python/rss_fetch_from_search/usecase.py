from pathlib import Path

from rss_fetch_from_search.reader import load_dist
from rss_fetch_from_search.scraper import fetch_techs_rss
from utils.writer import save_json


async def fetch_rss():
    input_path = (
        Path(__file__).parent.parent / "inputs/rss_fetch_from_search/tech_keywords.json"
    )
    techs = load_dist(input_path)

    data = await fetch_techs_rss(techs)

    save_json(data, "outputs/rss_fetch_from_search/techs.json")
