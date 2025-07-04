import asyncio
import sys

from playwright.async_api import Error

from playwright_stock_scraper.scraper import scrape
from playwright_stock_scraper.writer import save_csv, save_json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol> [csv|json]")
        sys.exit(1)

    symbol = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "csv"
    OUTPUT_PATH = "outputs/playwright_stock_scraper"

    try:
        data = asyncio.run(scrape(symbol))
        if output_format == "json":
            save_json(data, f"{OUTPUT_PATH}/{symbol.upper()}.{output_format}")
        else:
            save_csv(data, f"{OUTPUT_PATH}/{symbol.upper()}.csv")
    except Error as e:
        print(f"❌ Playwright Error: {e}")
