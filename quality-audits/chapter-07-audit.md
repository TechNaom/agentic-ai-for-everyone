# Chapter 7 Quality Audit: Evaluating Agent Reliability

Session date: 2026-09-30. This session built Chapter 7 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, a real standalone chapter-mini-project `project/`
(README + RUBRIC + index.html + ai-paired.html + starter.py +
solution.py, per the brief's instruction that Chapter 7 returns to a
full scaffold, unlike Chapters 5-6's signposts to the L2 project), this
audit, wiring `assets/chapters-data.js` and `docs/curriculum/index.html`,
updating root `index.html`'s hero stats, building Module 1-3's
combined assessments (a pre-existing gap flagged but not built by any
prior session), and rewriting `PROJECT_STATE.md`'s "Next Recommended
Task" for Chapter 8.

## Honest self-critique

**What's strong:**
- **A genuine, unscripted live-model non-determinism result became
  this chapter's central worked example.** The identical fact-check
  task was sent to `llama3.2:latest` six separate times, asking only
  "which tool would you call first?" Results: `verify_source_
  credibility`, `verify_source_credibility`, `cross_check_claim`,
  `cross_check_claim`, `cross_check_claim`, `search_archive` -- only
  the last run matched the correct ground-truth first step
  (`search_archive`). This is not a manufactured example; it's the
  literal output of a live call captured verbatim, and it's exactly
  the phenomenon Sections 9-11 build a harness to measure at scale.
- **A genuine bug in this session's own tool code became a second,
  unplanned, and arguably more valuable teaching moment.**
  `cross_check_claim()`'s word-overlap heuristic reported that a claim
  saying "the bridge cost $12M" MATCHED an archive record that actually
  said "$9.4M," because both strings share enough non-numeric words.
  This was discovered while testing the lesson's own Section 5 example,
  not invented afterward -- it was kept in and built into Sections 5-8
  and 15 rather than quietly patched, because it's a real, concrete
  demonstration of exactly the gap this chapter teaches: task success
  and trajectory correctness can both report a pass while the
  underlying content is wrong.
- Ollama's cold-load warm-up took 348.7 seconds this session (disclosed
  exactly, via the real `total_duration`/`load_duration` fields),
  comfortably inside the 450s budget but far from instant; once warm,
  subsequent calls ranged 0.56s-14.04s. Disclosed honestly either way,
  per this course's policy, with no claim that either number
  generalizes.
- Every deterministic Python snippet in the lesson (all tool functions,
  both metric functions, the harness, pass@k, the drift demo, cost-
  per-success, the full eval report, and the eval-maturity checklist)
  was actually run in a scratch directory before being transcribed into
  `lesson.html`; every printed number in the lesson was cross-checked
  against a single combined script that reproduces every section's
  output in one pass (see "Code tested before writing" below).
