#!/usr/bin/env python
"""Entry point script for running the Telegram Bot for Torrent Downloader"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Check for required Telegram token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    print("\n" + "="*60)
    print("ERROR: Telegram Bot Token Not Found")
    print("="*60)
    print("\nTo run the Telegram bot, you need to set TELEGRAM_BOT_TOKEN in .env")
    print("\nSteps:")
    print("1. Create a bot with BotFather on Telegram (@BotFather)")
    print("2. Copy the token provided")
    print("3. Add to .env file:")
    print("   TELEGRAM_BOT_TOKEN=<your_token_here>")
    print("\nOptional settings in .env:")
    print("   API_URL=http://localhost:8000  (default is localhost)")
    print("   MOVIES_ROOT_FOLDER=<path>      (optional, for movies)")
    print("   SERIES_ROOT_FOLDER=<path>      (optional, for series)")
    print("="*60 + "\n")
    sys.exit(1)

# Add repo to path so we can import telegram_bot module
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import and run the bot
try:
    from telegram_bot.bot import main
    
    print("\n" + "="*60)
    print("Torrent Downloader - Telegram Bot")
    print("="*60)
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    api_url = os.getenv("API_URL", "http://localhost:8000")
    print(f"API URL: {api_url}")
    print("\nThe bot is starting...")
    print("Send /start to see available commands")
    print("Press Ctrl+C to stop the bot")
    print("="*60 + "\n")
    
    main()
    
except KeyboardInterrupt:
    print("\n\nBot stopped by user (Ctrl+C)")
    sys.exit(0)
except ImportError as e:
    print(f"\nERROR: Failed to import telegram bot module: {e}")
    print("\nMake sure you have installed the required dependencies:")
    print("  pip install -r telegram_bot/requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
