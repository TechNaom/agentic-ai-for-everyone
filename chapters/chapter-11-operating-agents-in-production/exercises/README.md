# Chapter 11 Exercises: Operating Agents in Production

These exercises use a second scenario, deliberately different from
the lesson's Harrowgate Logistics Exchange/DockScout-YardScout hook:
**Cindermoor Parcel Network**, a fictional regional parcel sorting
cooperative. Its two PEER agents, **SortScout** and **RouteScout**,
must run unattended overnight — which means every claim needs an
idempotency key, every call/agent/exchange needs a timeout at the
right layer, every event needs a structured log line, and the night's
run needs a summary computed from that log. Applying this chapter's
production-operating concepts to a fresh scenario is the point —
recalling the lesson's answers by heart won't get you through these.

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

1. **Map facts to production-operating concepts** — assign the correct
   concept (idempotency, retries with backoff, per-call timeout,
   structured logging, crash-survivable run summary) to five Cindermoor
   facts.
2. **Retry de-duplication reasoning** — decide whether a retry system
   should de-duplicate by comparing raw call arguments.
3. **(Production-gear) `idempotency_key` + `commit_once`** — a side
   effect commits exactly once even across a retried call.
4. **(Production-gear) `call_with_retries`** — bounded attempts with
   exponential backoff, never silently unbounded.
5. **(Production-gear) `classify_timeout_layer`** — classify a failure
   description into the per-call, per-agent, or per-exchange layer.
6. **(Production-gear) `event` + `run_summary_from_log`** — structured
   JSON-line logging and a summary computed from the log alone.
7. **(Production-gear) `production_report`** — combine a run summary
   with Chapter 8's `is_within_budget`, reused unchanged.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 19/19.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
