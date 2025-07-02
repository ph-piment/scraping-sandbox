"""
Scraper entry point

This script uses Playwright (async) to scrape historical stock data
from Minkabu's stock detail page with paging support.
"""

import asyncio
import csv
from playwright.async_api import async_playwright
import sys


async def scrape(symbol: str):
    url = f"https://minkabu.jp/stock/{symbol}/daily_bar"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        table_selector = "#fourvalue_timeline"

        await page.goto(url, timeout=60000)
        await page.wait_for_selector(table_selector, timeout=10000)

        print(f"✅ Scraping {url}")

        all_data = []

        while True:
            rows = await page.query_selector_all(f"{table_selector} tbody tr")
            for row in rows:
                td_cols = await row.query_selector_all("td")
                if len(td_cols) != 7:
                    continue

                date = await td_cols[0].inner_text()
                opening_price = await td_cols[1].inner_text()
                high_price = await td_cols[2].inner_text()
                low_price = await td_cols[3].inner_text()
                closing_price = await td_cols[4].inner_text()
                # adjusted_closing_price = await td_cols[5].inner_text()
                volume = await td_cols[6].inner_text()

                all_data.append({
                    "Date": date.strip(),
                    "Open": opening_price.strip(),
                    "High": high_price.strip(),
                    "Low": low_price.strip(),
                    "Close": closing_price.strip(),
                    "Volume": volume.strip(),
                })

            next_button = await page.query_selector("a.next_page")
            if next_button:
                await next_button.click()
                await page.wait_for_timeout(1000)
            else:
                break

        await browser.close()

        output_file = f"{symbol}_output.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Date", "Open", "High", "Low", "Close", "Volume"])
            writer.writeheader()
            writer.writerows(all_data)

        print(f"✅ Scraped {len(all_data)} rows and saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python scraper.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    try:
        asyncio.run(scrape(symbol))
    except Exception as e:
        print(f"❌ Error: {e}")
