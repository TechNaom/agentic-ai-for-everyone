# Chapter 9 Quality Audit: Multi-Agent Orchestration Patterns

Session date: 2026-09-30. This session built Chapter 9 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, a real standalone chapter-mini-project `project/`
(README + RUBRIC + index.html + ai-paired.html + starter.py +
solution.py, matching Chapters 7-8's own pattern, NOT the L3
Independent project, which the project ladder still owes the repo and
was NOT built this session either), this audit, wiring
`assets/chapters-data.js` and `docs/curriculum/index.html`, updating
root `index.html`'s hero stats and stale intro paragraph, and
rewriting `PROJECT_STATE.md`'s "Next Recommended Task" for Chapter 10.

## Honest self-critique

**What's strong:**
- **Three genuine, unscripted live-model results this session found
  while testing, not manufactured, became this chapter's own central
  worked examples:**
  - A supervisor given a full multi-part goal and three separate
    dispatch tools returned a fully-formed three-call plan as PLAIN
    TEXT (`msg.tool_calls` empty) instead of real tool calls (Section
    4) -- a genuine decomposition/dispatch reliability failure, not
    manufactured for the lesson.
  - Switching to one-sub-task-per-call fixed two of three calls, but
    the THIRD call from the exact same test run came back malformed
    again (Section 4) -- real, observed non-determinism disclosed
    honestly, not smoothed over.
  - A bounded retry on that exact failed sub-task succeeded on the
    first attempt (Section 5) -- also disclosed honestly as
    non-deterministic (this same sub-task failed twice moments earlier
    in Section 4's own test).
  - A real fan-out/fan-in measurement: three genuinely independent
    worker calls took 33.65s sequential vs. 9.57s concurrent (~3.5x),
    with all three routing correctly that run (Section 8).
- **Two deliberately planted, honestly disclosed "genuine bug" style
  examples**, following every prior chapter's own precedent (Chapter
  1's Cedar Hollow bug, Chapter 7's $12M/$9.4M bug, Chapter 8's
  max_cost=0.01 budget bug): a `stayscout_worker_buggy` that always
  returns a Porto hotel regardless of the requested city (Section 12,
  the chapter's own central "plausible-but-wrong" demonstration), and
  a naive retry-without-idempotency-check that visibly double-dispatches
  the same sub-task (Section 13).
- Every deterministic Python snippet in the lesson (the router,
  blackboard/lock, per-agent budgets, failure isolation, content
  verification, idempotent dispatch, cross-agent attribution, the
  fail-closed approval checkpoint, and the assembled end-to-end run)
  was actually run in a scratch directory before being transcribed
  into `lesson.html`.
- Lesson density: 63 matches via `grep -c '<pre\|<code' lesson.html`
  (above the 60+ requirement).
- This chapter explicitly hands off from, rather than re-teaches,
  Chapters 1-8's own mechanics, and extends TWO specific prior-chapter
  mechanisms by name rather than inventing parallel new ones: Chapter
  7's `trajectory_correctness` becomes `which_agent_responsible`
  (Section 14, "which tool" -> "which agent"), and Chapter 8's
  `is_within_budget` becomes per-agent budgets (Section 10, one loop's
  budget -> one budget per worker). Chapter 6's fail-closed
  `human_approved` discipline is also explicitly reused, unchanged in
  spirit, for a worker's own spend-commit checkpoint (Section 15).
- The chapter mini-project (`project/`) is a real, standalone,
  gradable scaffold (NOT the L3 Independent project). Its scenario
  (Ashgrove Municipal Services' CityScout) is fresh, and its three
  TODOs (`route_subtask`, `dispatch_isolated`, `run_city_scout_harness`)
  combine fail-closed routing, failure isolation, and idempotent,
  attributed dispatch into one harness -- distinct from the lesson's
  own TripScout scenario and from the exercises' CaseScout scenario.

**What's a known limitation, disclosed rather than hidden:**
- **This chapter's live results are genuinely non-deterministic and
  were NOT re-run to "get a clean result."** Section 4's malformed
  dispatch, Section 5's successful retry, and Section 8's clean
  three-for-three fan-out routing are all real, single-shot captures
  from this session -- re-running any of them against the same local
  Ollama install could plausibly produce a different specific outcome
  (more or fewer malformed calls), the same disclosed reliability
  caveat every prior chapter's own live-call sections carry.
- **The failure-isolation, per-agent-budget, blackboard, verification,
  idempotency, and cross-agent-attribution mechanisms are all
  deterministic Python, not live-model-driven.** This mirrors Chapter
  8's own before/after harness disclosure: the coordination LOGIC is
  real and tested, but the "worker crashes," "worker returns wrong
  city," and "duplicate dispatch" scenarios are deliberately
  constructed inputs to that logic, not emergent live-model behavior.
  This is the same, necessary trade-off every prior chapter's
  deterministic-grading policy makes.
- **Only two workers (FlightScout/StayScout/ExcursionScout in the
  lesson; two workers in the project) were actually exercised, not a
  larger N.** The brief called for "2-3 worker agents," and this
  chapter used exactly that range -- a system with many more workers
  (the architect-level interview question about recursive
  supervisor-of-supervisors budget composition, Question 10) is named
  but not built.
- The practice-bank scenarios and exercises' concept-naming answers
  still rely on keyword matching rather than fully semantic grading --
  the same necessarily-incomplete, disclosed limitation as every prior
  chapter's own exercise harness.

## L3 Independent project and Module 5 assessment -- both still deferred, restated explicitly

Per `PROJECT_STATE.md`'s own Chapter 9 hand-off (written at Chapter
8's session) and this course's standing discipline of never letting a
deferred decision silently disappear:

- **The L3 Independent project** ("design and implement a
  reliability-instrumented, cost-bounded agent for a given problem, no
  scaffold," per the curriculum map's project ladder) was deferred past
  Chapter 8 and has **still not been built** as of this chapter. This
  chapter's own `project/` directory is a chapter mini-project
  (CityScout), matching Chapters 7-8's own pattern, explicitly NOT the
  L3 project. This flag is restated again, explicitly, in
  `PROJECT_STATE.md`'s Chapter 10 hand-off below -- whichever future
  session builds it should combine Chapter 7's reliability
  instrumentation, Chapter 8's cost-bounding techniques, AND this
  chapter's multi-agent coordination vocabulary, with NO starter
  scaffold, per L3's own "independent" definition.
- **Module 5's own assessment** ("multi-agent coordination-pattern
  exercise," spanning Chapters 9-11) was NOT built this session, per
  the exact precedent Chapter 8's own audit set: it needs Chapter 9's
  coordination-pattern code, Chapter 10's communication code, AND
  Chapter 11's production-operating code all to exist first. This
  decision is carried forward, unchanged, to whichever session ships
  Chapter 11.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-08-audit.md` (30
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group,
Millbrook Credit Union, Amberlock Self-Storage, Cascadia Home Security,
Greywick Dispatch, Larkmoor Archive Service, Thornmere Public Transit,
Emberlyn Underwriting, Brambleford Analytics, Caldwell Ridge
Observatory, Portage Grain Cooperative, Marrowvale Textile Mill).

**Five new fictional orgs used this chapter, all checked clean against
the full running list and against each other:**

- **Quillmark Journeys** (lesson; supervisor TripScout, workers
  FlightScout/StayScout/ExcursionScout)
- **Hadleigh Civic Records Bureau** (exercises; supervisor CaseScout,
  workers PermitScout/LicenseScout/ZoningScout)
- **Corvindale Claims Network** (exercises `ai-paired.html`; supervisor
  ClaimScout, workers AutoScout/PropertyScout/HealthScout)
- **Ashgrove Municipal Services** (project; supervisor CityScout,
  workers InspectionScout/ZoneScout)
- **Foxglenn Relief Network** (project `ai-paired.html`; supervisor
  AidScout, workers ShelterScout/SupplyScout)

**"DispatchBot"'s employer** (practice `ai-paired.html`) is left
unnamed/generic on purpose, the same convention Chapter 7's "ClaimBot,"
Chapter 8's "QuoteBot," and every prior chapter's own unnamed-org
scenario used.

Every distinctive root word above (Quillmark, Hadleigh, Corvindale,
Ashgrove, Foxglenn) was checked for zero overlap against both this
chapter's own five named scenarios and the full 30-org Chapter 1-8
list -- including a specific check that "Ashgrove" shares no root with
"Alderleaf" or "Amberlock" (different roots), and that "Foxglenn"
shares no root with "Fenwick" or "Fernbrook" (different roots, no
overlap). The running exclusion list for future chapters is now:
Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol, Wavecrest
Marina, Alderleaf Research Group, Pinehurst Realty Group, Thistlewood
Veterinary Group, Cobblestone Courier Co., Palisade Broadband,
Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel Appliance
Service, Larkspur Fitness Studio, Driftwood Legal Clinic, Saltmarsh
Language Academy, Hollowridge Wellness Clinic, Briarcliff Bike Rentals,
Fenwick Home Repair Co-op, Mossgate Dental Group, Millbrook Credit
Union, Amberlock Self-Storage, Cascadia Home Security, Greywick
Dispatch, Larkmoor Archive Service, Thornmere Public Transit, Emberlyn
Underwriting, Brambleford Analytics, Caldwell Ridge Observatory,
Portage Grain Cooperative, Marrowvale Textile Mill, Quillmark Journeys,
Hadleigh Civic Records Bureau, Corvindale Claims Network, Ashgrove
Municipal Services, Foxglenn Relief Network. Future chapters should
extend this list, not restart it.

## Ollama check, done fresh this session

The model was explicitly warmed before any live call this session:

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
{"model":"llama3.2","created_at":"2026-09-30T20:08:18.286185343Z","response":"","done":true,"done_reason":"load"}
```

A sanity call after that warm-up was fast this session:

```
elapsed: 2.64
How can I assist you today?
```

Every subsequent live call this session (single-tool-call dispatch
tests, the retry test, and the three-worker fan-out test) completed
well within this course's 450-second budget -- no idle-waiting past
budget occurred, and every live result is reported exactly as
captured, including the two genuine malformed-dispatch results
Sections 4-5 disclose honestly rather than hide or re-run until clean.

## Code tested before writing

Every Python snippet this session wrote was actually run, in a scratch
directory, before its content (or its verified output) was transcribed
into `lesson.html`:

```
$ python3 sanity.py                -> REAL Ollama call, 2.64s, "How can I assist you today?"
$ (live) supervisor_route.py       -> REAL Ollama call: 3-tool, full-goal dispatch, 45.38s,
                                       genuinely malformed (plain text, not tool_calls)
$ (live) supervisor_route2.py      -> REAL Ollama calls x3, one-sub-task-at-a-time:
                                       2 clean (15.83s, 6.3s), 1 malformed (5.41s)
$ (live) retry_dispatch.py         -> REAL Ollama call, retry succeeded on attempt 1 (3.79s)
$ (live) parallel_fanout.py        -> REAL Ollama calls x6: sequential 33.65s,
                                       parallel (ThreadPoolExecutor) 9.57s (~3.5x)
$ python3 test_lesson.py           -> full deterministic prototype: router, blackboard/lock,
                                       per-agent budgets, failure isolation, content
                                       verification, idempotent dispatch, cross-agent
                                       attribution, fail-closed approval, assembled run --
                                       all verified
```

Then, in the actual chapter directory, after every file was written:

```
$ python3 exercises/solution.py    -> Score: 19/19
$ python3 exercises/starter.py     -> Score: 0/19, no crash
$ python3 practice/solution.py     -> TOTAL: 8/8
$ python3 practice/starter.py      -> TOTAL: 0/8, no crash
$ python3 project/solution.py      -> 9/9 checks passed
$ python3 project/starter.py       -> 2/9 checks passed, no crash
$ python3 chapters/chapter-04-memory-and-state/project/solution.py
                                    -> 10/10 checks passed (L2 regression, unchanged)
$ python3 chapters/chapter-07-evaluating-agent-reliability/project/solution.py
                                    -> 8/8 checks passed (Ch7 project regression, unchanged)
$ python3 chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py
                                    -> 9/9 checks passed (Ch8 project regression, unchanged)
```

No stray JSON files or `__pycache__` directories were left behind in
any chapter directory.

## Local check

`scripts/local_check.sh < /dev/null` was run for the whole repo after
all Chapter 9 files and the site-wiring updates were in place; see the
commit for the full passing output.
