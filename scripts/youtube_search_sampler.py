#!/usr/bin/env python3
"""
Sample YouTube search results for a list of queries.

Usage:
  export YOUTUBE_API_KEY="your_key"
  python scripts/youtube_search_sampler.py --queries data/seed_queries.csv --out data/youtube_sample.csv --max-results 25 --max-queries 3

Quota note:
  YouTube Data API search.list costs quota per query request. Reducing
  --max-results does not reduce the number of search calls; reducing
  --max-queries does.
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import requests
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUERIES = REPO_ROOT / "data" / "seed_queries.csv"
DEFAULT_OUT = REPO_ROOT / "data" / "youtube_sample.csv"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def read_queries(path: Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "query" not in reader.fieldnames:
            raise ValueError("Query CSV must include a 'query' column.")
        return list(reader)


def search_youtube(api_key: str, query: str, max_results: int) -> List[Dict]:
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": min(max_results, 50),
        "key": api_key,
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=30)

    if response.status_code == 403:
        try:
            payload = response.json()
            errors = payload.get("error", {}).get("errors", [])
            reasons = {error.get("reason") for error in errors}
            if "quotaExceeded" in reasons:
                raise RuntimeError(
                    "YouTube API quota exceeded. This is quota-unit exhaustion, "
                    "not a normal billing-credit issue. Wait for quota reset, "
                    "reduce --max-queries, reuse an existing sample with --skip-search, "
                    "or request a YouTube Data API quota increase."
                )
        except ValueError:
            pass

    response.raise_for_status()
    return response.json().get("items", [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-results", type=int, default=25)
    parser.add_argument(
        "--max-queries",
        type=int,
        default=None,
        help="Limit how many search phrases are sent to YouTube. This is the main quota-saving option.",
    )
    args = parser.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("Missing YOUTUBE_API_KEY environment variable.", file=sys.stderr)
        return 2

    queries = read_queries(args.queries)
    if args.max_queries is not None:
        queries = queries[: args.max_queries]

    if not queries:
        print("No queries to run.", file=sys.stderr)
        return 2

    print(
        f"Running {len(queries)} YouTube search request(s). "
        "To conserve quota, lower --max-queries or use run_pipeline.py --skip-search."
    )

    rows = []
    collected_at = datetime.now(timezone.utc).isoformat()

    for qrow in queries:
        query = qrow["query"]
        category = qrow.get("category", "")
        print(f"Searching: {query}")
        try:
            items = search_youtube(api_key, query, args.max_results)
        except RuntimeError as exc:
            print(f"Quota/error searching {query!r}: {exc}", file=sys.stderr)
            break
        except Exception as exc:
            print(f"Error searching {query!r}: {exc}", file=sys.stderr)
            continue

        for rank, item in enumerate(items, start=1):
            video_id = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})
            rows.append({
                "collected_at": collected_at,
                "query": query,
                "query_category": category,
                "platform": "YouTube",
                "rank": rank,
                "title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
                "publish_date": snippet.get("publishedAt", ""),
                "description": snippet.get("description", ""),
                "audience": "",
                "content_angle": "",
                "format": "",
                "cluster": "",
                "quality_notes": "",
                "gap_notes": "",
                "differentiation_notes": "",
            })

    fieldnames = [
        "collected_at","query","query_category","platform","rank","title","channel",
        "url","publish_date","description","audience","content_angle","format",
        "cluster","quality_notes","gap_notes","differentiation_notes"
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())