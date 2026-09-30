# Module 1 Combined Assessment Rubric: Agent-Loop Tracing + Planning Exercise

Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total). See `README.md` for the
full scenario.

## 1. Agent-loop tracing accuracy (0-5)

- **5:** `PART_1_ANSWER` is exactly `ch1.run_agent("c19",
  ch1.FakeModel("normal"))`'s real result -- a tuple whose first
  element is `"Slip C19 is available."`, correctly reflecting that
  slip c19 is available in Chapter 1's own fixture data.
- **3:** The tuple is present but the answer string doesn't match
  exactly (e.g., wrong slip ID capitalization or wording).
- **0:** `PART_1_ANSWER` is missing, `None`, or calls `run_agent` with
  the wrong slip ID.

## 2. Planning-decision accuracy (0-5)

- **5:** Both `PART_2_NEXT_TOOL` (correctly `"check_weather_conditions"`
  -- the given history's notes mention "weather" and "icy," which
  `decide_next_delay_check`'s own branching checks before anything
  else) and `PART_2_PLANNING_MODE` (correctly `"emergent"`, since the
  next diagnostic step genuinely depends on the previous result) are
  correct.
- **2:** One of the two is correct.
- **0:** Both are missing or incorrect.

## 3. Cross-chapter synthesis quality (0-5)

- **5:** `PART_3_JUSTIFICATION` correctly explains that SlipBot's loop
  has only one possible tool to call at any step, so there is no real
  branching decision the way the delay-diagnosis task has -- and
  explicitly uses `classify_task_planning_mode`'s own criteria
  (whether later steps depend on earlier results) to make the case,
  not just an assertion that "fixed is simpler."
- **3:** Correctly identifies SlipBot as fixed, but the justification
  doesn't engage with `classify_task_planning_mode`'s actual logic.
- **0:** Missing, a placeholder, or asserts the wrong classification.

## 4. Self-check completeness (0-5)

- **5:** All 4 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **2:** 2-3 of the 4 checks pass.
- **0:** 0-1 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass."
