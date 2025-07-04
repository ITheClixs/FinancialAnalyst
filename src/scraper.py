import sqlite3
import time
from playwright.sync_api import sync_playwright # Changed to sync_playwright

DB_PATH = "stocks.db"

def create_table():
    """Create the stocks table if it does not exist.""" 
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
    """Save stock data to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO stocks (symbol, name, price) VALUES (?, ?, ?) 
    ''', (symbol, name, price))
    conn.commit()
    conn.close()

def run(): # Changed to def run()
    """Main function to run the scraping process."""
    print("Starting scraping process...")
    create_table()
    
    with sync_playwright() as p: # Changed to sync_playwright
        browser = p.chromium.launch(headless=True)  # Set to True for production
        page = browser.new_page()
        
        try:
            page.goto("https://finance.yahoo.com/markets/stocks/most-active/", wait_until="domcontentloaded", timeout=120000) # Increased timeout
            
            page.wait_for_timeout(10000) # Longer wait for dynamic content

            # Wait for the table to load
            page.wait_for_selector('table', timeout=60000) # Generic table selector, increased timeout
            
            # Get all table rows
            rows = page.locator('table tbody tr').all()
            print(f"Found {len(rows)} rows.")
            
            if len(rows) == 0:
                print("No rows found. Page might have changed structure.")
                return
            
            # Extract data from each row
            for i, row in enumerate(rows[:10]):  # Limit to first 10 for testing
                try:
                    cells = row.locator('td').all()
                    if len(cells) >= 3:
                        symbol = cells[0].inner_text()
                        name = cells[1].inner_text()
                        price = cells[3].inner_text()
                        
                        # Clean up the data
                        symbol = symbol.strip()
                        name = name.strip()
                        price = price.strip()
                        
                        print(f"{symbol} | {name} | Price: {price}")
                        save_stock(symbol, name, price)
                        
                except Exception as e:
                    print(f"Error processing row {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()

def scrape_stock_details(symbol):
    """Scrape news and analysis for a given stock symbol."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(f"https://finance.yahoo.com/quote/{symbol}", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(10000)

            # Scrape news
            news_headlines = []
            news_items = page.locator('li.js-stream-content').all()
            for item in news_items[:5]: # Get top 5 news
                headline = item.locator('h3').inner_text()
                link = item.locator('a').get_attribute('href')
                news_headlines.append({"headline": headline, "link": link})

            # Scrape analysis
            analysis = {}
            # This is a placeholder for more complex analysis scraping
            # For now, we'll just get some key stats
            pe_ratio = page.locator('td[data-test="PE_RATIO-value"]').inner_text()
            eps = page.locator('td[data-test="EPS_RATIO-value"]').inner_text()
            market_cap = page.locator('td[data-test="MARKET_CAP-value"]').inner_text()
            analysis["pe_ratio"] = pe_ratio
            analysis["eps"] = eps
            analysis["market_cap"] = market_cap

            return {"news": news_headlines, "analysis": analysis}

        except Exception as e:
            print(f"Error scraping details for {symbol}: {e}")
            return None
        finally:
            browser.close()
