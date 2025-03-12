import requests
import time
import os

class DataLoader:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str = None):
        """
        Initialize the DataLoader with an API key.
        """
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("Alpha Vantage API key is required.")

    def _fetch_data(self, params: dict) -> dict:
        """
        Private method to handle API requests with rate limit management.
        """
        params["apikey"] = self.api_key
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise ConnectionError(f"API request failed: {response.status_code}")

        data = response.json()

        # Check for rate limit message
        if "Note" in data:
            print("Rate limit exceeded, waiting for 60 seconds...")
            time.sleep(60)
            return self._fetch_data(params)  # Retry after waiting

        return data

    def get_bulk_data(self, symbols: list, function="TIME_SERIES_QUARTERLY_ADJUSTED") -> dict:
        """
        Fetch bulk financial data (default: quarterly adjusted time series) for multiple stocks.
        """
        results = {}

        for symbol in symbols:
            print(f"Fetching data for {symbol}...")
            params = {
                "function": function,
                "symbol": symbol,
                "outputsize": "full"
            }
            results[symbol] = self._fetch_data(params)
            time.sleep(15)  # Alpha Vantage rate limit: 5 requests per minute

        return results

    def get_stock_price(self, symbol: str) -> dict:
        """
        Fetch the latest stock price for a given symbol.
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol
        }
        return self._fetch_data(params)

    def get_company_overview(self, symbol: str) -> dict:
        """
        Fetch fundamental company data such as market cap, EPS, and description.
        """
        params = {
            "function": "OVERVIEW",
            "symbol": symbol
        }
        return self._fetch_data(params)

    def get_sector_performance(self) -> dict:
        """
        Fetch sector performance data.
        """
        params = {"function": "SECTOR"}
        return self._fetch_data(params)

    def get_income_statement(self, symbol: str):
        """
        Fetch income statement data.
        """
        params = {"function": "INCOME_STATEMENT",
                  "symbol": symbol
        }
        return self._fetch_data(params)
