# Chapter 3 Quality Audit: Tool Use and Function Calling

Session date: 2026-09-28. This session built Chapter 3 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, the entire `project/` folder, this audit, wiring
`assets/chapters-data.js` and `docs/curriculum/index.html`, updating
root `index.html`'s hero stats, and rewriting `PROJECT_STATE.md`'s
"Next Recommended Task" for Chapter 4.

## Honest self-critique

**What's strong:**
- The lesson goes deep on exactly what Chapter 2's own closing
  paragraph flagged as Chapter 3's job: wrong-tool-choice among
  genuinely overlapping candidates (Section 3's real, demonstrated
  `naive_first_match` failure), argument-formatting drift beyond one
  normalize pattern (Section 5's two distinct normalizers for two
  distinct drift shapes), and three differentiated tool-failure types
  with three differentiated retry policies (Sections 8-11), summarized
  in one explicit table that states the chapter's central claim
  plainly.
- Every single code example in the lesson was actually run before
  being written into `lesson.html` — see "Code tested before writing"
  below for the full list of scratch files executed.
- A real bug was caught and fixed during testing, not manufactured:
  the first draft of the unified dispatcher's timeout-retry branch
  (Section 12) passed the same `_simulate_hang: True` flag to every
  retry attempt, so it never actually recovered — the fix (only force
  the hang on the first attempt) is the same "an unscripted failure
  surfaced by testing became the lesson's own honest example" pattern
  Chapter 1's Cedar Hollow bug and Chapter 2's free-text planning
  failure both used.
- Lesson density: 70 lines match `<pre\|<code` via
  `grep -c '<pre\|<code' lesson.html` (comfortably above the 60+
  requirement, and above both Chapter 1's 61 and Chapter 2's 63), or
  130 total tag occurrences via `grep -oE '<pre|<code' | wc -l`.
- This session verified every `solution.py` across `exercises/`,
  `practice/`, and `project/` scores a perfect total, and every
  corresponding `starter.py` fails cleanly (low score, no crash) with
  its `TODO`s unfilled — all six files actually executed this session,
  not assumed.
- The new `project/` folder is explicitly labeled a **chapter
  mini-project**, not one of this course's numbered L1-L4 projects —
  `docs/curriculum/CURRICULUM_MAP.md`'s project ladder places the next
  numbered slot (L2 Assisted) after Chapter 4, confirmed by reading the
  map before building, the same precedent Chapter 2 set.

**Honest gaps:**
- **No live Ollama call succeeded this session, despite two genuine
  attempts, each budgeted to this course's documented 450-second
  ceiling.** A plain "Say OK" sanity check and a real tool-selection
  call (with `tools=TOOLS` against the ambiguous "my internet is down"
  prompt) were both launched in the background and both were killed by
  a 440-second `timeout` wrapper with no output at all (exit code
  124) — worse than Chapter 1's disclosed 138-second hang or the prior
  session's disclosed 432-second hang, past even this course's own
  ceiling. This is disclosed in `lesson.html` Section 2 itself, not
  hidden or papered over with a fabricated transcript. Every lesson
  example instead runs against real, executed Python — deterministic
  logic that mirrors the failure modes a live model would plausibly
  exhibit (Section 3's naive keyword-matching failure stands in for
  what a real model matching tool descriptions on surface wording
  would do), the same disclosed-and-deterministic approach Chapter 1's
  guard demo and Chapter 2's `decide_next_step` already used for
  reproducibility, applied here for availability.
- Because no live call succeeded, this chapter cannot honestly claim a
  captured example of a real model choosing between NetBot's three
  overlapping tools, or a real model's own argument-formatting quirks
  on this chapter's specific tools. The mechanism for grounding tool
  choice in the real API (`tools=TOOLS`) is described and pointed to
  Chapter 2 Section 4's own working live transcript of the same
  `client.chat.completions.create(..., tools=TOOLS)` pattern, rather
  than re-claiming a transcript this session doesn't have.
- Only `llama3.2:latest` was ever targeted (the one model available in
  this sandbox), consistent with Chapters 1-2 — no claim is made that
  any described model behavior generalizes beyond what was actually,
  deterministically demonstrated.
- Exercises/practice/project scoring for free-text-style answers still
  relies on exact-string or keyword matching rather than fully semantic
  grading — the same necessary, disclosed limitation as every prior
  chapter's own exercise harness.
