# main.py
import sys
import asyncio
from scraper import scrape

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <symbol>")
        sys.exit(1)

    symbol = sys.argv[1]

    try:
        asyncio.run(scrape(symbol))
    except Exception as e:
        print(f"❌ Error: {e}")