- Lesson density: 61 lines match `grep -c '<pre\|<code' lesson.html`
  (above the 60+ requirement, comparable to Chapter 6's own 62), 121
  total tag occurrences via `grep -o '<pre\|<code' | wc -l` (Chapter
  6: 127).
- This chapter's boundary against `llm-evaluation-for-everyone` is
  enforced by name throughout, not just in one disclaimer section:
  Section 1 states the boundary explicitly, and Sections 4, 8, and 15
  each return to the SAME concrete example (the $12M/$9.4M bug) to show
  exactly where this chapter's process metrics stop and that course's
  output-correctness methodology (LLM-as-judge, Chapters 5-6 there)
  would need to take over.
- The chapter mini-project (`project/`) is a real, standalone,
  gradable scaffold -- not a signpost -- matching the brief's
  instruction that Chapter 7 returns to a full `project/` build, unlike
  Chapters 5-6. Its scenario (Emberlyn Underwriting's TriageScout) is
  fresh, and its three TODOs (`task_success`, `trajectory_correctness`,
  `run_harness`) mirror the lesson's own three pillars.
- Module 1-3's combined assessments (a pre-existing gap flagged by
  every prior session since Module 1 completed, and never actually
  built) were built this session rather than deferred a fourth time.
  Each one reuses the EXACT, already-tested functions from that
  module's own two chapters, loaded via `importlib` directly from
  their real `project/solution.py` files -- not reimplemented or
  paraphrased -- applied to a small combined scenario, following
  `ai-engineering-for-everyone`'s own `module-4-cost-latency-
  reliability-engineering-exercise` format (confirmed by reading that
  file directly this session, not assumed from memory).

**What's a known limitation, disclosed rather than hidden:**
- **The bulk N-run harness (Sections 9-14) is a seeded deterministic
  simulation, not live model calls.** This is disclosed explicitly and
  repeatedly in the lesson (Section 10 names the calibration source:
  the live 1/6 result from Section 2), in `PROJECT_STATE.md`'s own
  brief (which explicitly permitted this), and here. Running 100 live
  calls per task across 5 tasks would have exceeded this course's
  per-call and per-session time budgets by a wide margin given this
  session's own 348.7s cold-load result. The simulation's 0.17
  step-error rate is calibrated from the real 1-in-6 live miss rate,
  not an invented number -- but it is still a simulation, and Chapter
  7's own interview questions (Q9) explicitly test whether a reader
  understands that distinction rather than treating it as equivalent
  to live measurement.
- Exercises/practice scoring for free-text-style answers still relies
  on exact-string or keyword matching rather than fully semantic
  grading -- the same necessary, disclosed limitation as every prior
  chapter's own exercise harness.
- The Module 1-3 assessments' Part-3 synthesis questions are graded by
  a basic substance check (length + one required keyword), the same
  necessarily-incomplete automated check the sibling course's own
  combined assessment uses for its open-ended justification field --
  real grading still requires the self-graded `RUBRIC.md` step.
- No module-level assessment exists yet for Module 4 -- see "Module
  1-3 assessment decision" below for why that's a deliberate choice,
  not an oversight.

## Module 1-3 assessment decision

`assessments/module-assessments/` was empty across the entire repo
before this session, despite Modules 1-3 all being complete for
several sessions -- a gap every prior chapter session flagged and
deferred again. This session made the decision explicitly rather than
repeating the deferral: **(a) build Modules 1-3's assessments now**,
since the format is clear (confirmed by reading `ai-engineering-for-
everyone`'s own `module-4-cost-latency-reliability-engineering-
exercise/` directly this session: README + RUBRIC + starter + solution,
reusing each covered chapter's own already-tested decision functions
applied to one small combined scenario, not a full second project) and
all three modules are already fully built and stable. **Module 4's own
assessment is explicitly NOT built this session** -- per the curriculum
map, it's a combined "reliability-plan + cost-control exercise"
spanning Chapters 7 AND 8, and Chapter 8 (cost/latency control) doesn't
exist yet. Building it now would mean either a Chapter-7-only stub that
would need rework once Chapter 8 ships, or guessing at Chapter 8's own
cost-control functions before they exist -- both worse than building it
for real, once, at Chapter 8's own session, following the exact
precedent `ai-engineering-for-everyone`'s combined assessment set (built
at its module's CLOSING chapter, not its opening one). This is now
scheduled concretely in `PROJECT_STATE.md`'s rewritten "Next Recommended
Task" for Chapter 8.

Each of the three built assessments:
- **Module 1** (`module-1-agent-loop-tracing-and-planning-exercise`) --
  reuses Chapter 1's `run_agent`/`FakeModel` and Chapter 2's
  `decide_next_delay_check`/`classify_task_planning_mode`, loaded
  directly from their real `project/solution.py` files via
  `importlib`. 4/4 self-check parts pass on `solution.py`; 0/4 on
  `starter.py`, no crash.
- **Module 2** (`module-2-tool-interface-and-memory-architecture-
  exercise`) -- reuses Chapter 3's `diagnose_appliance_issue` and
  Chapter 4's `MemoryStore`/`build_working_context`/`run_visit_
  session`. 5/5 on `solution.py`; 0/5 on `starter.py`, no crash; the
  scratch memory file it creates during grading is confirmed cleaned
  up after each run.
- **Module 3** (`module-3-reliability-and-safety-design-review`) --
  reuses `guardrail_check_booking()` and `reflect_on_response()`,
  BOTH of which live inside Chapter 4's own project file (Chapters 5
  and 6 extended that file in place rather than shipping their own
  project directories, per the L2 project's own design) -- confirmed
  by reading that file directly rather than assuming its contents.
  3/3 on `solution.py`; 0/3 on `starter.py`, no crash.

No existing site-wiring convention for module assessments was found to
extend: neither this repo's own root `index.html`/`docs/curriculum/
index.html` nor `ai-engineering-for-everyone`'s equivalent pages link
to their module-assessment directories anywhere. Nothing was invented
to fill that gap this session -- the three new directories are
reachable by path, matching the sibling course's own precedent, and
this is noted here rather than silently assumed away.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-06-audit.md` (22
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group,
Millbrook Credit Union, Amberlock Self-Storage, Cascadia Home
Security).

**4 new fictional orgs used this chapter, all checked clean against the
full running list and against each other:**

- **Greywick Dispatch** (lesson hook; product: FactScout)
- **Larkmoor Archive Service** (exercises; product: RecordScout)
- **Thornmere Public Transit** (exercises `ai-paired.html`; product:
  TransitScout)
- **Emberlyn Underwriting** (project; product: TriageScout)

**"ClaimBot"'s insurance-adjustment employer** (practice
`ai-paired.html`) is left unnamed/generic on purpose, the same
convention Chapter 6's EscrowBot/title-company scenario (and Chapter
5's RenewBot, Chapter 4's MemoBot, Chapter 3's HandoffBot, Chapter 2's
EscalationBot, Chapter 1's ConciergeBot) used -- a small,
two-or-three-fact scenario doesn't need an invented company name.

