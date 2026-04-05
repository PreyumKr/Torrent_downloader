"""Aria2 integration for torrent downloading"""
import asyncio
import json
import logging
from typing import Dict, Optional, List
import websockets
from uuid import uuid4
from app.config import config

logger = logging.getLogger(__name__)


class Aria2Client:
    """Client for Aria2 RPC interface"""
    
    def __init__(self, rpc_url: str = None, secret: str = None):
        """
        Initialize Aria2 client
        
        Args:
            rpc_url: WebSocket URL for Aria2 RPC (default from config)
            secret: RPC secret/token if required (default from config)
        """
        self.rpc_url = rpc_url or config.ARIA2_RPC_URL
        self.secret = secret or config.ARIA2_SECRET
        self.session = None
    
    async def _call_rpc(self, method: str, params: List = None) -> Dict:
        """
        Make an RPC call to Aria2
        
        Args:
            method: RPC method name
            params: List of parameters for the method
            
        Returns:
            Response dictionary
        """
        if params is None:
            params = []
        
        # Add secret token if configured
        if self.secret:
            params = [f"token:{self.secret}"] + params
        
        request = {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": method,
            "params": params,
        }
        
        try:
            async with websockets.connect(self.rpc_url) as websocket:
                await websocket.send(json.dumps(request))
                response = await asyncio.wait_for(websocket.recv(), timeout=10)
                return json.loads(response)
        except Exception as e:
            logger.error(f"Aria2 RPC error: {e}")
            return {"error": str(e)}
    
    async def add_torrent(
        self,
        magnet_link: str,
        output_dir: str,
        options: Dict = None,
    ) -> Optional[str]:
        """
        Add torrent download via magnet link
        
        Args:
            magnet_link: Magnet link URI
            output_dir: Output directory for download
            options: Additional options for aria2c
            
        Returns:
            GID (download ID) if successful, None otherwise
        """
        if options is None:
            options = {}
        
        # Default options
        default_options = {
            "dir": output_dir,
            "bt-max-peers": "55",
            "seed-time": "120",
            "bt-seed-uncontrolled": "false",
        }
        default_options.update(options)
        
        try:
            logger.info(f"[ARIA2] Adding torrent download to {output_dir}")
            logger.debug(f"[ARIA2] Magnet link: {magnet_link[:100]}...")
            logger.debug(f"[ARIA2] Options: {default_options}")
            
            response = await self._call_rpc("aria2.addUri", [[magnet_link], default_options])
            logger.debug(f"[ARIA2] RPC Response: {response}")
            
            if "result" in response:
                gid = response["result"]
                logger.info(f"[ARIA2] ✓ Torrent added with GID: {gid}")
                return gid
            else:
                error_msg = response.get('error', {}).get('message', 'Unknown error')
                logger.error(f"[ARIA2] Failed to add torrent: {error_msg}")
                return None
                return None
                
        except Exception as e:
            logger.error(f"Error adding torrent: {e}")
            return None
    
    async def get_download_status(self, gid: str) -> Dict:
        """
        Get download status
        
        Args:
            gid: Download ID
            
        Returns:
            Status dictionary
        """
        try:
            response = await self._call_rpc("aria2.tellStatus", [gid])
            
            if "result" in response:
                return response["result"]
            else:
                logger.error(f"Failed to get status: {response.get('error', 'Unknown error')}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting download status: {e}")
            return {}
    
    async def pause_download(self, gid: str) -> bool:
        """Pause a download"""
        try:
            response = await self._call_rpc("aria2.pause", [gid])
            return "result" in response
        except Exception as e:
            logger.error(f"Error pausing download: {e}")
            return False
    
    async def resume_download(self, gid: str) -> bool:
        """Resume a paused download"""
        try:
            response = await self._call_rpc("aria2.unpause", [gid])
            return "result" in response
        except Exception as e:
            logger.error(f"Error resuming download: {e}")
            return False
    
    async def remove_download(self, gid: str) -> bool:
        """Remove a download"""
        try:
            response = await self._call_rpc("aria2.remove", [gid])
            return "result" in response
        except Exception as e:
            logger.error(f"Error removing download: {e}")
            return False
    
    async def get_active_downloads(self) -> List[Dict]:
        """Get all active downloads"""
        try:
            response = await self._call_rpc("aria2.tellActive")
            if "result" in response:
                return response["result"]
            return []
        except Exception as e:
            logger.error(f"Error getting active downloads: {e}")
            return []
    
    async def get_completed_downloads(self) -> List[Dict]:
        """Get completed downloads"""
        try:
            response = await self._call_rpc("aria2.tellStopped", [0, 1000])
            if "result" in response:
                return response["result"]
            return []
        except Exception as e:
            logger.error(f"Error getting completed downloads: {e}")
            return []


# Global Aria2 client instance
aria2_client = Aria2Client()
