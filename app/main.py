"""Main FastAPI application for torrent downloader"""
import asyncio
import logging
import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from app.config import config
from app.scraper import scraper, TorrentInfo
from app.aria2_handler import aria2_client
from app.ollama_selector import ollama_selector
from app.series_info import series_lookup, plan_generator
from app.tvmd_client import tvmd_client
from app.fs_utils import list_seasons_and_episodes, build_tree
from app.compare_and_plan import compare_series_metadata
from app.logging_config import configure_api_logging

# Configure API logging (writes to logs/torrent_api.log)
configure_api_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Torrent Downloader API",
    description="Download torrents from 1337x.to with AI-powered selection for series",
    version="1.0.0",
)

# Pydantic models
class DownloadRequest(BaseModel):
    """Request model for torrent download"""
    
    name: str = Field(..., description="Name of the movie or series")
    year: Optional[int] = Field(None, description="Release year")
    is_series: bool = Field(False, description="Whether this is a series")
    out_folder: str = Field(
        default=None,
        description="Output folder for downloads (uses DEFAULT_DOWNLOAD_FOLDER if not specified)"
    )
    content_type: Optional[str] = Field(
        default="movie",
        description="Content type: 'movie', 'series', or 'other' (overrides is_series if provided)",
    )
    existing_items: Optional[List[str]] = Field(
        default=None,
        description="Optional list of existing item names in the destination folder (provided by clients/LLM)",
    )
    max_results: int = Field(10, description="Maximum search results to consider")
    auto_select: bool = Field(
        True,
        description="Automatically select best torrent (uses Ollama for series)"
    )


class SearchRequest(BaseModel):
    """Request model for search"""
    
    query: str = Field(..., description="Search query")
    is_series: bool = Field(False, description="Whether searching for a series")
    year: Optional[int] = Field(None, description="Release year")
    max_results: int = Field(10, description="Maximum search results")


class SearchResponse(BaseModel):
    """Response model for search results"""
    
    query: str
    results_count: int
    torrents: List[dict]
    plan: Optional[dict] = None


class DownloadResponse(BaseModel):
    """Response model for download"""
    
    status: str
    gid: Optional[str] = None
    torrent_name: str
    output_dir: str
    message: str


class DownloadStatusResponse(BaseModel):
    """Response model for download status"""
    
    gid: str
    name: str
    status: str
    progress: float
    speed: str
    eta: str


# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "torrent-downloader"}


