# Chapter 8 Project: A Cost-Controlled Harness for YieldScout

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects (per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, the L3 Independent project -- "design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold" -- ships AFTER Chapter 8, not during it). This mini-project
exists so this chapter's own three pillars (per-step accounting, a
fail-closed budget, and a cost-controlled harness reusing
`cost_per_success`) get one combined, hands-on build of their own, the
same pattern Chapter 7's TriageScout mini-project used. Scenario:
**Portage Grain Cooperative**, a fictional grain-storage cooperative,
wants **YieldScout** built the same way the lesson's FactScout was
cost-controlled — a fresh scenario you build yourself.

## The three pillars, combined

**Task success.** `task_success()` is deliberately forgiving: did the
(possibly budget-truncated) trace include `check_inventory_level` and
at least one of the tools that actually produces this specific silo's
correct outcome (a yield estimate, a quality flag, or an escalation —
which one is correct depends on the silo, exactly like the lesson's
T1-T5 having different `success_field`s).

**Fail-closed budget.** `is_within_budget()` is strict: both a step
cap AND a dollar-cost cap must be respected — exceeding EITHER one
denies the step, the same fail-closed discipline as the lesson's
`BudgetGuard`.

**Cost-controlled harness.** `run_cost_controlled_harness()` runs each
task 20 times with a single shared seeded `random.Random`, walking
each simulated trace step by step and applying `is_within_budget()`
before allowing each step — any step past the budget is denied, and
the harness reports the resulting truncated success rate and total
cost, on top of which `cost_per_success()` (given, reused from Chapter
7's own pattern) can be computed.

## The three TODOs

`starter.py` gives you all three tasks, the silo fixtures, model
routing (`choose_model_for_step`), the seeded `simulate_agent_run()`,
per-step accounting (`step_cost`), and `cost_per_success()` already
implemented — this project is about the *budget-enforcement and
harness-design* layer, not re-building the lesson's tool-dispatch
mechanics.

1. **TODO 1** — `task_success()`: the forgiving, order-independent
   check.
2. **TODO 2** — `is_within_budget()`: the fail-closed, both-caps-
   required check.
3. **TODO 3** — `run_cost_controlled_harness()`: walks each simulated
   run's trace step by step, denying any step once the budget is
   exceeded, and returns a results dict with the resulting success
   rate and total cost.

## Why a deterministic seeded simulation, not a live Ollama call

Same grading policy as this chapter's own lesson (Section 12) and
every prior chapter's `exercises/`/`practice/`/`project/`:
`solution.py`'s pass/fail checks never depend on a live model, so
grading works the same way everywhere, including CI with no Ollama
server running.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 9 checks across task success, the
fail-closed budget, and the aggregate cost-controlled harness.

## How to check your work for real

1. Run the structural self-check above until all 9 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional extension: add an early-termination check (Section 6's
   `confident_enough`) to `run_cost_controlled_harness()`'s per-step
   walk, and compare the resulting cost against the un-extended
   version.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 9 checks.
- `RUBRIC.md` — self-grading criteria.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  fourth scenario.
