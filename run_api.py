#!/usr/bin/env python
"""Entry point script for running separated Torrent Downloader APIs"""
import sys
import os
import subprocess
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def start_aria2c():
    """Start aria2c daemon if enabled in .env"""
    aria2_enabled = os.getenv("ARIA2_ENABLED", "true").lower() == "true"
    if not aria2_enabled:
        return
    
    aria2_port = os.getenv("ARIA2_PORT", "6800")
    aria2_path = Path("./aria2-1.37/aria2c.exe")
    
    if not aria2_path.exists():
        print(f"[WARNING] aria2c not found at {aria2_path.absolute()}")
        return
    
    print(f"[INFO] Starting aria2c on port {aria2_port}...")
    subprocess.Popen(
        [str(aria2_path.absolute()), "--enable-rpc", "--rpc-listen-all=true", f"--rpc-listen-port={aria2_port}", "--daemon"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(1)

if __name__ == "__main__":
    start_aria2c()
    
    api_host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"\n[INFO] Starting Movie API on {api_host}:8001...")
    movie_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.api_movies:app", "--host", api_host, "--port", "8001"])
    
    print(f"[INFO] Starting Series Test API on {api_host}:8002...")
    series_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.api_series:app", "--host", api_host, "--port", "8002"])

    print("\nServices are running. Press Ctrl+C to stop all.")
    try:
        movie_proc.wait()
        series_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        movie_proc.terminate()
        series_proc.terminate()
        print("Done.")
