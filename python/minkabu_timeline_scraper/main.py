# main.py
import asyncio
import sys

from playwright.async_api import Error
from minkabu_timeline_scraper.scraper import scrape

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    try:
        asyncio.run(scrape(symbol))
    except Error as e:
        print(f"❌ Playwright Error: {e}")
