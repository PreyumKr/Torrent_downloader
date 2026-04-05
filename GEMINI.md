# Torrent Downloader Project Context

## Project Overview
This project is an automated torrent downloader designed for high-quality movie and TV series acquisition, optimized for **Jellyfin** media servers. It features a FastAPI backend, a Telegram bot interface, and uses `aria2c` for downloading.

### Key Technologies
- **Python 3.12+**: Core programming language.
- **FastAPI**: REST API for management and automation.
- **Aria2**: Download engine via RPC (`aria2c`).
- **Ollama**: Local LLM integration for intelligent selection and organization decisions.
- **PirateBay (via apibay.org)**: Primary torrent source.
- **TVMD API**: Metadata source for series/movie information.
- **Python Telegram Bot**: User interface for remote control.

## Series Download Workflow (Jellyfin Optimized)
When a series name is provided, the system follows this robust workflow:
1.  **Metadata Lookup**: Fetches canonical series info (seasons/episodes) from **TVMD**.
2.  **Local Sync**: Scans the destination folder for the existing Jellyfin-compatible structure (e.g., `Series Name/Season 01/`).
3.  **Strategy Planning**: 
    - Pass both TVMD metadata and local folder tree to **Ollama**.
    - LLM decides what's missing: complete seasons, individual episodes, or multi-season bundles.
    - LLM suggests specific search queries for the missing parts.
4.  **Download & Inspection**:
    - Torrents are first downloaded to a **temporary folder** (`downloads/temp/`).
    - After completion, the system (assisted by LLM) inspects the downloaded structure.
    - Files are then moved to their final, organized Jellyfin-compatible location.
5.  **Status**: The series service currently operates in a "Test Mode" on port 8002 to refine these decisions before full integration.

## Project Structure
- `app/`: Core application logic.
    - `api_movies.py`: Production API for movie downloads (Port 8001).
    - `api_series.py`: Test API for refining series download logic (Port 8002).
    - `scraper.py`: PirateBay API integration.
    - `ollama_selector.py`: LLM-based torrent selection and organizational logic.
    - `tvmd_client.py`: Metadata fetching from TVMD.
    - `fs_utils.py`: Jellyfin-compatible filesystem utilities.
- `telegram_bot/`: Bot implementation (Movie/Other enabled, Series in testing).
- `run_api.py`: Multi-service entry point.

## Development Conventions
- **Git Workflow**: Commit and push changes immediately after implementation and verification.
- **Jellyfin Compatibility**: All series downloads MUST follow the `Series Name/Season XX/SXXEXX - Title.ext` structure.
- **Logs**: Do not commit the `logs/` folder. Use `logs/torrent_api.log` for debugging decision-making.
- **Configuration**: Use `app/config.py` and document all keys in `.env.example`.
