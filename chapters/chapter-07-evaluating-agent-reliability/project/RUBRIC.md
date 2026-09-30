# Chapter 7 Project Rubric: An Eval Harness for TriageScout

This project is a build-and-verify task (see `README.md` for why a
deterministic seeded simulation is used instead of a live model).
Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. `task_success` (TODO 1) (0-5)

- **5:** Correctly returns `True` only when `"pull_claim_record"` is
  present AND at least one of the task's `success_tools` is present
  anywhere in the trace, regardless of order or extra steps.
- **3:** Checks for a success tool but forgets to also require
  `"pull_claim_record"`, or vice versa.
- **0:** Always returns the same value regardless of trace content.

## 2. `trajectory_correctness` (TODO 2) (0-5)

- **5:** Correctly filters the trace to tools present in `expected`,
  collapses consecutive duplicates, and does an exact-order
  comparison — `True` for the correct order, `False` for any
  scrambled order, exactly mirroring the lesson's Section 7.
- **3:** Order-sensitivity works but consecutive-duplicate collapsing
  is missing, so a deliberate re-check trace incorrectly fails.
- **0:** Always returns the same value regardless of order, or crashes
  on a trace containing a tool not in `expected`.

## 3. `run_harness` (TODO 3) (0-5)

- **5:** Runs `simulate_agent_run` exactly `n_runs_per_task` times per
  task using one shared `random.Random(seed)` instance, computes both
  metrics per run, and returns a dict per task with
  `task_success_rate`, `trajectory_correctness_rate`, and the raw
  `successes` list (length 20) — all four self-check assertions pass.
- **3:** The rates are computed correctly, but the raw `successes`
  list is missing or the wrong length, breaking the pass@k check.
- **0:** Returns an empty dict, wrong keys, or crashes.

## 4. Self-check completeness (0-5)

- **5:** All 8 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-7 of the 8 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 3 (`run_harness`) is the one most worth getting
to a full 5, since a harness that computes correct rates but drops the
raw per-run successes list silently breaks every pass@k calculation
downstream — the exact kind of measurement gap this chapter's own
Section 16 checklist is built to catch.
