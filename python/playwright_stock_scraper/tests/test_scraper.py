import pytest
from playwright.async_api import async_playwright

from playwright_stock_scraper.scraper import extract_table_rows, parse_row

@pytest.mark.asyncio
async def test_parse_row_with_mock_html():
    html = """
    <table id="fourvalue_timeline">
      <tbody>
        <tr>
          <td>2024-01-01</td>
          <td>100</td>
          <td>110</td>
          <td>90</td>
          <td>105</td>
          <td>-</td>
          <td>123456</td>
        </tr>
      </tbody>
    </table>
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html)
        rows = await extract_table_rows(page, "#fourvalue_timeline")

        assert len(rows) == 1

        result = await parse_row(rows[0])
        assert result["Date"] == "2024-01-01"
        assert result["Open"] == "100"
        assert result["High"] == "110"
        assert result["Low"] == "90"
        assert result["Close"] == "105"
        assert result["Volume"] == "123456"

        await browser.close()


@pytest.mark.asyncio
async def test_parse_row_with_incomplete_row():
    html = """
    <table id="fourvalue_timeline">
      <tbody>
        <tr>
          <td>2024-01-01</td>
          <td>100</td>
          <td>110</td>
          <td>90</td>
          <td>105</td>
          <td>-</td>
          <!-- Volume 欠損 -->
        </tr>
      </tbody>
    </table>
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html)
        rows = await extract_table_rows(page, "#fourvalue_timeline")

        assert len(rows) == 1
        result = await parse_row(rows[0])

        assert result is None

        await browser.close()


@pytest.mark.asyncio
async def test_extract_table_rows_empty():
    html = """<table id="fourvalue_timeline"><tbody></tbody></table>"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html)
        rows = await extract_table_rows(page, "#fourvalue_timeline")

        assert rows == []

        await browser.close()

