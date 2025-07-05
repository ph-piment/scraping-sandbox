import asyncio
from unittest.mock import MagicMock, patch

import pytest

from playwright_stock_scraper.usecase import run_scraping_and_save


@pytest.mark.asyncio
@patch("playwright_stock_scraper.usecase.save_json")
@patch("playwright_stock_scraper.usecase.scrape")
async def test_run_scraping_and_save_json(mock_scrape, mock_save_json, capsys):
    mock_scrape.return_value = {"price": 1234}

    await run_scraping_and_save("TEST", "json", output_path="outputs/test")

    mock_scrape.assert_called_once_with("TEST")
    mock_save_json.assert_called_once_with({"price": 1234}, "outputs/test/TEST.json")

    captured = capsys.readouterr()
    assert "✅ Saved to outputs/test/TEST.json" in captured.out


@pytest.mark.asyncio
@patch("playwright_stock_scraper.usecase.save_csv")
@patch("playwright_stock_scraper.usecase.scrape")
async def test_run_scraping_and_save_csv(mock_scrape, mock_save_csv, capsys):
    mock_scrape.return_value = {"price": 5678}

    await run_scraping_and_save("AAA", "csv", output_path="outputs/test")

    mock_scrape.assert_called_once_with("AAA")
    mock_save_csv.assert_called_once_with({"price": 5678}, "outputs/test/AAA.csv")

    captured = capsys.readouterr()
    assert "✅ Saved to outputs/test/AAA.csv" in captured.out
