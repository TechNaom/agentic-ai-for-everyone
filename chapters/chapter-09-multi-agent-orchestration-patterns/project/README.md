# Chapter 9 Project: A Supervisor Harness for CityScout

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects. Per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, the **L3 Independent project** ("design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold") was deferred past Chapter 8 and has **still not been
built** as of this chapter — it is NOT built here either. See
`PROJECT_STATE.md`'s hand-off for Chapter 10, which restates this flag
explicitly so it is never silently dropped. This mini-project exists
so this chapter's own three pillars (fail-closed routing, per-worker
failure isolation, and an idempotent supervisor harness with
cross-agent attribution) get one combined, hands-on build of their
own, the same pattern Chapters 7-8's mini-projects used. Scenario:
**Ashgrove Municipal Services**, a fictional municipal
building-services office, wants **CityScout** built the same way the
lesson's TripScout was coordinated — a fresh scenario you build
yourself.

## The three pillars, combined

**Fail-closed routing.** `route_subtask()` returns the single
highest-scoring worker by keyword match — UNLESS the highest score is
0, in which case it returns `None` rather than guessing, the same
fail-closed discipline as the lesson's own router.

**Failure isolation.** `dispatch_isolated()` wraps a worker call in a
try/except so a worker's exception never propagates to the caller —
the caller always gets back a well-formed `{"ok": bool, ...}` dict.

**Idempotent, attributed supervisor harness.** `run_city_scout_harness()`
walks each case's subtasks, routes each one (skipping unroutable
subtasks, attributed to `"unrouted"`), skips a duplicate `(subtask,
worker)` dispatch instead of re-dispatching it, calls each worker
through the isolation boundary, and reports `which_agent_responsible()`
(given, reused from the lesson's own pattern) per case.

## The three TODOs

`starter.py` gives you both worker functions, the case fixtures, and
`which_agent_responsible()` already implemented — this project is
about the *coordination* layer, not re-building single-agent worker
mechanics.

1. **TODO 1** — `route_subtask()`: the fail-closed keyword router.
2. **TODO 2** — `dispatch_isolated()`: the per-worker failure
   isolation boundary.
3. **TODO 3** — `run_city_scout_harness()`: the assembled supervisor
   harness — routing, idempotent dispatch, isolated worker calls, and
   per-case attribution.

## Why a deterministic seeded simulation, not a live Ollama call

Same grading policy as this chapter's own lesson and every prior
chapter's `exercises/`/`practice/`/`project/`: `solution.py`'s
pass/fail checks never depend on a live model, so grading works the
same way everywhere, including CI with no Ollama server running.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 9 checks across routing, failure
isolation, and the aggregate supervisor harness.

## How to check your work for real

1. Run the structural self-check above until all 9 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional extension: add a per-worker budget (Section 10's pattern)
   to `run_city_scout_harness()`'s per-subtask walk, and report which
   case would have been budget-limited first.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 9 checks.
- `RUBRIC.md` — self-grading criteria.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  fourth scenario.
