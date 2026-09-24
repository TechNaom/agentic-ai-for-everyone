# Chapter 1 Exercises: The Agent Loop

These exercises use a second scenario, deliberately different from the
lesson's Northbeam Outdoors/TrailBot hook: **Summit Gear Co-op**, a
fictional camping-gear rental shop. Its agent, **GearBot**, answers
questions using two tools: `check_availability` (is an item in stock)
and `get_rental_price` (its daily rental price). Applying this
chapter's concepts to a fresh scenario is the point — recalling the
lesson's answers by heart won't get you through these.

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
score climb toward the total (17 points across 8 tasks).

## The eight tasks

1. **Map failures to loop concepts** — assign the correct agent-loop
   concept (perception, reasoning, action, observation, or guard) to
   five GearBot failures.
2. **Loop-dependency reasoning** — decide whether one gap makes another
   gap's failure more likely.
3. **(Production-gear) Write a tool schema** — describe a third tool,
   `get_return_date`, as a real JSON schema.
4. **(Production-gear) Fix a wrong-argument bug** — write a
   `normalize_item()` that tolerates a realistic argument variation,
   the same failure class the lesson's Cedar Hollow bug had.
5. **(Production-gear) Implement the iteration guard** — complete a
   loop so it halts after `max_iterations` even when the (fake) model
   never stops requesting a tool.
6. **(Production-gear) Diagnose a failure type** — read a real trace
   and correctly name the failure as a hallucinated result despite a
   real observation, not a wrong tool or wrong argument.
7. **(Production-gear) Add a timeout budget** — complete
   `call_with_budget()` so it raises `TimeoutError` past a budget,
   mirroring the lesson's Ollama-hang guard.
8. **Full-checklist completeness check** — confirm all five loop
   concepts from Task 1 were actually used, the same completeness gate
   a real reliability review would run.

## Checking your work

`score_exercise_*()` functions built into both `starter.py` and
`solution.py` grade your work automatically. Run either file directly
to see a score report. `solution.py` is the fully filled-in reference
and scores 17/17 when run.

## After this

See `ai-paired.html` for a solo-diagnosis-then-critique exercise: you
diagnose a fresh scenario yourself first, then review a
plausible-but-flawed AI-generated diagnosis of the same scenario and
catch what it got wrong.
