# main.py
import asyncio
import sys

from scraper import scrape
from playwright.async_api import Error

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    try:
        asyncio.run(scrape(symbol))
    except Error as e:
        print(f"❌ Playwright Error: {e}")
