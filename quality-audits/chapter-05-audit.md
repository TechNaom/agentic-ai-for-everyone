# Chapter 5 Quality Audit: Reflection and Self-Correction

Session date: 2026-09-28. This session built Chapter 5 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, a signpost `project/` (README + index.html, per
the brief's instruction that the L2 project itself is extended in
place inside `chapters/chapter-04-memory-and-state/project/`, not
re-created here), the real extension of Chapter 4's L2 project
(`reflect_on_response()` filled in for real, plus a new TODO 4 in
`starter.py`), this audit, wiring `assets/chapters-data.js` and
`docs/curriculum/index.html`, updating root `index.html`'s hero stats,
and rewriting `PROJECT_STATE.md`'s "Next Recommended Task" for
Chapter 6.

## Honest self-critique

**What's strong:**
- This chapter's own sandbox hang **did recur**, honestly disclosed
  rather than hidden: the very first live call (Section 3's BikeBot
  draft, asked to price and evaluate an electric-bike rental for a
  15-year-old) took **413.8 seconds**, despite the exact same pre-warm
  discipline Chapter 4's session used successfully. This is disclosed
  in the lesson text itself (Section 2's "what's different" box,
  Section 3's own output label), not smoothed over.
- **Two genuine, unscripted live-model results became this chapter's
  central worked examples**, neither manufactured: (1) Section 3's
  real BikeBot draft correctly refused the underage electric-bike
  rental but never stated a dollar total for the standard-bike
  alternative it offered, despite the customer explicitly asking "how
  much would that cost" — a real incomplete-answer failure; (2)
  Section 7/12's real live self-critique call correctly diagnosed that
  exact gap (VERDICT: INCOMPLETE, with an accurate REASON) but its own
  REVISED text still never stated the correct number ($24) — a live
  self-critique call catching the right problem class and still
  failing to guarantee the fix. This second result is arguably the
  chapter's most important finding: it's the concrete, demonstrated
  reason a grounded, deterministic check (Section 4's `verify_draft()`)
  is presented as necessary, not optional, rather than being asserted
  as a design preference.
- **A genuine bug was caught and fixed while testing this chapter's
  own code, in the same honest tradition as Chapter 1's Cedar Hollow
  bug and Chapter 4's blind-overwrite bug.** `extract_dollar_amount()`
  originally used `re.search()` (first match), which misread "$8/hour
  x 7 hours = $56" as the draft's claimed price ($8, the per-hour
  rate) instead of the actual stated total ($56) — this would have
  caused Section 6's own correct, unprompted-correct live draft to be
  wrongly flagged as an error. Caught by actually running
  `verify_draft()` against the real Section 6 transcript before
  finalizing the lesson, fixed by switching to the *last* dollar match,
  and disclosed directly in the lesson's own Section 4 code comment. A
  second, smaller discrepancy (Section 10's bounded-reflect example
  claiming the loop converged in 0 attempts when the actual returned
  value is 1) was caught the same way and turned into an explicit
  "why the returned count is 1, not 0" explanation rather than quietly
  fixed and hidden.
- Lesson density: 62 lines match `<pre\|<code` via
  `grep -c '<pre\|<code' lesson.html` (above the 60+ requirement,
  matching Chapter 4's own 62 exactly), or 118 total tag occurrences
  via `grep -oE '<pre|<code' | wc -l`.
- This session verified every `solution.py` across `exercises/` and
  `practice/` scores a perfect total, and every corresponding
  `starter.py` fails cleanly (low score, no crash) with its `TODO`s
  unfilled. The Chapter 4 L2 project's `solution.py` (now with the
  real reflection body) scores 8/8, and its `starter.py` (now with a
  new TODO 4) scores 2/8 with no crash — both actually executed this
  session.
- **This chapter's own L2 project extension is real, not cosmetic.**
  `chapters/chapter-04-memory-and-state/project/solution.py`'s
  `reflect_on_response()` now catches a genuine class of mistake
  (CareBot drafting a routine confirmation for a visit with an
  unresolved, serious condition and an actual booking) with a real
  before/after shown in the lesson's own Section 14, using the exact
  same mechanism (a grounded check against real facts) the chapter's
  own BikeBot material builds. TODOs 1-3 and their original Chapter 4
  self-checks were read first and confirmed unchanged before any edit
  was made, per the brief's explicit instruction.
- A `CHAPTER 6 EXTENSION POINT` comment was added at the exact call
  site inside `run_visit_session()` (immediately before
  `schedule_followup()` is dispatched), and the same forward-reference
  appears in `project/README.md`, `RUBRIC.md`, and this chapter's own
  Section 14 — a consistent, explicit hand-off for Chapter 6 to pick
  up, matching Chapter 4's own precedent of wiring a labeled extension
  point rather than a vague forward-reference.

**Honest gaps:**
- This chapter's live-call timing was worse than Chapter 4's, not
  better — the documented sandbox hang is not resolved, and future
  chapters should continue to budget up to 450 seconds and disclose
  honestly rather than assume any session's pre-warm discipline
  guarantees fast calls.
- Only `llama3.2:latest` was targeted, consistent with Chapters 1-4 —
  no claim is made that either the incomplete-answer failure or the
  live self-critique's incomplete fix generalizes to any other model.
  Both are reported as exactly what this specific model did on these
  specific real calls.
- Section 5's arithmetic-error demonstration uses a deliberately-naive
  *deterministic* draft generator, clearly labeled as such in the
  lesson text, rather than a live model call that happened to make a
  math error — this session's two real live draft calls (Sections 3
  and 6) did not produce a pure arithmetic mistake on their own
  (one had an incomplete-answer failure instead, the other was fully
  correct), so a deterministic stand-in was used honestly rather than
  the lesson claiming a live call produced an error it didn't.
