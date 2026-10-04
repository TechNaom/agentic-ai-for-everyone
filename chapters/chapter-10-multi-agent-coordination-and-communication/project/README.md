# Chapter 10 Project: A Peer Coordination Harness for Ravenshollow Talent Agency

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects. Per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, the **L3 Independent project** ("design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold") was deferred past Chapter 8, past Chapter 9, and has
**still not been built** as of this chapter — it is NOT built here
either. See `PROJECT_STATE.md`'s hand-off for Chapter 11, which
restates this flag explicitly so it is never silently dropped. This
mini-project exists so this chapter's own three pillars (message
validation, an atomic shared claim-check, and an assembled harness that
detects duplicates and breaks a deadlock) get one combined, hands-on
build of their own, the same pattern Chapters 7-9's mini-projects used.
Scenario: **Ravenshollow Talent Agency**, a fictional talent-booking
agency, runs two PEER agents — **CastingScout** and **BookingScout** —
that must claim audition/booking gigs from a shared pool by exchanging
messages directly, the same way the lesson's DockScout and YardScout
coordinated shipments. No supervisor routes work between them.

## The three pillars, combined

**Message validation.** `parse_message_safely()` normalizes safe
whitespace padding in a message's keys, but fails closed (returns
`{"ok": False, ...}`) when a required field is genuinely missing or
renamed — never guesses a mapping.

**Atomic shared claim-check.** `coordinated_claim()` wraps a
check-then-claim operation in a SINGLE lock, so two peers calling it
concurrently (or in sequence, in this deterministic harness) can never
both succeed on the same gig — the same discipline the lesson's
Section 9 built after Section 8's own live duplicated-work result.

**Assembled, attributed harness.** `run_ravenshollow_harness()` walks
each case's claim attempts through `coordinated_claim`, detects and
breaks a deadlock using the given (already-implemented)
`break_deadlock_if_needed()`, and attributes any duplicate to the
specific agent whose claim was rejected via the given
`which_agent_caused_duplicate()`.

## The three TODOs

`starter.py` gives you the deadlock detection/breaking functions and
the duplicate-attribution function already implemented — this project
is about the *validation and claim-check* layer, not re-building the
deadlock-timeout mechanics the lesson already covered in depth.

1. **TODO 1** — `parse_message_safely()`: normalize whitespace, fail
   closed on a missing/renamed field.
2. **TODO 2** — `coordinated_claim()`: the atomic, locked
   check-and-claim.
3. **TODO 3** — `run_ravenshollow_harness()`: the assembled harness —
   claim processing, deadlock handling, and attribution, across all
   four cases.

## Why deterministic, constructed cases, not a live Ollama call

Same grading policy as this chapter's own lesson and every prior
chapter's `exercises/`/`practice/`/`project/`: `solution.py`'s
pass/fail checks never depend on a live model, so grading works the
same way everywhere, including CI with no Ollama server running.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 9 checks across message
validation, the shared claim-check, and the assembled harness.

## How to check your work for real

1. Run the structural self-check above until all 9 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional extension: add a per-pair message-exchange log (list of
   `Message` objects, Section 3's pattern) to
   `run_ravenshollow_harness()`'s claim walk, and report the full
   exchange alongside each case's result.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 9 checks.
- `RUBRIC.md` — self-grading criteria.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  fourth scenario.
