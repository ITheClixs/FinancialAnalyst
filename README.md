# FinancialAnalyst — Stock Scraper and Database Logger

## Overview

FinancialAnalyst is a Python-based asynchronous web scraper designed to collect the most active stock data from Yahoo Finance and store it in a local SQLite database. This tool leverages modern headless browsing via Playwright and reliable local data persistence using SQLite, making it suitable for stock data monitoring, financial analysis, or learning purposes.

---

## Features

- Asynchronous scraping with Playwright
- Scrapes Most Active Stocks from Yahoo Finance
- Extracts:
  - Stock Symbol
  - Company Name
  - Current Price
- Logs data into a SQLite database (`stocks.db`)
- Automatic table creation on first run
- Console output for real-time scraping feedback
- Error handling for missing data or page load failures
- Debug printing of page content if stock data is missing

---

## Requirements

- Python 3.9+
- `playwright`
- SQLite3 (comes pre-installed with Python)

### Python Dependencies

Install dependencies via:

```bash
pip install playwright
```

Then install required browser binaries:

```bash
playwright install
```

---

## Project Structure

```
FinancialAnalyst/
├── data/
│   └── requirements.txt      # Lists Python dependencies (currently only playwright)
├── src/
│   └── scraper.py            # Main stock scraper source code
├── venv/                     # Python virtual environment directory (optional)
├── stocks.db                 # SQLite database storing scraped stock data
├── .gitignore                # Git ignore rules (e.g., to exclude venv, __pycache__)
└── README.md                 # Project documentation
```

### File and Directory Functions

- `data/requirements.txt`: Specifies the Python dependencies required for the project, facilitating environment setup.
- `src/scraper.py`: Contains the main scraper script that collects and saves stock data asynchronously.
- `venv/`: The Python virtual environment directory used to isolate project dependencies (commonly excluded from version control).
- `stocks.db`: The SQLite database file where scraped stock records are stored.
- `.gitignore`: Defines files and directories that Git should ignore, typically including the virtual environment and compiled files.

---

## How to Use

1. **Set up the environment**

   Navigate to the project root and create a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies**

   ```bash
   pip install -r data/requirements.txt
   playwright install
   ```

3. **Run the scraper**

   From the project root:

   ```bash
   python src/scraper.py
   ```

4. **Access the database**

   - The scraped stock data is saved in `stocks.db`.
   - You can open this database using any SQLite viewer or via command line:

     ```bash
     sqlite3 stocks.db
     SELECT * FROM stocks;
     ```

---

## Notes

- The scraper attempts to click the cookie consent button if it appears.
- If no stock rows are found on the page, the scraper prints the page content for debugging.
- The database and `stocks` table are created automatically if they do not exist.
- The database schema includes the following fields:

  ```
  id           INTEGER PRIMARY KEY AUTOINCREMENT
  symbol       TEXT
  name         TEXT
  price        TEXT
  scraped_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ```

---

## License

This project is open-source and available for educational and personal use.

---

## Contributions

Contributions and improvements are welcome. Feel free to fork the repository and submit pull requests.
