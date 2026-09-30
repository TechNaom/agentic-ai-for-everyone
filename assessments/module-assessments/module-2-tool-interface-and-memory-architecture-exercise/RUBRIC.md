# Module 2 Combined Assessment Rubric: Tool-Interface Design + Memory-Architecture Exercise

Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total). See `README.md` for the
full scenario.

## 1. Tool-interface accuracy (0-5)

- **5:** `PART_1_ANSWER` is exactly `("check_warranty_status", {"status":
  "expired"})` -- correctly selecting the cheap, decisive warranty
  check over the more expensive diagnostic, per Chapter 3's own
  tool-selection discipline.
- **3:** Calls the right tool but the result value is wrong or
  incomplete.
- **0:** Missing, `None`, or calls `run_diagnostic` instead.

## 2. Memory-architecture accuracy (0-5)

- **5:** All three of `PART_2_CONTEXT_BEFORE` (empty), `PART_2_VISIT_
  RESULT` (persists the allergy as a condition), and `PART_2_CONTEXT_
  AFTER` (a fresh context call still sees it) are correct, correctly
  demonstrating that the fact survives beyond the single session call
  that created it.
- **2:** Two of the three are correct.
- **0:** Zero or one correct.

## 3. Cross-chapter synthesis quality (0-5)

- **5:** `PART_3_JUSTIFICATION` correctly identifies RepairBot's tools
  as stateless (each call is self-contained) and correctly identifies
  the SPECIFIC consequence for CareBot if it lacked memory (a
  clinically relevant fact reported in one visit would be invisible to
  a later, separate visit) -- not just a generic "memory is useful"
  statement.
- **3:** Correctly identifies RepairBot as stateless, but doesn't
  name the specific cross-visit consequence for CareBot.
- **0:** Missing, a placeholder, or gets the direction backwards.

## 4. Self-check completeness (0-5)

- **5:** All 5 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself, and no
  stray memory-scratch file is left behind after the run.
- **2:** 3-4 of the 5 checks pass.
- **0:** 0-2 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass."
