import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = REPO_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

API_LOG_FILE = LOGS_DIR / "torrent_api.log"
TELEGRAM_LOG_FILE = LOGS_DIR / "telegram_bot.log"


def configure_api_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # File handler for API
    fh = RotatingFileHandler(str(API_LOG_FILE), maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Avoid adding duplicate handlers
    if not any(isinstance(h, RotatingFileHandler) and h.baseFilename == str(API_LOG_FILE) for h in root.handlers if hasattr(h, 'baseFilename')):
        root.addHandler(ch)
        root.addHandler(fh)


def configure_telegram_logging(level=logging.INFO):
    logger = logging.getLogger("telegram_bot")
    logger.setLevel(level)

    # File handler for telegram bot only
    fh = RotatingFileHandler(str(TELEGRAM_LOG_FILE), maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8')
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Console handler scoped to telegram bot
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    if not any(getattr(h, 'baseFilename', None) == str(TELEGRAM_LOG_FILE) for h in logger.handlers):
        logger.addHandler(ch)
        logger.addHandler(fh)
