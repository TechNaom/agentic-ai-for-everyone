# Chapter 4 Project Rubric: CareBot for Hollowridge Wellness Clinic (L2 Assisted)

This project is a build-and-verify task (see `README.md` for why
deterministic fixtures are used instead of a live model, and why
reflection is a labeled no-op this chapter). Grade your own completed
`starter.py` against the four criteria below, each worth up to 5
points (20 points total).

## 1. Working-context merge (TODO 1) (0-5)

- **5:** `build_working_context()` returns an empty list for a
  never-seen patient, and correctly builds one system message per
  non-empty fact category (conditions, preferences) for a patient with
  persisted facts, using the exact prefixes the lesson's own pattern
  uses.
- **3:** Merges facts but misses one category, or the message format
  doesn't cleanly separate conditions from preferences.
- **0:** Always returns an empty working memory regardless of what's
  persisted, or crashes on a patient with no facts on file.

## 2. Fact promotion (TODO 2) (0-5)

- **5:** `promote_worthy_and_persist()` correctly classifies and
  writes both a condition and a preference statement to the persisted
  store using read-modify-write (via the given `MemoryStore` methods),
  and a second, later write doesn't destroy the first.
- **3:** Promotes one category correctly but not the other, or the
  classification logic is present but misses an obvious case.
- **0:** Never writes to the store at all, or a second promotion
  overwrites/destroys a previously persisted fact (the blind-overwrite
  bug the lesson's Section 9 demonstrated).

## 3. Composed visit flow (TODO 3) (0-5)

- **5:** `run_visit_session()` correctly merges context, appends user
  messages, promotes facts, dispatches `check_appointment_slot` (and
  `schedule_followup` only when the slot is available), builds a
  condition-aware draft response, and calls `reflect_on_response()` at
  the given call site before returning — reproducing the exact
  structure `solution.py` uses.
- **3:** The flow works but skips one piece (e.g., never checks slot
  availability before booking, or omits the `reflect_on_response()`
  call site entirely).
- **0:** Returns a hardcoded/empty result regardless of input, or
  crashes.

## 4. Self-check completeness (0-5)

- **5:** All 7 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-6 of the 7 checks pass.
- **0:** 0-3 checks pass.

## A fifth thing to check, worth noting but not scored numerically

Confirm you did **not** implement real reflection logic inside
`reflect_on_response()`. That function's body must stay exactly as
given — this project's job is to have the *call site* correctly wired
so Chapter 5 can drop a real implementation in without touching
`run_visit_session()`'s own structure. A learner who "gets ahead" and
implements reflection early has actually broken the scaffold's
extension contract, even if their code happens to work.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 2 (fact promotion via read-modify-write) is the
one most worth getting to a full 5, since the blind-overwrite bug it
guards against is invisible on a patient's first-ever visit and only
surfaces on their second.
