# Chapter 12 Exercises: Designing Agent Architectures

These exercises use a second scenario, deliberately different from
the lesson's Copperfield Municipal Utilities hook: **Lantern Hill
Senior Living**, a fictional senior-living community. Its proposed
agent handles two very different request types — routine medication
check-ins and 24/7 unattended fall-sensor alert dispatch — against the
SAME decision framework the lesson built
(`characterize_problem`/`select_mechanisms`/`reliability_cost_budget`/
`architecture_smell_check`/`build_adr`). Applying the framework to a
fresh scenario is the point — recalling the lesson's Copperfield
verdicts by heart won't get you through these.

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
your score climb toward the total (17 points across 7 tasks).

## The seven tasks

1. **Map facts to decision-framework concepts** — assign the correct
   concept (single-agent characterization, operating-layer load-
   bearing, reliability-measurement load-bearing, an over-engineering
   smell, an under-engineering smell) to five Lantern Hill facts.
2. **Characterization reasoning** — decide whether two very different
   request types, by themselves, justify a multi-agent split.
3. **`characterize_problem` on Lantern Hill** — confirm the framework
   reaches single-agent, and why.
4. **`select_mechanisms` on Lantern Hill** — confirm guardrails,
   reliability measurement, and the operating layer are load-bearing,
   and multi-agent dispatch is not.
5. **`reliability_cost_budget` on Lantern Hill** — confirm the
   tighter, irreversible-action tier applies.
6. **`architecture_smell_check`** — confirm a correct selection raises
   zero flags, and a selection that forgets the operating layer
   (despite `runs_unattended: True`) raises exactly one.
7. **`build_adr`** — assemble a consistent Architecture Decision
   Record for Lantern Hill and confirm it names every load-bearing
   mechanism.

## Files

- `starter.py` — the scaffold with 8 `# TODO`s and the score report.
- `solution.py` — the fully filled-in reference; scores 17/17.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a third
  scenario.
