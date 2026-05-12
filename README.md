# Topic Coverage Mapper

A practical research kit for estimating how much coverage exists for a topic on platforms like YouTube, then turning that landscape into distinctive client positioning.

This repo was created from a client strategy question:

> How much coverage exists on YouTube for topics such as “young adult career coaching / mentoring,” and how can we find a distinctive angle without reinventing the wheel?

The answer is not to chase a perfect count of videos. The better answer is to build a directional coverage map: what exists, who is saying it, which search phrases surface it, which content clusters are crowded, and where the current market is generic, stale, shallow, sales-heavy, or underserved.

## What this is

This is a client-ready research framework for:

- YouTube topic landscape scans
- content gap analysis
- early competitor mapping
- demand/supply comparison
- creator/content strategy discovery
- market positioning work
- lightweight client reports

The working example is **young adult career coaching / mentoring**, but the method can be reused for many topics.

## Core principle

Do not start with:

> How many videos are there?

Start with:

> What kinds of content dominate the search surface, what problems do they actually solve, what do they ignore, and where could a new entrant be meaningfully different?

YouTube search results and YouTube Data API results should be treated as **directional evidence**, not a complete census. Search is dynamic, personalized, time-sensitive, and affected by ranking systems.

## Repo structure

```text
.
├── README.md
├── docs/
│   ├── research-playbook.md
│   ├── client-brief-template.md
│   ├── query-map-young-adult-career-coaching.md
│   ├── coverage-scoring-rubric.md
│   ├── distinctive-positioning.md
│   ├── client-discovery-questions.md
│   ├── youtube-api-notes.md
│   └── project-operating-model.md
├── data/
│   ├── seed_queries.csv
│   ├── spreadsheet_template.csv
│   └── example_cluster_scores.csv
├── sample-outputs/
│   ├── client-memo-example.md
│   └── opportunity-hypotheses-example.md
├── scripts/
│   ├── youtube_search_sampler.py
│   ├── analyze_samples.py
│   └── build_client_report.py
├── requirements.txt
└── .gitignore
```

## Fast start

### Manual version

1. Open `data/seed_queries.csv`.
2. Search each phrase on YouTube.
3. Capture the top 25–50 results per phrase in `data/spreadsheet_template.csv`.
4. Deduplicate by video URL and channel.
5. Group videos into clusters.
6. Score each cluster using `docs/coverage-scoring-rubric.md`.
7. Summarize findings using `docs/client-brief-template.md`.

### API-assisted version

```bash
pip install -r requirements.txt
export YOUTUBE_API_KEY="your_api_key_here"
python scripts/youtube_search_sampler.py --queries data/seed_queries.csv --out data/youtube_sample.csv --max-results 25
python scripts/analyze_samples.py --input data/youtube_sample.csv --out sample-outputs/generated-summary.md
```

## Client-facing deliverable concept

A client deliverable from this repo could be called:

> YouTube Landscape Scan: Young Adult Career Coaching & Mentoring

It would include topic definition, search phrase map, sample size and caveats, top content clusters, recurring channels / voices, signs of demand, signs of content saturation, quality gaps, positioning opportunities, recommended content wedges, and suggested next experiments.

## Example positioning hypothesis

For the young adult career coaching example, the likely opportunity is not simply “career advice.” That space is crowded.

The stronger wedge may be:

> Plain-English career mentoring for young adults who are overwhelmed by vague advice, unsure how workplaces actually work, and need help translating messy experience into a credible next step.
