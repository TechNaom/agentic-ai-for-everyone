# Chapter 6 Project: L2 Assisted Project, Guardrail Stage (Final)

Chapter 6 does **not** ship a new, separate project folder here. Per
`docs/curriculum/CURRICULUM_MAP.md`'s project ladder, the **L2
Assisted** project is a single, continuous project that ships partial
after Chapter 4 and is *extended in place* through Chapters 5 and 6 —
not re-created chapter by chapter. This directory exists (with a
`.gitkeep` sibling) purely as a scaffold placeholder and a signpost.

## Where the actual work is

**`chapters/chapter-04-memory-and-state/project/`** is the canonical
home of the L2 Assisted project (Hollowridge Wellness Clinic's
CareBot). That is where all of the following live:

- `README.md` — full project description, including "Why the
  guardrail fails closed: `human_approved` defaults to `False`" and
  "Reflection stays on as a genuine defense-in-depth backstop."
- `starter.py` / `solution.py` — now with **5 TODOs** (TODOs 1-3 from
  Chapter 4, TODO 4: reflection from Chapter 5, and **TODO 5: the
  guardrail**, added this chapter).
- `RUBRIC.md` — self-grading criteria, now 6 criteria (30 points).
- `index.html` / `ai-paired.html` — the browsable project pages.

## What Chapter 6 changed there

`run_visit_session()`, which has dispatched `schedule_followup()`
since Chapter 4 with no guardrail at all, now calls
`guardrail_check_booking(current_facts, human_approved=human_approved)`
**immediately before** that dispatch — a hard, enforced check, not a
message revised after the fact. With a blocking condition on file and
no explicit approval, `schedule_followup` never appears in
`tool_trace` at all; CareBot's response instead says the visit needs
care-team review. This mirrors, in CareBot's own domain, the exact
mechanism this chapter's own lesson built for a fresh scenario
(Millbrook Credit Union's LedgerBot): a hard boundary at the
tool-dispatch step, checked before the action, not after.

TODOs 1-4 (working-context merge, fact promotion, the composed visit
flow, and reflection) were **not** touched or restructured — their
Chapter 4-5 self-checks (1-8) still pass unchanged. Two new checks (9
and 10) prove the guardrail actually holds an unapproved booking and
releases it once approved.

## The guardrail vs. reflection: kept as defense-in-depth, not replaced

Chapter 5's `reflect_on_response()` was deliberately **kept**, not
removed, now that the guardrail exists — this project's own README (in
`chapter-04-memory-and-state/project/`) documents the full reasoning:
the two layers catch different failure shapes, and two independent
checks against the same failure class is a legitimate, common
production pattern (defense-in-depth), not redundant engineering.

## This project is now complete

Per the curriculum map's L2 project description ("ships after Ch. 4,
extended through Ch. 5-6's reflection/guardrail material"), this
project now demonstrates all three of Module 3's (and Module 2's)
pillars in one composed system: persisted memory across sessions (Ch.
4), a reflection step that revises what CareBot *says* (Ch. 5), and a
guardrail that stops or holds what CareBot *does* before it happens
(Ch. 6). No further chapters extend this file.

## Why extend in place instead of duplicating files here

Three copies of the same CareBot scaffold (one per chapter) would let
Chapters 5 and 6 drift out of sync with each other and with Chapter
4's own grading contract. Keeping one canonical `project/` directory
and extending its `starter.py`/`solution.py` in place, chapter by
chapter, is the only way "partial scaffold, extended through Ch. 5-6"
(the curriculum map's own words) stays true across all three chapters.
