# Chapter 2 Exercises: Planning and Task Decomposition

These exercises use a second scenario, deliberately different from the
lesson's Alderleaf Research Group/ScoutBot hook: **Pinehurst Realty
Group**, a fictional residential brokerage. Its agent, **ListBot**,
handles two kinds of task: listing a new property (a fixed, up-front
plan) and diagnosing why a showing fell through (an emergent,
one-step-at-a-time investigation). Applying this chapter's planning
concepts to a fresh scenario is the point — recalling the lesson's
answers by heart won't get you through these.

## How to run

You'll need Python 3 installed. Check with:

```bash
python3 --version
```

Then run the starter file:

```bash
python3 starter.py
```

It prints a score report. Fill in each `# TODO`, re-run, and watch your
score climb toward the total (16 points across 8 tasks).

## The eight tasks

1. **Map facts to planning concepts** — assign the correct concept
   (fixed plan, emergent plan, re-planning, wrong-plan failure,
   planning guard) to five ListBot facts.
2. **Dependency reasoning** — decide whether pre-committing a step
   before reading an earlier result makes a wrong-plan failure more or
   less likely.
3. **(Production-gear) Write a fixed plan** — the ordered 3-step
   listing plan as real data.
4. **(Production-gear) Fix a wrong-argument bug** — write a
   `normalize_address()` that tolerates a realistic argument
   variation.
5. **(Production-gear) Implement the emergent decision function** —
   complete `decide_next_showing_step()` so the right follow-up check
   depends on what the showing log actually says.
6. **(Production-gear) Diagnose a failure type** — read a real trace
   and correctly name a wrong-plan failure, where every tool call
   succeeded but the plan itself was wrong.
7. **(Production-gear) Implement a re-plan guard** — complete a
   `max_replans`-bounded retry, mirroring the lesson's
   `run_fixed_plan_with_replan_guard`.
8. **Full-checklist completeness check** — confirm all five planning
   concepts from Task 1 were actually used.

## Checking your work

`score_exercise_*()` functions built into both `starter.py` and
`solution.py` grade your work automatically. Run either file directly
to see a score report. `solution.py` is the fully filled-in reference
and scores 16/16 when run.

## After this

See `ai-paired.html` for a solo-diagnosis-then-critique exercise: you
diagnose a fresh scenario yourself first, then review a
plausible-but-flawed AI-generated diagnosis of the same scenario and
catch what it got wrong.
