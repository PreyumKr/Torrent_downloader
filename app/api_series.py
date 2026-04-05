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
from app.tvmd_client import tvmd_client
from app.fs_utils import list_seasons_and_episodes
from app.compare_and_plan import compare_series_metadata
from app.ollama_selector import ollama_selector
from app.logging_config import configure_api_logging

# Configure API logging
configure_api_logging()
logger = logging.getLogger("series_test_api")

app = FastAPI(
    title="Series Downloader API (Test Mode)",
    description="Service for evaluating series download decisions (Logs only)",
    version="1.1.0",
)

class DownloadRequest(BaseModel):
    name: str = Field(..., description="Name of the series")
    year: Optional[int] = Field(None, description="Release year")
    series_folder: Optional[str] = Field(None, description="Local folder path for the series")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "series-downloader-test"}

@app.post("/test-decision")
async def test_series_decision(request: DownloadRequest):
    """
    Evaluates what torrent would be selected for a series and logs everything.
    Uses TVMD metadata and scans local folder to decide on a strategy.
    DOES NOT START DOWNLOAD.
    """
    try:
        logger.info(f"=== TEST SERIES DECISION START ===")
        logger.info(f"Name: {request.name}")
        
        # 1. TVMD Metadata Lookup
        logger.info(f"Step 1: TVMD Metadata Lookup")
        series_id = tvmd_client.find_series_id(request.name)
        if not series_id:
            logger.warning(f"TVMD: No ID found for series '{request.name}'")
            return {"status": "error", "message": "TVMD metadata lookup failed"}
        
        seasons_meta = tvmd_client.get_series_seasons(series_id) or []
        per_season = {}
        for s in seasons_meta:
            sn = s.get("season_number") or s.get("number")
            cnt = s.get("episode_count") or s.get("episodes") or None
            if sn is not None:
                per_season[int(sn)] = int(cnt) if cnt is not None else None
        
        canonical = {
            "canonical_name": request.name,
            "seasons": len(seasons_meta) or None,
            "per_season": per_season,
            "is_series": True,
            "year": request.year
        }
        logger.info(f"TVMD Canonical Info: {canonical}")

        # 2. Local Filesystem Scan (Jellyfin structure)
        logger.info(f"Step 2: Local Filesystem Scan")
        series_folder = request.series_folder or str(Path(getattr(config, 'SERIES_ROOT_FOLDER', None) or config.DEFAULT_DOWNLOAD_FOLDER).joinpath('series', request.name))
        local_tree = list_seasons_and_episodes(series_folder)
        logger.info(f"Local tree for '{series_folder}': {local_tree}")

        # 3. Compare and Plan (LLM Strategy Preparation)
        logger.info(f"Step 3: Strategy Planning")
        plan = compare_series_metadata(canonical, local_tree)
        logger.info(f"Missing Seasons: {plan['missing']['seasons']}")
        logger.info(f"Missing Episodes: {plan['missing']['episodes']}")
        
        if not plan["missing"]["seasons"] and not plan["missing"]["episodes"]:
            logger.info("Decision: SERIES IS COMPLETE LOCALLY")
            return {"decision": "complete", "message": "All seasons and episodes are already present."}

        # 4. Search and Select
        logger.info(f"Step 4: Torrent Search and LLM Selection")
        # Search for both "complete" and individual seasons if needed
        search_query = f"{request.name} complete"
        logger.info(f"Searching PirateBay for: {search_query}")
        torrents = scraper.search_torrents(search_query, page=1)
        
        if not torrents:
            logger.warning(f"No torrents found for search query: {search_query}")
            return {"status": "no_results", "query": search_query}

        # Use Ollama to select based on the detailed plan
        # We pass the prompt from compare_series_metadata to Ollama
        logger.info(f"Invoking Ollama for selection decision...")
        selected = ollama_selector.select_best_torrent(
            torrents,
            request.name,
            plan["llm_prompt"], # Detailed context for the LLM
            list(local_tree.keys()) # Existing seasons
        )

        if isinstance(selected, ollama_selector.AlreadyPresent):
            logger.info(f"Decision: ALREADY PRESENT ({selected.reason})")
            return {"decision": "already_present", "reason": selected.reason}

        if selected:
            logger.info(f"Decision: SELECTED '{selected.name}'")
            logger.info(f"Strategy: {selected.name} will be downloaded to temp/ then organized.")
            return {
                "decision": "selected",
                "torrent": selected.name,
                "seeds": selected.seeds,
                "size": selected.size,
                "plan": plan["missing"],
                "logs_check": "torrent_api.log"
            }
        else:
            logger.info(f"Decision: NO TORRENT SELECTED")
            return {"decision": "none", "logs_check": "torrent_api.log"}

    except Exception as e:
        logger.error(f"Error in series test decision: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host=config.API_HOST, port=int(os.getenv("SERIES_API_PORT", "8002")))
