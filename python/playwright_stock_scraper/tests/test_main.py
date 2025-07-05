import sys
from unittest.mock import patch

import pytest
from playwright.async_api import Error

from playwright_stock_scraper import main as main_module


def test_main_no_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit) as e:
        main_module.main()
    assert e.value.code == 1


@patch("playwright_stock_scraper.main.run_scraping_and_save")
def test_main_success(mock_run, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "TEST", "json"])

    mock_run.return_value = None

    main_module.main()

    mock_run.assert_called_once_with("TEST", "json")


@patch("playwright_stock_scraper.main.run_scraping_and_save")
def test_main_playwright_error(mock_run, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "TEST", "csv"])

    async def raise_error(symbol, fmt):
        raise Error("Mock Playwright Error")

    mock_run.side_effect = raise_error

    with pytest.raises(SystemExit) as e:
        main_module.main()

    captured = capsys.readouterr()
    assert "Playwright Error" in captured.out
    assert e.value.code == 1
