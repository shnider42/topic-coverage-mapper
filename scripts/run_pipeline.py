#!/usr/bin/env python3
"""
Run the full topic coverage pipeline in sequence.

This script runs:
  1. youtube_search_sampler.py
  2. analyze_samples.py
  3. generate_cluster_scores.py
  4. build_client_report.py

It is intended to work on Windows, macOS, Linux, PyCharm, and hosted environments
as long as the required environment variables are available.
"""

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

DEFAULT_QUERIES = REPO_ROOT / "data" / "seed_queries.csv"
DEFAULT_SAMPLE = REPO_ROOT / "data" / "youtube_sample.csv"
DEFAULT_SUMMARY = REPO_ROOT / "sample-outputs" / "generated-summary.md"
DEFAULT_SCORES = REPO_ROOT / "data" / "cluster_scores.csv"
DEFAULT_REPORT = REPO_ROOT / "sample-outputs" / "client-report-generated.md"


def run_step(label: str, command: list[str]) -> None:
    print(f"\n=== {label} ===")
    print(" ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run YouTube sampling, analysis, scorecard generation, and client report generation."
    )
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--topic", default="Young Adult Career Coaching / Mentoring")
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Number of YouTube results per query. This affects row count, not search-call quota.",
    )
    parser.add_argument(
        "--max-queries",
        type=int,
        default=3,
        help="Number of search phrases to send to YouTube. This is the main quota-saving option.",
    )
    parser.add_argument(
        "--skip-search",
        action="store_true",
        help="Skip YouTube API collection and reuse the existing sample CSV.",
    )
    args = parser.parse_args()

    python = sys.executable

    if not args.skip_search:
        run_step(
            "1/4 Sampling YouTube search results",
            [
                python,
                str(SCRIPTS_DIR / "youtube_search_sampler.py"),
                "--queries",
                str(args.queries),
                "--out",
                str(args.sample),
                "--max-results",
                str(args.max_results),
                "--max-queries",
                str(args.max_queries),
            ],
        )
    else:
        print("\n=== 1/4 Skipping YouTube search ===")
        print(f"Reusing sample CSV: {args.sample}")

    run_step(
        "2/4 Analyzing sample CSV",
        [
            python,
            str(SCRIPTS_DIR / "analyze_samples.py"),
            "--input",
            str(args.sample),
            "--out",
            str(args.summary),
        ],
    )

    run_step(
        "3/4 Generating cluster scorecard",
        [
            python,
            str(SCRIPTS_DIR / "generate_cluster_scores.py"),
            "--sample",
            str(args.sample),
            "--out",
            str(args.scores),
        ],
    )

    run_step(
        "4/4 Building client report",
        [
            python,
            str(SCRIPTS_DIR / "build_client_report.py"),
            "--sample",
            str(args.sample),
            "--summary",
            str(args.summary),
            "--scores",
            str(args.scores),
            "--out",
            str(args.report),
            "--topic",
            args.topic,
        ],
    )

    print("\nPipeline complete.")
    print(f"Sample CSV: {args.sample}")
    print(f"Generated summary: {args.summary}")
    print(f"Cluster scorecard: {args.scores}")
    print(f"Client report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