- The project's grading (7 structural self-checks against deterministic
  fixtures, no live model call) is a design choice for gradability, the
  same disclosed approach Chapter 1's `FakeModel` and Chapter 2's
  project both used, not a claim that it exercises a live model's
  actual non-determinism. `project/README.md` gives the live-Ollama
  swap pattern explicitly.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-02-audit.md` (8
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co.).

**4 new fictional orgs used in this chapter, all checked clean against
the full running list and against each other:**

- **Palisade Broadband** (lesson hook; product: NetBot)
- **Thornbury Insurance Group** (exercises; product: ClaimBot)
- **Wrenhollow Auto Rentals** (exercises `ai-paired.html`; product:
  FleetBot)
- **Kestrel Appliance Service** (project; product: RepairBot)

**HandoffBot's logistics service** (practice `ai-paired.html`) is left
unnamed/generic on purpose, the same convention Chapter 1's
`ConciergeBot` and Chapter 2's `EscalationBot` scenarios both used — a
small, two-or-three-tool scenario doesn't need an invented company
name.

Every distinctive root word above (Palisade, Thornbury, Wrenhollow,
Kestrel) was checked for zero overlap against both this chapter's own
four named scenarios and the full 8-org Chapter 1-2 list (Northbeam,
Summit Gear, Fernbrook, Wavecrest, Alderleaf, Pinehurst, Thistlewood,
Cobblestone). The running exclusion list for future chapters is now:
Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol, Wavecrest
Marina, Alderleaf Research Group, Pinehurst Realty Group, Thistlewood
Veterinary Group, Cobblestone Courier Co., Palisade Broadband,
Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel Appliance
Service. Future chapters should extend this list, not restart it.

## Source verification, done honestly

Like Chapters 1-2, this is a from-scratch code walkthrough, not a
claims-and-citations chapter — no external papers or docs required
WebFetch verification. The one environment claim carried forward and
extended (the sandbox's documented intermittent Ollama hang) is
sourced from this course's own `PROJECT_STATE.md`, Chapter 1's audit
(138s), and the Chapter 2 session's own disclosed prior-sibling data
point (432s) — this session adds its own new data point (two separate
440-second-budgeted calls, both non-returning) to that same disclosed
history, not a new external source.

## Ollama check, done fresh this session

Two live calls were genuinely attempted this session, each under a
`timeout 440` wrapper (this course's documented ~450s reliability
ceiling, rounded down slightly for the wrapper's own overhead):

```
$ timeout 440 python3 check_ollama.py   # plain "Say OK" sanity check
[exit code 124 -- no output before the timeout elapsed]

$ timeout 440 python3 live_call1.py     # tool-selection call with tools=TOOLS
[exit code 124 -- no output before the timeout elapsed]
```

Neither call returned. Per this course's own reliability policy
(budget up to 450s, never idle-wait past it, disclose rather than
fabricate), this session did not retry indefinitely and did not invent
a transcript. This is disclosed in `lesson.html` Section 2 directly, in
addition to here.

## Code tested before writing

Every Python file this session wrote was actually run, in a scratch
directory, before its content was transcribed into `lesson.html`:

```
$ python3 tools.py            -> all 5 tool functions verified against real fixtures
$ python3 schemas.py          -> TOOLS list constructed, length and names verified
$ python3 normalize.py        -> normalize_account_id and normalize_zip verified
                                   against 5 and 4 real input variants respectively
$ python3 failures.py         -> call_with_timeout (hang + normal case) and
                                   call_with_malformed_check (malformed + clean case)
                                   both verified
$ python3 retry_policy.py     -> all three failure-type policies (timeout-retry,
                                   malformed-no-retry, outcome-verify) verified
$ python3 selection.py        -> naive_first_match and diagnose_connectivity_issue
                                   (all 3 branches) verified
$ python3 more_demos.py       -> naive-normalize failure, ZIP+4/int normalize,
                                   3x-identical-malformed-retry proof, and the
                                   unified dispatcher (all 3 policies) verified --
                                   this file's first version had the retry-timeout
                                   bug described above, caught and fixed before
                                   being written into the lesson
$ python3 netbot_agent.py     -> the finished agent, all 3 end-to-end cases verified
```

Then, in the actual chapter directory, after every file was written:

```
$ python3 exercises/solution.py   -> TOTAL: 16/16
$ python3 exercises/starter.py    -> TOTAL: 3/16, no crash
$ python3 practice/solution.py    -> TOTAL: 8/8
$ python3 practice/starter.py     -> TOTAL: 0/8, no crash
$ python3 project/solution.py     -> 7/7 checks passed
$ python3 project/starter.py      -> 2/7 checks passed, no crash
```

## Local check

`scripts/local_check.sh` was run for the whole repo after all Chapter
3 files were in place — see `PROJECT_STATE.md`'s Session 3 entry for
the result captured this session.
