import pandas as pd

class DataProcessor:
    def __init__(self):
        """
        Initialize the DataProcessor.
        """
        pass

    def json_to_dataframe(self, data: dict, nested_key: str = None) -> pd.DataFrame:
        """
        Convert JSON data (e.g., from Alpha Vantage API) into a pandas DataFrame.

        Args:
            data (dict): The JSON data to convert.
            nested_key (str): The key in the JSON data that contains the nested data (e.g., "Time Series (Daily)").

        Returns:
            pd.DataFrame: A DataFrame containing the processed data.
        """
        if nested_key:
            data = data.get(nested_key, {})
        
        if not data:
            raise ValueError("No data found in the provided JSON.")

        # Convert JSON to DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')
        
        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        
        # Convert columns to numeric
        df = df.apply(pd.to_numeric, errors='coerce')
        
        return df

    def clean_stock_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize stock data DataFrame.

        Args:
            df (pd.DataFrame): The raw stock data DataFrame.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        # Rename columns to be more descriptive
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })

        # Drop any rows with missing values
        df = df.dropna()

        return df

    def calculate_returns(self, df: pd.DataFrame, price_column: str = 'Close') -> pd.DataFrame:
        """
        Calculate daily and cumulative returns for a stock.

        Args:
            df (pd.DataFrame): The stock data DataFrame.
            price_column (str): The column containing the price data (default: 'Close').

        Returns:
            pd.DataFrame: The DataFrame with added 'Daily Return' and 'Cumulative Return' columns.
        """
        df['Daily Return'] = df[price_column].pct_change()
        df['Cumulative Return'] = (1 + df['Daily Return']).cumprod()
        
        return df

    def calculate_moving_average(self, df: pd.DataFrame, price_column: str = 'Close', window: int = 20) -> pd.DataFrame:
        """
        Calculate the moving average for a stock.

        Args:
            df (pd.DataFrame): The stock data DataFrame.
            price_column (str): The column containing the price data (default: 'Close').
            window (int): The window size for the moving average (default: 20).

        Returns:
            pd.DataFrame: The DataFrame with an added 'Moving Average' column.
        """
        df['Moving Average'] = df[price_column].rolling(window=window).mean()
        
        return df

    def merge_data(self, dfs: list, on: str = 'Date', how: str = 'inner') -> pd.DataFrame:
        """
        Merge multiple DataFrames on a common column (e.g., 'Date').

        Args:
            dfs (list): A list of DataFrames to merge.
            on (str): The column to merge on (default: 'Date').
            how (str): The type of merge to perform (default: 'inner').

        Returns:
            pd.DataFrame: The merged DataFrame.
        """
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = pd.merge(merged_df, df, on=on, how=how)
        
        return merged_df

    def filter_by_date(self, df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter a DataFrame by date range.

        Args:
            df (pd.DataFrame): The DataFrame to filter.
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        mask = (df.index >= start_date) & (df.index <= end_date)
        return df.loc[mask]