# Module 4 Combined Assessment: Reliability-Plan and Cost-Control Exercise

Per `docs/curriculum/CURRICULUM_MAP.md`, Module 4's stated assessment
is a "reliability-plan + cost-control exercise," spanning Chapter 7
(evaluating agent reliability) and Chapter 8 (cost and latency
control). Built during Chapter 8's own session, following the exact
precedent set at Chapter 7 for Modules 1-3's own combined assessments
(see `quality-audits/chapter-07-audit.md`'s assessment-decision
section): reuse each covered chapter's own already-tested functions,
loaded directly via `importlib`, applied to one small combined
scenario, rather than inventing new content.

## The scenario

Chapter 7's chapter mini-project (`chapters/chapter-07-evaluating-
agent-reliability/project/solution.py`, Emberlyn Underwriting's
TriageScout) and Chapter 8's chapter mini-project (`chapters/
chapter-08-cost-and-latency-control-of-agent-loops/project/
solution.py`, Portage Grain Cooperative's YieldScout) each already
have real, tested functions for exactly the two halves of this
module's outcome: measuring reliability (Chapter 7) and controlling
cost (Chapter 8). This assessment reuses those EXACT functions,
unchanged, applied together.

## The task

Using `starter.py`, produce:

1. **Reliability check** (Chapter 7) — call `trajectory_correctness`
   and `task_success` (both loaded from Chapter 7's own project file)
   against a correct-order trace and a wrong-order trace for the same
   task, confirming they correctly disagree.
2. **Cost-control check** (Chapter 8) — call `is_within_budget` and
   `step_cost` (both loaded from Chapter 8's own project file) to
   confirm the fail-closed budget denies a step-cap violation AND a
   cost-cap violation independently, and that the cheap/strong model
   tiers produce genuinely different per-step costs.
3. **Cross-chapter synthesis** — the one genuinely new task this
   assessment adds: explain why Chapter 7's reliability instrumentation
   and Chapter 8's cost control cannot be optimized independently,
   referencing the `cost_per_success` idea and what an overly
   aggressive fail-closed budget could do to a task's own success
   rate.

## Why this exercise, and why this scope

This reuses the exact functions Chapters 7 and 8 each already built
and tested in their own chapter mini-projects, applied together to one
scenario, rather than inventing new content — intentionally smaller
than a full chapter project, matching Modules 1-3's own combined
assessments' scope.

## How to run it

```bash
python3 starter.py
```

Part 3's justification is open-ended, so the script runs a
**structural self-check** on Parts 1-2 plus a basic substance check on
Part 3.

## How to check your work for real

1. Run the structural self-check above until it passes.
2. Compare your full response against `solution.py`.
3. Self-grade against `RUBRIC.md`.

## Files

- `starter.py` — the scenario, your response template, and the
  structural self-check. It loads Chapter 7's AND Chapter 8's own
  `project/solution.py` files directly via `importlib`.
- `solution.py` — one complete, valid reference response.
- `RUBRIC.md` — the grading criteria.
