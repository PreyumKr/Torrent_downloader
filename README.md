# Torrent Downloader

An automated torrent downloader with AI-powered selection for movies and TV series.

## Features
- **Movie Downloader**: Dedicated service on port 8001, integrated with Telegram bot.
- **Series Test Service**: Evaluation mode on port 8002 to test AI decisions without downloading.
- **AI Selection**: Uses Ollama (local LLM) to pick the best torrent based on quality, size, and metadata.
- **Telegram Interface**: Remote control via bot commands.
- **Aria2 Integration**: High-performance downloading via `aria2c`.

## Prerequisites
- **Python 3.12+**
- **Ollama**: [Installed and running](https://ollama.ai/) with the `llama2` model (default).
- **Aria2**: Included in the repository (Windows).

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Or using `uv`:*
   ```bash
   uv sync
   ```
3. Set up environment variables:
   Copy `.env.example` to `.env` and provide your `TELEGRAM_BOT_TOKEN`.

## How to Run
### 1. Start the API Services
This command starts the `aria2c` daemon, the Movie API (port 8001), and the Series Test API (port 8002).
```bash
python run_api.py
```

### 2. Start the Telegram Bot
```bash
python run_telegrambot.py
```

## How to Test the Series API
The Series service runs in "Test Mode" on port 8002. It logs all its search results and AI selection decisions without initiating actual downloads. It uses a Jellyfin-optimized workflow to determine what's missing.

To test a series decision, send a POST request to the `/test-decision` endpoint:

### Using cURL:
```bash
curl -X POST http://localhost:8002/test-decision \
     -H "Content-Type: application/json" \
     -d '{"name": "The Boys", "year": 2019}'
```

### What to expect:
- The API will search for "The Boys complete" (and other variations) on **PirateBay**.
- It will fetch canonical metadata for the series from **TVMD**.
- It will scan the local series folder for existing **Jellyfin-compatible** content.
- **Ollama** will evaluate the found torrents against the local state and select the "best" strategy (e.g., download a complete season vs individual episodes).
- **Check the logs**: View detailed decision-making logs in `logs/torrent_api.log`.

## Logging
- **API Logs**: `logs/torrent_api.log` (Decision-making, search results, and selection logs)
- **General Logs**: `logs/torrent_downloader.log`
