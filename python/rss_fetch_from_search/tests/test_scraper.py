from unittest.mock import AsyncMock, MagicMock, Mock, patch
from urllib.parse import urlparse

import pytest
from playwright.async_api import Error as PlaywrightError

from rss_fetch_from_search.scraper import (
    choose_best_url,
    create_context,
    extract_repo_path,
    extract_rss_links,
    fetch_techs_rss,
    get_tech_info_with_fallbacks,
    handle_simple_captcha,
    is_excluded_url,
    resolve_redirect,
    score_repo_path,
    search_bing_and_get_top_result,
    search_brave_and_get_top_result,
    search_mojeek_and_get_top_result,
)


@pytest.mark.asyncio
async def test_search_brave_and_get_top_result_finds_release_url():
    mock_page = MagicMock()

    # Brave 検索結果リンクモック
    release_url = "https://github.com/example/project/releases"
    other_url = "https://example.com/notgithub"

    mock_result_links = MagicMock()
    mock_result_links.count = AsyncMock(return_value=2)

    def nth_link_stub(i):
        mock_link = MagicMock()
        mock_link.get_attribute = AsyncMock(return_value=[other_url, release_url][i])
        return mock_link

    mock_result_links.nth.side_effect = nth_link_stub

    def locator_stub(selector):
        assert selector == "#results > div > a"
        return mock_result_links

    mock_page.locator = Mock(side_effect=locator_stub)
    mock_page.goto = AsyncMock()

    with patch("rss_fetch_from_search.scraper.handle_simple_captcha", new=AsyncMock()):
        result = await search_brave_and_get_top_result(mock_page, "example")

    assert result == release_url


@pytest.mark.asyncio
async def test_search_mojeek_and_get_top_result_returns_release_url():
    mock_page = MagicMock()

    github_url_1 = "https://github.com/example/project"
    github_url_2 = "https://github.com/example/another"

    mock_result_items = MagicMock()
    mock_result_items.count = AsyncMock(return_value=2)

    def result_item_nth_stub(i):
        mock_item = MagicMock()
        mock_link = MagicMock()
        mock_link.get_attribute = AsyncMock(
            return_value=[github_url_1, github_url_2][i]
        )
        mock_item.locator.return_value.nth.return_value = mock_link
        return mock_item

    mock_result_items.nth.side_effect = result_item_nth_stub

    def locator_stub(selector):
        if selector == "div.results > ul > li":
            return mock_result_items
        return MagicMock()  # fallback for other selectors if needed

    mock_page.locator = Mock(side_effect=locator_stub)
    mock_page.goto = AsyncMock()
    mock_page.title = AsyncMock(return_value="Example Project · GitHub")

    with patch("rss_fetch_from_search.scraper.handle_simple_captcha", new=AsyncMock()):
        with patch(
            "rss_fetch_from_search.scraper.choose_best_url", return_value=github_url_1
        ):
            result = await search_mojeek_and_get_top_result(mock_page, "example")

    assert result == f"{github_url_1}/releases"
    mock_page.goto.assert_called()


@pytest.mark.asyncio
async def test_search_bing_returns_copilot_url():
    mock_page = MagicMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()

    def locator_stub(selector):
        if selector == "div.b_tpcn > a":
            mock_locator = MagicMock()
            mock_locator.count = AsyncMock(return_value=1)
            mock_first = MagicMock()
            mock_first.get_attribute = AsyncMock(
                return_value="https://github.com/copilot"
            )
            mock_locator.first = mock_first
            return mock_locator
        if selector == "li.b_algo h2 a":
            mock_locator = MagicMock()
            mock_locator.count = AsyncMock(return_value=0)
            return mock_locator
        raise ValueError(f"Unexpected selector: {selector}")

    mock_page.locator.side_effect = locator_stub

    result = await search_bing_and_get_top_result(mock_page, "FastAPI")
    assert result == "https://github.com/copilot"


