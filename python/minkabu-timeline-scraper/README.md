# Minkabu Timeline Scraper 📈

This script scrapes historical stock data from the [Minkabu](https://minkabu.jp/) stock detail page using [Playwright](https://playwright.dev/python/).  
It handles pagination and outputs the result as a CSV file.

---

## 📌 Features

- Headless scraping using Playwright (async)
- Target: Minkabu's `/daily_bar` page for a stock symbol
- Extracts Date, Open, High, Low, Close, Volume
- Clicks through pages with "次へ" button
- Outputs data to `{symbol}_output.csv`
- Includes basic error handling

---

## 🚀 Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

💡 playwright install is required to download the browser binaries.

### 2. Run the script
```bash
python scraper.py 281A
```
Replace 281A with any valid Minkabu stock symbol (e.g., 6501, 7203, etc).

## 🧪 Output Sample

Output file will be named like 281A_output.csv.

```bash
Date,Open,High,Low,Close,Volume
2025/07/01,1570,1590,1550,1560,1,234,000
2025/06/28,1540,1580,1530,1570,1,002,000
...
```

## 📄 Notes

- Minkabu allows scraping of /stock/{symbol} URLs per their robots.txt.
- Do not overwhelm the site with frequent requests. This script includes a small delay between pages.
- Educational use only. Respect the target website and its terms of service.

## 📂 File Structure

```bash
minkabu-timeline-scraper/
├── scraper.py
├── requirements.txt
└── README.md
```
