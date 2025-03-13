from celery import Celery
from ..src.data_loader import DataLoader
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery('tasks', broker='redis://localhost:6379/0')

loader = DataLoader(api_key=os.environ.get("ALPHA_VANTAGE_API_KEY"))

# Celery tasks
@app.task
def refresh_stock_price(symbol: str):
    """
    Fetch and cache the latest stock price for a given symbol.
    """
    return loader.get_stock_price(symbol)

@app.task
def refresh_company_overview(symbol: str):
    """
    Fetch and cache fundamental company data such as market cap, EPS, and description.
    """
    return loader.get_company_overview(symbol)

@app.task
def refresh_sector_performance():
    """
    Fetch and cache sector performance data.
    """
    return loader.get_sector_performance()

@app.task
def refresh_income_statement(symbol: str):
    """
    Fetch and cache income statement data.
    """
    return loader.get_income_statement(symbol)

@app.task
def refresh_bulk_data(symbols: list, function="TIME_SERIES_QUARTERLY_ADJUSTED"):
    """
    Fetch and cache bulk financial data (default: quarterly adjusted time series) for multiple stocks.
    """
    return loader.get_bulk_data(symbols, function)