@pytest.mark.asyncio
async def test_search_bing_returns_fallback_url():
    mock_page = MagicMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()

    def locator_stub(selector):
        if selector == "div.b_tpcn > a":
            mock_locator = MagicMock()
            mock_locator.count = AsyncMock(return_value=0)
            return mock_locator
        if selector == "li.b_algo h2 a":
            mock_locator = MagicMock()
            mock_locator.count = AsyncMock(return_value=1)
            mock_first = MagicMock()
            mock_first.get_attribute = AsyncMock(
                return_value="https://github.com/fallback"
            )
            mock_locator.first = mock_first
            return mock_locator
        raise ValueError(f"Unexpected selector: {selector}")

    mock_page.locator.side_effect = locator_stub

    result = await search_bing_and_get_top_result(mock_page, "FastAPI")
    assert result == "https://github.com/fallback"


@pytest.mark.asyncio
async def test_search_bing_returns_none_if_no_results():
    mock_page = MagicMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()

    def locator_stub(_):
        mock_locator = MagicMock()
        mock_locator.count = AsyncMock(return_value=0)
        return mock_locator

    mock_page.locator.side_effect = locator_stub

    result = await search_bing_and_get_top_result(mock_page, "FastAPI")
    assert result is None


@pytest.mark.asyncio
async def test_handle_simple_captcha_success():
    mock_page = MagicMock()

    mock_locator = MagicMock()
    mock_locator.count = AsyncMock(return_value=1)
    mock_locator.click = AsyncMock()

    def locator_stub(selector):
        assert selector == 'button:has-text("I\'m not a robot")'
        return mock_locator

    mock_page.locator = locator_stub
    mock_page.wait_for_timeout = AsyncMock()

    result = await handle_simple_captcha(mock_page)
    assert result is True

    mock_locator.click.assert_awaited_once_with(timeout=3000)
    mock_page.wait_for_timeout.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_simple_captcha_click_fail():
    mock_page = MagicMock()
    mock_locator = MagicMock()
    mock_locator.count = AsyncMock(return_value=1)
    mock_locator.click = AsyncMock(side_effect=PlaywrightError("Click error"))

    def locator_stub(_):
        return mock_locator

    mock_page.locator = locator_stub
    mock_page.wait_for_timeout = AsyncMock()

    result = await handle_simple_captcha(mock_page)
    assert result is False


@pytest.mark.asyncio
async def test_fetch_techs_rss_success():
    techs = {
        "fastapi": {"name": "FastAPI"},
        "numpy": {"name": "NumPy"},
    }

    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()

    mock_playwright_context = AsyncMock()
    mock_playwright_context.__aenter__.return_value = MagicMock()

    with patch(
        "rss_fetch_from_search.scraper.async_playwright",
        return_value=mock_playwright_context,
    ), patch(
        "rss_fetch_from_search.scraper.create_browser", return_value=mock_browser
    ), patch(
        "rss_fetch_from_search.scraper.create_context", return_value=mock_context
    ), patch.object(
        mock_context, "new_page", side_effect=[mock_page, mock_page]
    ), patch(
        "rss_fetch_from_search.scraper.get_tech_info_with_fallbacks",
        side_effect=[
            (
                "https://github.com/tiangolo/fastapi",
                "https://github.com/tiangolo/fastapi/releases.atom",
            ),
            (
                "https://github.com/numpy/numpy",
                "https://github.com/numpy/numpy/releases.atom",
            ),
        ],
    ):

        result = await fetch_techs_rss(techs)

    assert len(result) == 2
    assert result[0]["url"] == "https://github.com/tiangolo/fastapi"
    assert result[0]["rss"] == "https://github.com/tiangolo/fastapi/releases.atom"
    assert result[1]["url"] == "https://github.com/numpy/numpy"
    assert result[1]["rss"] == "https://github.com/numpy/numpy/releases.atom"


@pytest.mark.asyncio
async def test_block_static_resources_behavior():
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_browser.new_context.return_value = mock_context

    route_callbacks = []

    async def route_side_effect(_, callback):
        route_callbacks.append(callback)

    mock_context.route.side_effect = route_side_effect

    await create_context(mock_browser)

    assert len(route_callbacks) == 1
    block_static_resources = route_callbacks[0]

    for resource_type in ["image", "stylesheet", "font"]:
        mock_route = AsyncMock()
        mock_request = MagicMock(resource_type=resource_type)
        await block_static_resources(mock_route, mock_request)
        mock_route.abort.assert_awaited_once()
        mock_route.continue_.assert_not_called()
        mock_route.abort.reset_mock()

    mock_route = AsyncMock()
    mock_request = MagicMock(resource_type="script")
    await block_static_resources(mock_route, mock_request)
    mock_route.continue_.assert_awaited_once()
    mock_route.abort.assert_not_called()


