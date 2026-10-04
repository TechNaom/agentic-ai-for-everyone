# Chapter 10 Project Rubric: A Peer Coordination Harness for Ravenshollow Talent Agency

This project is a build-and-verify task (see `README.md` for why
deterministic, constructed cases are used instead of a live model).
Grade your own completed `starter.py` against the four criteria below,
each worth up to 5 points (20 points total).

## 1. `parse_message_safely` (TODO 1) (0-5)

- **5:** Correctly normalizes whitespace in keys without changing
  values, and returns `{"ok": False, ...}` naming the missing fields
  when a required field is genuinely missing or renamed — never
  guesses a mapping for an unrecognized key.
- **3:** Normalizes whitespace correctly but also crashes or silently
  accepts a message missing a required field.
- **0:** Always returns `{"ok": True, ...}` regardless of the input.

## 2. `coordinated_claim` (TODO 2) (0-5)

- **5:** Correctly performs the check-and-claim as ONE atomic
  operation inside a single lock, returning `{"ok": True, ...}` on a
  fresh gig and `{"ok": False, ..., "reason": "already claimed"}` on a
  gig already in `_shared_claims` — matching the lesson's Section 9
  pattern exactly.
- **3:** Catches the duplicate case but the check and the claim happen
  as two separate operations (even if each individually looks safe),
  leaving the race window Section 8 demonstrated still theoretically
  open.
- **0:** Always returns `{"ok": True, ...}`, letting every claim
  succeed regardless of prior claims.

## 3. `run_ravenshollow_harness` (TODO 3) (0-5)

- **5:** Correctly resets shared state, walks every case's claims
  through `coordinated_claim`, routes deadlock cases through the given
  `break_deadlock_if_needed`, and returns a per-case dict with an
  accurate `trace`, `deadlock_status`, and `first_duplicate_agent` —
  all 9 self-check assertions pass.
- **3:** The harness runs and returns dicts of the right shape, but
  either the deadlock case or the duplicate-attribution case is
  handled incorrectly (e.g., claims aren't routed through
  `coordinated_claim`, so duplicates are never caught).
- **0:** Returns an empty dict, wrong keys, or crashes.

## 4. Self-check completeness (0-5)

- **5:** All 9 structural self-checks pass when `python3 starter.py`
  is run, with no modifications to the self-check code itself.
- **3:** 4-8 of the 9 checks pass.
- **0:** 0-3 checks pass.

## Passing bar

15/20 (75%) with **zero** criteria scoring 0 is the bar for "solid
first pass." Criterion 2 (`coordinated_claim`) is the one most worth
getting to a full 5, since a claim-check with a race window still open
defeats the exact guarantee (atomic, locked commit) this chapter's own
Sections 8-9 build toward.
