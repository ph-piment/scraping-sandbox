"""
Scraper entry point

This script uses Playwright (async) to scrape historical stock data
from Minkabu's stock detail page with paging support.
"""

import asyncio
import random

from playwright.async_api import async_playwright

MIN_SLEEP_SECONDS = 0.5
MAX_SLEEP_SECONDS = 3.0
PAGE_LOAD_TIMEOUT = 60000
ROW_WAIT_TIMEOUT = 10000
CLICK_WAIT_MILLISECONDS = 1000


async def scrape(symbol: str) -> list[dict]:
    url = f"https://minkabu.jp/stock/{symbol}/daily_bar"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        table_selector = "#fourvalue_timeline"

        await page.goto(url, timeout=PAGE_LOAD_TIMEOUT)

        print(f"✅ Scraping {url}")

        all_data = []

        first = True
        while True:
            rows = await extract_table_rows(page, table_selector)
            for row in rows:
                parsed = await parse_row(row)
                if parsed is not None:
                    all_data.append(parsed)

            next_button = await page.query_selector("a.next_page")
            if next_button:
                if not first:
                    sleep_time = random.uniform(MIN_SLEEP_SECONDS, MAX_SLEEP_SECONDS)  # nosec B311
                    print(f"🕒 Sleeping for {sleep_time:.2f} seconds before next page")
                    await asyncio.sleep(sleep_time)
                else:
                    first = False

                await next_button.click()
                await page.wait_for_timeout(CLICK_WAIT_MILLISECONDS)
            else:
                break

        await browser.close()

        print(f"✅ Scraped {len(all_data)} rows")

        return all_data


async def extract_table_rows(page, selector):
    await page.wait_for_selector(selector, timeout=ROW_WAIT_TIMEOUT, state="attached")
    return await page.query_selector_all(f"{selector} tbody tr")


async def parse_row(row):
    cols = await row.query_selector_all("td")
    if len(cols) != 7:
        return None
    return {
        "Date": (await cols[0].inner_text()).strip(),
        "Open": (await cols[1].inner_text()).strip(),
        "High": (await cols[2].inner_text()).strip(),
        "Low": (await cols[3].inner_text()).strip(),
        "Close": (await cols[4].inner_text()).strip(),
        # "AdjustedClosingPrice": (await cols[5].inner_text()).strip(),
        "Volume": (await cols[6].inner_text()).strip(),
    }