@pytest.mark.asyncio
async def test_get_tech_info_with_valid_rss():
    mock_page = AsyncMock()
    tech_name = "FastAPI"
    search_order = ["bing"]

    with patch(
        "rss_fetch_from_search.scraper.SEARCH_ENGINES", {"bing": AsyncMock()}
    ) as mock_engines, patch(
        "rss_fetch_from_search.scraper.is_excluded_url", return_value=False
    ), patch(
        "rss_fetch_from_search.scraper.resolve_redirect", new_callable=AsyncMock
    ) as mock_resolve_redirect, patch(
        "rss_fetch_from_search.scraper.extract_rss_links", new_callable=AsyncMock
    ) as mock_extract_rss:

        mock_engines["bing"].return_value = "https://example.com/project"
        mock_resolve_redirect.return_value = "https://github.com/tiangolo/fastapi"
        mock_extract_rss.return_value = (
            "https://github.com/tiangolo/fastapi/releases.atom"
        )

        resolved_url, rss_url = await get_tech_info_with_fallbacks(
            mock_page, tech_name, search_order
        )

        assert resolved_url == "https://github.com/tiangolo/fastapi"
        assert rss_url == "https://github.com/tiangolo/fastapi/releases.atom"


@pytest.mark.asyncio
async def test_get_tech_info_with_all_fallbacks_fail():
    mock_page = AsyncMock()
    tech_name = "UnknownTech"
    search_order = ["bing", "mojeek", "brave"]

    with patch(
        "rss_fetch_from_search.scraper.SEARCH_ENGINES",
        {
            "bing": AsyncMock(return_value=None),
            "mojeek": AsyncMock(return_value=None),
            "brave": AsyncMock(return_value=None),
        },
    ), patch(
        "rss_fetch_from_search.scraper.is_excluded_url", return_value=False
    ), patch(
        "rss_fetch_from_search.scraper.resolve_redirect", new_callable=AsyncMock
    ) as mock_resolve, patch(
        "rss_fetch_from_search.scraper.extract_rss_links", new_callable=AsyncMock
    ) as mock_extract:

        resolved_url, rss_url = await get_tech_info_with_fallbacks(
            mock_page, tech_name, search_order
        )

        assert resolved_url is None
        assert rss_url is None
        mock_resolve.assert_not_awaited()
        mock_extract.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_redirect_success_github():
    mock_page = AsyncMock()
    mock_page.url = "https://github.com/user/repo"

    mock_page.goto = AsyncMock()
    mock_page.wait_for_load_state = AsyncMock()
    mock_page.wait_for_timeout = AsyncMock()

    original_url = "https://example.com/redirect"
    result = await resolve_redirect(mock_page, original_url)

    assert result == "https://github.com/user/repo"
    mock_page.goto.assert_called_with(original_url, wait_until="load", timeout=10000)
    assert urlparse(result).netloc == "github.com"


@pytest.mark.asyncio
async def test_resolve_redirect_fail_non_github():
    mock_page = AsyncMock()
    mock_page.url = "https://other.com/page"

    mock_page.goto = AsyncMock()
    mock_page.wait_for_load_state = AsyncMock()
    mock_page.wait_for_timeout = AsyncMock()

    url = "https://example.com/some-redirect"
    result = await resolve_redirect(mock_page, url)

    assert result == url  # fallback to original URL


@pytest.mark.asyncio
async def test_resolve_redirect_exception_handling():
    mock_page = AsyncMock()
    mock_page.goto.side_effect = PlaywrightError("Timeout error")

    url = "https://example.com/fail"
    result = await resolve_redirect(mock_page, url)

    assert result == url  # fallback


