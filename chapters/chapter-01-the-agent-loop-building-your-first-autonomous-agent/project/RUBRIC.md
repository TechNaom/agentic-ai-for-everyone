# Chapter 1 Project Rubric: Build and Trace a Minimal Agent Loop

This project is a build-and-verify task (see `README.md` for why a
gradable, deterministic `FakeModel` is used instead of a live model).
Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. Final-answer recognition (TODO 1) (0-5)

- **5:** `run_agent()` correctly recognizes a message with no
  `tool_calls` as a final answer and returns `(msg.content, trace)`
  immediately, without executing any further loop iterations.
- **3:** Final-answer detection works in the common case but the
  function keeps looping an extra iteration, or the returned `trace`
  is inconsistent with what actually happened.
- **0:** Final answers are never recognized (loop always falls through
  to the guard), or the wrong value is returned.

## 2. Action + observation execution (TODO 2) (0-5)

- **5:** Every requested tool call is parsed with `json.loads`,
  executed against the real function in `TOOL_IMPLS`, appended to
  `trace` as a real `(name, args, result)` tuple, and its result is
  correctly fed forward as `last_observation` for the model's next
  step.
- **3:** Tool calls are executed and traced, but `last_observation`
  isn't updated correctly, so the `FakeModel`'s second-turn answer is
  wrong even though the first-turn action was right.
- **0:** Tool calls are never actually executed, or `trace` is empty
  or wrong.

## 3. Guard correctness (TODO 3) (0-5)

- **5:** The loop halts cleanly at exactly `max_iterations` when the
  model never stops requesting tools, returning `(None, trace)` with
  `trace` containing exactly `max_iterations` entries — matches
  Check 4 in the self-check exactly.
- **3:** The guard eventually halts the loop but returns the wrong
  value, or the trace length is off by one due to an off-by-one loop
  bound.
- **0:** No guard — the function would loop indefinitely against a
  real runaway model (Python's `range(1, max_iterations + 1)` itself
  prevents an actual infinite loop here, but a wrong implementation
  that ignores `max_iterations` entirely still counts as 0).

## 4. Self-check completeness (0-5)

- **5:** All 4 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 2-3 of the 4 checks pass.
- **0:** 0-1 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass" — Criterion 3 (the guard) is the one most worth getting to
a full 5, since it's the exact mechanism Chapter 6 builds the rest of
this course's safety material on top of.
