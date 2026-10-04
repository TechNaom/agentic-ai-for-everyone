# Chapter 11 Project Rubric: An Overnight Operating Harness for Wrenfield Dispatch Alliance

This project is a build-and-verify task (see `README.md` for why
deterministic, constructed cases are used instead of a live model).
Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. `idempotency_key` + `commit_once` (TODO 1) (0-5)

- **5:** `idempotency_key` builds its key from `(agent, shipment_id,
  action)` only, never from a raw call-argument payload. `commit_once`
  checks and writes `_committed_keys` inside a single lock, returns
  `replayed: False` and runs `effect_fn()` on a fresh key, and returns
  `replayed: True` with the FIRST result (never re-running `effect_fn`)
  on a repeated key.
- **3:** The key and commit logic work for a fresh key, but a repeated
  key still re-runs `effect_fn` (defeats the "exactly once" guarantee)
  or the check-and-write isn't atomic under the lock.
- **0:** Always runs `effect_fn()` and returns `replayed: False`
  regardless of whether the key was seen before.

## 2. `call_with_retries` (TODO 2) (0-5)

- **5:** Retries up to `max_attempts` times, logs a `retry_attempt`
  event (with `ok`) for every attempt, sleeps
  `base_delay * (2 ** (attempt - 1))` between failed attempts (skipping
  the wait after the last one), and raises `RetriesExhausted` with a
  `retries_exhausted` event logged if every attempt fails.
- **3:** Retries correctly but doesn't log every attempt, or doesn't
  raise `RetriesExhausted` on total failure (e.g., returns `None`
  silently instead).
- **0:** Calls `fn()` exactly once with no retry logic at all.

## 3. `run_summary_from_log` (TODO 3) (0-5)

- **5:** Computes `dispatches`, `success_rate`, `commits`,
  `failed_retry_attempts`, and `exhausted` entirely by re-parsing the
  passed-in log lines with `json.loads` — matches the lesson's Section
  11 pattern exactly, and all case-dependent self-checks pass.
- **3:** Parses the log but one or more fields are computed
  incorrectly (e.g., `success_rate` counts all events, not just
  `dispatch` events).
- **0:** Always returns the all-zero default regardless of the log
  passed in.

## 4. Self-check completeness (0-5)

- **5:** All 9 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-8 of the 9 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 1 (`idempotency_key` + `commit_once`) is the
one most worth getting to a full 5, since a key built from the wrong
fields defeats the exact guarantee (a side effect commits exactly
once) this chapter's own Sections 4-5 build toward.
