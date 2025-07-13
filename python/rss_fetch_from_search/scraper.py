import asyncio
from typing import Dict, List, Optional
from urllib.parse import quote, urljoin, urlparse

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import Page, async_playwright

BING_EXCLUDE_SITES = [
    "reddit.com",
    "wikipedia.org",
    "zhihu.com",
    "linkedin.com",
]

CONCURRENCY = 3

BLOCKED_RESOURCES = {"image", "stylesheet", "font"}

FALLBACK_ORDERS = [
    ["brave", "mojeek", "bing"],
    ["mojeek", "bing", "brave"],
    ["bing", "brave", "mojeek"],
]


async def search_brave_and_get_top_result(page: Page, keyword: str) -> str | None:
    query = f'"{keyword}" releases site:github.com'
    brave_url = f"https://search.brave.com/search?q={query}"

    # print(f"🔍 Brave URL: {brave_url}")
    await page.goto(brave_url, timeout=30000, wait_until="load")
    await handle_simple_captcha(page, "I'm not a robot")
    # await page.screenshot(path=f"screenshots/{keyword.replace(' ', '_')}_brave.png")

    result_links = page.locator("#results > div > a")
    count = await result_links.count()

    for i in range(min(count, 5)):
        url = await result_links.nth(i).get_attribute("href")
        if url and "github.com" in url and "/releases" in url:
            return url

    return None


async def search_mojeek_and_get_top_result(page: Page, keyword: str) -> str | None:
    query = f'"{keyword}" site:github.com'
    mojeek_url = f"https://www.mojeek.com/search?q={query}"

    # print(f"🔍 Mojeek URL: {mojeek_url}")
    await page.goto(mojeek_url, timeout=30000, wait_until="load")
    await handle_simple_captcha(page, "I'm not a robot")
    # await page.screenshot(path=f"screenshots/{keyword.replace(' ', '_')}_mojeek.png")

    result_items = page.locator("div.results > ul > li")
    count = await result_items.count()

    urls = []

    for i in range(min(count, 10)):
        item = result_items.nth(i)
        link = item.locator("a").nth(0)
        url = await link.get_attribute("href")
        if url and "github.com" in url:
            urls.append(url)

    best_base_url = choose_best_url(urls, keyword)
    if not best_base_url:
        return None

    releases_url = best_base_url.rstrip("/") + "/releases"
    try:
        await page.goto(releases_url, timeout=10000)
        if "Not Found" not in await page.title():
            return releases_url
    except (PlaywrightError, TimeoutError) as e:
        print(f"❌ Failed to access /releases page: {e}")

    return best_base_url


async def search_bing_and_get_top_result(
    page: Page,
    keyword: str,
) -> Optional[str]:
    query = quote(f'"{keyword}" releases site:github.com')
    exclude_sites = " ".join(f"-site:{site}" for site in BING_EXCLUDE_SITES)
    search_query = f"{query} {exclude_sites}"

    bing_url = f"https://www.bing.com/search?q={search_query}&setlang=en-us&cc=US"

    try:
        await page.goto(bing_url, timeout=30000, wait_until="load")
        await page.wait_for_selector("li.b_algo h2 a", timeout=10000)
    except (PlaywrightError, TimeoutError) as e:
        print(f"❌ Bing search failed: {e}")
        return None

    copilot_locator = page.locator("div.b_tpcn > a")
    if await copilot_locator.count() > 0:
        copilot = copilot_locator.first
        url = await copilot.get_attribute("href")
        if url:
            return url

    fallback_locator = page.locator("li.b_algo h2 a")
    if await fallback_locator.count() > 0:
        fallback = fallback_locator.first
        url = await fallback.get_attribute("href")
        if url:
            return url

    return None


SEARCH_ENGINES = {
    "brave": search_brave_and_get_top_result,
    "mojeek": search_mojeek_and_get_top_result,
    "bing": search_bing_and_get_top_result,
}


async def handle_simple_captcha(
    page: Page, label: str = "I'm not a robot", wait_ms: int = 5000
) -> bool:
    selector = f'button:has-text("{label}")'
    captcha_button = page.locator(selector)

    try:
        if not await captcha_button.count():
            return False

        await captcha_button.click(timeout=3000)
        await page.wait_for_timeout(wait_ms)
        return True

    except (PlaywrightError, TimeoutError) as e:
        print(f"❌ Failed to click CAPTCHA button: {e}")
        return False


