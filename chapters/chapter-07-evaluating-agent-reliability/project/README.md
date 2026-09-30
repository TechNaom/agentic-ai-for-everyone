# Chapter 7 Project: An Eval Harness for TriageScout

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects (per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, the L2 Assisted project closed at Chapter 6, and the next
numbered project, L3 Independent -- "design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold" -- ships after Chapter 8, not this chapter). This mini-project
exists so this chapter's own three pillars (task success, trajectory
correctness, and pass@k/variance) get one combined, hands-on build of
their own, the same "not yet on the numbered ladder" pattern Chapters
2-3 used before the L2 slot opened. Scenario: **Emberlyn Underwriting**,
a fictional insurance claims office, wants **TriageScout** built the
same way the lesson's FactScout was — a fresh scenario you build
yourself.

## The three pillars, combined

**Task success.** `task_success()` is deliberately forgiving: did the
trace include `pull_claim_record` and at least one of the tools that
actually produces this specific claim's correct outcome (a payout
estimate, an escalation, or a documents request — which one is correct
depends on the claim, exactly like the lesson's T1-T5 having different
`success_field`s).

**Trajectory correctness.** `trajectory_correctness()` is strict:
right tools, right order, collapsing only consecutive self-recovering
duplicates — mirroring the lesson's Section 7 exactly.

**Non-determinism.** `run_harness()` runs each task 20 times with a
single shared seeded `random.Random`, and returns each task's raw
per-run successes list so `pass_at_k()` (given, not a TODO) can be
computed on top of it — the same pass@1-vs-pass@3 distinction the
lesson's Section 11 taught.

## The three TODOs

`starter.py` gives you all three tasks, the claim fixtures, the seeded
`simulate_agent_run()`, and `pass_at_k()` already implemented — this
project is about the *harness-design* layer, not re-building the
lesson's tool-dispatch mechanics.

1. **TODO 1** — `task_success()`: the forgiving, order-independent
   check.
2. **TODO 2** — `trajectory_correctness()`: the strict, order-sensitive
   check.
3. **TODO 3** — `run_harness()`: runs both checks across N seeded runs
   per task and returns a results dict with the raw successes list.

## Why a deterministic seeded simulation, not a live Ollama call

Same grading policy as this chapter's own lesson (Section 10) and every
prior chapter's `exercises/`/`practice/`/`project/`: `solution.py`'s
pass/fail checks never depend on a live model, so grading works the
same way everywhere, including CI with no Ollama server running. The
lesson's own live, unscripted, six-run non-determinism test (Section 2)
is exactly the kind of result this offline harness makes cheap to
compute at scale (20 runs x 3 tasks, in milliseconds) once it's been
calibrated against a small number of real live calls, disclosed
honestly rather than presented as equivalent to live measurement.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 8 checks across task success,
trajectory correctness, and the aggregate harness (including a
pass@3 >= pass@1 sanity check).

## How to check your work for real

1. Run the structural self-check above until all 8 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional extension: swap `simulate_agent_run()` for a real
   `openai`-against-Ollama tool-selection call using the exact pattern
   from `lesson.html` Section 2, and compare the live result's
   variance against this harness's seeded simulation.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 8 checks.
- `RUBRIC.md` — self-grading criteria.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  fourth scenario.
