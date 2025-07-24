# 📸 FotoSource Store Scraper

[![codecov](https://codecov.io/gh/ph-piment/scraping-sandbox/graph/badge.svg?token=ejJtwle3T4)](https://codecov.io/gh/ph-piment/scraping-sandbox)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An asynchronous web scraper for Canadian photo store listings from [FotoSource](https://fotosource.com/store-selector), powered by [Playwright for Python](https://playwright.dev/python/).

---

## ✨ Features

- ✅ Async scraping using Playwright (headless mode)
- 🗺 Selects regions dynamically from the dropdown
- 🏪 Extracts per-store info:
  - region, city, name, address, phone, status, hours, link
- 💾 Outputs clean CSV at ./outputs/fotosource_scraper/stores.csv
- 🧪 Includes unit tests with mocks for scrape/save logic

## 🗂 Scraping Target

This tool scrapes store listings from:

🔗 https://fotosource.com/store-selector

It loops through all selectable regions and collects structured data per store, including website links and contact info.

---

## 🚀 Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

💡 playwright install is required to download the browser binaries.

### 2. Run the scraper
```bash
PYTHONPATH=. python fotosource_scraper/main.py
```

Example output:
```bash
✅ Scraping https://fotosource.com/store-selector
🌎 Selecting region: Alberta
...
✅ Scraped 1170 rows
✅ Saved to CSV File(outputs/fotosource_scraper/stores.csv)
```

### 3. Output sample

./outputs/fotosource_scraper/stores.csv:

```csv
region,city,name,address,phone,status,hours,link
Alberta,"Antigonish, NS, Canada",The Photo Shop at the 5-100 Foto Source,"245 Main Street, P.O. Box 1538",(902) 863-2571,OPEN,- until 9:00 PM,https://thephotoshop.fotosource.com
Alberta,"Belleville, ON, Canada",Japan Camera - Belleville,"366 North Front St, Bay Camera Limited",(613) 966-5056,OPEN,- until 9:00 PM,https://japancamerabelleville.com/
...
```

## 📄 Notes

- ✅ robots.txt allows access to /store-selector
- 🧘‍♂️ Uses controlled waits between actions to simulate human behavior
- 📊 Suitable for data analysis or location mapping
- 📦 Easily extendable to JSON or DB output

## 📂 Project Structure

```bash
fotosource_scraper/
├── main.py                 # CLI entrypoint
├── scraper.py              # Core scraping logic
├── usecase.py              # Run + Save orchestration
├── tests/
│   └── test_usecase.py     # Use case test with mocks
├── outputs/
│   └── fotosource_scraper/ # Output directory
└── utils/
    ├── playwright.py       # Playwright context helpers
    ├── writer.py           # save_csv utilities
    └── error_handling.py   # Centralized error handler
```