- Section 8's "gather-more-evidence correction" (the second kind of
  self-correction named) is deliberately not built out as a full
  worked example with its own live/deterministic demonstration — the
  chapter names the distinction and explains why building it out fully
  would duplicate Chapter 3's own tool-selection material, rather than
  manufacturing a shallow example just to have one.
- Exercises/practice scoring for free-text-style answers still relies
  on exact-string or keyword matching rather than fully semantic
  grading — the same necessary, disclosed limitation as every prior
  chapter's own exercise harness.
- Chapter 5's `project/` directory is intentionally a signpost, not a
  working scaffold — this is a deliberate reading of the brief's
  "extend in place, don't recreate" instruction, not an oversight; the
  actual gradable project files remain solely in
  `chapters/chapter-04-memory-and-state/project/`.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-04-audit.md` (16
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic).

**3 new fictional orgs used this chapter, all checked clean against
the full running list and against each other:**

- **Briarcliff Bike Rentals** (lesson hook; product: BikeBot)
- **Fenwick Home Repair Co-op** (exercises; product: RepairBot)
- **Mossgate Dental Group** (exercises `ai-paired.html`; product:
  DentalBot)

**RenewBot's software subscription service** (practice `ai-paired.html`)
is left unnamed/generic on purpose, the same convention Chapter 4's
MemoBot scenario (and Chapter 3's HandoffBot, Chapter 2's EscalationBot,
Chapter 1's ConciergeBot) used — a small, two-or-three-fact scenario
doesn't need an invented company name.

**Hollowridge Wellness Clinic** (CareBot) is reused deliberately, not a
new org — it's the L2 project's own canonical scenario, extended in
place per the brief, not a fresh chapter scenario.

Every distinctive root word above (Briarcliff, Fenwick, Mossgate) was
checked for zero overlap against both this chapter's own three named
scenarios and the full 16-org Chapter 1-4 list. The running exclusion
list for future chapters is now: Northbeam Outdoors, Summit Gear
Co-op, Fernbrook Ski Patrol, Wavecrest Marina, Alderleaf Research
Group, Pinehurst Realty Group, Thistlewood Veterinary Group, Cobblestone
Courier Co., Palisade Broadband, Thornbury Insurance Group, Wrenhollow
Auto Rentals, Kestrel Appliance Service, Larkspur Fitness Studio,
Driftwood Legal Clinic, Saltmarsh Language Academy, Hollowridge
Wellness Clinic, Briarcliff Bike Rentals, Fenwick Home Repair Co-op,
Mossgate Dental Group. Future chapters should extend this list, not
restart it.

## Source verification, done honestly

Like Chapters 1-4, this is a from-scratch code walkthrough, not a
claims-and-citations chapter — no external papers or docs required
WebFetch verification. No external source claims are made this
chapter; every factual claim about model behavior is backed by a real,
captured transcript from this session's own local Ollama calls, or
labeled explicitly as a deterministic stand-in where no live call was
used.

## Ollama check, done fresh this session

The model was explicitly pre-warmed before any lesson code was
written, using this course's documented recovery command:

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
{"model":"llama3.2","created_at":"2026-09-28T12:57:32.319951141Z","response":"","done":true,"done_reason":"load"}

$ python3 check_ollama.py   # plain "Say OK" sanity check
elapsed: 5.06
OK
```