@pytest.mark.asyncio
async def test_extract_rss_links_success():
    mock_page = AsyncMock()

    mock_page.goto = AsyncMock()
    mock_page.wait_for_timeout = AsyncMock()

    mock_locator = MagicMock()
    mock_tag1 = AsyncMock()
    mock_tag2 = AsyncMock()

    def locator_stub(selector):
        assert selector == 'link[rel="alternate"][type="application/atom+xml"]'
        return mock_locator

    mock_page.locator = locator_stub

    mock_locator.count = AsyncMock(return_value=2)
    mock_locator.nth.side_effect = [mock_tag1, mock_tag2]

    mock_tag1.get_attribute = AsyncMock(return_value="rss.xml")
    mock_tag2.get_attribute = AsyncMock(return_value="https://example.com/feed.atom")

    url = "https://example.com/project"
    result = await extract_rss_links(mock_page, url)

    assert result == "https://example.com/rss.xml"


@pytest.mark.asyncio
async def test_extract_rss_links_missing_href():
    mock_page = AsyncMock()

    mock_page.goto = AsyncMock()
    mock_page.wait_for_timeout = AsyncMock()

    mock_locator = MagicMock()
    mock_tag1 = AsyncMock()
    mock_tag2 = AsyncMock()

    def locator_stub(selector):
        assert selector == 'link[rel="alternate"][type="application/atom+xml"]'
        return mock_locator

    mock_page.locator = locator_stub

    mock_locator.count = AsyncMock(return_value=2)
    mock_locator.nth.side_effect = [mock_tag1, mock_tag2]

    mock_tag1.get_attribute = AsyncMock(return_value=None)
    mock_tag2.get_attribute = AsyncMock(return_value=None)

    url = "https://example.com/project"
    result = await extract_rss_links(mock_page, url)

    assert result is None


@pytest.mark.asyncio
async def test_extract_rss_links_page_load_failure():
    mock_page = AsyncMock()
    mock_page.goto.side_effect = PlaywrightError("Failed to load")
    mock_page.wait_for_timeout = AsyncMock()

    url = "https://example.com"
    result = await extract_rss_links(mock_page, url)

    assert result is None


@pytest.mark.asyncio
async def test_extract_rss_links_empty_url():
    mock_page = AsyncMock()
    result = await extract_rss_links(mock_page, "")
    assert result is None


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com/page", True),
        ("http://subdomain.excluded.org/page", True),
        ("https://ignore.net/resource", True),
        ("https://validsite.dev", False),
        ("https://github.com/user/repo", False),
    ],
)
def test_is_excluded_url(monkeypatch, url, expected):
    monkeypatch.setattr(
        "rss_fetch_from_search.scraper.BING_EXCLUDE_SITES",
        ["example.com", "excluded.org", "ignore.net"],
    )
    assert is_excluded_url(url) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://github.com/user/repo", "user/repo"),
        ("https://github.com/user/repo/", "user/repo"),
        ("https://github.com/user/repo/issues", "user/repo"),
        ("https://github.com/user", None),
        ("not a url", None),
        ("", None),
        (None, None),
    ],
)
def test_extract_repo_path(url, expected):
    assert extract_repo_path(url) == expected


def test_choose_best_url_exact_match():
    urls = [
        "https://github.com/facebook/react",
        "https://github.com/other/irrelevant",
        "https://github.com/reactjs/react",
    ]
    keyword = "react"

    result = choose_best_url(urls, keyword)

    assert result == "https://github.com/reactjs/react"


def test_choose_best_url_partial_match():
    urls = [
        "https://github.com/foobar/reactive",
        "https://github.com/awesome/react-hooks",
    ]
    keyword = "react"

    result = choose_best_url(urls, keyword)

    assert result in urls


def test_choose_best_url_invalid_urls():
    urls = ["https://example.com/notgithub", "https://github.com/invalid"]
    keyword = "react"

    result = choose_best_url(urls, keyword)

    assert result is None


def test_choose_best_url_empty_list():
    assert choose_best_url([], "react") is None


@pytest.mark.parametrize(
    "repo_path, keyword, expected_score",
    [
        ("user1/react", "react", 10 + 2),
        ("react/dev", "react", 5 + 1),
        ("user123/reactjs", "react", 2),
        ("react-user/devlib", "react", 1),
        ("react/react", "react", 10 + 5 + 2 + 1),
        ("user/repo", "react", 0),
    ],
)
def test_score_repo_path_valid(repo_path, keyword, expected_score):
    assert score_repo_path(repo_path, keyword) == expected_score


def test_score_repo_path_invalid_format():
    with pytest.raises(ValueError, match="Invalid repo path"):
        score_repo_path("invalid_format", "react")
