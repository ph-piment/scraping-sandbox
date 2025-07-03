# 📈 Minkabu Timeline Scraper

An elegant, asynchronous scraper for historical stock data from [Minkabu](https://minkabu.jp/), built with [Playwright for Python](https://playwright.dev/python/).

---

## ✨ Features

- ✅ Async scraping via Playwright (headless)
- 📄 Targets `/daily_bar` timeline for a given stock symbol
- 🔍 Extracts: `Date`, `Open`, `High`, `Low`, `Close`, `Volume`
- 🔁 Handles pagination by clicking `次へ`
- 💾 Outputs `{symbol}_output.csv`
- 🛠 Includes basic error handling & retry logic

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
PYTHONPATH=. python minkabu_timeline_scraper/main.py 281A
```
Replace 281A with any valid Minkabu stock symbol (e.g., 6501, 7203, etc).

### 3. Output sample

Creates a CSV like 281A_output.csv:

```bash
Date,Open,High,Low,Close,Volume
2025/07/01,1570,1590,1550,1560,1,234,000
2025/06/28,1540,1580,1530,1570,1,002,000
...
```

## 🧪 Testing & Quality

This repo includes built-in CI checks:

✅ pytest + coverage
🎨 black, isort, flake8, pylint, mypy
🔐 bandit, pip-audit for security
📦 Uses requirements.txt for consistent builds
To run tests locally:

```
PYTHONPATH=. pytest
```

## 📄 Notes

- ✅ Minkabu's /stock/{symbol} is allowed in robots.txt
- 🧘‍♂️ Includes sleep between pages to avoid overloading the server
- 🚫 Use responsibly — this is for educational/demo use only

## 📂 Project Structure

```bash
minkabu_timeline_scraper/
├── main.py                 # CLI entrypoint
├── scraper.py              # Scraper logic
├── tests/
│   └── test_scraper.py     # Basic unit tests
├── requirements.txt
└── README.md
```
