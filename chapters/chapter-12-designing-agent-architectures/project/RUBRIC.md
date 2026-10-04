# Chapter 12 Project Rubric (L3 Independent): Driftlight Energy Cooperative

This is a build-and-verify, no-scaffold task (see `README.md` for why
there is no `starter.py`). Grade your own independent attempt against
the five criteria below, each worth up to 5 points (25 points total).

## 1. Characterization and mechanism selection (0-5)

- **5:** Correctly reaches single-agent (no distinct independently-
  runnable subtasks, no concurrent independent actors), and correctly
  identifies all five load-bearing mechanisms (memory, guardrails,
  reliability measurement, cost control, operating layer) **and**
  correctly identifies the three that are NOT load-bearing (reflection,
  multi-agent dispatch, peer communication) — each with the specific
  stated fact that decides it, not a guess.
- **3:** Reaches the correct single-agent verdict and most of the five
  load-bearing mechanisms, but misses one (most commonly: forgets
  memory is load-bearing because the pledge persistence fact is easy
  to overlook), or states a verdict without naming the deciding fact.
- **0:** Reaches an unjustified multi-agent verdict, or can't name
  which mechanisms are load-bearing and why.

## 2. Reliability/cost budget (0-5)

- **5:** States the budget as two numbers (a minimum task-success
  rate, a maximum cost per run), explicitly reusing Chapter 7/8's own
  vocabulary and threshold logic (not reinvented), and correctly
  applies the tighter, irreversible-action tier because Driftlight's
  credit is real money leaving the cooperative.
- **3:** States a budget, but as a vague aspiration ("should be
  reliable and cheap") rather than two checkable numbers, or applies
  the wrong tier.
- **0:** No stated budget at all.

## 3. Implementation (0-5)

- **5:** `MemoryStore` genuinely persists a pledge across two separate
  instantiations (not just an in-memory dict that happens to survive
  within one process); `apply_credit` is fail-CLOSED by default
  (blocks above-threshold credits unless explicitly approved, not
  fail-open); `commit_once`/`idempotency_key` genuinely prevent a
  repeated key from re-running the credit side effect.
- **3:** All three mechanisms exist but one has a real gap (e.g., the
  guardrail defaults to approved, or the idempotency key is built from
  raw call arguments instead of the fields that define the effect —
  the exact Chapter 11 mistake that chapter's own lesson diagnosed).
- **0:** One or more of the three mechanisms is missing entirely, or
  is a no-op stub.

## 4. Instrumentation and proof (0-5)

- **5:** A harness runs multiple trials per task type, computes a real
  measured task-success rate and cost-per-success per task using
  Chapter 7/8-style formulas, and the submission explicitly checks
  those measured numbers against the budget stated in Criterion 2 —
  not just asserting the budget is met, but showing the real numbers
  that prove it (or honestly reporting a shortfall if one exists).
- **3:** A harness exists and produces numbers, but the submission
  never actually checks them against the stated budget.
- **0:** No harness; the budget is asserted with no measurement at
  all.

## 5. Architecture Decision Record (0-5)

- **5:** Assembles context, the characterization verdict and reason,
  every load-bearing mechanism, the stated budget, at least one named
  and rejected alternative (with the specific cost of NOT choosing
  it), and the smell-check result, in one document a reviewer who
  wasn't in the room could evaluate.
- **3:** An ADR exists but is missing one section (most commonly: no
  rejected alternative, or no smell-check result).
- **0:** No ADR, or a document that just lists the final design with
  no stated facts or alternatives.

## Passing bar

18/25 (72%) with **zero** criteria scoring 0 is the bar for "a real,
independent L3 submission." Criterion 1 is the one most worth
double-checking: an architect who gets the mechanism-selection facts
wrong (most commonly here: missing that the pledge's cross-session
persistence makes memory load-bearing) has produced a design that
will fail in exactly the way Chapter 4's own lesson predicts — a fact
told once, forgotten the next time it matters.
