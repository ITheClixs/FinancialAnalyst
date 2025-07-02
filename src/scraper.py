import yfinance as yf
import sqlite3

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
            price REAL,
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

def run():
    """Main function to run the scraping process."""
    print("Starting scraping process...")
    create_table()

    try:
        # Get the most active stocks
        most_active = yf.Tickers(yf.Screener().get_screeners('most_actives')['most_actives']['quotes'])
        
        print(f"Found {len(most_active.tickers)} most active stocks.")

        for ticker in most_active.tickers:
            try:
                info = ticker.info
                symbol = info.get('symbol')
                name = info.get('longName')
                price = info.get('regularMarketPrice')

                if symbol and name and price:
                    print(f"{symbol} | {name} | {price}")
                    save_stock(symbol, name, price)
            except Exception as e:
                print(f"Error processing ticker: {e}")
                continue

    except Exception as e:
        print(f"Error during scraping: {e}")

if __name__ == "__main__":
    run()