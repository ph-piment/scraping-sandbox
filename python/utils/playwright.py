DEFAULT_BROWSER_ARGS = [
    # Hides automation-related browser features like navigator.webdriver
    "--disable-blink-features=AutomationControlled",
    # Disables web security (CORS)
    # useful for local testing or interacting with cross-origin iframes
    "--disable-web-security",
    # Disables site isolation features that can block cross-origin iframe interactions
    "--disable-features=IsolateOrigins,site-per-process",
    # Runs the browser without sandboxing (required in some restricted environments like Docker)
    "--no-sandbox",
    # Disables GPU hardware acceleration to avoid unnecessary overhead or crashes in headless mode
    "--disable-gpu",
    # Prevents issues with /dev/shm in small shared memory environments (like Docker containers)
    "--disable-dev-shm-usage",
    # Disables all browser extensions — helps reduce variability and speeds up loading
    "--disable-extensions",
    # Removes "Chrome is being controlled by automated test software" infobar
    "--disable-infobars",
    # Sets a fixed window size to ensure consistent layout rendering
    "--window-size=1280,800",
]


async def create_browser(
    playwright, headless: bool = True, args: list[str] | None = None
):
    browser_args = args if args is not None else DEFAULT_BROWSER_ARGS

    browser = await playwright.chromium.launch(
        headless=headless,
        args=browser_args,
    )
    return browser


DEFAULT_BROWSER_CONTEXT_ARGS = {
    # Set browser locale (used for UI language, formatting dates, etc.)
    "locale": "en-US",
    # Define fixed viewport size for consistent rendering and layout
    "viewport": {"width": 1280, "height": 720},
    # Custom user agent string to mimic a real browser and avoid bot detection
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ),
    # Add common HTTP headers that make the request look more like a human browser
    "extra_http_headers": {
        # Preferred language for content negotiation
        "Accept-Language": "en-US,en;q=0.9",
        # Do Not Track header to signal user privacy preferences
        "DNT": "1",
    },
    # Ignore invalid HTTPS certificates (e.g., self-signed, expired)
    # Useful when scraping dev or staging environments
    "ignore_https_errors": True,
    # Bypass Content Security Policy to allow JavaScript injection or debugging
    # Often helpful when testing or scraping dynamic content
    "bypass_csp": True,
    # Enable download handling (e.g., for downloading CSV, PDF files)
    "accept_downloads": True,
    # Set browser timezone to ensure correct time-dependent rendering
    "timezone_id": "Asia/Tokyo",
    # No preloaded cookies or local storage; use clean session by default
    "storage_state": None,
}
BLOCKED_RESOURCES = {"image", "stylesheet", "font"}


async def create_context(browser):
    context = await browser.new_context(**DEFAULT_BROWSER_CONTEXT_ARGS)

    async def block_static_resources(route, request):
        resource_type = getattr(request, "resource_type", "")
        if resource_type in BLOCKED_RESOURCES:
            await route.abort()
        else:
            await route.continue_()

    await context.route("**/*", block_static_resources)

    return context
