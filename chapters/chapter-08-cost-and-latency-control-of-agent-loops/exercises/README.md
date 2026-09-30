# Chapter 8 Exercises: Cost and Latency Control of Agent Loops

These exercises use a second scenario, deliberately different from the
lesson's Greywick Dispatch/FactScout hook: **Brambleford Analytics**, a
fictional business-intelligence office. Its query agent,
**InsightScout**, can fetch a dataset, validate its freshness, compute
a summary, flag an anomaly, or escalate an uncertain result to a human
analyst. Applying this chapter's cost/latency-control concepts to a
fresh scenario is the point — recalling the lesson's answers by heart
won't get you through these.

## How to run

You'll need Python 3 installed. Check with:

```bash
python3 --version
```

Then run the starter file:

```bash
python3 starter.py
```

It prints a score report. Fill in each `# TODO`, re-run, and watch
your score climb toward the total (19 points across 7 tasks).

## The seven tasks

1. **Map facts to cost/latency-control concepts** — assign the correct
   concept (model routing, caching, early termination, fail-closed
   budget, latency percentile) to five InsightScout facts.
2. **Staleness/dependency reasoning** — decide whether a cache with no
   invalidation stays safe for a value that changes over time.
3. **(Production-gear) `step_cost`** — per-step token/cost accounting
   against a model-rate table.
4. **(Production-gear) `is_within_budget`** — a fail-closed check that
   denies a step if EITHER a step cap or a cost cap is exceeded.
5. **(Production-gear) `percentile`** — the standard linear-
   interpolation percentile estimator, for p50/p95 latency.
6. **(Production-gear) `classify_cost_control_gap`** — classify a
   cost-control setup's biggest blind spot from a capability dict.
7. **(Production-gear) `cache_hit_rate`** — hits divided by total
   lookups, guarded against division by zero.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 19/19.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
