# 🐍 Python Scraping Recipes

This directory contains Python-based scraping examples using Playwright, asyncio, and more.
Each folder is a self-contained project with its own entrypoint and tests.

[![codecov](https://codecov.io/gh/ph-piment/scraping-sandbox/graph/badge.svg?token=ejJtwle3T4)](https://codecov.io/gh/ph-piment/scraping-sandbox)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../../LICENSE)

---

## 📦 Projects Overview

### 📸 [`fotosource_scraper`](./fotosource_scraper/)

Scrapes the full list of store locations from [fotosource.com/store-selector](https://fotosource.com/store-selector).

- 🌎 Selects all dropdown regions dynamically
- 🏬 Extracts city, store name, address, phone, hours, link
- 💾 Outputs CSV: `./outputs/fotosource_scraper/stores.csv`
- ⚙️ Built with Playwright async + locator API

➡️ [View README](./fotosource_scraper/README.md)

---

### 📈 [`playwright_stock_scraper`](./playwright_stock_scraper/)

Scrapes historical stock data from Minkabu `/daily_bar` timeline using Playwright.

- 📊 Fetches OHLCV (Open/High/Low/Close/Volume)
- 🔁 Supports pagination via `次へ` button
- 💾 Outputs: `./outputs/playwright_stock_scraper/{symbol}.csv|json`
- 🛡 Bot-like detection mitigation via randomized delays

➡️ [View README](./playwright_stock_scraper/README.md)

---

### 🔎 [`rss_fetch_from_search`](./rss_fetch_from_search/)

Scrapes RSS feeds or search pages from Upwork to discover scraping-related jobs.

- 🔍 Extracts job titles, budgets, descriptions, verification flags
- 📡 Supports RSS & HTML-based job discovery
- 📤 Sends alerts to Slack via webhook
- 🐳 Designed for serverless / Lambda use

➡️ [View README](./rss_fetch_from_search/README.md)

---

## 🧪 Quality & Testing

Each project includes:

- ✅ Unit tests with `pytest`
- 🎨 Linting with `black`, `flake8`, `isort`, `mypy`
- 🔐 Security checks via `bandit`, `pip-audit`
- 📦 Central `requirements.txt`

```bash
# Run full quality suite
make lint-test
```

---

## 📂 Directory Structure

```bash
python/
├── fotosource_scraper/         # Store info scraper (Playwright)
├── playwright_stock_scraper/   # Stock OHLCV scraper from Minkabu
├── rss_fetch_from_search/      # Upwork job feed notifier
├── utils/                      # Shared helpers (browser, writer, error handling)
└── README.md                   # ← you are here
```
