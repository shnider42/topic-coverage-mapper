# YouTube API Notes

## Use case

The YouTube Data API can be used to sample search results, collect video metadata, and create a directional view of platform coverage.

## Important constraints

The API is not a perfect way to count all YouTube videos on a topic. It is better used for structured sampling.

## Quota notes

Google’s official documentation says:

- `search.list` returns search results matching query parameters.
- `search.list` has a quota cost of 100 units per call.
- YouTube Data API projects have a default quota allocation of 10,000 units per day.
- Quotas can change and should be checked in Google Cloud Console.

Useful docs:

- Search endpoint: https://developers.google.com/youtube/v3/docs/search/list
- Quota cost calculator: https://developers.google.com/youtube/v3/determine_quota_cost
- Quota and compliance: https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits

## Practical implication

At 100 units per `search.list` request, a default 10,000 unit quota can support roughly 100 search requests per day before considering other API calls.

However:

- pagination costs more quota
- enrichment calls cost additional quota
- invalid requests can still consume quota
- quotas are project-level

## Suggested sampling approach

For a lean scan:

```text
15 queries × 1 search request each = 1,500 quota units
```

For a deeper scan:

```text
40 queries × 2 pages each = 8,000 quota units
```

Then use low-cost metadata enrichment where needed.

## Manual alternative

Manual sampling is acceptable for early client discovery:

1. Search phrase in YouTube.
2. Capture first 25–50 results.
3. Repeat across phrases.
4. Deduplicate.
5. Cluster and score.

Manual sampling can be more useful than the API when qualitative interpretation is the main goal.
