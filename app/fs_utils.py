"""Filesystem utilities for inspecting series folders."""
from pathlib import Path
from typing import Dict, List
import re


def build_tree(root: str, depth: int = 3) -> Dict:
    """Return a nested dict representing directory tree (limited depth).

    Example:
    {"name": "downloads/series/The Show", "dirs": [...], "files": [...]}
    """
    p = Path(root)
    def _node(path: Path, d: int):
        node = {"name": path.name, "path": str(path), "dirs": [], "files": []}
        if d <= 0:
            return node
        try:
            for child in sorted(path.iterdir()):
                if child.is_dir():
                    node["dirs"].append(_node(child, d-1))
                else:
                    node["files"].append(child.name)
        except Exception:
            pass
        return node

    return _node(p, depth)


_season_re = re.compile(r"(?:s(?:eason)?[\s._-]*0*(\d+))", re.I)
_ep_re = re.compile(r"(?:e(?:p|pisode)?[\s._-]*0*(\d+))", re.I)


def list_seasons_and_episodes(series_folder: str) -> Dict[int, List[str]]:
    """Return mapping season_number -> list of episode filenames (best-effort).

    Looks for directories named like 'Season 1', 'S01', or files named 'S01E02' patterns.
    """
    root = Path(series_folder)
    seasons = {}
    if not root.exists():
        return seasons

    # First: directories matching season patterns
    for child in sorted(root.iterdir()):
        if child.is_dir():
            m = _season_re.search(child.name)
            if m:
                season_no = int(m.group(1))
                files = [f.name for f in sorted(child.iterdir()) if f.is_file()]
                seasons.setdefault(season_no, []).extend(files)

    # Second: try to parse files in root that include SxxExx patterns
    for f in sorted(root.rglob("*")):
        if f.is_file():
            fname = f.name
            # S01E02
            m = re.search(r"S(\d{1,2})E(\d{1,2})", fname, re.I)
            if m:
                s = int(m.group(1))
                seasons.setdefault(s, []).append(fname)
                continue
            # season folderless pattern
            m2 = _season_re.search(fname)
            if m2:
                s = int(m2.group(1))
                seasons.setdefault(s, []).append(fname)

    # Normalize lists (unique, sorted)
    for s in list(seasons.keys()):
        items = sorted(list(dict.fromkeys(seasons[s])))
        seasons[s] = items

    return seasons
