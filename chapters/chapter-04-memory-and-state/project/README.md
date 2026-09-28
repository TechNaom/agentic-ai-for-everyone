# Chapter 4 Project (L2 Assisted, extended by Ch. 5 and Ch. 6): CareBot for Hollowridge Wellness Clinic

**This is this course's numbered L2 Assisted project**, not a chapter
mini-project — per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder: *"Build a multi-tool agent with memory and a reflection step
for a provided scenario, partial scaffold, ships after Ch. 4, extended
through Ch. 5-6's reflection/guardrail material."* Chapters 2-3 both
built chapter mini-projects instead, because the ladder had no
numbered slot for them yet. Chapter 4 is where the ladder says the L2
project actually begins. **As of Chapter 6, this project is complete**
— it now demonstrates all three of this module's pillars: persisted
memory (Ch. 4), reflection (Ch. 5), and guardrails (Ch. 6).

**Update, Chapter 5:** this file's reflection half is no longer a
no-op. `reflect_on_response()`'s body now contains a real,
deterministic self-critique-and-revise step — see "TODO 4: reflection,
filled in by Chapter 5" below. TODOs 1-3 and their original self-checks
are untouched.

**Update, Chapter 6:** `run_visit_session()` now calls
`guardrail_check_booking()` — a hard, enforced check — **before**
`schedule_followup()` is ever dispatched. A blocking condition on file
now genuinely holds the booking (returns a "needs review" response and
never calls the booking tool) unless `human_approved=True` is passed.
See "TODO 5: the guardrail, filled in by Chapter 6" below. TODOs 1-4
and their original self-checks (1-8) are untouched and still pass.

## Why the guardrail's default is `human_approved=True`, disclosed explicitly

