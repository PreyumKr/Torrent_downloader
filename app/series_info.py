"""Series information lookup via Google"""
import logging
import re
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class SeriesInfoLookup:
    """Lookup series information including seasons and episodes"""
    
    @staticmethod
    def get_series_info(series_name: str) -> Optional[Dict]:
        """
        Search Google for series information (seasons and episodes)
        
        Args:
            series_name: Name of the series
            
        Returns:
            Dictionary with series info or None
        """
        try:
            # Google search
            search_url = "https://www.google.com/search"
            params = {
                "q": f"{series_name} seasons episodes",
                "hl": "en",
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            logger.info(f"Looking up series info for: {series_name}")
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract seasons info from knowledge panel or snippets
            info_text = soup.get_text()
            
            # Try to extract seasons information
            seasons_match = re.search(r'(\d+)\s+seasons?', info_text, re.IGNORECASE)
            episodes_match = re.search(r'(\d+)\s+episodes?', info_text, re.IGNORECASE)
            
            info = {}
            if seasons_match:
                info["seasons"] = int(seasons_match.group(1))
            if episodes_match:
                info["episodes"] = int(episodes_match.group(1))
            
            if info:
                logger.info(f"Found info for {series_name}: {info}")
                return info
            
            logger.warning(f"Could not find detailed series info for: {series_name}")
            return {"note": "Could not determine seasons/episodes, using heuristics"}
            
        except Exception as e:
            logger.error(f"Error looking up series info: {e}")
            return None


class DownloadPlanner:
    """Plan what to download for movies vs series"""
    
    @staticmethod
    def plan_download(
        name: str,
        is_series: bool,
        year: Optional[int] = None,
    ) -> Dict:
        """
        Create a download plan based on whether it's a movie or series
        
        Args:
            name: Content name
            is_series: Whether this is a series
            year: Release year (optional)
            
        Returns:
            Dictionary with download plan
        """
        plan = {
            "name": name,
            "type": "series" if is_series else "movie",
            "year": year,
            "search_query": name,
            "expected_torrents": [],
            "notes": [],
        }
        
        if is_series:
            # For series, look up seasons/episodes
            series_info = SeriesInfoLookup.get_series_info(name)
            
            if series_info and "seasons" in series_info:
                seasons = series_info["seasons"]
                plan["total_seasons"] = seasons
                plan["notes"].append(
                    f"Series has {seasons} seasons. "
                    "Ollama will help select the best complete torrent."
                )
                plan["search_query"] = f"{name} complete collection"
            else:
                plan["notes"].append(
                    "Could not determine total seasons. "
                    "Will search and use Ollama to select quality torrent."
                )
            
            plan["expected_torrents"].append("Complete series torrent")
            plan["expected_torrents"].append("Season pack torrents")
            plan["expected_torrents"].append("Individual season torrents")
            
        else:
            # For movies
            if year:
                plan["search_query"] = f"{name} {year}"
            
            plan["notes"].append("Movie download. Select torrent with best quality and seeds.")
            plan["expected_torrents"].append("Full movie torrent")
        
        return plan


series_lookup = SeriesInfoLookup()
plan_generator = DownloadPlanner()

# NOTE: Google/Wikipedia helper code removed in favor of TVMD API usage.
