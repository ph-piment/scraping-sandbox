import asyncio
import os
import sys

from playwright.async_api import Error

from playwright_stock_scraper.scraper import scrape
from playwright_stock_scraper.writer import save_csv, save_json

OUTPUT_PATH = "outputs/playwright_stock_scraper"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol> [csv|json]")
        sys.exit(1)

    symbol = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "csv"

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    try:
        data = asyncio.run(scrape(symbol))
        filename = f"{OUTPUT_PATH}/{symbol.upper()}.{output_format}"

        if output_format == "json":
            save_json(data, filename)
        elif output_format == "csv":
            save_csv(data, filename)
        else:
            print("❌ Invalid format. Use 'csv' or 'json'.")
            sys.exit(1)

        print(f"✅ Data saved to {filename}")
    except Error as e:
        print(f"❌ Playwright Error: {e}")
