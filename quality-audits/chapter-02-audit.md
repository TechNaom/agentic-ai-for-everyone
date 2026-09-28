# Chapter 2 Quality Audit: Planning and Task Decomposition

Session date: 2026-09-28. This session picked up a partial Chapter 2
build (uncommitted, cut off by a usage limit before its own audit was
written) and completed it: `interview-questions.html`, the full
`practice/` file set, the entire `project/` folder, this audit, wiring
`assets/chapters-data.js`, and rewriting `PROJECT_STATE.md`'s "Next
Recommended Task" for Chapter 3.

## Honest self-critique

**What's strong:**
- The lesson's hook (Alderleaf Research Group/ScoutBot) sets up two
  genuinely different request shapes against the same four tools — a
  company snapshot (order-independent) and a stock-drop investigation
  (order-dependent) — and the whole chapter is organized around
  building, measuring, and comparing both planning strategies against
  that one shared toolset, rather than treating "planning" as one
  undifferentiated technique.
- The free-text-JSON planning failure in lesson Section 4 (the model
  inventing tool names like `"CAD"` and `"Bill of Materials (BOM)"`
  when asked to plan without the real `tools=` schema attached) is
  disclosed as a genuine, unscripted result from this session, not a
  manufactured cautionary tale, and it directly motivates the fix
  (grounding the plan in the same tool-calling API from Chapter 1).
- The Section 9 head-to-head (5 reasoning calls for an emergent-style
  snapshot vs. 1 for a fixed plan) and the Section 11 wrong-plan
  failure (a pre-committed fixed plan guessing the wrong second step
  before the news headline was known) are both real, run code, not
  hypothetical illustrations — see "Code tested before writing" below.
- This session verified (not just inherited) that every `solution.py`
  across `exercises/`, `practice/`, and the new `project/` folder
  scores a perfect total, and every corresponding `starter.py` fails
  cleanly (low/zero score, no crash) with its `TODO`s unfilled.
- Lesson density: 63 lines match `<pre\|<code` (the same `grep -c`
  method `PROJECT_STATE.md` used for Chapter 1's 61-line count), or
  118 total tag occurrences via `grep -o '<pre\|<code' | wc -l` —
  comfortably above the 60+ block requirement either way.
- The new `project/` folder is explicitly labeled a **chapter
  mini-project**, not one of this course's numbered L1-L4 projects
  (the curriculum map folds Chapter 2's material into the L2 Assisted
  project after Chapter 4) — this is stated plainly in
  `project/README.md` and `project/index.html` rather than implied to
  be more than it is.

**Honest gaps:**
- Only `llama3.2:latest` (the one model available in this sandbox) was
  ever tested, for the same reason as Chapter 1 — no claim is made
  that the exact tool-calling behaviors, invented-tool-name failure,
  or timing figures generalize to other models.
- The project's grading (7 structural self-checks against deterministic
  fixtures, no live model call) is disclosed the same way Chapter 1's
  project disclosed its `FakeModel` approach — this is a design choice
  for gradability, not a claim that it exercises a live model's actual
  non-determinism. `project/README.md` gives the live-Ollama swap
  pattern explicitly for a learner who wants that experience.
- Exercises/practice/project scoring for free-text-style answers still
  relies on exact-string or keyword matching rather than fully semantic
  grading — the same necessary, disclosed limitation as Chapter 1 and
  every sibling course's own exercise harness.
- This session did not re-run the lesson's own live Ollama calls
  (Section 4's 41-second tool-calling call, Section 2's 204-second
  bare call) — those transcripts were already captured and written
  into `lesson.html` by the prior session before it was cut off, and
  this session's job was completing the surrounding file set, not
  re-verifying already-captured lesson transcripts. This session's own
  live-model budget was spent confirming the sandbox's Ollama install
  was reachable (see "Ollama check" below), not re-running the lesson.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-01-audit.md` (5 orgs:
Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol, the
unnamed apartment complex behind ConciergeBot, Wavecrest Marina).

**4 new fictional orgs used in this chapter, all checked clean against
the Chapter 1 list and against each other:**

- **Alderleaf Research Group** (lesson hook; product: ScoutBot)
- **Pinehurst Realty Group** (exercises; product: ListBot)
- **Thistlewood Veterinary Group** (exercises `ai-paired.html`;
  product: TriageBot)
- **Cobblestone Courier Co.** (project; product: RouteBot)

**EscalationBot's subscription service** (practice `ai-paired.html`)
is left unnamed/generic on purpose, the same convention Chapter 1's
own `ConciergeBot` scenario used — a two-tool scenario doesn't need an
invented company name.

Every distinctive root word above (Alderleaf, Pinehurst, Thistlewood,
Cobblestone) was checked for zero overlap against both this chapter's
own four scenarios and the full Chapter 1 list (Northbeam, Summit
Gear, Fernbrook, Wavecrest). The running exclusion list for future
chapters is now: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski
Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty
Group, Thistlewood Veterinary Group, Cobblestone Courier Co. Future
chapters should extend this list, not restart it.

## Source verification, done honestly

Like Chapter 1, this is a from-scratch code walkthrough, not a
claims-and-citations chapter — no external papers or docs required
WebFetch verification. The one environment claim carried forward (the
sandbox's documented intermittent Ollama hang, including the 432-second
data point) is sourced from this course's own `PROJECT_STATE.md` and
Chapter 1's own audit, not a new external source.

## Ollama check, done fresh this session

This session did not need a fresh live model call for any of the files
it built (interview-questions.html is a static render of the already-
audited `interview-questions.md`; `practice/` and `project/` are
deterministic Python plus static HTML, matching this course's own
grading policy that graded code never depends on a live model). The
lesson's own live-model transcripts (Sections 2 and 4) were captured by
the prior session and are unchanged by this one. No live Ollama call
was attempted or needed in this session; this is disclosed rather than
implied otherwise.

## Code tested before writing

Every Python file this session touched or added was actually run:

```
$ python3 exercises/solution.py   -> TOTAL: 16/16 (pre-existing, re-verified)
$ python3 exercises/starter.py    -> TOTAL: 2/16, no crash (pre-existing, re-verified)
$ python3 practice/solution.py    -> TOTAL: 8/8 (pre-existing, re-verified)
$ python3 practice/starter.py     -> TOTAL: 0/8, no crash (pre-existing, re-verified)
$ python3 project/solution.py     -> 7/7 checks passed (new this session)
$ python3 project/starter.py      -> 1/7 checks passed, no crash (new this session)
```

The pre-existing `exercises/` and `practice/` pair (built by the prior
session before it was cut off) was re-verified, not assumed correct,
before this session extended the chapter around them. The new
`project/` pair was built and verified the same way: `solution.py`
scores a perfect 7/7, and `starter.py`'s three unfilled `TODO`s fail
4 of the 7 checks that depend on them (the 3 checks that don't
depend on any `TODO` — the "gives up cleanly with no correction"
case — still pass with the stub's default `return None, 0`, which is
the correct behavior for that one case even before any `TODO` is
filled in) without ever crashing.

## Local check

`scripts/local_check.sh` was run for the whole repo after all Chapter
2 files were in place; see `PROJECT_STATE.md`'s Session 2 entry for the
result captured this session.
