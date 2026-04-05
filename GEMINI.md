# Torrent Downloader Project Context

## Project Overview
This project is an automated torrent downloader designed to search for and download movies and TV series. It features a FastAPI backend, a Telegram bot interface, and uses `aria2c` for high-performance downloading. A key highlight is the AI-powered selection of the best torrents (especially for TV series) using **Ollama**.

### Key Technologies
- **Python 3.12+**: Core programming language.
- **FastAPI**: Provides the REST API for searching, downloading, and status tracking.
- **Aria2**: The underlying download engine, controlled via RPC (`aria2c`).
- **Ollama**: Local LLM integration for intelligent torrent selection based on quality, size, and metadata.
- **Python Telegram Bot**: User interface for remote control and notifications.
- **BeautifulSoup4 / Cloudscraper**: Used for scraping 1337x.to.
- **Pydantic**: Data validation and settings management.

## Project Structure
- `app/`: Core application logic.
    - `api_movies.py`: FastAPI application for movie downloads (Port 8001).
    - `api_series.py`: FastAPI application for testing series decisions (Port 8002, Logs only).
    - `config.py`: Centralized configuration management (loads from `.env`).
    - `scraper.py`: 1337x.to search and scraping logic.
    - `aria2_handler.py`: Interface with `aria2c` RPC.
    - `ollama_selector.py`: AI logic for selecting the best torrent.
    - `tvmd_client.py`: Client for interacting with TVMD API for metadata.
- `telegram_bot/`: Telegram bot implementation (Series option commented out).
- `run_api.py`: Entry point for starting BOTH Movie and Series Test APIs.

- `aria2-1.37/`: Contains the `aria2c.exe` binary for Windows.
- `logs/`: Directory for API and application logs.
- `downloads/`: Default directory for downloaded content.
- `run_api.py`: Entry point for the FastAPI server and automatic `aria2c` daemon startup.
- `run_telegrambot.py`: Entry point for the Telegram bot.
- `check_aria2.py`: Interactive CLI tool to monitor and control active downloads.

## Building and Running

### Prerequisites
1.  **Python 3.12+**: Ensure Python is installed.
2.  **Ollama**: Install and run Ollama locally (default model: `llama2`).
3.  **Environment Setup**: Copy `.env.example` to `.env` and fill in the required values (especially `TELEGRAM_BOT_TOKEN`).

### Installation
```powershell
pip install -r requirements.txt
# OR if using uv
uv sync
```

### Running the API
Starts the FastAPI server on `http://localhost:8000` (by default) and launches the `aria2c` daemon.
```powershell
python run_api.py
```

### Running the Telegram Bot
Starts the bot to interact with the API.
```powershell
python run_telegrambot.py
```

### Monitoring Downloads
Use the interactive CLI tool to list, pause, or remove downloads.
```powershell
python check_aria2.py
```

## Development Conventions
- **Git Workflow**: For all changes from now on, you MUST commit the changes with a descriptive message and push them to the remote repository immediately after implementation and verification.
- **Configuration**: Always add new settings to `app/config.py` and document them in `.env.example`.
- **Logging**: Use the configured loggers in `app/logging_config.py`. Logs are stored in `logs/torrent_api.log` and `logs/torrent_downloader.log`.
- **Error Handling**: Use `HTTPException` for API-level errors and ensure all internal services (scraper, aria2, ollama) have robust error handling and logging.
- **Typing**: Use Python type hints and Pydantic models for all data structures and API requests/responses.
- **Git**: Do not commit the `.env` file or the `downloads/` directory.

## Key Files Summary
- `run_api.py`: Main entry point for the backend.
- `app/main.py`: Contains API routes for `/search`, `/download`, `/health`, etc.
- `app/ollama_selector.py`: Implements the `select_best_torrent` logic using LLM prompts.
- `telegram_bot/bot.py`: Handles `/movie`, `/series`, `/status`, and other Telegram commands.
- `check_aria2.py`: Provides a quick way to manage the `aria2` queue from the terminal.
