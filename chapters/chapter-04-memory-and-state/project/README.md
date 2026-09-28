# Chapter 4 Project (L2 Assisted, partial scaffold): CareBot for Hollowridge Wellness Clinic

**This is this course's numbered L2 Assisted project**, not a chapter
mini-project — per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder: *"Build a multi-tool agent with memory and a reflection step
for a provided scenario, partial scaffold, ships after Ch. 4, extended
through Ch. 5-6's reflection/guardrail material."* Chapters 2-3 both
built chapter mini-projects instead, because the ladder had no
numbered slot for them yet. Chapter 4 is different: this is the
chapter where the ladder says the L2 project actually begins.

## What Chapter 4 ships, and what it deliberately doesn't

This project ships the **multi-tool-plus-memory half** of the L2
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

**The reflection half is intentionally a no-op**, not implemented
early. `reflect_on_response(draft_response, context)` is wired into
`run_visit_session()`'s call path exactly where a real reflection step
belongs, and its body currently just returns `draft_response`
unchanged. This is what "partial scaffold, extended through Ch. 5-6"
means concretely: **Chapter 5 will replace this function's body (not
its call site)** with a real self-critique-and-revise step, once
reflection is actually taught. Building a fake or premature reflection
step here would misrepresent material this course hasn't covered yet
— the honest, correct move is a clearly labeled extension point, not a
placeholder pretending to be the real thing.

## The three TODOs

`starter.py` gives you all the tools, fixtures, `MemoryStore`, the
promote-worthy classifier, and the `reflect_on_response` no-op already
implemented — this project is about composing Chapter 4's own memory
mechanisms correctly, not re-deriving Chapters 1-3's tool-calling
mechanics or building reflection early.

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

## Why deterministic fixtures, not a live Ollama call

Same grading policy as this chapter's `exercises/` and `practice/`,
and every prior chapter's own project: `solution.py`'s pass/fail
checks never depend on a live model, so grading works the same way
everywhere, including CI with no Ollama server running. The lesson's
own Section 8 (`live_grounded_reply.py`) shows the exact live-Ollama
pattern for turning persisted facts into a real, personalized reply —
swap it in here once your self-check passes, using
`base_url="http://localhost:11434/v1"`, `model="llama3.2:latest"`.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 7 checks across working-context
merge, fact promotion (conditions and preferences), cross-process
persistence (a fresh `MemoryStore` instance still seeing visit 1's
facts), correct tool dispatch (not booking an unavailable slot), and
the reflection no-op passthrough.

## How to check your work for real

1. Run the self-check above until all 7 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional: try the live-Ollama swap described above.

## What Chapter 5 will do with this file

Chapter 5 ("Reflection and Self-Correction") will extend this exact
project — not start a new one — by replacing `reflect_on_response()`'s
body with a real self-critique-and-revise step that can catch and fix
a draft response before it's returned (for example, catching a draft
that recommends scheduling a follow-up despite an unresolved condition
that should have blocked it). Chapter 6 ("Guardrails and Safety") is
expected to extend it again with bounds/approval checks around the
tool-dispatch step. Nothing about this file's TODOs 1-3 should need to
change for either extension — that's the point of wiring the call site
in now.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 7 checks.
- `RUBRIC.md` — self-grading criteria.
- `ai-paired.html` — a solo-build-then-critique exercise using this
  same CareBot scenario.
