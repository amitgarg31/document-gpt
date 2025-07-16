from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")