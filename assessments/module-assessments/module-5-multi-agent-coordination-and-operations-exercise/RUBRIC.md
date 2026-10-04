# Module 5 Combined Assessment Rubric: Multi-Agent Coordination-Pattern Exercise

Grade your own completed `starter.py` against the four criteria below
(each worth up to 5 points, 20 points total). See `README.md` for the
full scenario.

## 1. Dispatch accuracy (0-5)

- **5:** `PART_1_ROUTE_CLEAR` (`"inspectionscout"`),
  `PART_1_ROUTE_UNROUTABLE` (`None`), and `PART_1_RESPONSIBLE`
  (`"zonescout"`) are all correct, correctly demonstrating Chapter 9's
  fail-closed routing and cross-agent attribution.
- **3:** Two of the three are correct.
- **0:** Zero or one correct, or crashes.

## 2. Communication accuracy (0-5)

- **5:** All four values (`PART_2_VALID`, `PART_2_INVALID`,
  `PART_2_CLAIM_1`, `PART_2_CLAIM_2`) are correct, correctly
  demonstrating Chapter 10's safe-whitespace normalization, fail-
  closed validation on a renamed field, and the locked claim-check
  rejecting a second claim on the same `gig_id`.
- **3:** 2-3 of the four values are correct.
- **0:** 0-1 correct, or crashes.

## 3. Operating accuracy (0-5)

- **5:** All values in Part 3 are correct: the first commit is NOT
  replayed, the second commit under the SAME key IS replayed with the
  identical result, and the flaky call recovers to `"recovered"`
  within its retry bound -- correctly demonstrating Chapter 11's
  idempotent commit and bounded retry.
- **3:** The commit behavior OR the retry behavior is correct, but not
  both.
- **0:** Neither is correct, or crashes.

## 4. Cross-chapter synthesis quality (0-5)

- **5:** `PART_4_JUSTIFICATION` correctly explains that
  `which_agent_responsible` (Ch9), `coordinated_claim` (Ch10), and
  `idempotency_key` (Ch11) form one layered system, and explains
  concretely what happens if a retried call bypasses the claim-check
  (a double-commit that attribution alone cannot prevent, only detect
  after the fact) -- not just "all three chapters matter."
- **3:** Correctly names all three functions and states they're
  related, without explaining the concrete failure (a retry bypassing
  the claim-check).
- **0:** Missing, a placeholder, or treats the three chapters as fully
  independent techniques.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 4 is the one most worth getting right: a
learner who can recite all three chapters' mechanics but can't explain
how a gap in one layer (a retry bypassing Chapter 10's claim-check)
defeats a guarantee in another hasn't actually internalized this
module's own outcome -- operating a coordinated system in production.