async def fetch_techs_rss(techs: Dict[str, Dict]) -> list[Dict]:
    results = []
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with async_playwright() as p:
        browser = await create_browser(p, headless=True)
        context = await create_context(browser)

        async def fetch_tech(index: int, tech: Dict):
            async with semaphore:
                page = await context.new_page()
                order = FALLBACK_ORDERS[index % len(FALLBACK_ORDERS)]
                try:
                    url, rss = await get_tech_info_with_fallbacks(
                        page, tech["name"], order
                    )
                    tech.update({"url": url, "rss": rss})
                except (PlaywrightError, TimeoutError, ValueError) as e:
                    print(f"❌ Error for {tech['name']}: {e}")
                    tech.update({"url": None, "rss": None})
                finally:
                    await page.close()
                    results.append(tech)
                    await asyncio.sleep(1)

        try:
            await asyncio.gather(
                *(fetch_tech(i, t) for i, t in enumerate(techs.values()))
            )
        finally:
            await context.close()
            await browser.close()

    return results


async def create_browser(playwright, headless: bool = True):
    browser = await playwright.chromium.launch(
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
        ],
    )
    return browser


def get_browser_context_args() -> dict:
    return {
        "locale": "en-US",
        "viewport": {"width": 1280, "height": 720},
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1",
        },
        "storage_state": None,
    }


async def create_context(browser):
    context = await browser.new_context(**get_browser_context_args())

    async def block_static_resources(route, request):
        resource_type = getattr(request, "resource_type", "")
        if resource_type in BLOCKED_RESOURCES:
            await route.abort()
        else:
            await route.continue_()

    await context.route("**/*", block_static_resources)

    return context


async def get_tech_info_with_fallbacks(
    page: Page, name: str, order: list[str]
) -> tuple[str | None, str | None]:
    for engine in order:
        search_fn = SEARCH_ENGINES[engine]
        url = await search_fn(page, name)
        # print(url)
        if url and not is_excluded_url(url):
            resolved_url = await resolve_redirect(page, url)
            if not resolved_url:
                return None, None
            # print(resolved_url)
            rss = await extract_rss_links(page, resolved_url)
            return resolved_url, rss
    return None, None


async def resolve_redirect(page: Page, url: str, max_retries: int = 3) -> str:
    for i, _ in enumerate(range(1, max_retries + 1), start=1):
        try:
            await page.goto(url, wait_until="load", timeout=10000 * i)
            await page.wait_for_load_state("networkidle", timeout=5000 * i)

            await page.wait_for_timeout(3000 * i)

            final_url = page.url
            if urlparse(final_url).netloc.lower() == "github.com":
                return final_url

        except (PlaywrightError, TimeoutError) as e:
            print(f"❌ Exception on attempt {i} ({type(e).__name__}): {e}")

        await asyncio.sleep(1)

    return url


async def extract_rss_links(page: Page, url: str) -> Optional[str]:
    if not url:
        return None

    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(5000)
    except (PlaywrightError, TimeoutError) as e:
        print(f"❌ Failed to load page {url}: {e}")
        return None

    rss_candidates = []

    link_tags = page.locator('link[rel="alternate"][type="application/atom+xml"]')
    try:
        count = await link_tags.count()
        for i in range(count):
            href = await link_tags.nth(i).get_attribute("href")
            if href:
                rss_candidates.append(urljoin(url, href))
    except (PlaywrightError, TimeoutError) as e:
        print(f"❌ Failed to extract RSS links from {url}: {e}")
        return None

    rss_list = list(dict.fromkeys(rss_candidates))

    return rss_list[0] if rss_list else None


def is_excluded_url(url: str) -> bool:
    domain = urlparse(url).netloc
    return any(excluded in domain for excluded in BING_EXCLUDE_SITES)


def extract_repo_path(url: Optional[str]) -> Optional[str]:
    if not isinstance(url, str):
        return None

    parts = urlparse(url).path.strip("/").split("/")
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return None


def choose_best_url(urls: List[str], keyword: str) -> Optional[str]:
    scored_urls = []

    for url in urls:
        repo_path = extract_repo_path(url)
        if repo_path:
            score = score_repo_path(repo_path, keyword)
            scored_urls.append((score, url))

    if not scored_urls:
        return None

    return max(scored_urls, key=lambda x: x[0])[1]


def score_repo_path(repo_path: str, keyword: str) -> int:
    try:
        user, repo = repo_path.split("/")
    except ValueError as e:
        raise ValueError("Invalid repo path") from e

    keyword = keyword.lower()
    user = user.lower()
    repo = repo.lower()

    score = 0
    if repo == keyword:
        score += 10
    if user == keyword:
        score += 5
    if keyword in repo:
        score += 2
    if keyword in user:
        score += 1
    return score
