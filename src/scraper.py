import asyncio
import sqlite3
from playwright.async_api import async_playwright

DB_PATH = "stocks.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            name TEXT,
            price TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_stock(symbol, name, price):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO stocks (symbol, name, price) VALUES (?, ?, ?)
    ''', (symbol, name, price))
    conn.commit()
    conn.close()

async def run():
    print("Starting scraping process...")
    create_table()  # ensure table exists

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://finance.yahoo.com/most-active", wait_until="networkidle", timeout=60000)

        try:
            await page.locator('button:has-text("Accept all")').click(timeout=5000)
        except:
            pass

        try:
            await page.wait_for_selector('tr.simpTblRow', timeout=15000)
        except:
            print("Timeout waiting for table rows")

        rows = await page.locator('tr.simpTblRow').all()
        print(f"Found {len(rows)} rows.")

        for row in rows:
            cells = await row.locator('td').all_text_contents()
            if len(cells) >= 3:
                symbol = cells[0]
                name = cells[1]
                price = cells[2]
                print(f"{symbol} | {name} | {price}")

                save_stock(symbol, name, price)  # save to DB

        await browser.close()

asyncio.run(run())





