"""Compare canonical TVMD metadata with local filesystem and produce a download plan.

This module does lightweight comparisons and prepares a prompt for an LLM
to handle complex cases. It does NOT call an LLM itself — the caller (bot
or server) may do so.
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def compare_series_metadata(canonical: Dict, local_seasons: Dict[int, List[str]]) -> Dict:
    """Compare canonical series metadata with local tree.

    canonical: {
      'canonical_name', 'seasons' (int or None), 'episodes' (maybe total), 'per_season': {season: count}
    }

    local_seasons: { season_number: [filenames...] }

    Returns a plan dict with missing seasons/episodes and a prepared LLM prompt.
    """
    plan = {
        "canonical_name": canonical.get("canonical_name") or canonical.get("name"),
        "is_series": canonical.get("is_series", True),
        "year": canonical.get("year"),
        "seasons_canonical": canonical.get("seasons"),
        "per_season_canonical": canonical.get("per_season", {}),
        "local_seasons": local_seasons,
        "missing": {
            "seasons": [],
            "episodes": {},
        },
        "notes": [],
        "llm_prompt": None,
    }

    # Determine missing seasons
    if canonical.get("seasons"):
        for s in range(1, canonical["seasons"] + 1):
            if s not in local_seasons:
                plan["missing"]["seasons"].append(s)

    # Per-season episode check
    per_season = canonical.get("per_season") or {}
    for s, expected_count in per_season.items():
        s = int(s)
        local_list = local_seasons.get(s, [])
        if expected_count is None:
            continue
        if len(local_list) < int(expected_count):
            plan["missing"]["episodes"][s] = {
                "expected": int(expected_count),
                "found": len(local_list),
                "missing_count": int(expected_count) - len(local_list),
            }

    # If no per-season info, attempt simple heuristics using total episodes
    if not per_season and canonical.get("episodes"):
        total_expected = canonical.get("episodes")
        total_found = sum(len(v) for v in local_seasons.values())
        if total_found < total_expected:
            plan["missing"]["episodes"]["total"] = {"expected": total_expected, "found": total_found, "missing": total_expected - total_found}

    # Prepare LLM prompt for advanced strategy if complex (mixed multi-season torrents etc.)
    needs_llm = False
    if plan["missing"]["seasons"] or plan["missing"]["episodes"]:
        needs_llm = True

    if needs_llm:
        prompt_lines = []
        prompt_lines.append(f"Series: {plan['canonical_name']} ({plan.get('year') or 'unknown year'})")
        prompt_lines.append("Canonical seasons: " + str(plan.get("seasons_canonical")))
        prompt_lines.append("Canonical per-season counts: " + str(plan.get("per_season_canonical")))
        prompt_lines.append("Local folder tree (showing seasons and files):")
        for s, files in sorted(local_seasons.items()):
            prompt_lines.append(f"Season {s}: {len(files)} files -> {files[:10]}")
        prompt_lines.append("")
        prompt_lines.append("Task: Determine which seasons/episodes are missing and advise on downloads. If torrents provide full-season or multi-season bundles, suggest a strategy and mappings to place files into seasons. Output in JSON with keys: missing_seasons, missing_episodes, suggested_downloads where each download entry contains {type: 'season'|'episode'|'multi-season', season(s), episodes (if any), suggested_query, reason}.")
        plan["llm_prompt"] = "\n".join(prompt_lines)

    return plan
