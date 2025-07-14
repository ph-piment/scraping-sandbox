import sys

from playwright.async_api import Error


def handle_playwright_error(e: Error):
    print(f"❌ Playwright Error: {e}")
    sys.exit(1)
