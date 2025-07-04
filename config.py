import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'stocks.db')
