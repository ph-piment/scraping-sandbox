from playwright_stock_scraper.scraper import scrape
from playwright_stock_scraper.writer import save_csv, save_json


async def run_scraping_and_save(
    symbol: str,
    output_format: str = "csv",
    output_path: str = "outputs/playwright_stock_scraper",
):
    data = await scrape(symbol)
    output_file = f"{output_path}/{symbol.upper()}.{output_format}"
    if output_format == "json":
        save_json(data, output_file)
    else:
        save_csv(data, output_file)

    print(f"✅ Saved to {output_file}")
