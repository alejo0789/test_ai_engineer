import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to load settings from environment variables.
    """
    # Google API Key for Gemini LLM
    # This key should be stored securely in the .env file.
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

    # Number of top documents to retrieve from the FAISS index
    # Default to 2 if not specified in .env
    TOP_K_DOCS: int = int(os.getenv("TOP_K_DOCS", 2))

    # Name of the Gemini model to use for generating responses
    # Default to "gemini-pro" if not specified, adjust as needed (e.g., "gemini-2.0-flash")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME")

    # Paths for data files
    # Ensure these paths are correct relative to where the script is run or adjusted for Docker
    PRODUCTS_DATA_PATH: str = "data/products.json"
    DOCS_DATA_PATH: str = "data/docs.json"
    FAISS_INDEX_PATH: str = "data/faiss.index"

    def __init__(self):
        # Basic validation for essential configurations
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        if not self.TOP_K_DOCS:
            raise ValueError("TOP_K_DOCS environment variable not set or invalid.")
        if not self.GEMINI_MODEL_NAME:
            raise ValueError("GEMINI_MODEL_NAME environment variable not set.")

# Instantiate the Config to be easily imported elsewhere
settings = Config()