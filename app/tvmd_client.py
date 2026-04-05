"""TVMD API client wrapper.

Usage:
  - Expects `TVMD_API_KEY` and optional `TVMD_API_URL` in environment/config
  - Provides: find_series_id(name), get_series_seasons(series_id), get_season_episodes(series_id, season)
"""
from typing import Optional, List, Dict
import os
import logging
import requests

from app.config import config

logger = logging.getLogger(__name__)


class TVMDClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.getenv("TVMD_API_URL") or getattr(config, 'TVMD_API_URL', None) or "").rstrip("/")
        self.api_key = api_key or os.getenv("TVMD_API_KEY")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _get(self, path: str, params: dict = None, timeout: int = 10) -> Optional[requests.Response]:
        if not self.base_url:
            raise RuntimeError("TVMD API base URL not configured (TVMD_API_URL)")
        url = f"{self.base_url}/{path.lstrip('/') }"
        try:
            resp = self.session.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp
        except Exception as e:
            logger.error(f"TVMD request failed: {e} -- URL: {url}")
            return None

    def find_series_id(self, name: str) -> Optional[str]:
        """Find a series or movie id by name. Returns the id or None."""
        resp = self._get("search", params={"q": name, "type": "series"})
        if not resp:
            # fallback: search without type
            resp = self._get("search", params={"q": name})
        if not resp:
            return None
        try:
            data = resp.json()
            # Expect data['results'] list of items with 'id' and 'title'
            results = data.get("results") or []
            if not results:
                return None
            # Prefer exact match-like title if possible
            for r in results:
                title = r.get("title", "")
                if title.lower() == name.lower():
                    return r.get("id")
            # else return first
            return results[0].get("id")
        except Exception:
            return None

    def get_series_seasons(self, series_id: str) -> Optional[List[Dict]]:
        """Return list of season metadata for a series id. Each item may include season_number and name."""
        resp = self._get(f"series/{series_id}/seasons")
        if not resp:
            return None
        try:
            data = resp.json()
            return data.get("seasons") or data.get("data") or []
        except Exception:
            return None

    def get_season_episodes(self, series_id: str, season_number: int) -> Optional[List[Dict]]:
        """Return list of episode metadata for a given season (title, number).
        """
        resp = self._get(f"series/{series_id}/seasons/{season_number}/episodes")
        if not resp:
            return None
        try:
            data = resp.json()
            return data.get("episodes") or data.get("data") or []
        except Exception:
            return None


# Global client instance
tvmd_client = TVMDClient()
