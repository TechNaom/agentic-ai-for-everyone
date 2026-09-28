# Chapter 5 Exercises: Reflection and Self-Correction

These exercises use a second scenario, deliberately different from the
lesson's Briarcliff Bike Rentals/BikeBot hook: **Fenwick Home Repair
Co-op**, a fictional handyman referral service. Its estimate agent,
**RepairBot**, drafts a price quote (hours times an hourly rate, plus
parts) for a repair job, and must flag jobs that legally require a
licensed technician (gas lines, electrical panels) rather than quoting
them as ordinary handyman work. Applying this chapter's reflection
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

It prints a score report. Fill in each `# TODO`, re-run, and watch
your score climb toward the total (18 points across 8 tasks).

## The eight tasks

1. **Map facts to reflection concepts** — assign the correct concept
   (first-pass draft, reflection step, grounded verification criteria,
   revise-the-answer correction, iteration bound) to five RepairBot
   facts.
2. **Dependency reasoning** — decide whether reflecting on every single
   request regardless of stakes makes unnecessary cost more or less
   likely.
3. **(Production-gear) Grounded price verifier** — check a draft's
   stated price against an independently recomputed correct price.
4. **(Production-gear) Licensed-referral policy check** — detect a job
   that needs a licensed technician, and whether a draft actually says
   so.
5. **(Production-gear) `reflect_and_revise` composition** — combine
   both checks into one function that revises a draft only when it's
   actually wrong.
6. **(Production-gear) Diagnose a failure type** — recognize "retry is
   not reflection" from a real trace.
7. **(Production-gear) Bounded reflect loop** — stop after a fixed
   number of correction attempts and escalate to a human instead of
   looping forever.
8. **Completeness check** — confirm all five reflection concepts were
   actually used.

## Files

- `starter.py` — the scaffold with 12 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 18/18.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
