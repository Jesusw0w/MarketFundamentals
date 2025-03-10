from backend.src.data_loader import *
tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

def test_bulk_data():
    assert DataLoader.bulk_data(tickers)