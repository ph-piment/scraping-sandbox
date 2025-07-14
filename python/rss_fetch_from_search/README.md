# 📈 IR Extractor For US Stocks

[![codecov](https://codecov.io/gh/ph-piment/scraping-sandbox/graph/badge.svg?token=ejJtwle3T4)](https://codecov.io/gh/ph-piment/scraping-sandbox)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An asynchronous RSS fetcher that searches for GitHub repositories related to specific technology keywords and collects their /releases RSS feeds via privacy-friendly search engines.

---

## ✨ Features

- 🔍 Asynchronously searches GitHub repositories using Brave, Mojeek, or Bing
- 🧠 Ranks search results based on keyword relevance
- 🧵 Fully parallel scraping with Playwright (async)
- 💤 Adds random delays to avoid aggressive consecutive requests
- 📤 Collects /releases.atom RSS feed URLs for GitHub repositories
- 💾 Outputs to ./outputs/rss_fetch_from_search/techs.json
- ✅ Designed for low-volume, ethical scraping use cases
- 🧪 Comes with tests, typing, and CI-friendly linting

---

## 🔎 Use Case

You want to:

- Track OSS releases related to react, fastapi, redis, etc.
- Collect all /releases RSS feed URLs from GitHub
- Avoid commercial search APIs and use Mojeek/Brave Search scraping instead

---

## 📁 Example Output

```bash
{
  "react": {
    "rss": "https://github.com/facebook/react/releases.atom",
    "html": "https://github.com/facebook/react/releases"
  },
  "fastapi": {
    "rss": "https://github.com/tiangolo/fastapi/releases.atom",
    "html": "https://github.com/tiangolo/fastapi/releases"
  }
}
```

---

## 🚀 Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install
```
### 2. Prepare keywords
Put your technology keywords into a JSON file like:

```bash
{
  "0": { "name": "fastapi" },
  "1": { "name": "django" },
  "2": { "name": "react" },
  "3": { "name": "nextjs" },
  "4": { "name": "pytorch" },
  "5": { "name": "transformers" },
  "6": { "name": "langchain" },
  "7": { "name": "supabase" },
  "8": { "name": "playwright" },
  "9": { "name": "redis" }
}
```
Save it as:

```bash
inputs/rss_fetch_from_search/tech_keywords.json
```
### 3. Run the fetcher
```bash
PYTHONPATH=. python rss_fetch_from_search/main.py
```
Outputs will be saved to:

```bash
outputs/rss_fetch_from_search/techs.json
```

---

## 🧪 Testing & Quality

This repo includes built-in CI checks:

✅ pytest + coverage
🎨 black, isort, flake8, pylint, mypy
🔐 bandit, pip-audit for security
📦 Uses requirements.txt for consistent builds
To run tests locally:

```bash
PYTHONPATH=. pytest
```

---

## 📂 Project Structure

```bash
rss_fetch_from_search/
├── main.py              # CLI entrypoint
├── reader.py            # Loads tech keywords JSON
├── scraper.py           # Mojeek scraping + scoring logic
├── usecase.py           # Orchestration layer
├── tests/
│   ├── test_main.py
│   ├── test_reader.py
│   └── test_scraper.py
```

---

## 📄 Notes

- 🌐 Uses Mojeek.com instead of Bing or Google to avoid rate limits
- 📌 GitHub /releases.atom is the preferred RSS format
- 🧩 CAPTCHA handling is simple, may not work for all queries
- ✅ Designed for low-volume, educational, or prototyping use
