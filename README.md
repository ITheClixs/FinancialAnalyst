# Financial Analyst Dashboard

## Overview

Financial Analyst Dashboard is a web application that scrapes real-time stock data from Yahoo Finance, stores it in a local SQLite database, and presents it through a modern, interactive web interface. Users can view a list of most active stocks, trigger new data scrapes, and click on individual stock cards to view detailed information, including company logos, price graphs, latest news, and key financial analysis.

---

## Features

-   **Real-time Stock Data Scraping:** Utilizes Playwright to scrape most active stock data from Yahoo Finance.
-   **Persistent Data Storage:** Stores scraped stock data in a local SQLite database (`stocks.db`).
-   **Interactive Web Interface:** Built with Flask, HTML, CSS, and JavaScript for a dynamic user experience.
-   **Modern UI/UX:** Features a vibrant purple theme, company logos, and small price graphs for each stock.
-   **Detailed Stock View:** Clicking on a stock card opens a modal displaying:
    -   A larger, detailed price graph.
    -   Latest news headlines with links.
    -   Key financial analysis metrics (e.g., Market Cap, PE Ratio, EPS).
-   **Asynchronous Operations:** Scraping processes run in a separate thread to avoid blocking the web application.
-   **Automatic Database Setup:** The database table is created automatically on the first run.

---

## Requirements

-   Python 3.9+
-   `Flask`
-   `playwright`
-   SQLite3 (comes pre-installed with Python)

### Python Dependencies

Install dependencies via:

```bash
pip install -r requirements.txt
```

Then install required browser binaries for Playwright:

```bash
playwright install
```

---

## Project Structure

```
FinancialAnalyst/
├── app.py                    # Main application entry point
├── config.py                 # Application configuration
├── requirements.txt          # Python dependencies
├── instance/
│   └── stocks.db             # SQLite database storing scraped stock data
├── src/
│   ├── __init__.py           # Initializes the Flask application
│   ├── routes.py             # Defines all web application routes (API endpoints and views)
│   └── scraper.py            # Contains the stock scraping logic
├── static/
│   ├── style.css             # Stylesheets for the web interface
│   └── script.js             # JavaScript for dynamic frontend functionality
├── templates/
│   └── index.html            # HTML template for the main dashboard
└── README.md                 # Project documentation
```

---

## How to Use

1.  **Set up the environment**

    Navigate to the project root and create a virtual environment (recommended):

    ```bash
    cd /path/to/FinancialAnalyst
    python3 -m venv venv
    source venv/bin/activate    # On Windows use `venv\Scripts\activate`
    ```

2.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3.  **Run the application**

    From the project root:

    ```bash
    python app.py
    ```

    The application will start, typically on `http://127.0.0.1:5000/`.

4.  **Access the Web Interface**

    Open your web browser and navigate to `http://127.0.0.1:5000/`.

5.  **Scrape Latest Data**

    Click the "Scrape Latest Data" button on the dashboard. The application will initiate the scraping process in the background, and the stock data will populate the dashboard after a short delay.

6.  **View Stock Details**

    Click on any stock card to open a modal window displaying a larger graph, the latest news headlines, and key financial analysis for that specific company.

7.  **Access the Database (Optional)**

    The scraped stock data is saved in `instance/stocks.db`. You can open this database using any SQLite viewer or via the command line:

    ```bash
    sqlite3 instance/stocks.db
    SELECT * FROM stocks;
    ```

---

## Notes

-   The database and `stocks` table are created automatically if they do not exist.
-   The database schema includes the following fields:

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