import asyncio
import sys

from playwright.async_api import Error

from playwright_stock_scraper.usecase import run_scraping_and_save

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol> [csv|json]")
        sys.exit(1)

    symbol = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "csv"

    try:
        asyncio.run(run_scraping_and_save(symbol, output_format))
    except Error as e:
        print(f"❌ Playwright Error: {e}")
        sys.exit(1)
