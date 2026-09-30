# Chapter 8 Quality Audit: Cost and Latency Control of Agent Loops

Session date: 2026-09-30. This session built Chapter 8 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, a real standalone chapter-mini-project `project/`
(README + RUBRIC + index.html + ai-paired.html + starter.py +
solution.py, matching Chapter 7's own pattern, NOT the L3 Independent
project, which ships separately), this audit, the Module 4 combined
assessment (`reliability-plan + cost-control exercise`, reusing
Chapter 7's AND Chapter 8's own already-tested project functions),
wiring `assets/chapters-data.js` and `docs/curriculum/index.html`,
updating root `index.html`'s hero stats and stale intro paragraph, and
rewriting `PROJECT_STATE.md`'s "Next Recommended Task" for Chapter 9.

## Honest self-critique

**What's strong:**
- **Chapter 7's own FactScout was reused directly as the chapter's
  scenario**, per the brief's own stated preference, rather than a new
  disconnected agent -- `trajectory_covers_goal` and
  `trajectory_correctness` are the literal Chapter 7 functions (Section
  1), and `cost_per_success` (Section 13) is re-run before AND after
  this chapter's own five techniques are applied, producing a real
  measured delta rather than an asserted one.
- **Three genuine, unscripted live-model results became this
  chapter's own central worked examples:**
  - A capped, one-word tool-selection call (4.76s) vs. an open-ended
    "explain your reasoning" call (94.45s) for the IDENTICAL model and
    task -- a real ~20x latency gap (Section 2/7), with the cheap-style
    call landing on the correct first step.
  - Two real Ollama calls run sequentially (5.14s total) vs. the same
    two calls run concurrently via `ThreadPoolExecutor` (1.61s total) --
    a real ~3.2x measured speedup on genuinely independent live calls
    against the same local server (Section 9).
  - A real 48.99s first-generation call after a load-only warm-up,
    disclosed honestly rather than presented as instant (Section 2).
