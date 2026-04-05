#!/usr/bin/env python
"""Test suite for the Torrent Downloader API"""
import asyncio
import json
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import requests
except ImportError:
    print("requests module not found. Install with: pip install requests")
    sys.exit(1)

# Import config to get DEFAULT_DOWNLOAD_FOLDER from .env
try:
        from app.config import config
        DEFAULT_FOLDER = str(config.DEFAULT_DOWNLOAD_FOLDER)
        # Optional per-type roots (can be set in app.config/.env)
        MOVIES_ROOT = getattr(config, "MOVIES_ROOT_FOLDER", None)
        SERIES_ROOT = getattr(config, "SERIES_ROOT_FOLDER", None)
except Exception:
    DEFAULT_FOLDER = "./downloads"


def resolve_out_folder(folder, content_type: str = "movie"):
    """Resolve an out_folder based on content type.

    content_type: 'movie' | 'series' | 'other'

    - 'movie'  -> use MOVIES_ROOT if set, otherwise DEFAULT_FOLDER/movies
    - 'series' -> use SERIES_ROOT if set, otherwise DEFAULT_FOLDER/series
    - 'other'  -> use DEFAULT_FOLDER directly

    Absolute `folder` values are returned unchanged. Relative `folder`
    values are joined onto the chosen base.
    """
    ct = (content_type or "movie").lower()

    if ct == "series":
        base = Path(SERIES_ROOT) if SERIES_ROOT else Path(DEFAULT_FOLDER).joinpath("series")
    elif ct == "movie":
        base = Path(MOVIES_ROOT) if MOVIES_ROOT else Path(DEFAULT_FOLDER).joinpath("movies")
    else:
        base = Path(DEFAULT_FOLDER)

    if folder is None:
        return str(base)

    p = Path(folder)
    if p.is_absolute():
        return str(p)

    try:
        return str(base.joinpath(p))
    except Exception:
        return str(Path(DEFAULT_FOLDER).joinpath(p))


def list_existing_items(content_type: str = "movie") -> list:
    """Return a list of existing top-level items under the chosen root.

    content_type: 'movie' | 'series' | 'other'
    """
    ct = (content_type or "movie").lower()
    if ct == "series":
        root_path = Path(SERIES_ROOT) if SERIES_ROOT else Path(DEFAULT_FOLDER).joinpath("series")
    elif ct == "movie":
        root_path = Path(MOVIES_ROOT) if MOVIES_ROOT else Path(DEFAULT_FOLDER).joinpath("movies")
    else:
        root_path = Path(DEFAULT_FOLDER)

    if not root_path.exists():
        return []

    items = []
    try:
        for child in sorted(root_path.iterdir()):
            items.append(child.name)
    except Exception:
        return []
    return items


