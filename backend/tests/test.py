import os
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from backend.src.data_loader import DataLoader
from backend.src.data_processor import DataProcessor
from backend.src.data_output import DataOutput

# Test symbols
tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

def test_data_loader():
    """Test the DataLoader class functionality"""
    print("\n=== Testing DataLoader ===")
    
    # Initialize DataLoader with API key from environment variable
    loader = DataLoader()
    
    # Test getting stock price
    print("\nTesting get_stock_price:")
    stock_price = loader.get_stock_price('AAPL')
    print(f"AAPL stock price data: {list(stock_price.keys())}")
    
    # Test getting company overview
    print("\nTesting get_company_overview:")
    company_overview = loader.get_company_overview('MSFT')
    print(f"MSFT company overview: {list(company_overview.keys())[:5]}...")
    
    # Test getting sector performance
    print("\nTesting get_sector_performance:")
    sector_perf = loader.get_sector_performance()
    print(f"Sector performance data: {list(sector_perf.keys())}")
    
    # Test getting income statement
    print("\nTesting get_income_statement:")
    income_stmt = loader.get_income_statement('GOOG')
    print(f"GOOG income statement data: {list(income_stmt.keys())}")
    
    # Test getting bulk data (limited to 2 symbols to avoid rate limiting)
    print("\nTesting get_bulk_data (limited sample):")
    bulk_data = loader.get_bulk_data(tickers[:2], function="TIME_SERIES_DAILY")
    print(f"Bulk data symbols: {list(bulk_data.keys())}")
    
    return loader

def test_data_processor(loader):
    """Test the DataProcessor class functionality"""
    print("\n=== Testing DataProcessor ===")
    
    processor = DataProcessor()
    
    # Get some data to process
    stock_data = loader.get_stock_price('AAPL')
    time_series_data = loader.get_bulk_data(['AAPL'], function="TIME_SERIES_DAILY")['AAPL']
    
    # Test JSON to DataFrame conversion
    print("\nTesting json_to_dataframe:")
    df = processor.json_to_dataframe(time_series_data, nested_key="Time Series (Daily)")
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns.tolist()}")
    print(f"DataFrame head:\n{df.head(3)}")
    
    # Test cleaning stock data
    print("\nTesting clean_stock_data:")
    cleaned_df = processor.clean_stock_data(df)
    print(f"Cleaned DataFrame columns: {cleaned_df.columns.tolist()}")
    print(f"Cleaned DataFrame head:\n{cleaned_df.head(3)}")
    
    # Test calculating returns
    print("\nTesting calculate_returns:")
    returns_df = processor.calculate_returns(cleaned_df)
    print(f"Returns DataFrame columns: {returns_df.columns.tolist()}")
    print(f"Returns DataFrame head:\n{returns_df[['Close', 'Daily Return', 'Cumulative Return']].head(3)}")
    
    # Test calculating moving average
    print("\nTesting calculate_moving_average:")
    ma_df = processor.calculate_moving_average(cleaned_df, window=10)
    print(f"Moving Average DataFrame head:\n{ma_df[['Close', 'Moving Average']].head(3)}")
    
    # Test filtering by date
    print("\nTesting filter_by_date:")
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    filtered_df = processor.filter_by_date(ma_df, start_date, end_date)
    print(f"Filtered DataFrame shape: {filtered_df.shape}")
    print(f"Date range: {filtered_df.index.min()} to {filtered_df.index.max()}")
    
    return processor, filtered_df

def test_data_output(processor, df):
    """Test the DataOutput class functionality"""
    print("\n=== Testing DataOutput ===")
    
    output = DataOutput(output_dir="test_output")
    
    # Test saving to Excel
    print("\nTesting save_to_excel:")
    excel_path = output.save_to_excel(df, "apple_stock_data.xlsx")
    
    # Test saving to JSON
    print("\nTesting save_to_json:")
    json_path = output.save_to_json(df, "apple_stock_data.json")
    
    # Test saving to CSV
    print("\nTesting save_to_csv:")
    csv_path = output.save_to_csv(df, "apple_stock_data.csv")
    
    # Test saving to multiple formats
    print("\nTesting save_to_multiple_formats:")
    multi_paths = output.save_to_multiple_formats(df, "apple_stock_data_multi")
    
    return output, multi_paths

def visualize_data(df):
    """Create and save some visualizations of the data"""
    print("\n=== Creating Visualizations ===")
    
    # Create output directory for plots
    plot_dir = "test_output/plots"
    os.makedirs(plot_dir, exist_ok=True)
    
    # Plot stock price
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['Moving Average'], label='10-day MA', linestyle='--')
    plt.title('Stock Price and Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = os.path.join(plot_dir, 'stock_price_ma.png')
    plt.savefig(plot_path)
    print(f"Saved plot to: {plot_path}")
    
    # Plot returns
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Cumulative Return'], label='Cumulative Return')
    plt.title('Cumulative Return')
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = os.path.join(plot_dir, 'cumulative_return.png')
    plt.savefig(plot_path)
    print(f"Saved plot to: {plot_path}")

def test_bulk_data():
    """Test bulk data loading and processing for multiple tickers"""
    print("\n=== Testing Bulk Data Processing ===")
    
    loader = DataLoader()
    processor = DataProcessor()
    output = DataOutput(output_dir="test_output/bulk")
    
    # Get data for a subset of tickers to avoid rate limiting
    test_tickers = tickers[:2]
    bulk_data = loader.get_bulk_data(test_tickers, function="TIME_SERIES_DAILY")
    
    results = {}
    for symbol, data in bulk_data.items():
        print(f"\nProcessing {symbol}...")
        
        # Convert to DataFrame
        df = processor.json_to_dataframe(data, nested_key="Time Series (Daily)")
        
        # Clean data
        df = processor.clean_stock_data(df)
        
        # Calculate metrics
        df = processor.calculate_returns(df)
        df = processor.calculate_moving_average(df)
        
        # Filter to recent data
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        df = processor.filter_by_date(df, start_date, end_date)
        
        # Save results
        output.save_to_multiple_formats(df, f"{symbol}_processed")
        
        results[symbol] = df
    
    return results

def run_all_tests():
    """Run all tests"""
    loader = test_data_loader()
    processor, processed_df = test_data_processor(loader)
    output, paths = test_data_output(processor, processed_df)
    visualize_data(processed_df)
    bulk_results = test_bulk_data()
    
    print("\n=== All Tests Completed Successfully ===")
    return {
        "loader": loader,
        "processor": processor,
        "output": output,
        "processed_data": processed_df,
        "bulk_results": bulk_results
    }

if __name__ == "__main__":
    results = run_all_tests()
