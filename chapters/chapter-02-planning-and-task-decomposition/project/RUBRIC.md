# Chapter 2 Project Rubric: Dual-Mode Planning for RouteBot

This project is a build-and-verify task (see `README.md` for why
deterministic fixtures are used instead of a live model). Grade your
own completed `starter.py` against the four criteria below, each worth
up to 5 points (20 points total).

## 1. Fixed-plan executor with re-planning (TODO 1) (0-5)

- **5:** `run_fixed_dispatch()` runs all three steps of
  `FIXED_DISPATCH_ORDER` in order, correctly detects a failed step,
  and — when a `correction` is available and `max_replans` hasn't been
  exhausted — rebuilds the whole plan with the corrected `order_id`
  and retries, exactly mirroring the lesson's Section 13 guard.
- **3:** The happy path (no failure) works, but the re-planning branch
  is missing or doesn't actually retry with the correction, so Check 2
  in the self-check fails.
- **0:** No re-planning logic at all, or the function crashes instead
  of returning `(None, attempt)` when nothing can recover it.

## 2. Emergent decision function (TODO 2) (0-5)

- **5:** `decide_next_delay_check()` correctly returns
  `"get_delay_status"` with no history, then branches correctly on the
  notes text for all three real cases (traffic, weather/icy, checked
  in), and returns `None` once nothing more needs checking.
- **3:** Some branches work but not all three — e.g., traffic is
  detected correctly but weather or driver check-in isn't.
- **0:** The function always returns the same thing regardless of the
  notes content, so none of Checks 4-6 pass.

## 3. Planning-mode heuristic (TODO 3) (0-5)

- **5:** `classify_task_planning_mode()` implements the exact
  three-branch rule from Section 12: dependency on earlier results
  wins first (always "emergent" if true), then known-in-advance
  decides ("fixed" if true), with "emergent" as the final default.
- **3:** Two of the three test combinations classify correctly but not
  the third — usually the "both true" case, which should still return
  "emergent" (dependency wins over knowability).
- **0:** The function is a stub or always returns the same string.

## 4. Self-check completeness (0-5)

- **5:** All 7 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-6 of the 7 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 3 (the heuristic) is the one most worth getting
to a full 5, since it's the reusable design rule the rest of this
course expects you to apply on new tasks without being told which
strategy to use.
