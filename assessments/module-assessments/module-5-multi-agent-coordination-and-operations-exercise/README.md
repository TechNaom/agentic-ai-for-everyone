# Module 5 Combined Assessment: Multi-Agent Coordination-Pattern Exercise

Per `docs/curriculum/CURRICULUM_MAP.md`, Module 5's stated assessment
is a "multi-agent coordination-pattern exercise," spanning Chapter 9
(orchestration/dispatch patterns), Chapter 10 (peer communication), and
Chapter 11 (operating a multi-agent system in production, Module 5's
closing chapter). Built during Chapter 11's own session, following
the exact precedent set at Chapter 8 for Module 4's own combined
assessment (see `quality-audits/chapter-08-audit.md`'s assessment-
decision section, and Chapters 9 and 10's own hand-offs, which both
carried this deliverable forward to Chapter 11 unchanged): reuse each
covered chapter's own already-tested functions, loaded directly via
`importlib`, applied to one small combined scenario, rather than
inventing new content.

## The scenario

Chapter 9's chapter mini-project (`chapters/chapter-09-multi-agent-
orchestration-patterns/project/solution.py`, Ashgrove Municipal
Services' CityScout), Chapter 10's chapter mini-project (`chapters/
chapter-10-multi-agent-coordination-and-communication/project/
solution.py`, Ravenshollow Talent Agency's CastingScout/BookingScout),
and Chapter 11's chapter mini-project (`chapters/chapter-11-operating-
agents-in-production/project/solution.py`, Wrenfield Dispatch
Alliance's ClaimScout/ShipScout) each already have real, tested
functions for exactly the three layers this module's outcome asks
for: dispatch and attribution (Chapter 9), peer validation and a
shared claim-check (Chapter 10), and idempotent, retried operating
(Chapter 11). This assessment reuses those EXACT functions, unchanged,
applied together.

## The task

Using `starter.py`, produce:

1. **Dispatch check** (Chapter 9) — call `route_subtask` (loaded from
   Chapter 9's own project file) on a clear request and an unroutable
   one, and `which_agent_responsible` on a failed trace, confirming
   fail-closed routing and correct attribution.
2. **Communication check** (Chapter 10) — call `parse_message_safely`
   and `coordinated_claim` (both loaded from Chapter 10's own project
   file) to confirm safe-whitespace normalization vs. a fail-closed
   renamed field, and that a second claim on the same `gig_id` is
   rejected.
3. **Operating check** (Chapter 11) — call `idempotency_key`,
   `commit_once`, and `call_with_retries` (all loaded from Chapter
   11's own project file) to confirm a side effect commits exactly
   once across a repeated key, and a flaky call recovers within its
   retry bound.
4. **Cross-chapter synthesis** — the one genuinely new task this
   assessment adds: explain why Chapter 9's `which_agent_responsible`,
   Chapter 10's `coordinated_claim`, and Chapter 11's
   `idempotency_key` together form ONE layered system, not three
   independent techniques, and what happens if a retried call
   bypasses the claim-check.

## Why this exercise, and why this scope

This reuses the exact functions Chapters 9, 10, and 11 each already
built and tested in their own chapter mini-projects, applied together
to one scenario, rather than inventing new content — intentionally
smaller than a full chapter project, matching Module 4's own combined
assessment's scope.

## How to run it

```bash
python3 starter.py
```

Part 4's justification is open-ended, so the script runs a
**structural self-check** on Parts 1-3 plus a basic substance check
on Part 4.

## How to check your work for real

1. Run the structural self-check above until it passes.
2. Compare your full response against `solution.py`.
3. Self-grade against `RUBRIC.md`.

## Files

- `starter.py` — the scenario, your response template, and the
  structural self-check. It loads Chapter 9's, Chapter 10's, AND
  Chapter 11's own `project/solution.py` files directly via
  `importlib`.
- `solution.py` — one complete, valid reference response.
- `RUBRIC.md` — the grading criteria.
