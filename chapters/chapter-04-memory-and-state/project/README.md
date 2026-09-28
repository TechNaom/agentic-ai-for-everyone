# Chapter 4 Project (L2 Assisted, extended by Ch. 5): CareBot for Hollowridge Wellness Clinic

**This is this course's numbered L2 Assisted project**, not a chapter
mini-project — per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder: *"Build a multi-tool agent with memory and a reflection step
for a provided scenario, partial scaffold, ships after Ch. 4, extended
through Ch. 5-6's reflection/guardrail material."* Chapters 2-3 both
built chapter mini-projects instead, because the ladder had no
numbered slot for them yet. Chapter 4 is where the ladder says the L2
project actually begins.

**Update, Chapter 5:** this file's reflection half is no longer a
no-op. `reflect_on_response()`'s body now contains a real,
deterministic self-critique-and-revise step — see "TODO 4: reflection,
filled in by Chapter 5" below. TODOs 1-3 and their original self-checks
are untouched. Chapter 6 will extend this same project a second time,
adding a guardrail check *before* `schedule_followup()` is dispatched
(see the `CHAPTER 6 EXTENSION POINT` comment inside `run_visit_session()`
in `solution.py`) — reflection fixes what CareBot *says*; it cannot
undo a tool call that already fired, which is exactly the gap Chapter
6's guardrails close.

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

## The four TODOs

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
4. **TODO 4 (new, Chapter 5)** — `reflect_on_response()`: check the
   draft against the blocking-condition policy and revise it when a
   blocking condition was persisted this visit AND a follow-up was
   actually booked; otherwise return the draft unchanged. Full
   instructions are in the function's own docstring in `starter.py`.

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

This prints a structural self-check: 8 checks across working-context
merge, fact promotion (conditions and preferences), cross-process
persistence (a fresh `MemoryStore` instance still seeing visit 1's
facts), correct tool dispatch (not booking an unavailable slot), and
(new) reflection correctly leaving a benign draft alone versus
revising an unsafe one.

## How to check your work for real

1. Run the self-check above until all 8 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional: try the live-Ollama swap described above.

## What Chapter 6 will do with this file

Chapter 6 ("Guardrails and Safety for Autonomous Agents") is expected
to extend this same project a third time (per the L2 project's own
ladder description), adding a bounds/approval check immediately before
`schedule_followup()` is dispatched inside `run_visit_session()` — see
the `CHAPTER 6 EXTENSION POINT` comment already sitting at that exact
line in `solution.py`. The honest gap Chapter 5's reflection step
leaves on purpose: by the time `reflect_on_response()` runs, an
available slot has *already* been booked — reflection can only revise
what CareBot says about it, not stop the booking itself. That's a
guardrail's job, not reflection's, and Chapter 6 is where it's added.

## Files

- `starter.py` — the scaffold with 4 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 8 checks.
- `RUBRIC.md` — self-grading criteria.
- `ai-paired.html` — a solo-build-then-critique exercise using this
  same CareBot scenario.
