# Chapter 4 Project Rubric: CareBot for Hollowridge Wellness Clinic (L2 Assisted)

**Updated by Chapter 6 (final).** This project is a build-and-verify
task (see `README.md` for why deterministic fixtures are used instead
of a live model). Grade your own completed `starter.py` against the six
criteria below (three from Chapter 4, one general self-check criterion,
one from Chapter 5, one new this chapter), each worth up to 5 points
(30 points total).

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

- **5:** All 10 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 6-9 of the 10 checks pass.
- **0:** 0-5 checks pass.

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

## 6. Guardrail before dispatch (TODO 5, new this chapter) (0-5)

- **5:** `guardrail_check_booking()` is called and its result recorded
  in `tool_trace` *before* any decision to call `schedule_followup()`;
  `schedule_followup` never appears in `tool_trace` for a
  blocking-condition visit called with `human_approved=False`, AND
  `schedule_followup` *does* appear when the same visit is called with
  `human_approved=True` — matching `solution.py`'s behavior on both the
  held and the approved cases, and matching Checks 9 and 10.
- **3:** The guardrail check runs and is recorded, but only one of the
  two cases (held vs. approved) behaves correctly, or the "needs review"
  response text doesn't clearly say the booking wasn't completed.
- **0:** `schedule_followup()` is still called unconditionally
  regardless of the guardrail's result (TODO 5 left unfilled or the gate
  check is present but not actually enforced before dispatch).

## A thing to check, worth noting but not scored numerically

Confirm the guardrail check happens **before** `schedule_followup()` is
even considered, not as a check on its result afterward, and confirm
`reflect_on_response()` was deliberately *kept*, not removed, as a
second, independent layer — see README.md's "Reflection stays on as a
genuine defense-in-depth backstop" section for the full reasoning. A
correct implementation should make reflection's blocking-condition
revision branch effectively unreachable for a held booking (since
`booked` becomes `False`), while Check 8 still exercises reflection's
original catch through the default `human_approved=True` path.

## Passing bar

23/30 (76%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 2 (fact promotion via read-modify-write),
Criterion 5 (reflection), and Criterion 6 (the guardrail) are the three
most worth getting to a full 5 — Criterion 2 because the blind-overwrite
bug it guards against is invisible on a patient's first visit and only
surfaces on their second; Criterion 5 because a reflection step that
revises *everything* (or *nothing*) is exactly as useless as no
reflection step at all; and Criterion 6 because a guardrail that can be
bypassed just by not checking its result is exactly as useless as no
guardrail at all — the entire point of this chapter is that the check
has to be *enforced*, not just *present*.
