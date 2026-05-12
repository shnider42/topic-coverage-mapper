#!/usr/bin/env python3
"""
Lightweight analysis for collected YouTube sample CSVs.
"""

import argparse
from pathlib import Path
import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/youtube_sample.csv")
    parser.add_argument("--out", default="sample-outputs/generated-summary.md")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    lines = []
    lines.append("# Generated YouTube Sample Summary\n")
    lines.append(f"Input file: `{args.input}`\n")
    lines.append(f"Raw rows: **{len(df):,}**\n")

    if "url" in df:
        lines.append(f"Unique videos: **{df['url'].nunique():,}**\n")
    if "channel" in df:
        lines.append(f"Unique channels: **{df['channel'].nunique():,}**\n")

    if "query" in df:
        lines.append("## Rows by query\n")
        counts = df["query"].value_counts().reset_index()
        counts.columns = ["query", "rows"]
        lines.append(counts.to_markdown(index=False))
        lines.append("")

    if "channel" in df:
        lines.append("## Most repeated channels in sample\n")
        channel_counts = df["channel"].value_counts().head(20).reset_index()
        channel_counts.columns = ["channel", "rows"]
        lines.append(channel_counts.to_markdown(index=False))
        lines.append("")

    if "cluster" in df and df["cluster"].notna().any():
        lines.append("## Rows by cluster\n")
        cluster_counts = df["cluster"].fillna("Unclustered").value_counts().reset_index()
        cluster_counts.columns = ["cluster", "rows"]
        lines.append(cluster_counts.to_markdown(index=False))
        lines.append("")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
