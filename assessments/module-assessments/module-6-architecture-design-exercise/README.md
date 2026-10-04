# Module 6 Combined Assessment: Architecture-Design Exercise

Per `docs/curriculum/CURRICULUM_MAP.md`, Module 6's stated assessment
is an **"architecture-design exercise (Ch. 12) + capstone rubric
(Ch. 13, architecture challenge, Level 4)"** — explicitly TWO separate
deliverables, unlike every prior module (1-5), which each had one
combined assessment spanning all of that module's chapters. This file
is the FIRST of those two, scoped to Chapter 12 alone. Chapter 13's
own capstone rubric is a separate deliverable that ships with Chapter
13 itself.

## Why this directory, not `assessments/architecture-challenges/`

The repo has both `assessments/module-assessments/` and
`assessments/architecture-challenges/` already scaffolded. This
session checked both before building: `architecture-challenges/` is
reserved for Chapter 13's own **capstone** ("architecture challenge,
Level 4" — the curriculum map's own term for Chapter 13's rubric
specifically). This module-6 assessment is the earlier, narrower
"architecture-design exercise" the curriculum map names for Chapter
12 alone, so it follows the SAME naming convention every prior
module's assessment used (`module-N-*-exercise/` under
`module-assessments/`), not the capstone's own directory.

## The scenario

A sixth fictional organization for Chapter 12's own content set (the
lesson used Copperfield Municipal Utilities, exercises used Lantern
Hill Senior Living, exercises' `ai-paired.html` used Vantage Peak Ski
Resorts, the project used Driftlight Energy Cooperative, the
project's own `ai-paired.html` used Mirelake Water Authority) —
**Alderwood Transit Cooperative**, a fictional paratransit operator.
It books rides (cancelling one late is costly to the rider and the
co-op both) and separately runs an **unattended overnight
wheelchair-lift maintenance-alert dispatch** (a lift fault at 3 AM
must page a technician with no staff watching).

This reuses Chapter 12's own tested framework functions
(`characterize_problem`, `select_mechanisms`,
`reliability_cost_budget`, `architecture_smell_check`, `build_adr`),
loaded unchanged via `importlib` from
`chapters/chapter-12-designing-agent-architectures/project/
solution.py`, applied to this brand-new scenario — the same reuse
precedent every prior module's own combined assessment used.

## The task

Using `starter.py`, produce:

1. **Characterization** (Part 1) — confirm Alderwood characterizes as
   single-agent, and why.
2. **Mechanism selection** (Part 2) — confirm guardrails, reliability
   measurement, cost control, and the operating layer are load-
   bearing; memory and multi-agent dispatch are not.
3. **Reliability/cost budget** (Part 3) — confirm the tight,
   irreversible-action tier applies.
4. **Smell check** (Part 4) — confirm the correct selection raises
   zero flags, and a selection that drops the guardrail despite the
   irreversible cancellation action raises exactly one.
5. **Architecture Decision Record** (Part 5) — assemble a consistent
   ADR naming both load-bearing mechanisms this task's synthesis
   question is about.
6. **Cross-cutting synthesis** (Part 6, free text) — the one
   genuinely new question this assessment adds: why does Alderwood
   need BOTH guardrails (Ch6) AND the operating layer (Ch11)
   together, not just one or the other? Name the specific, DIFFERENT
   fact each one is load-bearing for.

## Why deterministic, constructed cases, not a live Ollama call

Same policy as Chapter 12's own lesson and every other assessment in
this course: grading never depends on a live model.

## How to run it

```bash
python3 starter.py
```

Prints a 6-part self-check. Fill in Parts 1-6, re-run, and watch the
score climb toward 6/6 (Part 6 is free text, self-graded in full
against `RUBRIC.md`, though a minimal keyword check prevents an
empty answer from passing).

## How to check your work for real

1. Run the self-check above until Parts 1-5 pass objectively.
2. Self-grade Part 6 against `RUBRIC.md`.
3. Compare your full answer against `solution.py` — not to match its
   exact wording, but to check whether your reasoning named the same
   two distinct facts.

## Files

- `starter.py` — the scaffold with 6 parts and the self-check.
- `solution.py` — the fully filled-in reference; scores 6/6.
- `RUBRIC.md` — self-grading criteria.
