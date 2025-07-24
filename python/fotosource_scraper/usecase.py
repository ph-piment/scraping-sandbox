from fotosource_scraper.scraper import scrape
from utils.writer import save_csv


async def run_scraping_and_save(
    output_path: str = "outputs/fotosource_scraper/stores.csv",
):
    data = await scrape()
    save_csv(data, output_path)
