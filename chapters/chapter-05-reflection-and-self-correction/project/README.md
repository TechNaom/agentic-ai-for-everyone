# Chapter 5 Project: L2 Assisted Project, Reflection Stage

Chapter 5 does **not** ship a new, separate project folder here. Per
`docs/curriculum/CURRICULUM_MAP.md`'s project ladder, the **L2
Assisted** project is a single, continuous project that ships partial
after Chapter 4 and is *extended in place* through Chapters 5 and 6 —
not re-created chapter by chapter. This directory exists (with a
`.gitkeep` sibling) purely as a scaffold placeholder and a signpost.

## Where the actual work is

**`chapters/chapter-04-memory-and-state/project/`** is the canonical
home of the L2 Assisted project (Hollowridge Wellness Clinic's
CareBot). That is where all of the following live:

- `README.md` — full project description, including "What Chapter 5
  did with this file" and "What Chapter 6 will do with this file."
- `starter.py` / `solution.py` — now with **4 TODOs** (TODOs 1-3 from
  Chapter 4, plus **TODO 4: reflection**, added this chapter).
- `RUBRIC.md` — self-grading criteria, now 5 criteria (25 points).
- `index.html` / `ai-paired.html` — the browsable project pages.

## What Chapter 5 changed there

`reflect_on_response(draft_response, context)`, wired into
`run_visit_session()` since Chapter 4 as a labeled no-op, now contains
a real self-critique-and-revise step: it checks whether a patient's
persisted conditions include a "blocking" one (e.g. unresolved chest
pain) AND whether a follow-up was actually booked this visit, and if
both are true, revises CareBot's draft response to flag the visit for
mandatory clinical review instead of a routine confirmation. This
mirrors, in CareBot's own domain, the exact mechanism this chapter's
own lesson built for a fresh scenario (Briarcliff Bike Rentals's
BikeBot): a grounded check against real facts, not just the model
"trying harder."

TODOs 1-3 (working-context merge, fact promotion, the composed visit
flow) were **not** touched or restructured — their Chapter 4 self-
checks still pass unchanged.

## What Chapter 6 will do there next

A `CHAPTER 6 EXTENSION POINT` comment already sits inside
`run_visit_session()`, immediately before `schedule_followup()` is
dispatched. Chapter 6 ("Guardrails and Safety for Autonomous Agents")
is expected to add a bounds/approval check *there* — stopping (or
requiring human approval for) an unsafe booking before it fires,
rather than only catching it after the fact the way this chapter's
reflection step does. That's the honest boundary this chapter's own
lesson names directly: reflection can revise what CareBot *says*, but
by the time it runs, `schedule_followup()` has already executed if a
slot was available — it cannot undo a tool call that already fired.
Preventing the call in the first place is a guardrail's job, not
reflection's.

## Why extend in place instead of duplicating files here

Three copies of the same CareBot scaffold (one per chapter) would let
Chapters 5 and 6 drift out of sync with each other and with Chapter
4's own grading contract. Keeping one canonical `project/` directory
and extending its `starter.py`/`solution.py` in place, chapter by
chapter, is the only way "partial scaffold, extended through Ch. 5-6"
(the curriculum map's own words) stays true across all three chapters.
