# Module 4 Combined Assessment Rubric: Reliability-Plan and Cost-Control Exercise

Grade your own completed `starter.py` against the three criteria below
(each worth up to 6-7 points, 20 points total). See `README.md` for
the full scenario.

## 1. Reliability accuracy (0-7)

- **7:** `PART_1_CORRECT_ORDER` (`True`), `PART_1_WRONG_ORDER`
  (`False`), and `PART_1_TASK_SUCCESS` (`True`) are all correct,
  correctly demonstrating that Chapter 7's `trajectory_correctness` is
  order-sensitive while `task_success` is not.
- **3:** Two of the three are correct.
- **0:** Zero or one correct, or crashes.

## 2. Cost-control accuracy (0-7)

- **7:** All five values (`PART_2_WITHIN_BUDGET`,
  `PART_2_OVER_STEP_BUDGET`, `PART_2_OVER_COST_BUDGET`,
  `PART_2_STEP_COST_CHEAP`, `PART_2_STEP_COST_STRONG`) are correct,
  correctly demonstrating that Chapter 8's `is_within_budget` denies
  on EITHER cap independently and that the cheap/strong model tiers
  produce a real cost difference.
- **3:** 3-4 of the five values are correct.
- **0:** 0-2 correct, or crashes.

## 3. Cross-chapter synthesis quality (0-6)

- **6:** `PART_3_JUSTIFICATION` correctly explains that Chapter 7's
  reliability instrumentation and Chapter 8's cost control cannot be
  optimized independently -- references the `cost_per_success` idea
  (or an equivalent explicit success-rate-aware cost metric) and
  explains concretely how an overly aggressive fail-closed budget
  could truncate a run before it reaches its outcome-producing tool
  call, lowering `task_success` -- not just "they're both important."
- **3:** Correctly states both concerns matter together, without
  explaining the concrete mechanism (budget truncation lowering
  success rate).
- **0:** Missing, a placeholder, or treats cost and reliability as
  fully independent concerns.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 3 is the one most worth getting right: a
learner who can recite both chapters' mechanics but can't explain why
they must be measured together hasn't actually internalized this
module's own outcome.
