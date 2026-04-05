"""Ollama AI integration for intelligent torrent selection"""
import logging
from typing import List, Dict, Optional
import requests
from app.scraper import TorrentInfo
from app.config import config

logger = logging.getLogger(__name__)


class OllamaSelector:
    """Use Ollama to intelligently select torrents for series"""
    
    def __init__(self, base_url: str = None, model: str = None):
        """
        Initialize Ollama selector
        
        Args:
            base_url: Ollama API base URL (default from config)
            model: Model name to use (default from config)
        """
        self.base_url = (base_url or config.OLLAMA_URL).rstrip("/")
        self.model = model or config.OLLAMA_MODEL
        self.timeout = 120000  #  seconds for Ollama response
    
    def _is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            logger.warning("Ollama service not available")
            return False
    
    class AlreadyPresent:
        def __init__(self, reason: str = ""):
            self.reason = reason

    def select_best_torrent(
        self,
        torrents: List[TorrentInfo],
        series_name: str,
        seasons_info: Optional[str] = None,
        existing_items: Optional[List[str]] = None,
    ) -> Optional[TorrentInfo] | "AlreadyPresent":
        """
        Use Ollama to select the best torrent for a series
        
        Args:
            torrents: List of torrent options
            series_name: Name of the series
            seasons_info: Information about seasons/episodes if available
            
        Returns:
            Selected TorrentInfo or None
        """
        if not config.USE_OLLAMA:
            logger.info("Ollama is disabled in config.")
            return None
            
        if not self._is_available():
            logger.error("Ollama service not available. Failing.")
            return None
        
        try:
            # Build prompt for Ollama
            torrents_text = self._format_torrents_for_prompt(torrents)
            
            # Determine if this is a series or movie based on seasons_info
            content_type = "series" if seasons_info else "movie"

            # Include existing_items for the LLM to decide if the requested
            # content is already present locally. Instruct the model to
            # respond with ALREADY_PRESENT: REASON if it determines the item
            # is already available.
            existing_text = "None"
            if existing_items:
                existing_text = "\n" + "\n".join(f"- {e}" for e in existing_items)

            prompt = f"""You are a torrent quality selector. Given these options for the {content_type} \"{series_name}\",\n
            First, check whether the requested content (movie/series) is already present in the following list of existing items (local files):\n
            {existing_text}\n
            If the item is already present, RESPOND EXACTLY with: ALREADY_PRESENT: <one-line reason explaining the match>.\n
            Otherwise, select the SINGLE BEST torrent based on these criteria (in order):\n
            1. PREFERRED RESOLUTION: 1080p (choose 1080p if available)\n+            2. Seed count (higher is better)\n+            3. File size (reasonable size, not too huge)\n+            4. Reliability and popularity\n
            {f'Series details: {seasons_info}' if seasons_info else ''}\n
            Available torrents:\n
            {torrents_text}\n
            Response format when NOT present: NUMBER: REASON (e.g., "2: 1080p and good seeds").\n
            Response format when present: ALREADY_PRESENT: REASON\n
            ONLY provide one line as the response."""
            
            logger.info(f"=== OLLAMA SELECTION ===")
            logger.info(f"Type: {content_type.upper()}")
            logger.info(f"Query: {series_name}")
            logger.info(f"Model: {self.model}")
            logger.info(f"Torrents to choose from: {len(torrents)}")
            logger.info(f"--- PROMPT START ---")
            for line in prompt.split("\n"):
                logger.info(line)
            logger.info(f"--- PROMPT END ---")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # Lower temperature for consistency
                },
                timeout=self.timeout,
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama API error: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return None
            
            result = response.json()
            response_text = result.get("response", "").strip()
            
            logger.info(f"--- RESPONSE START ---")
            logger.info(response_text)
            logger.info(f"--- RESPONSE END ---")
            
            # If the model indicates the item is already present, return sentinel
            if response_text.upper().startswith("ALREADY_PRESENT"):
                # Extract reason after ':'
                parts = response_text.split(":", 1)
                reason = parts[1].strip() if len(parts) > 1 else "Detected as present locally"
                logger.info(f"Ollama determined content already present: {reason}")
                return OllamaSelector.AlreadyPresent(reason)

            # Parse response to extract torrent number
            selection = self._parse_selection_response(response_text)
            logger.info(f"Parsed selection index: {selection}")

            # selection can be 0 (first item) so explicitly check for None
            if selection is not None and 0 <= selection < len(torrents):
                selected_torrent = torrents[selection]
                logger.info(
                    f"Ollama selected torrent #{selection+1}: {selected_torrent.name} (seeds: {selected_torrent.seeds})"
                )
                return selected_torrent
            else:
                logger.warning(f"Could not parse Ollama response: {response_text}")
                return None
                
        except Exception as e:
            logger.error(f"Error using Ollama: {e}")
            return None
    
    @staticmethod
    def _format_torrents_for_prompt(torrents: List[TorrentInfo]) -> str:
        """Format torrents for LLM prompt"""
        lines = []
        for i, t in enumerate(torrents, 1):
            lines.append(
                f"{i}. {t.name} | "
                f"Seeds: {t.seeds} | "
                f"Leeches: {t.leeches} | "
                f"Size: {t.size} | "
                f"Date: {t.upload_date}"
            )
        return "\n".join(lines)
    
    @staticmethod
    def _parse_selection_response(response: str) -> Optional[int]:
        """Parse LLM response to extract selection number"""
        try:
            import re

            # 1) Prefer a number at the start followed by ':' or similar: "1: reason"
            m = re.search(r"^\s*(\d{1,3})\s*[:\.\-]", response)
            if m:
                return int(m.group(1)) - 1

            # 2) Otherwise, find a small standalone number (1-99). Avoid matching '1080' from '1080p'
            nums = re.findall(r"\b(\d{1,2})\b", response)
            if nums:
                return int(nums[0]) - 1
        except:
            pass
        return None
    
    @staticmethod
    def _select_by_seeds(torrents: List[TorrentInfo]) -> Optional[TorrentInfo]:
        """Fallback: select torrent with best seed ratio"""
        if not torrents:
            return None
        
        # Sort by seed count and ration
        sorted_torrents = sorted(
            torrents,
            key=lambda t: (t.seeds, t.seeds / max(t.leeches, 1)),
            reverse=True,
        )
        
        best = sorted_torrents[0]
        logger.info(f"Selected by seeds: {best.name}")
        return best


# Global Ollama selector instance
ollama_selector = OllamaSelector()
