# Module 3 Combined Assessment Rubric: Reliability-and-Safety Design Review

Grade your own completed `starter.py` against the three criteria below
(each worth up to 6-7 points, 20 points total). See `README.md` for
the full scenario.

## 1. Guardrail accuracy (0-7)

- **7:** Both `PART_1_DENIED` (`allowed: False`) and `PART_1_APPROVED`
  (`allowed: True`) are correct for the identical blocking condition,
  correctly demonstrating that approval status alone changes the
  outcome.
- **3:** One of the two is correct.
- **0:** Both missing or incorrect.

## 2. Reflection accuracy (0-7)

- **7:** `PART_2_REFLECTED_DRAFT` correctly revises the routine
  confirmation into the clinical-review message, naming the specific
  blocking condition, because the context shows BOTH a blocking
  condition AND that `schedule_followup` actually dispatched.
- **3:** Recognizes reflection should trigger but the resulting draft
  is malformed or missing the condition name.
- **0:** Returns the unrevised draft, or crashes.

## 3. Cross-chapter synthesis quality (0-6)

- **6:** `PART_3_JUSTIFICATION` correctly explains that the guardrail
  and reflection are independent, defense-in-depth layers -- the
  guardrail stops most unsafe bookings before dispatch, while
  reflection remains as a second, independent check against a future
  bug, code path, or refactor that bypasses the guardrail's one
  guarded call site -- not just "more checks are better."
- **3:** Correctly states both mechanisms should be kept, without
  explaining the defense-in-depth reasoning.
- **0:** Missing, a placeholder, or argues one mechanism should be
  removed.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass."