`run_visit_session()`'s new `human_approved` parameter defaults to
`True`, not `False`. This is a deliberate, disclosed trade-off, not an
oversight: Chapters 4 and 5 already shipped and locked in 8 self-checks
against this file's exact behavior, including one (`"reflect_on_response
revises the draft when a blocking condition was booked (Ch5)"`) that
requires `schedule_followup()` to have actually fired for its own
blocking-condition test case. The brief for this chapter requires those
8 checks to **still pass unchanged**. Defaulting `human_approved=True`
preserves that exact behavior for every existing call site, while the
guardrail's real enforcement is fully exercised by two **new** checks
(9 and 10, below) that call `run_visit_session()` with
`human_approved=False` explicitly. **In a real production system, the
safe default for a brand-new session would be `False`** ("not yet
approved"), not `True` — this scaffold's default exists specifically so
Chapters 4-5's regression tests don't have to be rewritten, and that
reasoning is stated here plainly rather than left implicit. A stricter
default is exactly the kind of change a real team would make in a
follow-up revision once the regression suite itself was updated to
match.

## What Chapter 4 shipped, and what Chapter 5 added

Chapter 4 shipped the **multi-tool-plus-memory half** of the L2
description in full:

- Three tools (`check_appointment_slot`, `get_patient_profile`,
  `schedule_followup`), reusing Chapters 1-3's tool-calling discipline
  without re-teaching it.
- A persisted long-term `MemoryStore` (read-modify-write, one JSON
  file, no vector database), exactly matching the lesson's own
  pattern.
- A promote-worthy classifier deciding which patient statements
  (conditions, preferences) get written to long-term memory.
- A composed `run_visit_session()` that merges persisted facts into a
  fresh session's working context, dispatches tools, and promotes new
  facts before the session ends — the same ordering discipline the
  lesson's Section 13 (promote-before-prune) established.

Chapter 5 adds the **reflection half**: a `is_blocking_condition()`
policy check (given, reused from Chapter 5's own lesson) and a real
`reflect_on_response()` that catches one concrete, demonstrable
mistake — CareBot drafting a routine-sounding confirmation for a visit
where a patient reported a serious, unresolved condition (e.g. "chest
pain that hasn't been evaluated") *and* a follow-up got booked. Before
Chapter 5, this case sailed through unflagged. After Chapter 5, the
draft is revised to name the concern and require clinical review
before it's presented as confirmed.

Chapter 6 adds the **guardrail half**: `guardrail_check_booking()`, a
hard, enforced check called *before* `schedule_followup()` is
dispatched. With a blocking condition on file and no explicit approval,
the booking simply never happens — `schedule_followup` never appears in
`tool_trace` at all, and CareBot's response says the visit needs
care-team review instead of implying anything was scheduled.

## Reflection stays on as a genuine defense-in-depth backstop (a deliberate choice)

Per this chapter's own brief, this project explicitly **keeps** Chapter
5's `reflect_on_response()` check active rather than removing it now
that the guardrail exists — this is the recommended, chosen design, not
an oversight. Reasoning:

- **They catch different failure shapes.** The guardrail only fires at
  the one call site inside `run_visit_session()` where
  `schedule_followup()` is dispatched. Reflection re-checks the
  *outgoing message itself*, which is a genuinely different, later
  surface — if a future code path ever built a CareBot response some
  other way (a different function, a retried call, a bug that bypasses
  the guardrail's call site by accident), reflection is still there to
  catch a routine-sounding confirmation for a blocking condition before
  it reaches the patient.
- **In this project's current code, the guardrail should make
  reflection's blocking-condition branch unreachable in the common
  case** — once the guardrail holds a booking, `booked` is `False`, so
  `reflect_on_response()`'s own `blocking and booked` condition is no
  longer `True` for that visit, and reflection correctly does nothing
  (see check 7, "reflect_on_response leaves a benign draft unchanged
  (Ch5)" — the same pass-through path). Check 8 (the one that *does*
  need `schedule_followup` to have fired) still exercises reflection's
  original catch, using `human_approved=True` implicitly via the
  default, exactly as designed above.
- **Two independent layers catching the same failure class is a
  legitimate, common production pattern** (defense-in-depth), not
  redundant engineering — a guardrail bug, a new code path that skips
  it, or a future refactor are all real risks a single layer can't
  cover alone. Removing reflection now would save a few lines but
  quietly remove the second layer this exact codebase already proved is
  necessary (Chapter 5's own lesson Section 12 showed a *live model's*
  self-critique correctly diagnosing a problem and still failing to fix
  it — a reminder that no single check should be trusted alone).

## The five TODOs

`starter.py` gives you all the tools, fixtures, `MemoryStore`, the
promote-worthy classifier, and (new) the `is_blocking_condition()`
policy helper already implemented — this project is about composing
Chapter 4's memory mechanisms and Chapter 5's reflection mechanism
correctly, not re-deriving Chapters 1-3's tool-calling mechanics.

1. **TODO 1** — `build_working_context()`: merge a patient's persisted
   conditions/preferences into a fresh session's working memory,
   mirroring the lesson's Section 5/15 pattern.
2. **TODO 2** — `promote_worthy_and_persist()`: classify and persist
   any promote-worthy fact stated during the visit, using
   read-modify-write.
3. **TODO 3** — `run_visit_session()`: compose the working-context
   merge, tool dispatch, and promotion into one visit flow, calling
   `reflect_on_response()` at the labeled call site (given — do not
   modify that line) before returning the final response.
4. **TODO 4 (Chapter 5)** — `reflect_on_response()`: check the
   draft against the blocking-condition policy and revise it when a
   blocking condition was persisted this visit AND a follow-up was
   actually booked; otherwise return the draft unchanged. Full
   instructions are in the function's own docstring in `starter.py`.
5. **TODO 5 (new, Chapter 6)** — inside `run_visit_session()`: call
   `guardrail_check_booking(current_facts, human_approved=human_approved)`
   before dispatching `schedule_followup()`, append the result to
   `tool_trace` as `("guardrail_check_booking", gate)`, only call
   `schedule_followup()` when `gate["allowed"]` is `True`, and build a
   "needs care-team review" response (naming `gate["blocking"]`) instead
   of a routine confirmation when it isn't. Full instructions are in the
   function's own docstring in `starter.py`.

## Why deterministic fixtures, not a live Ollama call

Same grading policy as this chapter's `exercises/` and `practice/`,
and every prior chapter's own project: `solution.py`'s pass/fail
checks never depend on a live model, so grading works the same way
everywhere, including CI with no Ollama server running. Chapter 5's
own lesson shows the live-Ollama self-critique pattern (a second model
call reviewing the first call's draft) for BikeBot — the same pattern
could be swapped in here once your self-check passes, using
`base_url="http://localhost:11434/v1"`, `model="llama3.2:latest"`; this
project's own grading stays deterministic either way.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 10 checks across working-context
merge, fact promotion (conditions and preferences), cross-process
persistence (a fresh `MemoryStore` instance still seeing visit 1's
facts), correct tool dispatch (not booking an unavailable slot),
reflection correctly leaving a benign draft alone versus revising an
unsafe one, and (new) the guardrail correctly holding a booking when
not approved versus releasing it once it is.

## How to check your work for real

1. Run the self-check above until all 10 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional: try the live-Ollama swap described above.

## This project is now complete (Chapters 4-6)

Per the curriculum map's L2 project description ("ships after Ch. 4,
extended through Ch. 5-6's reflection/guardrail material"), this
project now has all three pieces in place: persisted memory across
sessions (Ch. 4), a reflection step that revises what CareBot *says*
(Ch. 5), and a guardrail that stops or holds what CareBot *does* before
it happens (Ch. 6). No further chapters extend this file.

## Files

- `starter.py` — the scaffold with 5 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 10 checks.
- `RUBRIC.md` — self-grading criteria.
- `ai-paired.html` — a solo-build-then-critique exercise using this
  same CareBot scenario.
