# Chapter 7 Exercises: Evaluating Agent Reliability

These exercises use a second scenario, deliberately different from the
lesson's Greywick Dispatch/FactScout hook: **Larkmoor Archive
Service**, a fictional historical-records office. Its research agent,
**RecordScout**, can search a property registry, check a record's
authenticity, cross-reference a deed against the registry, generate a
research report, or escalate an uncertain record to a human
archivist. Applying this chapter's eval concepts to a fresh scenario
is the point — recalling the lesson's answers by heart won't get you
through these.

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

1. **Map facts to eval concepts** — assign the correct concept (task
   success, trajectory correctness, pass@k, cost-per-success,
   multi-turn drift) to five RecordScout facts.
2. **Dependency reasoning** — decide whether a task-success check that
   only verifies tool presence catches a content error inside a
   tool's own output.
3. **(Production-gear) `trajectory_correctness`** — exact-order
   comparison against a ground-truth trajectory, collapsing
   consecutive duplicates.
4. **(Production-gear) `task_success`** — a forgiving, tool-presence
   check independent of order.
5. **(Production-gear) `pass_at_k`** — the unbiased pass@k estimator.
6. **(Production-gear) `diagnose_eval_gap`** — classify an eval
   setup's biggest blind spot from a capability dict.
7. **(Production-gear) `cost_per_success`** — cost divided by
   successes, not by total runs.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 19/19.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
