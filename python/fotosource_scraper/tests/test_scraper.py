from unittest.mock import AsyncMock, MagicMock

import pytest

from fotosource_scraper.scraper import LINK_LOCATOR, parse_li


@pytest.mark.asyncio
async def test_parse_li_all_fields_present():
    region = "TestRegion"
    mock_li = MagicMock()

    lines = [
        "Tokyo",
        "Test Store",
        "Tokyo Address",
        "03-1234-5678",
        "Open",
        "9:00-18:00",
    ]

    store_text_locator = AsyncMock()
    store_text_locator.all_inner_texts.return_value = lines

    link_locator = AsyncMock()
    link_locator.count.return_value = 1
    link_locator.get_attribute.return_value = "https://example.com/store"

    def locator_side_effect(selector):
        if selector == "p.d-store-finder-store-text":
            return store_text_locator
        if selector == LINK_LOCATOR:
            return link_locator
        raise ValueError(f"Unexpected selector: {selector}")

    mock_li.locator.side_effect = locator_side_effect

    result = await parse_li(region, mock_li)

    assert result == {
        "region": "TestRegion",
        "city": "Tokyo",
        "name": "Test Store",
        "address": "Tokyo Address",
        "phone": "03-1234-5678",
        "status": "Open",
        "hours": "9:00-18:00",
        "link": "https://example.com/store",
    }


@pytest.mark.asyncio
async def test_parse_li_partial_fields_missing():
    region = "EmptyRegion"
    mock_li = MagicMock()

    lines = [
        "Osaka",
        "Mini Shop",
        "Osaka City Address",
    ]

    store_text_locator = AsyncMock()
    store_text_locator.all_inner_texts.return_value = lines

    link_locator = AsyncMock()
    link_locator.count.return_value = 0

    def locator_side_effect(selector):
        if selector == "p.d-store-finder-store-text":
            return store_text_locator
        if selector == LINK_LOCATOR:
            return link_locator
        raise ValueError(f"Unexpected selector: {selector}")

    mock_li.locator.side_effect = locator_side_effect

    result = await parse_li(region, mock_li)

    assert result == {
        "region": "EmptyRegion",
        "city": "Osaka",
        "name": "Mini Shop",
        "address": "Osaka City Address",
        "phone": "",
        "status": "",
        "hours": "",
        "link": "",
    }