Despite the successful pre-warm, this session's documented sandbox
hang **recurred**: the very first substantive live call (Section 3's
BikeBot draft) took **413.8 seconds** — inside this course's 450-second
policy ceiling, but a genuine, unscripted recurrence, not a smooth
repeat of Chapter 4's fast session. Two subsequent live calls (Section
6's second draft, Section 7's self-critique) completed fast (10.2s and
40.8s respectively) with the model still resident, consistent with a
one-time cold-start-adjacent stall rather than a persistent slowdown.
All three real calls are shown in the lesson with their actual real
elapsed times, not rounded or omitted.

## Code tested before writing

Every Python snippet this session wrote was actually run, in a
scratch directory, before its content (or its verified output) was
transcribed into `lesson.html`:

```
$ python3 bikebot_core.py          -> compute_price/check_policy/extract_dollar_amount
                                       verified against hand-picked cases
$ python3 draft_call.py            -> REAL Ollama call, 413.8s, captured verbatim
$ python3 draft_call2.py           -> REAL Ollama call, 10.2s, captured verbatim
$ python3 critique_call.py         -> REAL Ollama call, 40.8s, captured verbatim
$ python3 bikebot_agent.py         -> the finished agent, both cases verified,
                                       including the real reflections_used counts
$ python3 checklist.py             -> the reflection-risk classifier verified
$ python3 verify_all_snippets.py   -> EVERY remaining inline lesson snippet
                                       (Sections 4, 6, 8, 9, 10, 11, 12, 13, 16)
                                       re-run as a consolidated script AFTER the
                                       extract_dollar_amount bug fix, confirming
                                       every claimed output in the lesson matches
                                       what the code actually produces
```

Then, in the actual chapter directory, after every file was written:

```
$ python3 exercises/solution.py    -> TOTAL: 18/18
$ python3 exercises/starter.py     -> TOTAL: 4/18, no crash
$ python3 practice/solution.py     -> TOTAL: 8/8
$ python3 practice/starter.py      -> TOTAL: 0/8, no crash
$ python3 chapters/chapter-04-memory-and-state/project/solution.py
                                    -> 8/8 checks passed (was 7/7 before this
                                       chapter's TODO 4 addition)
$ python3 chapters/chapter-04-memory-and-state/project/starter.py
                                    -> 2/8 checks passed, no crash
```

No stray JSON files were left behind in any chapter directory by any
of the `exercises/`, `practice/`, or `project/` runs (each script
cleans up its own test fixtures on exit).

## Local check

`scripts/local_check.sh` was run for the whole repo after all Chapter
5 files were in place and the L2 project extension was committed to
disk — see `PROJECT_STATE.md`'s Session 5 entry for the result
captured this session.
