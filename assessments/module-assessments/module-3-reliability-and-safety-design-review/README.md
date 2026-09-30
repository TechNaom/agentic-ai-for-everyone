# Module 3 Combined Assessment: Reliability-and-Safety Design Review

Per `docs/curriculum/CURRICULUM_MAP.md`, Module 3's stated assessment is
a "reliability-and-safety design review," spanning Chapter 5
(reflection and self-correction) and Chapter 6 (guardrails and safety).
Built during Chapter 7's own session, closing a pre-existing gap across
all of Modules 1-3 (see `quality-audits/chapter-07-audit.md`'s
assessment-decision section).

## The scenario

Chapters 5 and 6 don't have their own standalone project files -- both
extended Chapter 4's CareBot project directly: `reflect_on_response()`
was added by Chapter 5, and `guardrail_check_booking()` was added by
Chapter 6, both living in
`chapters/chapter-04-memory-and-state/project/solution.py`. This
assessment reuses those EXACT functions, applied to one combined
review case: a patient with `"unevaluated chest pain"` on file (one of
Chapter 4's own `BLOCKING_CONDITION_PHRASES`).

## The task

Using `starter.py`, produce:

1. **Guardrail behavior** (Chapter 6) — call
   `guardrail_check_booking()` twice for the same blocking condition:
   once unapproved (denied), once approved (allowed).
2. **Reflection behavior** (Chapter 5) — call `reflect_on_response()`
   on a routine-sounding draft, given a context showing the same
   blocking condition AND that `schedule_followup` was actually
   dispatched.
3. **Cross-chapter synthesis** — the one genuinely new task this
   assessment adds: explain why CareBot keeps BOTH the guardrail and
   reflection as independent layers, referencing Chapter 6's own
   "defense-in-depth" framing rather than a generic "more checks are
   better" claim.

## Why this exercise, and why this scope

This reuses the exact functions Chapters 5 and 6 each added to the
same shared project file, applied together to one scenario, rather
than inventing new content — intentionally smaller than a full chapter
project.

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
  structural self-check. It loads Chapter 4's own `project/solution.py`
  file directly via `importlib` (the file both Chapter 5 and Chapter 6
  extended).
- `solution.py` — one complete, valid reference response.
- `RUBRIC.md` — the grading criteria.
