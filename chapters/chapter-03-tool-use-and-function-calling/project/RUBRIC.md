# Chapter 3 Project Rubric: Robust Tool Use for RepairBot

This project is a build-and-verify task (see `README.md` for why
deterministic fixtures are used instead of a live model). Grade your
own completed `starter.py` against the four criteria below, each worth
up to 5 points (20 points total).

## 1. Tool-selection function (TODO 1) (0-5)

- **5:** `diagnose_appliance_issue()` checks `check_warranty_status`
  first and returns immediately with `("check_warranty_status", ...)`
  when the warranty is expired, without ever calling `run_diagnostic`
  in that case; falls through to `run_diagnostic` correctly otherwise.
- **3:** The fallthrough case works, but the expired-warranty
  short-circuit is missing or still calls `run_diagnostic` anyway.
- **0:** Always returns the same tool regardless of warranty status.

## 2. Timeout-retry policy (TODO 2) (0-5)

- **5:** `run_diagnostic_with_retry()` retries on a timeout up to
  `max_retries` times and returns the real result once an attempt
  succeeds, exactly mirroring the lesson's timeout-handling pattern.
- **3:** Retries happen, but the attempt count or the recovered result
  is wrong (e.g., off-by-one on `attempt`).
- **0:** No retry logic at all, or the function crashes instead of
  returning `(None, max_retries)` when every attempt times out.

## 3. Outcome-verification function (TODO 3) (0-5)

- **5:** `verify_repair_outcome()` checks `get_repair_ticket_status`'s
  real `"status"` field and only reports `resolved: True` when it's
  exactly `"completed"` — never trusting `schedule_repair_visit`'s own
  reported success on its own.
- **3:** The function checks *something* but doesn't correctly
  distinguish "completed" from "scheduled" (e.g., treats any non-error
  status as resolved).
- **0:** Always returns the same `resolved` value regardless of ticket
  status, or never calls `get_repair_ticket_status` at all.

## 4. Self-check completeness (0-5)

- **5:** All 7 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-6 of the 7 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 3 (outcome verification) is the one most worth
getting to a full 5, since a tool that always reports success is the
failure type easiest to miss in a real production trace — nothing
ever throws an error.
