#!/usr/bin/env python3
"""
Build a Markdown client report from the sampled YouTube data, the generated
analysis summary, and the cluster scorecard.

Intended pipeline:
  1. python scripts/youtube_search_sampler.py
  2. python scripts/analyze_samples.py
  3. python scripts/build_client_report.py
"""

import argparse
from pathlib import Path
from typing import Optional

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE = REPO_ROOT / "data" / "youtube_sample.csv"
DEFAULT_SUMMARY = REPO_ROOT / "sample-outputs" / "generated-summary.md"
DEFAULT_SCORES = REPO_ROOT / "data" / "example_cluster_scores.csv"
DEFAULT_OUT = REPO_ROOT / "sample-outputs" / "client-report-generated.md"


def read_markdown_if_exists(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def read_csv_if_exists(path: Path) -> Optional[pd.DataFrame]:
    if not path.exists():
        return None
    return pd.read_csv(path)


def append_sample_snapshot(lines: list[str], sample: pd.DataFrame, sample_path: Path) -> None:
    lines.extend([
        "## Sample snapshot",
        "",
        f"Sample file: `{sample_path}`",
        "",
        f"Raw rows: **{len(sample):,}**",
        "",
    ])

    if "url" in sample:
        lines.extend([f"Unique videos: **{sample['url'].nunique():,}**", ""])

    if "channel" in sample:
        lines.extend([f"Unique channels: **{sample['channel'].nunique():,}**", ""])

    if "query" in sample:
        lines.extend(["### Rows by query", ""])
        query_counts = sample["query"].value_counts().reset_index()
        query_counts.columns = ["query", "rows"]
        lines.extend([query_counts.to_markdown(index=False), ""])

    if "channel" in sample:
        lines.extend(["### Most repeated channels in sample", ""])
        channel_counts = sample["channel"].value_counts().head(20).reset_index()
        channel_counts.columns = ["channel", "rows"]
        lines.extend([channel_counts.to_markdown(index=False), ""])

    if "cluster" in sample and sample["cluster"].notna().any():
        lines.extend(["### Rows by cluster", ""])
        cluster_counts = sample["cluster"].fillna("Unclustered").value_counts().reset_index()
        cluster_counts.columns = ["cluster", "rows"]
        lines.extend([cluster_counts.to_markdown(index=False), ""])


def append_scorecard(lines: list[str], scores: pd.DataFrame, scores_path: Path) -> None:
    lines.extend([
        "## Cluster scorecard",
        "",
        f"Score file: `{scores_path}`",
        "",
        scores.to_markdown(index=False),
        "",
    ])

    if "opportunity_score" in scores and "cluster" in scores:
        lines.extend(["## Highest-priority opportunities", ""])
        top = scores.sort_values("opportunity_score", ascending=False).head(5)

        for _, row in top.iterrows():
            note = row.get("notes", "")
            lines.append(
                f"- **{row['cluster']}** — opportunity score {row['opportunity_score']}: {note}"
            )

        lines.append("")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--topic", default="Young Adult Career Coaching / Mentoring")
    args = parser.parse_args()

    sample = read_csv_if_exists(args.sample)
    summary = read_markdown_if_exists(args.summary)
    scores = read_csv_if_exists(args.scores)

    lines = [
        f"# YouTube Landscape Scan: {args.topic}",
        "",
        "## Executive summary",
        "",
        (
            "This is a directional landscape scan intended to identify coverage patterns, "
            "crowded areas, and distinctive opportunities. It combines the sampled YouTube "
            "data, the generated sample summary, and the cluster scorecard when those files "
            "are available."
        ),
        "",
    ]

    if sample is None:
        lines.extend([
            "## Sample snapshot",
            "",
            f"No sample CSV found at `{args.sample}`.",
            "",
            "Run `python scripts/youtube_search_sampler.py` first, or pass `--sample path/to/file.csv`.",
            "",
        ])
    else:
        append_sample_snapshot(lines, sample, args.sample)

    if summary is None:
        lines.extend([
            "## Generated analysis summary",
            "",
            f"No generated summary found at `{args.summary}`.",
            "",
            "Run `python scripts/analyze_samples.py` first, or pass `--summary path/to/generated-summary.md`.",
            "",
        ])
    else:
        lines.extend([
            "## Generated analysis summary",
            "",
            summary,
            "",
        ])

    if scores is None:
        lines.extend([
            "## Cluster scorecard",
            "",
            f"No scorecard found at `{args.scores}`.",
            "",
            "Create a cluster score CSV or pass `--scores path/to/scores.csv`.",
            "",
        ])
    else:
        append_scorecard(lines, scores, args.scores)

    lines.extend([
        "## Caveats",
        "",
        "- This is not a complete census of YouTube.",
        "- Search surfaces shift over time.",
        "- View count and ranking are directional signals, not proof of demand or fit.",
        "- Manual qualitative review is still needed before final recommendations.",
        "",
        "## Suggested next steps",
        "",
        "1. Review repeated channels and repeated themes.",
        "2. Manually tag audience, content angle, format, and cluster fields in the sample CSV.",
        "3. Update the cluster scorecard based on the actual sample.",
        "4. Re-run this report builder.",
        "5. Convert the strongest gaps into client-facing positioning and content experiments.",
    ])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())