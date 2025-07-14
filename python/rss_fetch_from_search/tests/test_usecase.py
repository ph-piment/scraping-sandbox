from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from rss_fetch_from_search import usecase


@pytest.mark.asyncio
async def test_fetch_rss():
    mocked_data = {"react": {"rss": "https://github.com/facebook/react/releases.atom"}}

    with patch(
        "rss_fetch_from_search.usecase.load_dist", return_value={"react": {}}
    ) as mock_load, patch(
        "rss_fetch_from_search.usecase.fetch_techs_rss",
        new_callable=AsyncMock,
        return_value=mocked_data,
    ) as mock_fetch, patch(
        "rss_fetch_from_search.usecase.save_json"
    ) as mock_save:

        await usecase.fetch_rss()

        input_path = (
            Path(__file__).parent.parent.parent
            / "inputs/rss_fetch_from_search/tech_keywords.json"
        )
        output_path = "outputs/rss_fetch_from_search/techs.json"

        mock_load.assert_called_once_with(input_path)
        mock_fetch.assert_awaited_once_with({"react": {}})
        mock_save.assert_called_once_with(mocked_data, output_path)
