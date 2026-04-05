#!/usr/bin/env python3
"""Telegram bot for the Torrent Downloader API.

This bot supports both immediate commands and a short conversational flow.

Behavior:
- `/movie <name> [year]` — start a movie download immediately when name is provided.
- `/series <name> [year]` — start a series download immediately when name is provided.
- `/other <name>` — start a download saved under the default download folder.

If a command is sent without arguments, the bot will prompt for the missing
fields (name -> optional year -> optional folder) and then start the download.

The bot sends `existing_items` (list of items in the destination root) to the
API so the LLM/server can check whether the item is already present.

Rate Limiting: Users are limited to 1 movie or series request per minute.

Required env vars (in project `.env` or environment):
- `TELEGRAM_BOT_TOKEN`

Optional env vars:
- `API_URL` (default: http://localhost:8000)
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import csv
import time
from datetime import datetime, timedelta

# Ensure repository root is on sys.path so `import app` works when running
# the bot from the repo root (python telegram_bot\bot.py)
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.config import config
import requests

# Read and validate API URL
API_URL = os.getenv("API_URL", "http://localhost:8000").strip()
if not API_URL:
    API_URL = "http://localhost:8000"
# Ensure URL has a scheme
if not API_URL.startswith(("http://", "https://")):
    API_URL = f"http://{API_URL}"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

DEFAULT_FOLDER = str(config.DEFAULT_DOWNLOAD_FOLDER)
MOVIES_ROOT = getattr(config, "MOVIES_ROOT_FOLDER", None)
SERIES_ROOT = getattr(config, "SERIES_ROOT_FOLDER", None)

# Rate limiting: one movie/series request per minute per user
RATE_LIMIT_SECONDS = 60
USERS_CSV = Path(__file__).parent.parent / "telegram_users.csv"


def init_users_csv():
    """Initialize or ensure the users CSV file exists with headers."""
    if not USERS_CSV.exists():
        with open(USERS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'username', 'first_name', 'first_login', 'last_download_time', 'total_downloads'])
        print(f"[INFO] Created users tracking file: {USERS_CSV}")


def get_user_record(user_id: int) -> dict | None:
    """Retrieve a user record from CSV by user_id."""
    if not USERS_CSV.exists():
        return None
    try:
        with open(USERS_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['user_id']) == user_id:
                    return row
    except Exception as e:
        print(f"[WARN] Error reading user record: {e}")
    return None


# Ensure the users CSV exists early (idempotent). This helps when the bot
# is started in environments where post-startup hooks may not run or fail.
try:
    init_users_csv()
except Exception as e:
    print(f"[WARN] Could not ensure users CSV on startup: {e}")


def update_user_record(user_id: int, username: str, first_name: str):
    """Update or create a user record in CSV."""
    init_users_csv()
    rows = []
    user_found = False
    
    try:
        with open(USERS_CSV, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Check if user exists
        for row in rows:
            if int(row['user_id']) == user_id:
                user_found = True
                break
        
        # If user doesn't exist, add them
        if not user_found:
            rows.append({
                'user_id': user_id,
                'username': username or '',
                'first_name': first_name or '',
                'first_login': datetime.now().isoformat(),
                'last_download_time': '',
                'total_downloads': 1
            })
        else:
            # Update last_download_time and increment count
            for row in rows:
                if int(row['user_id']) == user_id:
                    row['last_download_time'] = datetime.now().isoformat()
                    row['total_downloads'] = str(int(row.get('total_downloads', 0)) + 1)
                    row['username'] = username or row.get('username', '')
                    row['first_name'] = first_name or row.get('first_name', '')
                    break
        
        # Write back to CSV
        with open(USERS_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['user_id', 'username', 'first_name', 'first_login', 'last_download_time', 'total_downloads'])
            writer.writeheader()
            writer.writerows(rows)
            
    except Exception as e:
        print(f"[WARN] Error updating user record: {e}")


def check_rate_limit(user_id: int) -> tuple[bool, str]:
    """Check if user has exceeded rate limit for movie/series downloads.
    
    Returns: (allowed: bool, message: str)
    """
    record = get_user_record(user_id)
    if not record or not record.get('last_download_time'):
        # First download or first movie/series
        return True, ""
    
    try:
        last_time = datetime.fromisoformat(record['last_download_time'])
        time_since = (datetime.now() - last_time).total_seconds()
        
        if time_since < RATE_LIMIT_SECONDS:
            wait_seconds = int(RATE_LIMIT_SECONDS - time_since)
            return False, f"⏱️ Rate limited. Please wait {wait_seconds} seconds before your next movie/series download."
        
        return True, ""
    except Exception as e:
        print(f"[WARN] Error checking rate limit: {e}")
        return True, ""


def resolve_out_folder(folder, content_type: str = "movie"):
    ct = (content_type or "movie").lower()
    if ct == "series":
        base = Path(SERIES_ROOT) if SERIES_ROOT else Path(DEFAULT_FOLDER).joinpath("series")
    elif ct == "movie":
        base = Path(MOVIES_ROOT) if MOVIES_ROOT else Path(DEFAULT_FOLDER).joinpath("movies")
    else:
        base = Path(DEFAULT_FOLDER)

    if folder is None:
        return str(base)

    p = Path(folder)
    if p.is_absolute():
        return str(p)

    try:
        return str(base.joinpath(p))
    except Exception:
        return str(Path(DEFAULT_FOLDER).joinpath(p))


def list_existing_items(content_type: str = "movie") -> list:
    ct = (content_type or "movie").lower()
    if ct == "series":
        root_path = Path(SERIES_ROOT) if SERIES_ROOT else Path(DEFAULT_FOLDER).joinpath("series")
    elif ct == "movie":
        root_path = Path(MOVIES_ROOT) if MOVIES_ROOT else Path(DEFAULT_FOLDER).joinpath("movies")
    else:
        root_path = Path(DEFAULT_FOLDER)

    if not root_path.exists():
        return []

    items = []
    try:
        for child in sorted(root_path.iterdir()):
            items.append(child.name)
    except Exception:
        return []
    return items


def resolve_telegram_folder(folder: str | None, content_type: str = "movie") -> str:
    """Resolve folder for telegram bot requests (NO ABSOLUTE PATHS allowed).
    
    This is a security-restricted version that only allows relative paths.
    Absolute paths are rejected to prevent directory traversal attacks.
    """
    if not folder or folder.lower() in ('skip', 'none', ''):
        # Use type-specific root
        ct = (content_type or "movie").lower()
        if ct == "series":
            return str(Path(SERIES_ROOT) if SERIES_ROOT else Path(DEFAULT_FOLDER).joinpath("series"))
        elif ct == "movie":
            return str(Path(MOVIES_ROOT) if MOVIES_ROOT else Path(DEFAULT_FOLDER).joinpath("movies"))
        else:
            return str(Path(DEFAULT_FOLDER))
    
    p = Path(folder.strip())
    
    # REJECT absolute paths (security)
    if p.is_absolute():
        raise ValueError("Absolute paths are not allowed via Telegram bot. Use relative paths only.")
    
    # Reject "..." or paths that try to escape (security)
    if ".." in str(p) or str(p).startswith("/"):
        raise ValueError("Invalid path: cannot use .. or root-relative paths")
    
    # Determine base root for the content type
    ct = (content_type or "movie").lower()
    if ct == "series":
        base = Path(SERIES_ROOT) if SERIES_ROOT else Path(DEFAULT_FOLDER).joinpath("series")
    elif ct == "movie":
        base = Path(MOVIES_ROOT) if MOVIES_ROOT else Path(DEFAULT_FOLDER).joinpath("movies")
    else:
        base = Path(DEFAULT_FOLDER)
    
    # Join the relative path safely
    try:
        resolved = base.joinpath(p)
        # Make sure the resolved path is still under base (no escape)
        resolved.resolve().relative_to(base.resolve())
        return str(resolved)
    except ValueError:
        raise ValueError(f"Invalid path: cannot escape base directory {base}")



async def do_download_request(payload: dict):
    try:
        def _post():
            return requests.post(f"{API_URL}/download", json=payload, timeout=60)

        return await asyncio.to_thread(_post)
    except Exception as e:
        return e


# Telegram bot using python-telegram-bot v20+ (async)
try:
    from telegram import Update, BotCommand, BotCommandScopeDefault
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
except Exception:
    print("python-telegram-bot not installed. Install with: pip install python-telegram-bot -U")
    raise


async def _handle_generic(update: Update, context: ContextTypes.DEFAULT_TYPE, content_type: str):
    args = context.args
    if not args:
        # No args: start conversational flow (handled by separate handlers)
        await update.message.reply_text(
            "No name provided — start a short conversation instead by issuing the command without args."
        )
        return

    name = " ".join(args)

    try:
        out_folder = resolve_telegram_folder(None, content_type=content_type)
    except ValueError as e:
        await update.message.reply_text(f"Error: {str(e)}")
        return
    
    Path(out_folder).mkdir(parents=True, exist_ok=True)

    existing = list_existing_items(content_type)

    payload = {
        "name": name,
        "is_series": content_type == "series",
        "out_folder": out_folder,
        "existing_items": existing,
        "auto_select": True,
    }

    await update.message.reply_text(f"Looking up and starting download for: {name}\nPosting to API...")

    resp = await do_download_request(payload)
    if isinstance(resp, Exception):
        await update.message.reply_text(f"Error contacting API: {resp}")
        return

    try:
        if resp.status_code == 200:
            data = resp.json()
            gid = data.get("gid")
            tname = data.get("torrent_name") or data.get("torrent") or "(unknown)"
            await update.message.reply_text(f"Download started: {tname}\nGID: {gid}")
        else:
            await update.message.reply_text(f"API error {resp.status_code}: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error processing API response: {e}")


async def movie_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If user supplied args, proceed immediately. Otherwise start prompt flow.
    if context.args:
        # Check rate limit for movie downloads
        user = update.message.from_user
        user_id = user.id
        allowed, message = check_rate_limit(user_id)
        
        if not allowed:
            await update.message.reply_text(message)
            return
        
        # Track user
        update_user_record(user_id, user.username, user.first_name)
        
        await _handle_generic(update, context, "movie")
        return
    # begin conversational prompt sequence
    context.user_data['awaiting'] = {'type': 'movie', 'step': 'name'}
    await update.message.reply_text("Please send the movie name (or /cancel to abort):")


async def series_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        # Check rate limit for series downloads
        user = update.message.from_user
        user_id = user.id
        allowed, message = check_rate_limit(user_id)
        
        if not allowed:
            await update.message.reply_text(message)
            return
        
        # Track user
        update_user_record(user_id, user.username, user.first_name)
        
        await _handle_generic(update, context, "series")
        return
    context.user_data['awaiting'] = {'type': 'series', 'step': 'name'}
    await update.message.reply_text("Please send the series name (or /cancel to abort):")


async def other_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await _handle_generic(update, context, "other")
        return
    context.user_data['awaiting'] = {'type': 'other', 'step': 'name'}
    await update.message.reply_text("Please send the item name (or /cancel to abort):")


async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop('awaiting', None)
    await update.message.reply_text("Cancelled.")


async def send_download(update: Update, context: ContextTypes.DEFAULT_TYPE, content_type: str, name: str, year: str | None, folder: str | None):
    # For conversational flow, check rate limit too
    if content_type in ("movie", "series"):
        user = update.message.from_user
        user_id = user.id
        allowed, message = check_rate_limit(user_id)
        
        if not allowed:
            await update.message.reply_text(message)
            return
        
        # Track user
        update_user_record(user_id, user.username, user.first_name)
    
    try:
        out_folder = resolve_telegram_folder(folder, content_type=content_type)
    except ValueError as e:
        await update.message.reply_text(f"Invalid folder path: {str(e)}")
        return
    
    Path(out_folder).mkdir(parents=True, exist_ok=True)
    existing = list_existing_items(content_type)

    payload = {
        "name": name,
        "year": int(year) if year and year.isdigit() else None,
        "is_series": content_type == "series",
        "out_folder": out_folder,
        "existing_items": existing,
        "auto_select": True,
    }

    await update.message.reply_text(f"Starting download: {name} (year: {year or 'N/A'})")
    resp = await do_download_request(payload)
    if isinstance(resp, Exception):
        await update.message.reply_text(f"Error contacting API: {resp}")
        return
    try:
        if resp.status_code == 200:
            data = resp.json()
            gid = data.get("gid")
            tname = data.get("torrent_name") or data.get("torrent") or "(unknown)"
            await update.message.reply_text(f"Download started: {tname}\nGID: {gid}")
        else:
            await update.message.reply_text(f"API error {resp.status_code}: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error processing API response: {e}")


async def text_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle conversational prompts for missing fields
    awaiting = context.user_data.get('awaiting')
    if not awaiting:
        return

    text = update.message.text.strip()
    ctype = awaiting.get('type')
    step = awaiting.get('step')

    if step == 'name':
        awaiting['name'] = text
        awaiting['step'] = 'year'
        context.user_data['awaiting'] = awaiting
        await update.message.reply_text("Optional: send year (e.g. 2023) or type 'skip' to continue without year:")
        return

    if step == 'year':
        if text.lower() in ('skip', 'none', ''):
            awaiting['year'] = None
        else:
            awaiting['year'] = text

        # For movies and series we do NOT ask for an output folder —
        # the bot will use the configured movies/series root by default.
        if ctype in ('movie', 'series'):
            name = awaiting.get('name')
            year = awaiting.get('year')
            # clear awaiting state
            context.user_data.pop('awaiting', None)
            await send_download(update, context, ctype, name, year, None)
            return

        # For other content types, continue to ask for folder
        awaiting['step'] = 'folder'
        context.user_data['awaiting'] = awaiting
        await update.message.reply_text(f"Optional: send folder relative to root (or absolute). Type 'skip' to use default for {ctype}:")
        return

    if step == 'folder':
        if text.lower() in ('skip', 'none', ''):
            awaiting['folder'] = None
        else:
            awaiting['folder'] = text

        # finalise and trigger download
        name = awaiting.get('name')
        year = awaiting.get('year')
        folder = awaiting.get('folder')
        # clear awaiting state
        context.user_data.pop('awaiting', None)
        await send_download(update, context, ctype, name, year, folder)
        return


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message with current command info."""
    help_text = """
Welcome to the Torrent Downloader Bot

**Available Commands:**
- `/movie` — Download a movie
- `/other` — Download other content (saved to default folder)
- `/cancel` — Cancel current action

**How to use:**
1. Click on a command above (or type it)
2. If you provide the name as an argument (e.g., `/movie Inception`), download starts immediately
3. If you just send the command alone (e.g., `/movie`), I'll ask for the name and year only

**Rate Limiting:**
- Limited to 1 movie download per minute per user
- "Other" downloads are not rate limited
- Your activity is tracked (user ID, name, last login)

**Examples:**
`/movie Inception 2010` — starts immediately
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def post_startup(app: Application) -> None:
    """Called on application startup to register bot commands, description, and short description."""
    
    # Initialize user tracking CSV
    init_users_csv()
    
    commands = [
        BotCommand("movie", "Download a movie (or prompt for details)"),
        BotCommand("other", "Download other content to default folder"),
        BotCommand("cancel", "Cancel current action"),
        BotCommand("start", "Show help and available commands"),
    ]
    
    description = (
        "Torrent Downloader Bot\n\n"
        "Download movies and other content directly via Telegram:\n\n"
        "- Search & download movies\n"
        "- Download other content\n"
        "- Organize by type (movie/other)\n"
        "- Automatic LLM selection of best torrent\n"
        "- Local aria2 download management\n"
        "- Rate limited: 1 movie per minute\n"
        "- User activity tracking\n\n"
        "Perfect for remote content acquisition!"
    )
    short_description = "Download torrents via Telegram commands"
    
    try:
        # Set commands with explicit DEFAULT scope (for private chats)
        scope = BotCommandScopeDefault()
        
        print("\n[INFO] Registering bot configuration...")
        print(f"[INFO] API URL: {API_URL}")
        
        # Set commands
        await app.bot.set_my_commands(commands, scope=scope)
        print("[OK] Bot commands registered")
        
        # Set main description (shown on empty chat and bot info page)
        # Note: set_my_description does NOT support scope parameter
        await app.bot.set_my_description(description)
        print("[OK] Bot description set")
        print(f"      Description: {description[:50]}...")
        
        # Set short description (shown in bot search results)
        # Note: set_my_short_description does NOT support scope parameter
        await app.bot.set_my_short_description(short_description)
        print("[OK] Bot short description set")
        print(f"      Short: {short_description}")
        
        # Verify what was set by retrieving it back
        print("\n[INFO] Verifying settings...")
        retrieved_cmds = await app.bot.get_my_commands(scope=scope)
        print(f"[OK] Retrieved {len(retrieved_cmds)} commands")
        
        retrieved_desc = await app.bot.get_my_description()
        print(f"[OK] Retrieved description: {retrieved_desc.description[:50]}...")
        
        retrieved_short = await app.bot.get_my_short_description()
        print(f"[OK] Retrieved short description: {retrieved_short.short_description}")
        
        print("\n[INFO] Bot startup complete. All settings registered.\n")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to register bot settings: {e}")
        import traceback
        traceback.print_exc()
        print()


def main():
    token = TELEGRAM_BOT_TOKEN
    if not token:
        print("TELEGRAM_BOT_TOKEN not set in environment or .env")
        return

    # Build application with post_init callback (like the reference bot)
    app = Application.builder().token(token).post_init(post_startup).build()
    
    # Add all handlers
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("movie", movie_cmd))
    # app.add_handler(CommandHandler("series", series_cmd))
    app.add_handler(CommandHandler("other", other_cmd))
    app.add_handler(CommandHandler("cancel", cancel_cmd))
    # Global text handler for conversational flows (name/year/folder)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_response))

    print("Starting Telegram bot...")
    print("On bot startup, commands and descriptions will be registered with Telegram.")
    app.run_polling()


if __name__ == "__main__":
    main()
