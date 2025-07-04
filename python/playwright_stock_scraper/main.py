import asyncio
import os
import sys

from playwright.async_api import Error

from playwright_stock_scraper.scraper import scrape
from playwright_stock_scraper.writer import save_csv, save_json

OUTPUT_DIR_PATH = "outputs/playwright_stock_scraper"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol> [csv|json]")
        sys.exit(1)

    symbol = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "csv"

    os.makedirs(OUTPUT_DIR_PATH, exist_ok=True)

    try:
        data = asyncio.run(scrape(symbol))
        OUTPUT_FILE_PATH = f"{OUTPUT_DIR_PATH}/{symbol.upper()}.{output_format}"

        if output_format == "json":
            save_json(data, OUTPUT_FILE_PATH)
        elif output_format == "csv":
            save_csv(data, OUTPUT_FILE_PATH)
        else:
            print("❌ Invalid format. Use 'csv' or 'json'.")
            sys.exit(1)

        print(f"✅ Data saved to {OUTPUT_FILE_PATH}")
    except Error as e:
        print(f"❌ Playwright Error: {e}")
