#!/usr/bin/env python3
"""
Sample YouTube search results for a list of queries.

Usage:
  export YOUTUBE_API_KEY="your_key"
  python scripts/youtube_search_sampler.py --queries data/seed_queries.csv --out data/youtube_sample.csv --max-results 25
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Iterable, List

import requests
from dotenv import load_dotenv


YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def read_queries(path: str) -> List[Dict[str, str]]:
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
    response.raise_for_status()
    return response.json().get("items", [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", default="data/seed_queries.csv")
    parser.add_argument("--out", default="data/youtube_sample.csv")
    parser.add_argument("--max-results", type=int, default=25)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("Missing YOUTUBE_API_KEY environment variable.", file=sys.stderr)
        return 2

    queries = read_queries(args.queries)
    rows = []
    collected_at = datetime.now(timezone.utc).isoformat()

    for qrow in queries:
        query = qrow["query"]
        category = qrow.get("category", "")
        print(f"Searching: {query}")
        try:
            items = search_youtube(api_key, query, args.max_results)
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
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
