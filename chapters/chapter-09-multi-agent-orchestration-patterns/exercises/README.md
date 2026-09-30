# Chapter 9 Exercises: Multi-Agent Orchestration Patterns

These exercises use a second scenario, deliberately different from
the lesson's Quillmark Journeys/TripScout hook: **Hadleigh Civic
Records Bureau**, a fictional municipal records office. Its
supervisor agent, **CaseScout**, decomposes an incoming case request
and dispatches sub-tasks to three specialist workers: **PermitScout**
(building permits), **LicenseScout** (business licenses), and
**ZoningScout** (zoning/variance questions). Applying this chapter's
supervisor/worker concepts to a fresh scenario is the point —
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

1. **Map facts to multi-agent coordination concepts** — assign the
   correct concept (failure isolation, idempotent dispatch,
   cross-agent attribution, content verification, fail-closed
   routing) to five CaseScout facts.
2. **Fail-closed routing reasoning** — decide whether a supervisor
   should dispatch to a worker when the router has no confident match.
3. **(Production-gear) `route_subtask`** — a fail-closed keyword
   router that returns `None` rather than guessing.
4. **(Production-gear) `verify_worker_result`** — content
   verification: does the result actually match what was requested.
5. **(Production-gear) `which_agent_responsible`** — cross-agent
   trajectory attribution, extending Chapter 7's tool-level version.
6. **(Production-gear) `classify_coordination_gap`** — classify a
   multi-agent setup's biggest blind spot from a capability dict.
7. **(Production-gear) `is_duplicate_dispatch`** — idempotency check
   keyed on the exact (subtask, worker) pair.

## Files

- `starter.py` — the scaffold with 11 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 19/19.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
