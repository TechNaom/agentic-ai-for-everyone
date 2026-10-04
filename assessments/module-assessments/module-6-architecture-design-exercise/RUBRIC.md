# Module 6 Assessment Rubric: Architecture-Design Exercise

Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. Characterization and mechanism selection (Parts 1-2) (0-5)

- **5:** Correctly reaches single-agent for Alderwood, and correctly
  identifies all four load-bearing mechanisms (guardrails, reliability
  measurement, cost control, operating layer) and the two that are
  NOT (memory, multi-agent dispatch), each traceable to a specific
  stated fact.
- **3:** Reaches the correct verdict and most mechanisms, but misses
  one (most commonly: forgets the operating layer is load-bearing
  because `runs_unattended` is easy to overlook when the OTHER task,
  ride booking, is clearly attended).
- **0:** Reaches an unjustified multi-agent verdict, or can't name
  which mechanisms are load-bearing and why.

## 2. Budget and smell check (Parts 3-4) (0-5)

- **5:** States the tight, irreversible-action budget tier (0.95 /
  0.08) correctly, and the smell check correctly raises zero flags on
  the real design and exactly one flag when the guardrail is
  deliberately dropped.
- **3:** Gets the budget tier right but the smell-check comparison is
  incomplete (e.g., only checks the good selection, never proves the
  check actually catches the bad one).
- **0:** No stated budget, or the smell check isn't run at all.

## 3. Architecture Decision Record (Part 5) (0-5)

- **5:** Assembles context, the characterization verdict, every
  load-bearing mechanism, the budget, at least one named and rejected
  alternative, and the smell-check result, in one document a reviewer
  who wasn't in the room could evaluate.
- **3:** An ADR exists but is missing one section (most commonly: no
  rejected alternative).
- **0:** No ADR, or a document that just lists the final design with
  no stated facts.

## 4. Cross-cutting synthesis (Part 6) (0-5)

- **5:** Names BOTH guardrails (Ch6) and the operating layer (Ch11)
  as load-bearing, and states the SPECIFIC, DIFFERENT fact that makes
  each one necessary (an irreversible cancellation action vs. running
  unattended) — and explains what gap would open if either one were
  dropped (an unattended system with no guardrail could auto-cancel
  with no approval; a guarded-but-unoperated system could still
  double-page or silently drop an overnight lift fault).
- **3:** Names both mechanisms but doesn't distinguish the two
  different facts each is load-bearing for, or only states the gap
  for one of the two.
- **0:** Names only one mechanism, or answers in generic terms with no
  reference to Alderwood's own two distinct facts.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "a solid
architecture-design pass." Criterion 4 is the one most worth getting
right: an architect who can select the right mechanisms but can't
explain WHY two load-bearing mechanisms are both necessary, for two
different reasons, hasn't yet internalized the chapter's own central
claim — that each mechanism is justified by one specific fact, not by
a blended "this system seems like it needs more safety."
