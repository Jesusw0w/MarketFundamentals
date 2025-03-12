from src.data_loader import DataLoader
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

data_loader = DataLoader(api_key=os.environ["alpha_api_key"])
print()