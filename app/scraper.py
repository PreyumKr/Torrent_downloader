"""Web scraper for multiple torrent sites with fallback support"""
import re
import time
import json
import cloudscraper
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import logging
from app.config import config

logger = logging.getLogger(__name__)


class TorrentInfo:
    """Data class for torrent information"""
    
    def __init__(
        self,
        name: str,
        magnet_link: str,
        seeds: int,
        leeches: int,
        size: str,
        upload_date: str,
        url: str,
    ):
        self.name = name
        self.magnet_link = magnet_link
        self.seeds = seeds
        self.leeches = leeches
        self.size = size
        self.upload_date = upload_date
        self.url = url
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "magnet_link": self.magnet_link,
            "seeds": self.seeds,
            "leeches": self.leeches,
            "size": self.size,
            "upload_date": self.upload_date,
            "url": self.url,
            "ratio": self.seeds / max(self.leeches, 1),  # Seeds to leech ratio
        }


class MultiSourceScraper:
    """Multi-source torrent scraper with fallback support"""
    
    def __init__(self):
        self.timeout = config.REQUEST_TIMEOUT
        self.scraper = cloudscraper.create_scraper()
        # TPB mirror that works reliably
        self.tpb_api_url = "https://apibay.org/q.php"
    
    def search_torrents(self, query: str, page: int = 1, max_retries: int = 2) -> List[TorrentInfo]:
        """
        Search for torrents via Pirate Bay API
        
        Args:
            query: Search query string
            page: Page number (default: 1)
            max_retries: Maximum retry attempts
            
        Returns:
            List of TorrentInfo objects
        """
        logger.info(f"Searching Pirate Bay API for: {query}")
        return self._search_pirate_bay(query)
    
    def _search_pirate_bay(self, query: str) -> List[TorrentInfo]:
        """
        Search The Pirate Bay using API
        
        Pirate Bay API returns: id, name, info_hash, leechers, seeders, num_files, size, pubdate, status
        """
        try:
            params = {"q": query}
            logger.info(f"Searching Pirate Bay API for: {query}")
            
            response = self.scraper.get(self.tpb_api_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, dict) and "error" in data:
                logger.error(f"Pirate Bay API error: {data['error']}")
                return []
            
            if not isinstance(data, list):
                logger.warning(f"Unexpected Pirate Bay response format: {type(data)}")
                logger.debug(f"Response data: {data}")
                return []
            
            torrents = []
            for item in data[:20]:  # Limit to 20 results
                try:
                    # Convert PB hash to magnet link
                    info_hash = item.get("info_hash", "").strip()
                    if not info_hash or len(info_hash) != 40:  # SHA1 hash must be 40 chars
                        logger.debug(f"Skipping invalid hash: {info_hash}")
                        continue
                    
                    # Reject all-zero hashes
                    if info_hash == "0000000000000000000000000000000000000000":
                        logger.debug(f"Skipping all-zero hash")
                        continue
                    
                    name = item.get("name", "Unknown").strip()
                    if not name or name == "Unknown":
                        logger.debug(f"Skipping unknown name")
                        continue
                    
                    seeders = int(item.get("seeders", 0))
                    leechers = int(item.get("leechers", 0))
                    
                    # Skip torrents with no seeds
                    if seeders < 1:
                        logger.debug(f"Skipping torrent with no seeds: {name}")
                        continue
                    
                    # Build magnet link from info hash with multiple trackers
                    magnet_link = (
                        f"magnet:?xt=urn:btih:{info_hash}"
                        f"&dn={name.replace(' ', '+')}"
                        f"&tr=udp://tracker.opentrackr.org:6969/announce"
                        f"&tr=udp://tracker.openbittorrent.com:80/announce"
                        f"&tr=udp://tracker.publicbt.com:80/announce"
                    )
                    
                    # Convert size in bytes to human readable
                    size_bytes = int(item.get("size", 0))
                    size = self._format_size(size_bytes)
                    
                    pubdate = item.get("pubdate", "Unknown")
                    
                    logger.info(f"[TORRENT-{len(torrents)+1}] Name: {name}")
                    logger.info(f"       Hash: {info_hash}")
                    logger.info(f"       Seeds: {seeders} | Leeches: {leechers} | Size: {size}")
                    
                    torrents.append(TorrentInfo(
                        name=name,
                        magnet_link=magnet_link,
                        seeds=seeders,
                        leeches=leechers,
                        size=size,
                        upload_date=str(pubdate),
                        url=f"https://thepiratebay.org/search.php?q={query}",
                    ))
                except Exception as e:
                    logger.error(f"Error parsing PB torrent: {e}", exc_info=True)
                    continue
            
            logger.info(f"Total valid torrents found: {len(torrents)} out of {len(data)}")
            return torrents
            
        except Exception as e:
            logger.error(f"Pirate Bay API search failed: {e}")
            return []
    
    @staticmethod
    def _parse_number(text: str) -> int:
        """Parse number from text (handles K, M suffixes)"""
        text = text.strip().lower()
        try:
            if "k" in text:
                return int(float(text.replace("k", "")) * 1000)
            elif "m" in text:
                return int(float(text.replace("m", "")) * 1000000)
            else:
                return int(float(text))
        except (ValueError, AttributeError):
            return 0
    
    @staticmethod
    def _format_size(bytes_size: int) -> str:
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f} {unit}".replace('.0 ', ' ')
            bytes_size /= 1024
        return f"{bytes_size:.1f} PB"


# Global scraper instance
scraper = MultiSourceScraper()
