# Capstone Rubric: L4 Architecture Challenge (Chapter 13)

Grade a completed L4 capstone attempt against the five criteria
below, each worth up to 5 points (25 points total). This rubric
grades `chapters/chapter-13-capstone-designing-and-defending-an-
autonomous-agent-system/project/solution.py` (Thornwick Marketplace
Collective) or your own independent attempt at the same problem
statement.

## 1. Characterization: BOTH multi-agent justifications, not just one (0-5)

- **5:** Correctly reaches multi-agent, AND names BOTH the
  subtask-independence justification (Ch9: distinct, specialized
  subtasks that run independently) AND the concurrent-actors
  justification (Ch10: multiple independent actors on shared state),
  each traced to a specific Thornwick fact.
- **3:** Reaches multi-agent and names ONE of the two justifications,
  but misses or never checks the second — the single most common
  partial-credit gap, since `characterize_problem` only reports the
  first branch that fires.
- **0:** Reaches a single-agent verdict, or can't name any specific
  fact behind the multi-agent claim.

## 2. Mechanism selection: all eight, each traced to a fact (0-5)

- **5:** Correctly identifies all eight of Chapters 4-11's mechanisms
  as load-bearing, each traceable to a specific stated Thornwick
  fact (not "all mechanisms, to be safe").
- **3:** Identifies most of the eight but misses one or two (most
  commonly: forgets peer communication requires BOTH
  `multi_agent_justified` AND `requires_concurrent_independent_actors`
  together, not just the first).
- **0:** Misses three or more mechanisms, or can't trace any
  selection back to a specific fact.

## 3. Budget, trade-off defense, and smell check (0-5)

- **5:** States the tight, irreversible-action budget tier (0.95 /
  0.08); names at least two genuine alternatives and the specific
  reason each is rejected (not "simpler" alone); and the smell check
  correctly raises zero flags on the real design and exactly one flag
  when a mechanism (e.g., guardrails) is deliberately dropped.
- **3:** Gets the budget and smell check right but the trade-off
  defense is generic (e.g., "a single agent would be simpler" with no
  Thornwick-specific reason).
- **0:** No stated budget, or the smell check isn't run against both
  a correct and a deliberately bad selection.

## 4. Reference implementation: every mechanism PROVEN, not just described (0-5)

- **5:** Implements AND proves, with real executed code: memory
  persisting across two separate process instantiations; a LOCKED
  claim-check (not an unlocked read-then-write) that lets exactly one
  of two concurrent claims on the same last unit win; a fail-closed
  guardrail that blocks by default and opens only on explicit
  approval; an idempotent commit that applies exactly once across a
  retried call; and a grounded reflection check that accepts a
  fact-complete explanation and rejects a fact-free one.
- **3:** Implements most of the above but one mechanism is only
  described in prose or asserted without a proof (most commonly: the
  claim-check exists but is never actually raced against a second
  concurrent claim in the same tick).
- **0:** Mechanisms are named in the ADR but no corresponding code
  exists, or the code crashes.

## 5. Instrumentation and the Architecture Decision Record (0-5)

- **5:** A deterministic harness runs multiple trials per task type,
  reports REAL measured success-rate and cost-per-success numbers,
  and explicitly checks them against the stated budget — and the
  assembled ADR names every load-bearing mechanism, the budget, at
  least two rejected alternatives, and the smell-check result, in one
  document a reviewer who wasn't in the room could evaluate.
- **3:** A harness exists and produces numbers, but the ADR is
  missing one section (most commonly: no rejected alternatives), or
  the numbers are never explicitly compared to the stated budget.
- **0:** No harness (the budget is asserted, never measured), or no
  ADR.

## Passing bar

20/25 (80%) with **zero** criteria scoring 0 is the bar for "a solid
L4 capstone pass." Criterion 1 is the one worth getting exactly
right: an architect who reaches the correct multi-agent verdict but
can only name ONE of its two possible justifications has done half
the job Chapters 9 and 10 together require — the same half-credit gap
this rubric's own Criterion 1 is built to catch, rather than reward a
correct final answer reached for an incomplete reason.
