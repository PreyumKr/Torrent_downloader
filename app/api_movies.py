"""FastAPI application for Movie downloads"""
import asyncio
import logging
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uvicorn

from app.config import config
from app.scraper import scraper
from app.aria2_handler import aria2_client
from app.ollama_selector import ollama_selector
from app.logging_config import configure_api_logging

# Configure API logging
configure_api_logging()
logger = logging.getLogger("movies_api")

app = FastAPI(
    title="Movie Downloader API",
    description="Dedicated service for movie downloads",
    version="1.0.0",
)

class DownloadRequest(BaseModel):
    name: str = Field(..., description="Name of the movie")
    year: Optional[int] = Field(None, description="Release year")
    out_folder: Optional[str] = Field(None)
    existing_items: Optional[List[str]] = Field(None)
    auto_select: bool = Field(True)

class DownloadResponse(BaseModel):
    status: str
    gid: Optional[str] = None
    torrent_name: str
    output_dir: str
    message: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "movie-downloader"}

@app.post("/download", response_model=DownloadResponse)
async def download_movie(request: DownloadRequest):
    try:
        output_folder = request.out_folder or str(Path(getattr(config, 'MOVIES_ROOT_FOLDER', None) or config.DEFAULT_DOWNLOAD_FOLDER).joinpath('movies'))
        output_dir = Path(output_folder)
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Movie Download Request: {request.name} ({request.year})")
        
        search_query = f"{request.name} {request.year}" if request.year else request.name
        torrents = scraper.search_torrents(search_query, page=1)
        
        if not torrents:
            raise HTTPException(status_code=404, detail="No torrents found")

        if request.auto_select:
            selected = ollama_selector.select_best_torrent(torrents, request.name, None, request.existing_items)
        else:
            selected = torrents[0]

        if isinstance(selected, ollama_selector.AlreadyPresent):
            return DownloadResponse(status="exists", torrent_name="", output_dir=str(output_dir), message=f"Already present: {selected.reason}")

        if not selected:
            raise HTTPException(status_code=400, detail="Could not select a torrent")

        gid = await aria2_client.add_torrent(selected.magnet_link, str(output_dir.absolute()))
        
        return DownloadResponse(
            status="downloading",
            gid=gid,
            torrent_name=selected.name,
            output_dir=str(output_dir.absolute()),
            message=f"Movie download started: {selected.name}"
        )
    except Exception as e:
        logger.error(f"Error in movie download: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