- **The full before/after (Section 13) is a real, executed
  measurement, not an assertion**: 51.0% cost reduction, 92.3% latency
  reduction, computed by re-running a Chapter-7-shaped 20-runs-per-
  task/5-task harness twice (before Section 4's naive baseline, after
  Section 12's controlled version) and recomputing `cost_per_success`
  both times. A real, disclosed small success-rate dip (0.7 -> 0.65 on
  three of five tasks) was found and reported honestly rather than
  hidden, with the report explicitly checking whether `cost_per_success`
  still improved despite it (it did, on every task).
- Every deterministic Python snippet in the lesson (accounting,
  `BudgetGuard`, early exit, model routing, the cache, percentiles,
  retry/backoff, the assembled controlled run, and the full before/
  after harness) was actually run in a scratch directory before being
  transcribed into `lesson.html`.
- Lesson density: 61 lines match `grep -c '<pre\|<code' lesson.html`
  (above the 60+ requirement, matching Chapter 7's own 61 exactly), 114
  total tag occurrences via `grep -o '<pre\|<code' | wc -l`.
- A real bug was found and fixed during this session's own scratch
  testing (not hidden): the first `BudgetGuard` configuration used in
  the before/after harness (`max_cost=0.01`) denied the AFTER version's
  very first strong-tier step on every task, driving its measured
  success rate to a false 0.0% -- caught by testing before it reached
  the lesson, corrected to `max_cost=0.05`, and the corrected, real
  numbers are what Sections 12-13 report.
- The chapter mini-project (`project/`) is a real, standalone,
  gradable scaffold, matching Chapter 7's own pattern per the brief
  (NOT the L3 Independent project, which the brief explicitly schedules
  separately, after this chapter). Its scenario (Portage Grain
  Cooperative's YieldScout) is fresh, and its three TODOs
  (`task_success`, `is_within_budget`, `run_cost_controlled_harness`)
  mirror the lesson's own budget-enforcement pillar specifically
  (distinct from Chapter 7's own task-success/trajectory/pass@k
  pillars).
- The Module 4 combined assessment was built THIS session, per the
  precedent set at Chapter 7 for Modules 1-3 (see "Module 4 assessment
  decision" below) -- it reuses Chapter 7's AND Chapter 8's own
  already-tested chapter-mini-project functions (`trajectory_
  correctness`, `task_success` from Chapter 7; `is_within_budget`,
  `step_cost` from Chapter 8), loaded via `importlib` directly from
  their real `project/solution.py` files, not reimplemented.

**What's a known limitation, disclosed rather than hidden:**
- **The before/after harness's own "before" and "after" runs are both
  seeded simulations, not live model calls at the full 20-runs-per-
  task/5-task scale.** This is the same disclosed trade-off Chapter
  7's own bulk harness made, for the same reason (per-call and per-
  session time budgets). What IS live and real in this chapter: the
  three specific latency comparisons named above (cheap-vs-strong
  call shape, sequential-vs-parallel calls, and the cold-load/warm
  sanity checks). The simulation's own `STEP_ERROR_RATE` (0.17) is the
  same constant Chapter 7 calibrated from its own live 1/6 result, not
  a new invented number.
- **The illustrative `MODEL_RATES` dollar-per-1K-token table is not
  tied to any real provider's published pricing.** It's disclosed as
  illustrative in the lesson itself (Section 3), used only for a
  consistent relative before/after comparison, not a claim about real-
  world dollar costs.
- **OpenRouter and Groq are named only conceptually** (Section 3, 7,
  11) -- no live call was made to either, matching this course's own
  no-paid-API-calls policy. The `swapping_in_a_cheap_hosted_tier.py`
  snippet (Section 11) shows only a `base_url`/`api_key` config shape,
  never an actual request.
- The two-fact practice-bank scenarios and exercises' free-text-style
  answers still rely on exact-string or keyword matching rather than
  fully semantic grading -- the same necessarily-incomplete, disclosed
  limitation as every prior chapter's own exercise harness.
- `scripts/local_check.sh`'s own glob does not cover `assessments/
  module-assessments/*/solution.py` (the same gap Chapter 7's audit
  noted, not introduced this session); the Module 4 assessment was
  verified manually instead (see "Code tested before writing" below).

## Module 4 assessment decision

`docs/curriculum/CURRICULUM_MAP.md` names Module 4's own assessment a
"reliability-plan + cost-control exercise," spanning Chapters 7 AND 8.
Chapter 7's own session deliberately did NOT build this, precisely so
it could be built for real, once, at Chapter 8's own closing session --
the exact precedent this session followed. Built
`assessments/module-assessments/module-4-reliability-plan-and-cost-
control-exercise/` (README + RUBRIC + starter.py + solution.py),
reusing:
- Chapter 7's `trajectory_correctness` and `task_success` (from
  `chapters/chapter-07-evaluating-agent-reliability/project/
  solution.py`, TriageScout's own T1/CLM-1 task, unchanged).
- Chapter 8's `is_within_budget` and `step_cost` (from `chapters/
  chapter-08-cost-and-latency-control-of-agent-loops/project/
  solution.py`, unchanged).

Both loaded via `importlib.util.spec_from_file_location`, the same
mechanism Modules 1-3's own combined assessments used at Chapter 7's
session. `solution.py` scores 3/3 objectively-checkable parts (Part 3
is self-graded prose); `starter.py` scores 0/3, no crash.

**Module 5 gap-audit, per the brief's own instruction to make this
decision explicitly rather than silently deferring again:** Module 5's
own assessment ("multi-agent coordination-pattern exercise," spanning
Chapters 9-11) should wait until Chapter 11 (Module 5's closing
chapter), NOT be built at Chapter 9. Reasoning, following the exact
precedent this session and Chapter 7's session both used: Module 4's
assessment needed BOTH of its chapters' real, tested functions to exist
before it could reuse them meaningfully rather than guess at a not-yet-
built chapter's shape; Module 5's assessment needs Chapter 9's
coordination-pattern code, Chapter 10's communication code, AND Chapter
11's production-operating code (retries, timeouts, structured logging)
all to exist first, since a "coordination-pattern exercise" that
doesn't yet know what Chapter 11 adds would either be incomplete or
need rework. This decision is carried forward explicitly into this
file's own Chapter 9 hand-off below, per the brief's instruction not to
silently defer without saying so.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-07-audit.md` (26
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group,
Millbrook Credit Union, Amberlock Self-Storage, Cascadia Home Security,
Greywick Dispatch, Larkmoor Archive Service, Thornmere Public Transit,
Emberlyn Underwriting).

**This chapter deliberately reused Greywick Dispatch/FactScout as its
own lesson scenario** (per the brief's own stated preference to
continue Chapter 7's agent rather than start a new, disconnected one)
-- NOT a new org, and not counted as a collision since it's an
intentional reuse, the same precedent Chapter 5-6's sessions used when
reusing Hollowridge Wellness Clinic/CareBot for the L2 project's own
continuity.

**4 new fictional orgs used this chapter, all checked clean against the
full running list and against each other:**

- **Brambleford Analytics** (exercises; product: InsightScout)
- **Caldwell Ridge Observatory** (exercises `ai-paired.html`; product:
  SkyScout)
- **Portage Grain Cooperative** (project; product: YieldScout)
- **Marrowvale Textile Mill** (project `ai-paired.html`; product:
  LoomScout)

**"QuoteBot"'s pricing-service employer** (practice `ai-paired.html`)
is left unnamed/generic on purpose, the same convention Chapter 7's
"ClaimBot," Chapter 6's EscrowBot, Chapter 5's RenewBot, Chapter 4's
MemoBot, Chapter 3's HandoffBot, Chapter 2's EscalationBot, and Chapter
1's ConciergeBot scenarios all used.

Every distinctive root word above (Brambleford, Caldwell, Portage,
Marrowvale) was checked for zero overlap against both this chapter's
own four named scenarios and the full 26-org Chapter 1-7 list --
including a specific check that "Caldwell Ridge" shares no root word
with any prior "Ridge"-adjacent name (none exists in the list) and that
"Marrowvale" shares no root with "Millbrook" or "Mossgate" (different
roots, no overlap). The running exclusion list for future chapters is
now: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group,
Millbrook Credit Union, Amberlock Self-Storage, Cascadia Home Security,
Greywick Dispatch, Larkmoor Archive Service, Thornmere Public Transit,
Emberlyn Underwriting, Brambleford Analytics, Caldwell Ridge
Observatory, Portage Grain Cooperative, Marrowvale Textile Mill. Future
chapters should extend this list, not restart it.

## Ollama check, done fresh this session

The model was explicitly warmed before any lesson code was written,
using this course's documented recovery command:

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
{"model":"llama3.2","created_at":"2026-09-30T19:38:23.526188227Z","response":"","done":true,"done_reason":"load"}
```

Unlike Chapter 7's session (348.7s cold load reported directly from the
`total_duration` field), this warm-up call used an empty prompt and
reported no duration fields at all -- so this session disclosed the
first REAL generation call's timing instead, which still took a while:

```
elapsed: 48.99
OK
```

Once genuinely warm, every subsequent call was fast (4.76s-94.45s,
with the range itself being this chapter's own central live result --
see Section 2/7 above). No call this session exceeded the course's
450-second budget; no idle-waiting past budget occurred.

## Code tested before writing

Every Python snippet this session wrote was actually run, in a scratch
directory, before its content (or its verified output) was transcribed
into `lesson.html`:

```
$ python3 test_lesson.py          -> full deterministic prototype: per-
                                      step accounting, BudgetGuard, early
                                      exit, model routing, caching,
                                      sequential-vs-parallel timing,
                                      percentiles, retry/backoff, and the
                                      full before/after harness -- all
                                      verified; the max_cost=0.01 budget
                                      bug DISCOVERED and FIXED here
                                      (see self-critique above)
$ (live) live_test.py             -> REAL Ollama call, 48.99s, "OK"
$ (live) live_test2.py            -> REAL Ollama calls: cheap-style
                                      4.76s ("search_archive", correct),
                                      strong-style 94.45s (long reasoning)
$ (live) live_test3.py            -> REAL Ollama calls x2, sequential
                                      5.14s vs. parallel (ThreadPoolExecutor)
                                      1.61s
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
                                    -> 10/10 checks passed (L2 regression
                                       check, unchanged from Chapter 7)
$ python3 chapters/chapter-07-evaluating-agent-reliability/project/solution.py
                                    -> 8/8 checks passed (Ch7 project
                                       regression check, unchanged)
```

And for the new Module 4 assessment:

```
$ python3 assessments/module-assessments/module-4-.../solution.py -> 3/3
$ python3 assessments/module-assessments/module-4-.../starter.py  -> 0/3, no crash
```

No stray JSON files or `__pycache__` directories were left behind in
any chapter or assessment directory (`__pycache__` directories were
removed explicitly before the final commit).

## Local check

`scripts/local_check.sh < /dev/null` was run for the whole repo after
all Chapter 8 files, the Module 4 assessment, and the site-wiring
updates were in place:

```
== 1. Checking required folders ==          OK
== 2. Scanning for placeholder text ==       OK
== 3. Python syntax check ==                 OK
== 4. Running every exercises/solution.py,
      project/solution.py, and
      practice/solution.py ==                OK
== 5. JS syntax + chapter-path validation == OK
== 6. Scanning for likely secrets ==         OK

All local checks passed. Safe to push.
```

Note: `local_check.sh`'s own glob does not cover `assessments/
module-assessments/*/solution.py` -- the Module 4 assessment was
verified manually above instead, the same pre-existing gap noted (not
introduced) by Chapter 7's own audit.
