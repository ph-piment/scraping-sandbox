from unittest.mock import AsyncMock, patch

import pytest

from fotosource_scraper import usecase


@pytest.mark.asyncio
async def test_run_scraping_and_save():
    mock_data = [{"region": "Tokyo", "name": "Test Store"}]

    with patch(
        "fotosource_scraper.usecase.scrape", new_callable=AsyncMock
    ) as mock_scrape, patch("fotosource_scraper.usecase.save_csv") as mock_save_csv:

        mock_scrape.return_value = mock_data

        await usecase.run_scraping_and_save()

        mock_scrape.assert_awaited_once()
        mock_save_csv.assert_called_once_with(
            mock_data, "outputs/fotosource_scraper/stores.csv"
        )


@pytest.mark.asyncio
async def test_run_scraping_and_save_with_custom_path():
    mock_data = [{"region": "Osaka", "name": "Another Store"}]
    custom_path = "outputs/custom/stores.csv"

    with patch(
        "fotosource_scraper.usecase.scrape", new_callable=AsyncMock
    ) as mock_scrape, patch("fotosource_scraper.usecase.save_csv") as mock_save_csv:

        mock_scrape.return_value = mock_data

        await usecase.run_scraping_and_save(output_path=custom_path)

        mock_scrape.assert_awaited_once()
        mock_save_csv.assert_called_once_with(mock_data, custom_path)
