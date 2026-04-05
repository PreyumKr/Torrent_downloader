"""Configuration management for the torrent downloader API"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Setup logging to file
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "torrent_downloader.log"

# Create file handler with explicit flushing
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

class Config:
    """Application configuration"""
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Aria2 Settings
    ARIA2_ENABLED = os.getenv("ARIA2_ENABLED", "true").lower() == "true"
    ARIA2_PORT = os.getenv("ARIA2_PORT", "6800")
    ARIA2_RPC_URL = os.getenv("ARIA2_RPC_URL", f"ws://localhost:{ARIA2_PORT}/jsonrpc")
    ARIA2_SECRET = os.getenv("ARIA2_SECRET", "")
    
    # Pirate Bay API Settings
    TORRENT_DOWNLOAD_TIMEOUT = int(os.getenv("TORRENT_DOWNLOAD_TIMEOUT", "300"))
    
    # Ollama Settings (for series torrent selection)
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
    
    # Download Settings - Convert to absolute path
    _download_folder = os.getenv("DEFAULT_DOWNLOAD_FOLDER", "./downloads")
    DEFAULT_DOWNLOAD_FOLDER = str(Path(_download_folder).expanduser().resolve().absolute())
    MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "3"))
    
    # Scraping Settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # Series Info Settings
    GOOGLE_SEARCH_ENABLED = os.getenv("GOOGLE_SEARCH_ENABLED", "true").lower() == "true"


config = Config()
