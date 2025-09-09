import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "google/gemini-flash-1.5"
CSV_FILE = "candidates.csv"
