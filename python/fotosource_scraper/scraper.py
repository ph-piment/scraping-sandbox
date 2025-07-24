from playwright.async_api import async_playwright

from utils.playwright import create_browser, create_context

URL = "https://fotosource.com/store-selector"
PAGE_LOAD_TIMEOUT = 60000
MENU_LOCATOR = "div.d-stores-map-menu.d-store-finder-menu"
LINK_LOCATOR = "a.d-store-finder-store-link"
UL_LOCATOR = "ul.d-stores-map-store-list.d-store-finder-store-list"


async def scrape() -> list[dict]:
    select_locator = (
        f"{MENU_LOCATOR} > div > div > "
        "div.d-stores-map-filters-form.d-store-finder-filters-form > div > select"
    )

    async with async_playwright() as p:
        browser = await create_browser(p, headless=True)
        context = await create_context(browser)
        page = await context.new_page()
        await page.goto(URL, timeout=PAGE_LOAD_TIMEOUT)
        await page.wait_for_selector(MENU_LOCATOR, timeout=PAGE_LOAD_TIMEOUT)
        print(f"✅ Scraping {URL}")

        # await page.screenshot(path="screenshots/fotosource.png")

        options = await page.locator(f"{select_locator} > option").all()
        all_data = []

        for option in options:
            value = await option.get_attribute("value")
            if value is None or value == "0":
                continue

            await page.select_option(select_locator, value=value)
            await page.wait_for_selector(UL_LOCATOR, timeout=PAGE_LOAD_TIMEOUT)

            option_texts = await option.all_inner_texts()
            option_text = option_texts[0] if option_texts else ""
            print(f"🌎 Selecting region: {option_text}")
            # await page.screenshot(path=f"screenshots/fotosource_{option_text}.png")

            lis = await page.locator(f"{UL_LOCATOR} > li").all()
            for li in lis:
                all_data.append(await parse_li(option_text, li))

        await page.close()
        await context.close()
        await browser.close()

        print(f"✅ Scraped {len(all_data)} rows")

        return all_data


async def parse_li(region, li):
    lines = await li.locator("p.d-store-finder-store-text").all_inner_texts()
    city_line = lines[0] if len(lines) > 0 else ""
    name_line = lines[1] if len(lines) > 1 else ""
    address_line = lines[2] if len(lines) > 2 else ""
    phone_line = lines[3] if len(lines) > 3 else ""
    status_line = lines[4] if len(lines) > 4 else ""
    time_line = lines[5] if len(lines) > 5 else ""

    link = ""
    if await li.locator(LINK_LOCATOR).count() > 0:
        link = await li.locator(LINK_LOCATOR).get_attribute("href")

    return {
        "region": region,
        "city": city_line,
        "name": name_line,
        "address": address_line,
        "phone": phone_line,
        "status": status_line,
        "hours": time_line,
        "link": link,
    }
