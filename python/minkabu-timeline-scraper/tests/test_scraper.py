import pytest
from playwright.async_api import async_playwright

from scraper import extract_table_rows, parse_row

HTML = """
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


@pytest.mark.asyncio
async def test_parse_row_with_mock_html():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(HTML)
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
