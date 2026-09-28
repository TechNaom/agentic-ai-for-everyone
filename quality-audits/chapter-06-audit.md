# Chapter 6 Quality Audit: Guardrails and Safety for Autonomous Agents

Session date: 2026-09-28. This session built Chapter 6 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, a signpost `project/` (README + index.html, per
the brief's instruction that the L2 project itself is extended in
place inside `chapters/chapter-04-memory-and-state/project/`, not
re-created here), the real third extension of Chapter 4's L2 project
(`guardrail_check_booking()` added, wired before `schedule_followup()`
dispatch, plus a new TODO 5 in `starter.py`), this audit, wiring
`assets/chapters-data.js` and `docs/curriculum/index.html`, updating
root `index.html`'s hero stats, and rewriting `PROJECT_STATE.md`'s
"Next Recommended Task" for Chapter 7.

## Honest self-critique

**What's strong:**
- **Two genuine, unscripted live-model results became this chapter's
  central worked examples**, neither manufactured: a real
  prompt-injection attempt via a transaction memo (a tool result, not
  a system prompt), tried twice against `llama3.2:latest` with two
  different system-prompt framings. Run 1 (a neutral "review this
  memo" framing): the model correctly identified the injected
  instruction as suspicious and took no action. Run 2 (a more
  "compliant, automate this" framing): the same model complied --
  but notably never emitted an actual `transfer_funds` tool call,
  only narrated in plain text that a transfer had occurred. This
  second result is arguably the chapter's most important finding: it
  demonstrates a subtler failure mode (false narrated compliance, no
  real action) distinct from "the model calls the dangerous tool,"
  and is the concrete, demonstrated reason a hard, code-level guardrail
  at the dispatch boundary is necessary, not optional -- a system that
  only checked whether a `transfer_funds` call appeared in the trace
  would have correctly shown nothing happened, but a system that
  trusted the model's own narration as a record of what occurred would
  have been fooled.
- Ollama was fast throughout this session (1.3s-15.8s per call), unlike
  Chapter 5's disclosed 413.8s stall -- disclosed honestly either way,
  per this course's policy, with no claim that this generalizes.
- Every deterministic Python snippet in the lesson (the guardrail
  dispatcher, all five guardrail mechanisms, the fail-safe wrapper, the
  composed session) was actually run in a scratch directory before
  being transcribed into `lesson.html`, including the naive-baseline
  demonstration (an unguarded `transfer_funds` call actually moving
  $600) and the full adversarial session (five guardrails, five real
  refusals, one real success).
- Lesson density: 62 lines match `<pre\|<code` via
  `grep -c '<pre\|<code' lesson.html` (above the 60+ requirement,
  matching Chapters 4-5's own 62 exactly), 129 total tag occurrences
  via `grep -oE '<pre|<code' | wc -l`.
- This session verified every `solution.py` across `exercises/` and
  `practice/` scores a perfect total, and every corresponding
  `starter.py` fails cleanly (low score, no crash) with its `TODO`s
  unfilled. The Chapter 4 L2 project's `solution.py` (now with the real
  guardrail) scores 10/10, and its `starter.py` (now with a new TODO 5)
  scores 2/10 with no crash -- both actually executed this session.
- **This chapter's own L2 project extension is real, not cosmetic.**
  `chapters/chapter-04-memory-and-state/project/solution.py`'s
  `run_visit_session()` now calls `guardrail_check_booking()`
  immediately before `schedule_followup()` is dispatched, and two new
  self-checks prove it: one confirms `schedule_followup` never appears
  in `tool_trace` for a blocking-condition visit with
  `human_approved=False`, the other confirms it does appear with
  `human_approved=True`. TODOs 1-4 and Chapters 4-5's original 8
  self-checks were read first and confirmed unchanged before any edit
  was made, per the brief's explicit instruction.
- **A genuine, disclosed design tension was found and resolved
  explicitly, not smoothed over:** the brief requires both (a) the
  guardrail stop an unsafe booking from proceeding automatically, and
  (b) the existing 8 self-checks (including one that requires
  `schedule_followup` to have fired for its own blocking-condition test
  case) pass unchanged. These two requirements are only simultaneously
  satisfiable if `human_approved` defaults to `True` (preserving
  existing call sites' behavior) with the guardrail's real enforcement
  exercised via new calls that pass `human_approved=False` explicitly.
  This trade-off, and the honest note that a production default should
  be `False`, is stated plainly in `project/README.md`'s own dedicated
  section, in `RUBRIC.md`, in this chapter's own `lesson.html` Section
  17, and here -- not left implicit.
- The brief's defense-in-depth decision point (keep or remove Chapter
  5's reflection now that a guardrail exists) was decided explicitly
  (kept, as a defense-in-depth backstop) and justified in
  `project/README.md`, matching the brief's own stated preference.

**Honest gaps:**
- Only `llama3.2:latest` was targeted, consistent with Chapters 1-5 --
  no claim is made that either injection-test result (resisted, or
  narrated false compliance) generalizes to any other model or even to
  a re-run of the exact same prompts against the same model.
- The "sandboxed tool execution" guardrail in this chapter is an
  allowlist/denylist over command-shape strings, not a real OS-level
  sandbox (containers, seccomp, network namespaces) -- explicitly
  scoped this way in the lesson's own Section 7 "what is... sandboxing
  honestly scoped to this course?" box, matching the brief's own
  explicit instruction that full container orchestration is out of
  scope for this no-framework, plain-Python course.
- The `human_approved=True` default (see above) is a real, disclosed
  compromise driven by the need to keep Chapters 4-5's regression tests
  passing unchanged -- a fresh implementation with no such constraint
  would default to `False`. This is stated at least three times across
  `project/README.md`, `RUBRIC.md`, and `lesson.html` so no reader
  encounters it as a surprise.
- Exercises/practice scoring for free-text-style answers still relies
  on exact-string or keyword matching rather than fully semantic
  grading -- the same necessary, disclosed limitation as every prior
  chapter's own exercise harness.
- Chapter 6's `project/` directory is intentionally a signpost, not a
  working scaffold -- this is a deliberate reading of the brief's
  "extend in place, don't recreate" instruction, not an oversight; the
  actual gradable project files remain solely in
  `chapters/chapter-04-memory-and-state/project/`.
- No module-level assessment file exists yet for Module 3 (or for
  Modules 1-2, which are also already complete) in
  `assessments/module-assessments/` -- that directory is empty across
  the whole repo. This is consistent with every prior module's own
  status, not a new gap this chapter introduced, and is flagged
  explicitly in `PROJECT_STATE.md`'s rewritten "Next Recommended Task"
  for a future session to pick up or consciously defer again.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-05-audit.md` (19
orgs: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group).

**3 new fictional orgs used this chapter, all checked clean against the
full running list and against each other:**

- **Millbrook Credit Union** (lesson hook; product: LedgerBot)
- **Amberlock Self-Storage** (exercises; product: DispatchBot)
- **Cascadia Home Security** (exercises `ai-paired.html`; product:
  GuardBot)

**"EscrowBot"'s title company** (practice `ai-paired.html`) is left
unnamed/generic on purpose, the same convention Chapter 5's RenewBot
scenario (and Chapter 4's MemoBot, Chapter 3's HandoffBot, Chapter 2's
EscalationBot, Chapter 1's ConciergeBot) used -- a small,
two-or-three-fact scenario doesn't need an invented company name.

**Hollowridge Wellness Clinic** (CareBot) is reused deliberately, not a
new org -- it's the L2 project's own canonical scenario, extended in
place per the brief, not a fresh chapter scenario.

Every distinctive root word above (Millbrook, Amberlock, Cascadia) was
checked for zero overlap against both this chapter's own three named
scenarios and the full 19-org Chapter 1-5 list -- including a specific
check that "Amberlock" and "Thornbury" (both self-storage/insurance-
adjacent) share no root word, and that "Cascadia" shares no root word
with any existing entry. The running exclusion list for future chapters
is now: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals, Kestrel
Appliance Service, Larkspur Fitness Studio, Driftwood Legal Clinic,
Saltmarsh Language Academy, Hollowridge Wellness Clinic, Briarcliff
Bike Rentals, Fenwick Home Repair Co-op, Mossgate Dental Group,
Millbrook Credit Union, Amberlock Self-Storage, Cascadia Home Security.
Future chapters should extend this list, not restart it.

## Source verification, done honestly

Like Chapters 1-5, this is a from-scratch code walkthrough, not a
claims-and-citations chapter -- no external papers or docs required
WebFetch verification. No external source claims are made this
chapter; every factual claim about model behavior is backed by a real,
captured transcript from this session's own local Ollama calls.

## Ollama check, done fresh this session

The model was explicitly pre-warmed before any lesson code was
written, using this course's documented recovery command:

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
{"model":"llama3.2","created_at":"2026-09-28T13:32:38.930417594Z","response":"","done":true,"done_reason":"load"}

$ python3 check_ollama.py   # plain "Say OK" sanity check
elapsed: 1.30
OK
```

Unlike Chapter 5's session (413.8s on the first substantive call), this
session's documented sandbox hang **did not recur** -- every live call
completed in under 16 seconds:

```
injection_live.py  (neutral framing)    call 1: 15.79s   call 2: 13.80s
injection_live2.py (compliant framing)  call 1: 11.02s   call 2: 9.60s
```

No claim is made that this generalizes -- this course's policy (budget
up to 450 seconds, never idle-wait past that, disclose honestly either
way) is what governed this session, and it happened to be a fast run.

## Code tested before writing

Every Python snippet this session wrote was actually run, in a scratch
directory, before its content (or its verified output) was transcribed
into `lesson.html`:

```
$ python3 ledgerbot_core.py        -> all four tools verified against
                                       hand-picked cases
$ python3 naive_baseline.py        -> REAL naive dispatch, $600 external
                                       transfer succeeded with zero checks
$ python3 guardrails.py            -> all five guardrail mechanisms
                                       (allowlist, approval, sandbox,
                                       budget, rate limit) verified
$ python3 test_pieces.py           -> each guardrail piece re-verified
                                       in isolation against edge cases
$ python3 injection_live.py        -> REAL Ollama call x2, 15.8s/13.8s,
                                       captured verbatim (model resisted)
$ python3 injection_live2.py       -> REAL Ollama call x2, 11.0s/9.6s,
                                       captured verbatim (model complied,
                                       narrated only, no real tool call)
$ python3 full_session.py          -> the guardrail correctly refusing
                                       the injected transfer's exact
                                       arguments, scripted deterministically
$ python3 failsafe.py              -> fail-safe default-deny paths verified
$ python3 ledgerbot_session.py     -> the finished, composed dispatcher
                                       run against a 6-call adversarial
                                       session, all 6 outcomes verified
$ python3 carebot_ext.py           -> the CareBot guardrail extension
                                       prototyped and verified (held,
                                       approved, and no-condition cases)
```

Then, in the actual chapter directory, after every file was written:

```
$ python3 exercises/solution.py    -> TOTAL: 19/19
$ python3 exercises/starter.py     -> TOTAL: 5/19, no crash
$ python3 practice/solution.py     -> TOTAL: 8/8
$ python3 practice/starter.py      -> TOTAL: 0/8, no crash
$ python3 chapters/chapter-04-memory-and-state/project/solution.py
                                    -> 10/10 checks passed (was 8/8 before
                                       this chapter's TODO 5 addition)
$ python3 chapters/chapter-04-memory-and-state/project/starter.py
                                    -> 2/10 checks passed, no crash
```

No stray JSON files were left behind in any chapter directory by any of
the `exercises/`, `practice/`, or `project/` runs (each script cleans
up its own test fixtures on exit).

## Local check

`scripts/local_check.sh` was run for the whole repo after all Chapter
6 files were in place and the L2 project extension was committed to
disk -- see `PROJECT_STATE.md`'s Session 6 entry for the result
captured this session.
