# Coverage Scoring Rubric

Use this rubric after collecting and clustering videos.

Each cluster receives a 1–5 score across the categories below.

## Scoring categories

### 1. Supply

How much content exists?

| Score | Meaning |
|---:|---|
| 1 | Very little visible content |
| 2 | Some content, but sparse |
| 3 | Moderate content |
| 4 | Crowded |
| 5 | Very crowded / saturated |

### 2. Demand signal

Do views, comments, recurring search presence, and related searches suggest audience demand?

| Score | Meaning |
|---:|---|
| 1 | Weak demand signal |
| 2 | Some interest |
| 3 | Moderate interest |
| 4 | Strong interest |
| 5 | Very strong interest |

### 3. Quality gap

Is the existing content shallow, repetitive, vague, outdated, salesy, or poorly matched to the audience?

| Score | Meaning |
|---:|---|
| 1 | Existing content is strong |
| 2 | Small quality gap |
| 3 | Noticeable quality gap |
| 4 | Large quality gap |
| 5 | Major quality gap |

### 4. Freshness gap

Is content stale, old, or disconnected from the current job market / culture / platform norms?

| Score | Meaning |
|---:|---|
| 1 | Current and fresh |
| 2 | Mostly current |
| 3 | Mixed |
| 4 | Somewhat stale |
| 5 | Very stale |

### 5. Distinctiveness potential

Can the client credibly say something different?

| Score | Meaning |
|---:|---|
| 1 | Hard to differentiate |
| 2 | Slight differentiation possible |
| 3 | Some distinctive angle |
| 4 | Strong distinctive angle |
| 5 | Very strong wedge |

### 6. Client fit

Does this cluster align with the client’s strengths, experience, story, and offer?

| Score | Meaning |
|---:|---|
| 1 | Poor fit |
| 2 | Weak fit |
| 3 | Plausible fit |
| 4 | Good fit |
| 5 | Excellent fit |

## Opportunity score

Suggested formula:

```text
opportunity_score =
  demand_signal
+ quality_gap
+ freshness_gap
+ distinctiveness_potential
+ client_fit
- supply_penalty
```

Where:

```text
supply_penalty = 0 if supply <= 3
supply_penalty = 1 if supply == 4
supply_penalty = 2 if supply == 5
```

## Interpretation

| Score | Meaning |
|---:|---|
| 20+ | Strong opportunity |
| 16–19 | Promising |
| 12–15 | Maybe / needs deeper review |
| <12 | Lower priority |

## Example

| Cluster | Supply | Demand | Quality Gap | Freshness Gap | Distinctiveness | Fit | Opportunity |
|---|---:|---:|---:|---:|---:|---:|---:|
| Resume tips | 5 | 5 | 2 | 2 | 2 | 3 | 10 |
| Workplace navigation | 2 | 4 | 4 | 3 | 5 | 5 | 21 |
| Career anxiety | 3 | 5 | 4 | 3 | 4 | 4 | 20 |
| LinkedIn tips | 5 | 4 | 2 | 2 | 2 | 3 | 9 |

The best opportunity is usually not the emptiest space. It is the space with visible demand, mediocre existing coverage, and a credible reason the client can be different.
