"""FastAPI application for Series downloads (Test/Logging Mode)"""
import asyncio
import logging
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from app.config import config
from app.scraper import scraper
from app.series_info import series_lookup
from app.ollama_selector import ollama_selector
from app.logging_config import configure_api_logging

# Configure API logging
configure_api_logging()
logger = logging.getLogger("series_test_api")

app = FastAPI(
    title="Series Downloader API (Test Mode)",
    description="Service for evaluating series download decisions (Logs only)",
    version="1.0.0",
)

class DownloadRequest(BaseModel):
    name: str = Field(..., description="Name of the series")
    year: Optional[int] = Field(None, description="Release year")
    existing_items: Optional[List[str]] = Field(None)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "series-downloader-test"}

@app.post("/test-decision")
async def test_series_decision(request: DownloadRequest):
    """
    Evaluates what torrent would be selected for a series and logs everything.
    DOES NOT START DOWNLOAD.
    """
    try:
        logger.info(f"=== TEST SERIES DECISION START ===")
        logger.info(f"Name: {request.name}")
        logger.info(f"Year: {request.year}")

        # Search torrents
        search_query = f"{request.name} complete"
        logger.info(f"Searching for: {search_query}")
        torrents = scraper.search_torrents(search_query, page=1)
        
        if not torrents:
            logger.warning(f"No torrents found for series: {request.name}")
            return {"status": "no_results", "message": "No torrents found"}

        logger.info(f"Found {len(torrents)} torrents")
        for i, t in enumerate(torrents[:5], 1):
            logger.info(f"[{i}] {t.name} (Seeds: {t.seeds}, Size: {t.size})")

        # Fetch series info
        logger.info(f"Fetching series info...")
        series_info = series_lookup.get_series_info(request.name)
        series_info_str = str(series_info) if series_info else "None found"
        logger.info(f"Metadata result: {series_info_str}")

        # Ollama Selection
        logger.info(f"Invoking Ollama for decision...")
        selected = ollama_selector.select_best_torrent(
            torrents,
            request.name,
            series_info_str,
            request.existing_items,
        )

        if isinstance(selected, ollama_selector.AlreadyPresent):
            logger.info(f"Decision: ALREADY PRESENT ({selected.reason})")
            return {
                "decision": "already_present",
                "reason": selected.reason,
                "logs_check": "torrent_api.log"
            }

        if selected:
            logger.info(f"Decision: SELECTED '{selected.name}'")
            return {
                "decision": "selected",
                "torrent": selected.name,
                "seeds": selected.seeds,
                "size": selected.size,
                "logs_check": "torrent_api.log"
            }
        else:
            logger.info(f"Decision: NO TORRENT SELECTED")
            return {
                "decision": "none",
                "logs_check": "torrent_api.log"
            }

    except Exception as e:
        logger.error(f"Error in series test decision: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
