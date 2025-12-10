import pytest
from playwright.async_api import async_playwright

from utils.playwright import create_browser, create_context


@pytest.mark.asyncio
async def test_browser_and_context_startup():
    async with async_playwright() as p:
        browser = await create_browser(p, headless=True)
        assert browser is not None

        context = await create_context(browser)
        assert context is not None

        page = await context.new_page()
        await page.goto("https://example.com")
        await page.screenshot(path="test_example_com.png")
        await browser.close()
