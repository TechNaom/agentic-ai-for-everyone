# Chapter 9 Project Rubric: A Supervisor Harness for CityScout

This project is a build-and-verify task (see `README.md` for why a
deterministic seeded simulation is used instead of a live model).
Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. `route_subtask` (TODO 1) (0-5)

- **5:** Correctly returns the highest-scoring worker by keyword
  match, and returns `None` (not a guess) when the highest score is
  0 — fail-closed, matching the lesson's router.
- **3:** Always returns some worker, never `None`, even when no
  keyword matches at all.
- **0:** Always returns the same value regardless of subtask content.

## 2. `dispatch_isolated` (TODO 2) (0-5)

- **5:** Correctly returns `{"ok": True, "result": ...}` on a normal
  call and `{"ok": False, "error": ...}` on any exception, with the
  exception NEVER propagating out of the function — fail-closed
  failure isolation, matching the lesson's Section 11 pattern.
- **3:** Catches the exception but crashes or returns an
  inconsistent shape on the success path (or vice versa).
- **0:** Lets the worker's exception propagate, crashing the caller.

## 3. `run_city_scout_harness` (TODO 3) (0-5)

- **5:** Correctly routes every subtask (attributing unroutable ones
  to `"unrouted"`), skips an already-dispatched `(subtask, worker)`
  pair via idempotency tracking, calls every routable, non-duplicate
  subtask through `dispatch_isolated`, and returns a per-case dict
  with an accurate `trace`, `success_rate`, and `first_failed_agent`
  — all self-check assertions pass.
- **3:** The harness runs and returns dicts of the right shape, but
  either the idempotency check or the unrouted-subtask handling is
  missing, so a duplicate gets re-dispatched or an unroutable subtask
  is silently skipped rather than attributed.
- **0:** Returns an empty dict, wrong keys, or crashes.

## 4. Self-check completeness (0-5)

- **5:** All 9 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-8 of the 9 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 3 (`run_city_scout_harness`) is the one most
worth getting to a full 5, since a harness that re-dispatches
duplicates or silently drops unroutable subtasks defeats the exact
two guarantees (idempotency and fail-closed routing) this chapter's
own Sections 6 and 13 build toward.
