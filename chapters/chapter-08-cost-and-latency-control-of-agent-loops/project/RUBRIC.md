# Chapter 8 Project Rubric: A Cost-Controlled Harness for YieldScout

This project is a build-and-verify task (see `README.md` for why a
deterministic seeded simulation is used instead of a live model).
Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. `task_success` (TODO 1) (0-5)

- **5:** Correctly returns `True` only when `"check_inventory_level"`
  is present AND at least one of the task's `success_tools` is present
  anywhere in the trace, regardless of order or extra steps.
- **3:** Checks for a success tool but forgets to also require
  `"check_inventory_level"`, or vice versa.
- **0:** Always returns the same value regardless of trace content.

## 2. `is_within_budget` (TODO 2) (0-5)

- **5:** Correctly returns `True` only when BOTH `steps_used <=
  max_steps` AND `cost_used <= max_cost` hold; `False` if either cap
  alone is exceeded — fail-closed, matching the lesson's `BudgetGuard`.
- **3:** Checks only one of the two caps (e.g., cost but not steps),
  so a step-budget violation alone is never caught.
- **0:** Always returns the same value regardless of the inputs.

## 3. `run_cost_controlled_harness` (TODO 3) (0-5)

- **5:** Runs `simulate_agent_run` exactly `n_runs_per_task` times per
  task using one shared `random.Random(seed)` instance, walks each
  resulting trace step by step applying `is_within_budget` BEFORE
  allowing each step (denying every step once the budget is
  exceeded), and returns a dict per task with `task_success_rate` and
  `total_cost` computed from the resulting (possibly truncated)
  traces — all self-check assertions pass.
- **3:** The harness runs and returns a dict of the right shape, but
  the budget check is applied after the fact (e.g., to the whole run)
  rather than per-step, so a run that should have been partially
  truncated is scored as if it ran in full.
- **0:** Returns an empty dict, wrong keys, or crashes.

## 4. Self-check completeness (0-5)

- **5:** All 9 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-8 of the 9 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 3 (`run_cost_controlled_harness`) is the one
most worth getting to a full 5, since a harness that checks the
budget only after a run completes silently defeats the entire point of
a *fail-closed* budget — the exact gap this chapter's own Section 5
warns against.
