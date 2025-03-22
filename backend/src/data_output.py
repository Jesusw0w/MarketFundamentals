import pandas as pd
import json
import os
from datetime import datetime

class DataOutput:
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the DataOutput class.

        Args:
            output_dir (str): The directory where output files will be saved (default: "output").
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    def save_to_excel(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Save a DataFrame to an Excel file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            filename (str): The name of the Excel file. If not provided, a timestamped filename will be used.

        Returns:
            str: The path to the saved Excel file.
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.xlsx"

        filepath = os.path.join(self.output_dir, filename)
        df.to_excel(filepath, index=True)
        print(f"Data saved to Excel file: {filepath}")
        return filepath

    def save_to_json(self, data: dict|pd.DataFrame, filename: str = None) -> str:
        """
        Save data (dict or DataFrame) to a JSON file.

        Args:
            data (dict or pd.DataFrame): The data to save.
            filename (str): The name of the JSON file. If not provided, a timestamped filename will be used.

        Returns:
            str: The path to the saved JSON file.
        """
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to JSON file: {filepath}")
        return filepath

    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Save a DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            filename (str): The name of the CSV file. If not provided, a timestamped filename will be used.

        Returns:
            str: The path to the saved CSV file.
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.csv"

        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=True)
        print(f"Data saved to CSV file: {filepath}")
        return filepath

    def save_to_multiple_formats(self, df: pd.DataFrame, base_filename: str = None) -> dict:
        """
        Save a DataFrame to multiple formats (Excel, JSON, and CSV).

        Args:
            df (pd.DataFrame): The DataFrame to save.
            base_filename (str): The base name for the files. If not provided, a timestamped name will be used.

        Returns:
            dict: A dictionary containing the paths to the saved files.
        """
        if not base_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"data_{timestamp}"

        excel_file = self.save_to_excel(df, f"{base_filename}.xlsx")
        json_file = self.save_to_json(df, f"{base_filename}.json")
        csv_file = self.save_to_csv(df, f"{base_filename}.csv")

        return {
            "excel": excel_file,
            "json": json_file,
            "csv": csv_file
        }