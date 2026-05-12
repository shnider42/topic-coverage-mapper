#!/usr/bin/env python3
"""
Generate a rough cluster scorecard from the sampled YouTube CSV.

This is intentionally heuristic. It is meant to turn the first-pass sample into
a changing, inspectable scorecard. Manual review should still replace or refine
these scores before a final client deliverable.
"""

import argparse
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SAMPLE = REPO_ROOT / "data" / "youtube_sample.csv"
DEFAULT_OUT = REPO_ROOT / "data" / "cluster_scores.csv"

CLUSTER_RULES = [
    ("Resume tips", ["resume", "cv"]),
    ("LinkedIn tips", ["linkedin", "linked in"]),
    ("Interview prep", ["interview", "behavioral", "hiring manager"]),
    ("Mentorship", ["mentor", "mentorship", "coach", "coaching"]),
    ("Career uncertainty", ["don't know", "dont know", "lost", "confused", "career path", "what career", "quarter life", "anxiety", "stuck"]),
    ("College-to-career transition", ["after college", "college graduate", "recent graduate", "graduate", "student"]),
    ("First job advice", ["first job", "entry level", "first corporate", "first office"]),
    ("Workplace navigation", ["manager", "workplace", "corporate", "office politics", "feedback", "soft skills", "professional"]),
    ("Career change", ["career change", "switch career", "pivot", "changing careers"]),
    ("Generic motivation", ["motivation", "motivational", "success", "habits", "mindset"]),
]

QUALITY_GAP_DEFAULTS = {
    "Resume tips": 2,
    "LinkedIn tips": 2,
    "Interview prep": 3,
    "Mentorship": 4,
    "Career uncertainty": 4,
    "College-to-career transition": 3,
    "First job advice": 4,
    "Workplace navigation": 4,
    "Career change": 3,
    "Generic motivation": 4,
    "Other / uncategorized": 3,
}

DISTINCTIVENESS_DEFAULTS = {
    "Resume tips": 2,
    "LinkedIn tips": 2,
    "Interview prep": 3,
    "Mentorship": 4,
    "Career uncertainty": 4,
    "College-to-career transition": 4,
    "First job advice": 4,
    "Workplace navigation": 5,
    "Career change": 3,
    "Generic motivation": 2,
    "Other / uncategorized": 3,
}

CLIENT_FIT_DEFAULTS = {
    "Resume tips": 3,
    "LinkedIn tips": 3,
    "Interview prep": 3,
    "Mentorship": 4,
    "Career uncertainty": 4,
    "College-to-career transition": 4,
    "First job advice": 5,
    "Workplace navigation": 5,
    "Career change": 3,
    "Generic motivation": 2,
    "Other / uncategorized": 3,
}


def score_from_count(count: int, max_count: int) -> int:
    if max_count <= 0:
        return 1
    ratio = count / max_count
    if ratio >= 0.80:
        return 5
    if ratio >= 0.55:
        return 4
    if ratio >= 0.30:
        return 3
    if ratio >= 0.12:
        return 2
    return 1


def infer_cluster(row: pd.Series) -> str:
    existing = str(row.get("cluster", "")).strip()
    if existing and existing.lower() not in {"nan", "none", "uncategorized"}:
        return existing

    haystack = " ".join(
        str(row.get(column, ""))
        for column in ["query", "query_category", "title", "description", "content_angle"]
    ).lower()

    for cluster, keywords in CLUSTER_RULES:
        if any(keyword in haystack for keyword in keywords):
            return cluster
    return "Other / uncategorized"


def build_scorecard(sample: pd.DataFrame) -> pd.DataFrame:
    sample = sample.copy()
    sample["derived_cluster"] = sample.apply(infer_cluster, axis=1)

    max_rows = int(sample["derived_cluster"].value_counts().max())
    rows = []

    for cluster, group in sample.groupby("derived_cluster"):
        raw_rows = len(group)
        unique_videos = group["url"].nunique() if "url" in group else raw_rows
        unique_channels = group["channel"].nunique() if "channel" in group else 0

        supply = score_from_count(raw_rows, max_rows)
        demand_signal = min(5, max(1, supply + (1 if unique_channels >= 5 else 0)))
        quality_gap = QUALITY_GAP_DEFAULTS.get(cluster, 3)
        freshness_gap = 3
        distinctiveness = DISTINCTIVENESS_DEFAULTS.get(cluster, 3)
        client_fit = CLIENT_FIT_DEFAULTS.get(cluster, 3)
        supply_penalty = 0 if supply <= 3 else 1 if supply == 4 else 2
        opportunity_score = (
            demand_signal
            + quality_gap
            + freshness_gap
            + distinctiveness
            + client_fit
            - supply_penalty
        )

        top_query = ""
        if "query" in group and not group["query"].dropna().empty:
            top_query = group["query"].value_counts().index[0]

        rows.append({
            "cluster": cluster,
            "sample_rows": raw_rows,
            "unique_videos": unique_videos,
            "unique_channels": unique_channels,
            "top_query": top_query,
            "supply": supply,
            "demand_signal": demand_signal,
            "quality_gap": quality_gap,
            "freshness_gap": freshness_gap,
            "distinctiveness": distinctiveness,
            "client_fit": client_fit,
            "opportunity_score": opportunity_score,
            "notes": "Auto-generated first-pass score. Review manually before client delivery.",
        })

    return pd.DataFrame(rows).sort_values(
        ["opportunity_score", "sample_rows"], ascending=[False, False]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    if not args.sample.exists():
        raise FileNotFoundError(
            f"Could not find sample CSV at {args.sample}. Run youtube_search_sampler.py first."
        )

    sample = pd.read_csv(args.sample)
    scorecard = build_scorecard(sample)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    scorecard.to_csv(args.out, index=False)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