class APITester:
    """Test the Torrent Downloader API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self) -> bool:
        """Test health check endpoint"""
        print("Testing health endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("[OK] Health check passed")
                print(f"  Response: {response.json()}\n")
                return True
            else:
                print(f"[FAIL] Health check failed: {response.status_code}\n")
                return False
        except Exception as e:
            print(f"[FAIL] Health check error: {e}\n")
            return False
    
    def test_search(self) -> bool:
        """Test search endpoint"""
        print("Testing search endpoint...")
        try:
            response = self.session.post(
                f"{self.base_url}/search",
                json={
                    "query": "The Matrix",
                    "is_series": False,
                    "year": 1999,
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Search successful")
                print(f"  Found {data['results_count']} torrents")
                print(f"  Query: {data['query']}")
                if data['torrents']:
                    print(f"  Top result: {data['torrents'][0]['name']}")
                print()
                return True
            else:
                print(f"✗ Search failed: {response.status_code}")
                print(f"  Response: {response.text}\n")
                return False
        except Exception as e:
            print(f"✗ Search error: {e}\n")
            return False
    
    def test_search_series(self) -> bool:
        """Test series search"""
        print("Testing series search...")
        try:
            response = self.session.post(
                f"{self.base_url}/search",
                json={
                    "query": "Breaking Bad",
                    "is_series": True,
                    "max_results": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Series search successful")
                print(f"  Found {data['results_count']} torrents")
                if data['plan']:
                    plan = data['plan']
                    print(f"  Type: {plan.get('type')}")
                    print(f"  Search query: {plan.get('search_query')}")
                    if 'total_seasons' in plan:
                        print(f"  Seasons: {plan['total_seasons']}")
                print()
                return True
            else:
                print(f"✗ Series search failed: {response.status_code}\n")
                return False
        except Exception as e:
            print(f"✗ Series search error: {e}\n")
            return False
    
    def test_download_movie(self) -> bool:
        """Test movie download with Ollama selection"""
        print("Testing movie download with Ollama selection...")
        try:
            out_folder = resolve_out_folder(None, content_type="movie")
            Path(out_folder).mkdir(parents=True, exist_ok=True)

            # Provide list of already-downloaded movies to the server/LLM
            existing = list_existing_items("movie")

            response = self.session.post(
                f"{self.base_url}/download",
                json={
                    "name": "The Matrix",
                    "year": 1999,
                    "is_series": False,
                    "out_folder": out_folder,
                    "existing_items": existing,
                    "auto_select": True
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Download started successfully")
                print(f"  GID: {data.get('gid')}")
                print(f"  Torrent: {data.get('torrent_name')}")
                print(f"  Status: {data.get('status')}")
                print(f"  Message: {data.get('message')}")
                print()
                return True
            else:
                print(f"✗ Download failed: {response.status_code}")
                print(f"  Response: {response.text}\n")
                return False
        except Exception as e:
            print(f"✗ Download error: {e}\n")
            return False
    
    def test_custom_movie(self, name: str, year: int = None, folder: str = None) -> bool:
        """Test movie download with custom movie name
        
        Args:
            name: Movie name to search for
            year: Release year (optional)
            folder: Download folder (default: from .env DEFAULT_DOWNLOAD_FOLDER)
        """
        # Resolve relative folder paths against DEFAULT_FOLDER root (movie by default)
        folder = resolve_out_folder(folder, content_type="movie")
        Path(folder).mkdir(parents=True, exist_ok=True)
        # Provide the server with list of existing movies so the LLM can decide
        existing = list_existing_items("movie")
        print(f"\nTesting custom movie download: '{name}' {f'({year})' if year else ''}")
        print("=" * 60)
        
        try:
            # First search to see what torrents are available
            print(f"\n1. Searching for torrents...")
            search_response = self.session.post(
                f"{self.base_url}/search",
                json={
                    "query": f"{name} {year}" if year else name,
                    "is_series": False,
                    "year": year,
                    "max_results": 10
                }
            )
            
            if search_response.status_code != 200:
                print(f"[FAIL] Search failed: {search_response.status_code}")
                return False
            
            search_data = search_response.json()
            torrents_found = search_data.get('results_count', 0)
            
            if torrents_found == 0:
                print(f"[FAIL] No torrents found for '{name}'")
                return False
            
            print(f"[OK] Found {torrents_found} torrents")
            print(f"\nAvailable torrents:")
            for i, torrent in enumerate(search_data['torrents'][:5], 1):
                seeds = torrent.get('seeds', 0)
                size = torrent.get('size', 'N/A')
                print(f"  [{i}] {torrent['name']}")
                print(f"      Seeds: {seeds} | Size: {size}")
            
            # Now download using auto-select
            print(f"\n2. Starting download with auto-selection...")
            download_response = self.session.post(
                f"{self.base_url}/download",
                json={
                    "name": name,
                    "year": year,
                    "is_series": False,
                    "out_folder": folder,
                    "existing_items": existing,
                    "auto_select": True
                }
            )
            
            if download_response.status_code == 200:
                data = download_response.json()
                print(f"\n[OK] Download started successfully!")
                print(f"\nDownload Details:")
                print(f"  GID: {data.get('gid')}")
                print(f"  Torrent: {data.get('torrent_name')}")
                print(f"  Status: {data.get('status')}")
                print(f"  Output: {data.get('output_dir')}")
                print(f"  Message: {data.get('message')}")
                print()
                return True
            else:
                print(f"[FAIL] Download failed: {download_response.status_code}")
                print(f"  Response: {download_response.text}\n")
                return False
                
        except Exception as e:
            print(f"[FAIL] Error: {e}\n")
            import traceback
            traceback.print_exc()
            return False
    
    def run_all_tests(self) -> dict:
        """Run all tests"""
        print("=" * 60)
        print("Torrent Downloader API Test Suite")
        print("=" * 60)
        print(f"Testing: {self.base_url}\n")
        
        results = {}
        # Run non-destructive tests by default
        results['health'] = self.test_health()
        results['search'] = self.test_search()
        results['series_search'] = self.test_search_series()
        # NOTE: Download tests are disabled by default to avoid automatic downloads.
        # If you want to include download tests, run the script with --run-all.
        
        # Summary
        print("=" * 60)
        print("Test Summary")
        print("=" * 60)
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"Passed: {passed}/{total}\n")
        
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {status}: {test_name}")
        
        print()
        return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test the Torrent Downloader API"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--movie",
        type=str,
        help="Download specific movie (e.g., --movie 'Inception 2010')"
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Movie release year (used with --movie)"
    )
    parser.add_argument(
        "--folder",
        type=str,
        default=DEFAULT_FOLDER,
        help=f"Download folder (default: {DEFAULT_FOLDER} from .env)"
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run all standard tests (default behavior)"
    )
    
    args = parser.parse_args()
    
    # Check if API is reachable
    try:
        requests.get("http://localhost:8000/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API at http://localhost:8000")
        print("\nMake sure to start the API first:")
        print("  python -m uvicorn app.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    tester = APITester(args.url)
    
    # If --movie is specified, test custom movie (explicit user action)
    if args.movie:
        print("\n" + "=" * 60)
        print("CUSTOM MOVIE DOWNLOAD TEST")
        print("=" * 60)
        result = tester.test_custom_movie(
            name=args.movie,
            year=args.year,
            folder=args.folder
        )
        sys.exit(0 if result else 1)

    # Otherwise, run default safe tests (no downloads)
    print("=" * 60)
    print("Torrent Downloader API Test Suite (safe mode)")
    print("=" * 60)
    print(f"Testing: {args.url}\n")
    
    results = {}
    results['health'] = tester.test_health()
    results['search'] = tester.test_search()
    results['series_search'] = tester.test_search_series()

    # If user explicitly requests full run, include download tests
    if args.run_all:
        print("\n-- Running full tests including downloads (requested via --run-all) --\n")
        results['download_movie'] = tester.test_download_movie()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print()
    
    # Interactive mode
    print("=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("  1. Download a custom movie")
        print("  2. Search for torrents")
        print("  3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            movie_name = input("Enter movie name: ").strip()
            if not movie_name:
                print("Movie name cannot be empty")
                continue
            
            year_input = input("Enter year (optional, press Enter to skip): ").strip()
            year = int(year_input) if year_input else None
            
            folder = input(f"Enter download folder (default: {DEFAULT_FOLDER}): ").strip() or DEFAULT_FOLDER
            
            result = tester.test_custom_movie(
                name=movie_name,
                year=year,
                folder=folder
            )
            
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if not query:
                print("Search query cannot be empty")
                continue
            
            print(f"\nSearching for: {query}")
            try:
                response = tester.session.post(
                    f"{tester.base_url}/search",
                    json={
                        "query": query,
                        "is_series": False,
                        "max_results": 10
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"\nFound {data.get('results_count', 0)} torrents:\n")
                    for i, torrent in enumerate(data.get('torrents', []), 1):
                        print(f"[{i}] {torrent['name']}")
                        print(f"    Seeds: {torrent.get('seeds', 0)} | Size: {torrent.get('size', 'N/A')}\n")
                else:
                    print(f"Search failed: {response.status_code}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select 1-3.")
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
