from flask import Flask, render_template, jsonify
import sqlite3
import threading
import asyncio
from src.scraper import run as scrape_run, DB_PATH, create_table

app = Flask(__name__)

# Ensure the database table exists when the app starts
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT symbol, name, price, scraped_at FROM stocks ORDER BY scraped_at DESC LIMIT 10')
    stocks = c.fetchall()
    conn.close()
    
    # Convert to a list of dictionaries for JSON response
    stock_list = []
    for stock in stocks:
        stock_list.append({
            'symbol': stock[0],
            'name': stock[1],
            'price': stock[2],
            'scraped_at': stock[3]
        })
    return jsonify(stock_list)

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    # Run the scraping in a separate thread to avoid blocking the Flask app
    # Note: For production, consider a proper task queue (e.g., Celery)
    threading.Thread(target=lambda: asyncio.run(scrape_run())).start()
    return jsonify({'message': 'Scraping initiated!'}), 202

if __name__ == '__main__':
    app.run(debug=True)