@app.post("/search", response_model=SearchResponse)
async def search_torrents(request: SearchRequest):
    """
    Search for torrents on 1337x.to
    
    Args:
        request: Search request with query, is_series, year, max_results
        
    Returns:
        SearchResponse with torrents found and download plan
    """
    try:
        # Build search query
        search_query = request.query
        if request.year and not request.is_series:
            search_query = f"{request.query} {request.year}"
        elif request.is_series:
            search_query = f"{request.query} complete"
        
        # Get download plan
        plan = plan_generator.plan_download(request.query, request.is_series, request.year)
        
        # Search torrents with exponential-backoff retry on transient empty results
        max_retries = 10
        delay = 0.5
        attempt = 1
        torrents = []
        while attempt <= max_retries:
            torrents = scraper.search_torrents(search_query, page=1)
            if torrents:
                break
            if attempt < max_retries:
                logger.warning(f"No torrents found for '{search_query}' (attempt {attempt}/{max_retries}). Retrying in {delay}s...")
                await asyncio.sleep(delay)
                delay *= 2
            attempt += 1

        torrents = torrents[:request.max_results]

        if not torrents:
            logger.error(f"No torrents found for: {search_query} after {max_retries} attempts")
            raise HTTPException(status_code=404, detail="No torrents found")
        
        return SearchResponse(
            query=search_query,
            results_count=len(torrents),
            torrents=[t.to_dict() for t in torrents],
            plan=plan,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching torrents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class LookupRequest(BaseModel):
    type: str = Field("series", description="'movie' or 'series'")
    name: str = Field(...)
    year: Optional[int] = Field(None)


class LookupResponse(BaseModel):
    canonical_name: str
    tvmd_id: Optional[str]
    seasons: Optional[int]
    episodes: Optional[int]
    per_season: Optional[Dict[int, int]] = None
    providers: Optional[List[dict]] = None
    notes: Optional[List[str]] = None


@app.post("/tvmd/lookup", response_model=LookupResponse)
async def tvmd_lookup(request: LookupRequest):
    """Lookup series/movie metadata using TVMD API."""
    try:
        typ = request.type.lower()
        name = request.name
        year = request.year
        notes = []

        series_id = tvmd_client.find_series_id(name)
        if not series_id:
            notes.append("TVMD: no id found")
            return LookupResponse(canonical_name=name, tvmd_id=None, seasons=None, episodes=None, per_season=None, providers=[], notes=notes)

        # Get seasons
        seasons_meta = tvmd_client.get_series_seasons(series_id) or []
        seasons_count = len(seasons_meta)
        per_season = {}
        for s in seasons_meta:
            sn = s.get("season_number") or s.get("number")
            # attempt to read episode_count
            cnt = s.get("episode_count") or s.get("episodes") or None
            if sn is not None:
                try:
                    per_season[int(sn)] = int(cnt) if cnt is not None else None
                except Exception:
                    per_season[int(sn)] = None

        # Compute episodes total if available
        episodes_total = None
        if per_season:
            episodes_total = sum([v for v in per_season.values() if isinstance(v, int)])

        notes.append(f"TVMD id: {series_id}")

        return LookupResponse(
            canonical_name=name,
            tvmd_id=series_id,
            seasons=seasons_count or None,
            episodes=episodes_total,
            per_season=per_season or None,
            providers=[],
            notes=notes,
        )
    except Exception as e:
        logger.error(f"tvmd_lookup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class CompareRequest(BaseModel):
    tvmd_id: str = Field(...)
    series_folder: str = Field(...)
    fetch_remote: bool = Field(True, description="If true, fetch season/episode metadata from TVMD")


class CompareResponse(BaseModel):
    plan: dict


@app.post("/tvmd/compare", response_model=CompareResponse)
async def tvmd_compare(request: CompareRequest):
    """Compare TVMD metadata with local folder and prepare download plan (and LLM prompt).

    Note: this endpoint does not call an LLM; it returns structured differences and a prompt
    that can be sent to an LLM (bot or server) to decide complex strategies.
    """
    try:
        series_id = request.tvmd_id
        folder = request.series_folder
        if request.fetch_remote:
            seasons_meta = tvmd_client.get_series_seasons(series_id) or []
            per_season = {}
            for s in seasons_meta:
                sn = s.get("season_number") or s.get("number")
                cnt = s.get("episode_count") or s.get("episodes") or None
                if sn is not None:
                    per_season[int(sn)] = int(cnt) if cnt is not None else None
            canonical = {"canonical_name": None, "seasons": len(seasons_meta) or None, "per_season": per_season, "is_series": True}
        else:
            canonical = {"canonical_name": None, "seasons": None, "per_season": {}, "is_series": True}

        local_tree = list_seasons_and_episodes(folder)
        plan = compare_series_metadata(canonical, local_tree)
        return CompareResponse(plan=plan)
    except Exception as e:
        logger.error(f"tvmd_compare error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download", response_model=DownloadResponse)
async def download_torrent(
    request: DownloadRequest,
    background_tasks: BackgroundTasks,
):
    """
    Download a torrent (movie or series)
    
    Args:
        request: Download request with name, year, type, output folder
        background_tasks: Background task queue
        
    Returns:
        Download status and GID
    """
    try:
        # Determine content type (support either explicit content_type or is_series flag)
        ctype = (request.content_type or ("series" if request.is_series else "movie")).lower()

        # Resolve default output folder when not provided, matching telegram bot behaviour
        if request.out_folder:
            output_folder = request.out_folder
        else:
            if ctype == "series":
                output_folder = str(Path(getattr(config, 'SERIES_ROOT_FOLDER', None) or config.DEFAULT_DOWNLOAD_FOLDER).joinpath('series'))
            elif ctype == "movie":
                output_folder = str(Path(getattr(config, 'MOVIES_ROOT_FOLDER', None) or config.DEFAULT_DOWNLOAD_FOLDER).joinpath('movies'))
            else:
                output_folder = str(config.DEFAULT_DOWNLOAD_FOLDER)

        # Validate output folder
        output_dir = Path(output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"=== DOWNLOAD REQUEST RECEIVED ===")
        logger.info(f"Name: {request.name}")
        logger.info(f"Type: {ctype.title()}")
        logger.info(f"Year: {request.year}")
        logger.info(f"Download folder: {output_dir.absolute()}")
        if request.existing_items:
            logger.info(f"Existing items provided: {len(request.existing_items)} entries")
        
        # Search for torrents
        search_query = request.name
        # For movies, try a canonical title lookup (best-effort) to improve search
        if ctype == "movie":
            try:
                canonical = movie_lookup.get_canonical_title(request.name, request.year)
                if canonical and canonical.strip():
                    # Prefer canonical title (include year if provided)
                    if request.year:
                        search_query = f"{canonical} {request.year}"
                    else:
                        search_query = canonical
                    logger.info(f"Canonical movie title used for search: {search_query}")
            except Exception as e:
                logger.debug(f"Movie canonicalization failed: {e}")
        elif request.year and ctype != "series":
            search_query = f"{request.name} {request.year}"
        elif ctype == "series":
            search_query = f"{request.name} complete"
        
        logger.info(f"Searching for torrents with query: {search_query}")
        torrents = scraper.search_torrents(search_query, page=1)
        logger.info(f"Found {len(torrents)} torrents")
        
        if not torrents:
            logger.error(f"No torrents found for: {search_query}")
            raise HTTPException(status_code=404, detail="No torrents found")
        
        # Log all torrents found - BEFORE sending to Ollama
        logger.info(f"=== TORRENTS AVAILABLE FOR SELECTION ({len(torrents)} total) ===")
        for i, t in enumerate(torrents, 1):
            logger.info(f"[{i}] {t.name}")
            logger.info(f"    Seeds: {t.seeds} | Leeches: {t.leeches} | Size: {t.size}")
        
        # Select best torrent
        logger.info(f"=== STARTING TORRENT SELECTION ===")
        logger.info(f"Auto-select enabled: {request.auto_select}")
        if request.auto_select:
            if ctype == "series":
                logger.info(f"Fetching series info for: {request.name}")
                series_info = series_lookup.get_series_info(request.name)
                series_info_str = str(series_info) if series_info else None
                logger.info(f"Series info: {series_info_str}")
                selected = ollama_selector.select_best_torrent(
                    torrents,
                    request.name,
                    series_info_str,
                    request.existing_items,
                )
            else:
                # Call Ollama for movies too (pass existing items)
                logger.info(f"Calling Ollama for movie selection")
                selected = ollama_selector.select_best_torrent(
                    torrents,
                    request.name,
                    None,  # No seasons info for movies
                    request.existing_items,
                )
        else:
            logger.info(f"Using first torrent (auto-select disabled)")
            selected = torrents[0]
        
        # Handle Ollama sentinel that indicates item already present
        if isinstance(selected, ollama_selector.AlreadyPresent):
            logger.info(f"Download skipped: item already present ({selected.reason})")
            return DownloadResponse(
                status="exists",
                gid=None,
                torrent_name="",
                output_dir=str(output_dir.absolute()),
                message=f"Already present: {selected.reason}",
            )

        if not selected:
            logger.error(f"Could not select a torrent")
            raise HTTPException(status_code=400, detail="Could not select a torrent")
        
        logger.info(f"=== SELECTED TORRENT ===")
        logger.info(f"Name: {selected.name}")
        logger.info(f"Seeds: {selected.seeds}")
        logger.info(f"Leeches: {selected.leeches}")
        logger.info(f"Size: {selected.size}")
        logger.info(f"Magnet: {selected.magnet_link[:100]}...")
        
        # Start download
        logger.info(f"Adding torrent to aria2...")
        gid = await aria2_client.add_torrent(
            selected.magnet_link,
            str(output_dir.absolute()),
        )
        
        if not gid:
            logger.error(f"Failed to add torrent to aria2")
            raise HTTPException(status_code=500, detail="Failed to start download with aria2")
        
        logger.info(f"=== DOWNLOAD STARTED ===")
        logger.info(f"GID: {gid}")
        logger.info(f"Torrent: {selected.name}")
        logger.info(f"Destination: {output_dir.absolute()}")
        
        return DownloadResponse(
            status="downloading",
            gid=gid,
            torrent_name=selected.name,
            output_dir=str(output_dir.absolute()),
            message=f"Torrent download started: {selected.name}",
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting download: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/{content_type}", response_model=DownloadResponse)
async def download_by_type(content_type: str, request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Download endpoint that explicitly accepts a content type in the path
    (movie, series, or other). This mirrors the Telegram bot commands.
    """
    c = (content_type or "").lower()
    if c not in ("movie", "series", "other"):
        raise HTTPException(status_code=400, detail="content_type must be 'movie', 'series', or 'other'")

    # Ensure content_type takes precedence and keep compatibility with is_series
    request.content_type = c
    request.is_series = (c == "series")
    return await download_torrent(request, background_tasks)


@app.get("/download/{gid}/status", response_model=DownloadStatusResponse)
async def get_download_status(gid: str):
    """
    Get download status
    
    Args:
        gid: Download ID from aria2
        
    Returns:
        Current download status
    """
    try:
        status = await aria2_client.get_download_status(gid)
        
        if not status:
            raise HTTPException(status_code=404, detail="Download not found")
        
        # Parse status
        completed_length = int(status.get("completedLength", 0))
        total_length = int(status.get("totalLength", 1))
        progress = (completed_length / total_length * 100) if total_length > 0 else 0
        
        # Format speed
        download_speed = int(status.get("downloadSpeed", 0))
        speed_str = f"{download_speed / 1024 / 1024:.2f} MB/s" if download_speed > 0 else "0 MB/s"
        
        # Estimate ETA
        if download_speed > 0:
            remaining = total_length - completed_length
            eta_seconds = remaining / download_speed
            eta_str = f"{int(eta_seconds // 3600)}h {int((eta_seconds % 3600) // 60)}m"
        else:
            eta_str = "Unknown"
        
        return DownloadStatusResponse(
            gid=gid,
            name=status.get("bittorrent", {}).get("info", {}).get("name", "Unknown"),
            status=status.get("status", "unknown"),
            progress=progress,
            speed=speed_str,
            eta=eta_str,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting download status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/{gid}/pause")
async def pause_download(gid: str):
    """Pause a download"""
    try:
        success = await aria2_client.pause_download(gid)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to pause download")
        return {"status": "paused", "gid": gid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pausing download: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/{gid}/resume")
async def resume_download(gid: str):
    """Resume a paused download"""
    try:
        success = await aria2_client.resume_download(gid)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to resume download")
        return {"status": "resumed", "gid": gid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resuming download: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/download/{gid}")
async def remove_download(gid: str):
    """Remove a download"""
    try:
        success = await aria2_client.remove_download(gid)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to remove download")
        return {"status": "removed", "gid": gid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing download: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/downloads/active")
async def get_active_downloads():
    """Get list of active downloads"""
    try:
        downloads = await aria2_client.get_active_downloads()
        return {"count": len(downloads), "downloads": downloads}
    except Exception as e:
        logger.error(f"Error getting active downloads: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG,
    )
