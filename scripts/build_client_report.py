#!/usr/bin/env python3
"""
Build a simple Markdown client report from cluster scores.
"""

import argparse
from pathlib import Path
import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", default="data/example_cluster_scores.csv")
    parser.add_argument("--out", default="sample-outputs/client-report-generated.md")
    parser.add_argument("--topic", default="Young Adult Career Coaching / Mentoring")
    args = parser.parse_args()

    scores = pd.read_csv(args.scores)
    lines = [
        f"# YouTube Landscape Scan: {args.topic}",
        "",
        "## Executive summary",
        "",
        "This is a directional landscape scan intended to identify coverage patterns, crowded areas, and distinctive opportunities.",
        "",
        "## Cluster scorecard",
        "",
        scores.to_markdown(index=False),
        "",
        "## Highest-priority opportunities",
        "",
    ]

    if "opportunity_score" in scores:
        top = scores.sort_values("opportunity_score", ascending=False).head(5)
        for _, row in top.iterrows():
            lines.append(f"- **{row['cluster']}** — opportunity score {row['opportunity_score']}: {row.get('notes', '')}")

    lines.extend([
        "",
        "## Caveats",
        "",
        "- This is not a complete census of YouTube.",
        "- Search surfaces shift over time.",
        "- Manual qualitative review is needed before final recommendations.",
    ])

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
