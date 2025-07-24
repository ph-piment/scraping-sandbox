import asyncio

from playwright.async_api import Error

from fotosource_scraper.usecase import run_scraping_and_save
from utils.error_handling import handle_playwright_error


def main():
    try:
        asyncio.run(run_scraping_and_save())
    except Error as e:
        handle_playwright_error(e)


if __name__ == "__main__":
    main()
