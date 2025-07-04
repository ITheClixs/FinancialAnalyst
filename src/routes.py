from flask import Blueprint, render_template, jsonify
import sqlite3
import threading
import asyncio
from .scraper import run as scrape_run, scrape_stock_details
from config import Config

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/stocks')
def get_stocks():
    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT symbol, name, price, scraped_at FROM stocks ORDER BY scraped_at DESC LIMIT 10')
    stocks = c.fetchall()
    conn.close()
    
    stock_list = []
    for stock in stocks:
        stock_list.append({
            'symbol': stock[0],
            'name': stock[1],
            'price': stock[2],
            'scraped_at': stock[3],
            'logo_url': f"https://logo.clearbit.com/{stock[1].replace(' ', '').replace('.', '')}.com",
            'graph_url': f"https://finviz.com/chart.ashx?t={stock[0]}&ty=c&ta=1&p=d&s=l"
        })
    return jsonify(stock_list)

@bp.route('/api/stock/<symbol>')
def get_stock_details_route(symbol):
    details = scrape_stock_details(symbol)
    if details:
        return jsonify(details)
    else:
        return jsonify({"error": "Could not fetch details"}), 404

@bp.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    def run_scraper_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coroutine = scrape_run()
        if asyncio.iscoroutine(coroutine):
            loop.run_until_complete(coroutine)
        else:
            scrape_run()
        loop.close()
    threading.Thread(target=run_scraper_in_thread).start()
    return jsonify({'message': 'Scraping initiated!'}), 202
