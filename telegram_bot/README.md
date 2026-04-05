# Telegram Bot for Torrent Downloader

This folder contains a Telegram bot that triggers downloads via the local
Torrent Downloader API. The bot supports immediate commands (with arguments)
and a short conversational flow when commands are issued without arguments.

Quickstart

1. Set env vars in the project `.env` or in your shell:

```
TELEGRAM_BOT_TOKEN=<your bot token>
API_URL=http://localhost:8000  # optional, defaults to localhost
```

2. Install dependencies (recommended in a venv):

```powershell
pip install -r telegram_bot\requirements.txt
```

3. Run the bot from the repository root:

```powershell
cd F:\\Torrent_downloader
python telegram_bot\bot.py
```

Commands & conversational flow

- `/movie <name> [year]` — start a movie download immediately. If you omit
	`<name>` the bot will prompt for the name, then optional year, then optional
	folder.
- `/series <name> [year]` — same as `/movie` but for series.
- `/other <name>` — saves directly into the `DEFAULT_DOWNLOAD_FOLDER` (or a
	specified absolute path).

Examples

```text
/movie Inception 2010
/series
	(bot will ask: name -> year -> folder)
```

Notes

- The bot sends `existing_items` to the API so the LLM/server can check for
	duplicates before starting a download.
- You can configure `MOVIES_ROOT_FOLDER` and `SERIES_ROOT_FOLDER` in `.env` to
	override default per-type locations.
