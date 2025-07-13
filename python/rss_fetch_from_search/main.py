import asyncio

from playwright.async_api import Error

from rss_fetch_from_search.usecase import fetch_rss
from utils.error_handling import handle_playwright_error


def main():
    try:
        asyncio.run(fetch_rss())
    except Error as e:
        handle_playwright_error(e)


if __name__ == "__main__":
    main()
