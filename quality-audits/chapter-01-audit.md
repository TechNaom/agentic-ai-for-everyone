# Chapter 1 Quality Audit: The Agent Loop: Building Your First Autonomous Agent

Session date: 2026-09-24. This is the first quality audit in this repo
(brand-new course, first build session), so it establishes the running
fictional-org exclusion list rather than extending one.

## Honest self-critique

**What's strong:**
- The hook (Northbeam Outdoors/TrailBot) sets up a real architectural
  failure — a single LLM call that correctly refuses to hallucinate a
  trail status, but is useless anyway because it has no way to look
  anything up — and the whole chapter is the fix: building a real
  action/observation loop, not a bigger prompt.
- Every code block that claims real output was actually run this
  session against `llama3.2:latest` over local Ollama (Sections 2, 5,
  6, 8, 9, 10) or as deterministic Python (Sections 3, 4, 7, 9's fix,
  10's guard, 11's timeout demo) — see "Code tested before writing"
  below for the full list.
- Section 8-9's wrong-argument bug (the model appending "trail" to
  "Cedar Hollow," causing both tool lookups to fail) is a **genuine,
  unscripted failure** discovered while testing this chapter's own
  code, not a manufactured teaching example — and the chapter shows
  the honest diagnosis and fix rather than quietly rewriting the
  scenario to avoid it.
- The chapter discloses this sandbox's real Ollama timing honestly:
  Section 2's first call took 138 seconds, matching (at a smaller
  scale) the 432-second hang this course's own build process
  encountered and disclosed in `PROJECT_STATE.md`. Section 11 turns
  that real observation into a tested, working timeout-guard pattern
  rather than glossing over it.
- Positioning against all four highest-risk neighbors
  (`ai-coding-agents-for-everyone`, `mcp-for-everyone`,
  `ai-engineering-for-everyone`, `llm-evaluation-for-everyone`) plus
  `context-engineering-for-everyone` is stated explicitly by name in
  `docs/discovery-notes.md`, with each neighbor's own curriculum map
  (and, for the two highest-risk, actual chapter content) read this
  session rather than assumed from the course title.
- All three `solution.py` files (exercises, practice, project) were
  run this session and score a perfect total; all three corresponding
  `starter.py` files were also run and confirmed to fail cleanly (not
  crash) with the TODOs unfilled.
- Lesson density: 61 `<pre>`/`<code>` blocks in `lesson.html`,
  comfortably above the 60-block hard requirement and the
  `python-for-everyone` Chapter 1/2 reference range (56/62).

**Honest gaps:**
- This chapter's project, like every sibling course's own Chapter 1
  project, is graded by a structural self-check (4 checks against a
  deterministic `FakeModel`), not by running a live model and grading
  its actual behavior — disclosed explicitly in `project/README.md`
  rather than implied to be more rigorous than it is. A learner who
  wants the live experience is given the exact swap-in pattern, but it
  is optional and not part of the graded self-check.
- Only `llama3.2:latest` (the one model available in this sandbox) was
  tested throughout. Tool-calling behavior, argument formatting
  (including the Section 9 bug), and timing are all specific to this
  model; the chapter does not claim these exact numbers or failure
  modes generalize to every model, only reports what was actually
  observed.
- The lesson's "go-deeper" timeout section names 450 seconds as this
  course's own build budget, explicitly flagged as specific to this
  sandbox's quirks rather than a general production recommendation —
  worth double-checking this framing still reads clearly once later
  chapters (8, specifically) build out latency control in full.
- Exercises/practice/project scoring is substance-checked for
  free-text answers (keyword matching) rather than fully semantic —
  the same necessary, disclosed limitation as every sibling course's
  exercise harness.

## Fictional-org exclusion check

This is the first chapter built in this repo, so this list starts
fresh here. Checked this session for internal collisions across this
chapter's own four scenarios (lesson, exercises, practice, project) —
no cross-repo exclusion list existed to check against yet, since this
is the ecosystem's newest course; future chapters and future sibling
courses should treat the list below as the starting exclusion set.

**5 fictional orgs used this session (all checked clean against each
other):**

- **Northbeam Outdoors** (lesson hook; product: TrailBot)
- **Summit Gear Co-op** (exercises; product: GearBot)
- **Fernbrook Ski Patrol** (exercises ai-paired.html; product: LiftBot)
- **ConciergeBot's apartment complex** (practice ai-paired.html, org
  left unnamed/generic on purpose — a single-tool scenario didn't need
  an invented company name)
- **Wavecrest Marina** (project; product: SlipBot)

Every distinctive root word above (Northbeam, Summit Gear, Fernbrook,
Wavecrest) was checked for zero overlap against the other four this
session. Future chapters in this repo should extend this list, not
restart it.

## Source verification, done honestly

This chapter is a from-scratch code walkthrough, not a claims-and-
citations chapter — it cites no external papers or docs requiring
WebFetch verification. Its one factual claim about this sandbox's own
prior behavior (the 432-second Ollama hang) is sourced from this
course's own `PROJECT_STATE.md`/task brief, not an external source, and
is reported as this session's own environment finding, not attributed
to a third party.

## Ollama check, done fresh this session

`curl http://localhost:11434/api/tags` responded normally and confirmed
two installed models (`llama3.2:latest`, `nomic-embed-text:latest`) —
the exact output shown in `lesson.html` Section 2's sanity-check block.
The first real `chat.completions.create` call (Section 2's bare call)
did not return within a 2-minute foreground timeout and was killed;
re-run with a 400-second budget, it completed in 138 seconds and
returned the real, unedited output shown in the lesson. All five
subsequent live tool-calling calls (Sections 5, 6, 8, 9's fix)
completed within 30-90 seconds each. This chapter's load-bearing live-
model dependency (the tool-calling decisions and the Cedar Hollow bug
discovery) is real, captured output, not illustrative.

## Code tested before writing

Every script version referenced in `lesson.html` was run for real in
the build scratchpad before being copied into the lesson:

```
$ python3 bare_call.py            -> real output, 138s (Section 2)
$ python3 tools.py                -> real output (Section 3)
$ python3 schema_preview.py       -> real output (Section 4)
$ python3 first_tool_call.py      -> real tool_calls response (Section 5)
$ python3 execute_and_observe.py  -> real final answer (Section 6)
$ python3 run_agent.py            -> real BUGGY output, discovered live (Section 8)
$ python3 (fixed tools.py + run)  -> real FIXED output (Section 9)
$ python3 guard_demo.py           -> real deterministic guard output (Section 10)
$ python3 timeout_wrapper.py      -> real deterministic timeout output (Section 11)
$ python3 exercises/solution.py   -> TOTAL: 17/17
$ python3 practice/solution.py    -> TOTAL: 8/8
$ python3 project/solution.py     -> 4/4 checks passed
```

The corresponding `starter.py` files in exercises/practice/project were
also run and confirmed to fail cleanly (low/zero score, or failed
structural checks) with no crash, confirming the scoring harness
actually discriminates between filled-in and empty answers.
