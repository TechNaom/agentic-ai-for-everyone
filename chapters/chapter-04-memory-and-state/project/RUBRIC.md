# Chapter 4 Project Rubric: CareBot for Hollowridge Wellness Clinic (L2 Assisted)

**Updated by Chapter 5.** This project is a build-and-verify task (see
`README.md` for why deterministic fixtures are used instead of a live
model). Grade your own completed `starter.py` against the five
criteria below (four from Chapter 4, one new this chapter), each worth
up to 5 points (25 points total).

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

- **5:** All 8 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 5-7 of the 8 checks pass.
- **0:** 0-4 checks pass.

## 5. Reflection self-critique-and-revise (TODO 4, new this chapter) (0-5)

- **5:** `reflect_on_response()` leaves a benign draft (no blocking
  condition, or a condition but no booking) unchanged, AND correctly
  revises the draft (mentioning the blocking condition and "clinical
  review") when a blocking condition was persisted this visit AND a
  follow-up was actually booked — matching `solution.py`'s behavior on
  both the pass-through and revision cases.
- **3:** Revises the draft in the blocking case but also incorrectly
  revises (or fails to revise) at least one non-blocking case, or the
  revised text doesn't clearly communicate the review requirement.
- **0:** Still a no-op passthrough (TODO 4 left unfilled), or revises
  every draft regardless of whether a blocking condition was actually
  booked.

## A sixth thing to check, worth noting but not scored numerically

Confirm `reflect_on_response()` only revises the *text* CareBot
returns — it must not, and cannot from this call site, undo an
already-dispatched `schedule_followup()` call. That's an intentional,
honest limit: reflection fixes what the agent *says*, not what a tool
already *did*. Preventing an unsafe booking from firing in the first
place is Chapter 6's job (see the `CHAPTER 6 EXTENSION POINT` comment
inside `run_visit_session()`), not this chapter's.

## Passing bar

19/25 (76%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 2 (fact promotion via read-modify-write) and
Criterion 5 (reflection) are the two most worth getting to a full 5 —
Criterion 2 because the blind-overwrite bug it guards against is
invisible on a patient's first-ever visit and only surfaces on their
second, and Criterion 5 because a reflection step that revises
*everything* (or *nothing*) is exactly as useless as no reflection
step at all.