Every distinctive root word above (Greywick, Larkmoor, Thornmere,
Emberlyn) was checked for zero overlap against both this chapter's own
four named scenarios and the full 22-org Chapter 1-6 list -- including
a specific check that "Thornmere" shares no root word with "Thornbury
Insurance Group," and that "Larkmoor" shares no root word with
"Larkspur Fitness Studio." The running exclusion list for future
chapters is now: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski
Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty
Group, Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group,
Millbrook Credit Union, Amberlock Self-Storage, Cascadia Home Security,
Greywick Dispatch, Larkmoor Archive Service, Thornmere Public Transit,
Emberlyn Underwriting. Future chapters should extend this list, not
restart it.

## Source verification, done honestly

This chapter names `llm-evaluation-for-everyone` specifically (its
chapter list and curriculum map, not just its title) in Section 1 and
Section 15. Before citing it, this session read that course's own
`docs/curriculum/CURRICULUM_MAP.md` directly this session and confirmed:
Chapter 3 ("Designing Golden Sets and Eval Datasets"), Chapter 4 ("Human
Evaluation and Inter-Annotator Agreement"), Chapters 5-6 ("Designing and
Validating an LLM Judge" / "Judge Bias and Failure Modes"), Chapters 7-8
("Sample Size, Variance, and Confidence Intervals" / "Significance
Testing for Model and Prompt Comparison"), and Chapter 11 ("Evaluating
Agents and Tool Use") all exist exactly where the lesson claims them to
be -- no chapter number or title was guessed or assumed from memory.
That course's own Module 4 purpose line ("evaluate agent/tool-use task
completion and trajectories") was also read directly and confirmed to
describe the output-measurement side this chapter's own Section 1
explicitly distinguishes itself from.

## Ollama check, done fresh this session

The model was explicitly warmed before any lesson code was written,
using this course's documented recovery command. The warm-up call
itself took its full cold-load time -- the first attempt (a 120s-
foreground `curl`) actually timed out at the harness's own 450s
ceiling and had to be retried once as a background task, which then
completed successfully:

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"say ok","stream":false,"keep_alive":"180m"}'
{"model":"llama3.2", ..., "response":"Ok. Is there something I can help you with?",
 "done":true,"done_reason":"stop",
 "total_duration":348660530214,   # ~348.7s
 "load_duration":345489398301,    # ~345.5s of that was loading
 "eval_duration":1051733999}      # ~1.05s of actual generation
```

Unlike Chapter 6's session (1.3s-15.8s throughout), this session's cold
load took the bulk of its budget (348.7s) before the model was usable
at all -- disclosed honestly, with no claim that either session's
timing generalizes. Once warm, calls were fast (0.56s-14.04s), including
the six-run non-determinism test that became Section 2's central
result.

## Code tested before writing

Every Python snippet this session wrote was actually run, in a scratch
directory, before its content (or its verified output) was transcribed
into `lesson.html`:

```
$ python3 harness.py               -> initial harness prototype: task
                                       success vs. trajectory correctness
                                       rates per task, pass@k, drift,
                                       cost-per-success all verified
$ python3 tools.py                 -> FactScout's 5 tools verified
                                       against hand-picked cases;
                                       cross_check_claim's $12M/$9.4M
                                       bug DISCOVERED here, kept in
$ (live) check_warm.py             -> REAL Ollama call, 14.04s, "OK"
$ (live) live_nondeterminism_test.py -> REAL Ollama call x6, 0.56s-5.09s,
                                       captured verbatim (1/6 matched
                                       the expected first step)
$ python3 full_lesson_check.py     -> every Sections 4-16 snippet run
                                       in one combined script; every
                                       printed value cross-checked
                                       against lesson.html verbatim
                                       (one rounding correction made:
                                       the Section 13 cost-sum total)
```

Then, in the actual chapter directory, after every file was written:

```
$ python3 exercises/solution.py    -> Score: 19/19
$ python3 exercises/starter.py     -> Score: 0/19, no crash
$ python3 practice/solution.py     -> TOTAL: 8/8
$ python3 practice/starter.py      -> TOTAL: 0/8, no crash
$ python3 project/solution.py      -> 8/8 checks passed
$ python3 project/starter.py       -> 2/8 checks passed, no crash
$ python3 chapters/chapter-04-memory-and-state/project/solution.py
                                    -> 10/10 checks passed (L2 regression
                                       check, unchanged from Chapter 6)
```

And for the three new module assessments:

```
$ python3 assessments/module-assessments/module-1-.../solution.py  -> 4/4
$ python3 assessments/module-assessments/module-1-.../starter.py   -> 0/4, no crash
$ python3 assessments/module-assessments/module-2-.../solution.py  -> 5/5
$ python3 assessments/module-assessments/module-2-.../starter.py   -> 0/5, no crash
$ python3 assessments/module-assessments/module-3-.../solution.py  -> 3/3
$ python3 assessments/module-assessments/module-3-.../starter.py   -> 0/3, no crash
```

No stray JSON files or `__pycache__` directories were left behind in
any chapter or assessment directory by any of these runs (each script
either avoids disk I/O entirely or cleans up its own scratch fixtures
on exit; `__pycache__` directories were removed explicitly before the
final commit).

## Local check

`scripts/local_check.sh < /dev/null` was run for the whole repo after
all Chapter 7 files, the module assessments, and the site-wiring
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

Note: `local_check.sh`'s own glob (`chapters/*/exercises|project|
practice/solution.py`) does not cover `assessments/module-assessments/
*/solution.py` -- those three were verified manually above instead,
since they fall outside this script's existing scope; not a gap this
session introduced.
