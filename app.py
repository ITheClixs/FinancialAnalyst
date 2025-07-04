import os
from src import create_app
from src.scraper import create_table
from config import Config

app = create_app()

# Ensure the database table exists when the app starts
with app.app_context():
    create_table()

if __name__ == '__main__':
    app.run(debug=True)