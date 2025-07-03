"""
Scraper entry point

This script uses Playwright (async) to scrape historical stock data
from Minkabu's stock detail page with paging support.
"""

from playwright.async_api import async_playwright

from minkabu_timeline_scraper.writer import save_csv


async def scrape(symbol: str):
    url = f"https://minkabu.jp/stock/{symbol}/daily_bar"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        table_selector = "#fourvalue_timeline"

        await page.goto(url, timeout=60000)

        print(f"✅ Scraping {url}")

        all_data = []

        while True:
            rows = await extract_table_rows(page, table_selector)
            for row in rows:
                parsed = await parse_row(row)
                if parsed is not None:
                    all_data.append(parsed)

            next_button = await page.query_selector("a.next_page")
            if next_button:
                await next_button.click()
                await page.wait_for_timeout(1000)
            else:
                break

        await browser.close()

        output_file = f"./outputs/minkabu_timeline_scraper/{symbol}.csv"
        save_csv(
            all_data, output_file, ["Date", "Open", "High", "Low", "Close", "Volume"]
        )

        print(f"✅ Scraped {len(all_data)} rows and saved to {output_file}")


async def extract_table_rows(page, selector):
    await page.wait_for_selector(selector, timeout=10000)
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
