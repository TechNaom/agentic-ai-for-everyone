# Chapter 11 Quality Audit: Operating Agents in Production

Session date: 2026-10-04. This session built Chapter 11 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.md` + `.html` (HTML generated from the
`.md` by a one-off script, matching Chapter 10's own precedent), the full
`exercises/` and `practice/` sets, a chapter mini-project `project/`
(README + RUBRIC + index.html + ai-paired.html + starter.py + solution.py,
matching Chapters 7-10's own pattern, NOT the L3 Independent project),
**Module 5's own combined assessment** (built this session, as scheduled),
this audit, wiring `assets/chapters-data.js` and
`docs/curriculum/index.html`, updating root `index.html`'s hero stats and
intro paragraph, and rewriting `PROJECT_STATE.md`'s "Next Recommended
Task" for Chapter 12.

## Honest self-critique

**What's strong:**
- **A genuine, unscripted argument-drift result became the chapter's
  central worked example.** The SAME retried request ("confirm shipment
  S-104 is claimed by you") produced two different real argument shapes
  across two live calls -- attempt 1 included an extra `"vehicle":"None"`
  key attempt 2 did not (Section 4). This was not manufactured, and it is
  the concrete, demonstrated reason this chapter's idempotency key is
  built from (agent, shipment_id, action) rather than raw argument
  equality (Section 5).
- **A genuine live timeout result, not an abstract claim.** A client
  configured with `timeout=0.5` seconds raised `APITimeoutError` at 3.07
  seconds, not 0.5 (Section 7) -- disclosed honestly as a real gap
  between a configured budget and the actual clock, not smoothed over.
- Every deterministic Python snippet in the lesson was actually run in
  `scratchpad/ch11/ops.py` and ad hoc scripts before being written into
  `lesson.html`.
- Lesson density: **60** matches via `grep -c '<pre\|<code' lesson.html`
  (meets the 60+ requirement; at the lower end of Chapters 1-10's own
  range, deliberately verified rather than padded).
- This chapter explicitly reuses six functions by name, unchanged, from
  Chapters 9-10's own `project/solution.py` files (`which_agent_responsible`,
  `is_within_budget` from Ch9; `coordinated_claim`, `parse_message_safely`,
  `break_deadlock_if_needed` from Ch10) and defines
  `which_agent_caused_miscommunication` consistently with Chapter 10's own
  lesson-text definition (that exact function existed only in Chapter 10's
  `lesson.html` prose, not yet in any `.py` file -- this chapter is the
  first to actually implement it as runnable code, in its own
  `project/solution.py`, matching the lesson's described behavior
  exactly).
- **Module 5's own assessment was built this session, as explicitly
  scheduled** (not deferred a third time): `assessments/module-
  assessments/module-5-multi-agent-coordination-and-operations-exercise/`,
  reusing Chapter 9's, Chapter 10's, AND Chapter 11's own tested
  `project/solution.py` functions via `importlib`, the same precedent
  Module 4 set at Chapter 8. `solution.py` passes 4/4 objectively-
  checkable parts; `starter.py` runs cleanly and fails all 4 with no
  crash.

**What's a known limitation, disclosed rather than hidden:**
- **The live results are non-deterministic and were NOT re-run to "get a
  clean result."** The argument-drift capture (Section 4) and the
  timeout-firing capture (Section 7) are each single-shot from this
  session. Re-running either could plausibly produce a different exact
  number (a different extra field, a different firing time), though the
  qualitative lesson -- drift happens, a timeout isn't exact -- is the
  point, not the specific values.
- **Retries, idempotency, logging, and the run summary are deterministic
  Python**, not emergent live-model behavior. The live calls this session
  made were used to MOTIVATE these mechanisms (Sections 4 and 7), not to
  demonstrate the mechanisms themselves running against a live model.
  This mirrors every prior chapter's own disclosure pattern for its
  deterministic core mechanics.
- **Only one correlation id / one run was exercised per example.** The
  lesson does not show multiple overlapping runs sharing a log file, which
  a real production system would need to handle (log rotation,
  concurrent runs writing to the same file) -- out of scope here per this
  chapter's own deferral to `ai-engineering-for-everyone`.
- The practice-bank and exercises' concept-naming answers still rely on
  keyword matching rather than fully semantic grading -- the same
  necessarily-incomplete, disclosed limitation as every prior chapter.

## L3 Independent project -- DEFERRED A FIFTH TIME (loud, explicit)

Per `PROJECT_STATE.md`'s own Chapter 11 hand-off (written at Chapter 10's
session), this chapter's production-operating material was explicitly
named as a natural fit for the L3 Independent project's "reliability-
instrumented, cost-bounded agent for a given problem, no scaffold"
definition, but building it was NOT mandated -- the brief left it to this
session's own judgment.

**Decision made this session: the L3 Independent project was NOT built.**
This is now deferred a FIFTH consecutive time (past Chapters 8, 9, 10, and
now 11). The reasoning: this session's scope already carried two
mandatory, non-negotiable deliverables for Chapter 11 (the chapter itself,
to the full file-set standard, and Module 5's own combined assessment,
explicitly scheduled and carried forward twice already). Building a
genuinely independent, no-scaffold L3 project to the standard the
curriculum map sets ("design and implement," not "extend a given
scaffold") inside the same session risked either shipping it shallow (a
disguised fourth mini-project rather than a real no-scaffold capstone) or
compromising the quality of the mandatory deliverables above to make room
for it. Shipping Chapter 11 and the Module 5 assessment correctly, and
deferring L3 explicitly rather than shipping it half-built, was judged the
better use of this session's scope.

This is **flagged loudly, for a sixth consecutive hand-off**, in
`PROJECT_STATE.md`'s Chapter 12 brief. Module 5 is now closed (Chapter 11
live, its own assessment built) with the project ladder still owing the
repo its L3 slot -- this should not be allowed to drift further without a
dedicated session, separate from any future chapter's own build, if it is
not folded into Chapter 12 or 13's own work.

## Module 5's own assessment -- BUILT THIS SESSION, as scheduled

Per Chapter 8's gap-audit decision, carried forward unchanged by Chapters
9 and 10: Module 5's assessment ("multi-agent coordination-pattern
exercise," spanning Chapters 9-11) was explicitly scheduled for Chapter
11's own session, Module 5's closing chapter. **It was built this
session, on schedule, NOT deferred a third time.** See
`assessments/module-assessments/module-5-multi-agent-coordination-and-
operations-exercise/` (README, RUBRIC, starter, solution). It reuses
Chapter 9's `route_subtask`/`which_agent_responsible`, Chapter 10's
`parse_message_safely`/`coordinated_claim`, and Chapter 11's
`idempotency_key`/`commit_once`/`call_with_retries`, all loaded via
`importlib`, unchanged, exactly matching Module 4's own precedent at
Chapter 8. `solution.py` passes 4/4 objectively-checkable parts;
`starter.py` fails cleanly, 0/4, with no crash. Module 5's feature card in
`docs/curriculum/index.html` now reads **"Complete."**

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-10-audit.md` (40 orgs).

**Four new fictional orgs used this chapter, all checked clean against
the full running list and against each other:**

- **Cindermoor Parcel Network** (exercises; peer agents SortScout and
  RouteScout)
- **Thistlebrook Fulfillment Co-op** (exercises `ai-paired.html`; peer
  agents PickScout and PackScout)
- **Wrenfield Dispatch Alliance** (project; peer agents ClaimScout and
  ShipScout)
- **Hollowgate Courier Network** (project `ai-paired.html`; peer agents
  PickupScout and DropoffScout)

**"NotaryBot"'s employer** (practice `ai-paired.html`) is left
unnamed/generic on purpose, the same convention every prior chapter's own
unnamed-org scenario used. The lesson itself reuses **Harrowgate Logistics
Exchange** (DockScout/YardScout), Chapter 10's own scenario, per the
brief's explicit permission -- the same precedent Chapter 8 set reusing
Chapter 7's FactScout.

Every distinctive root word above (Cindermoor, Thistlebrook, Wrenfield,
Hollowgate) was checked for zero overlap against the chapter's own
scenarios and the full 40-org Chapter 1-10 list. The running exclusion
list for future chapters is now:
Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol, Wavecrest
Marina, Alderleaf Research Group, Pinehurst Realty Group, Thistlewood
Veterinary Group, Cobblestone Courier Co., Palisade Broadband, Thornbury
Insurance Group, Wrenhollow Auto Rentals, Kestrel Appliance Service,
Larkspur Fitness Studio, Driftwood Legal Clinic, Saltmarsh Language
Academy, Hollowridge Wellness Clinic, Briarcliff Bike Rentals, Fenwick
Home Repair Co-op, Mossgate Dental Group, Millbrook Credit Union,
Amberlock Self-Storage, Cascadia Home Security, Greywick Dispatch,
Larkmoor Archive Service, Thornmere Public Transit, Emberlyn Underwriting,
Brambleford Analytics, Caldwell Ridge Observatory, Portage Grain
Cooperative, Marrowvale Textile Mill, Quillmark Journeys, Hadleigh Civic
Records Bureau, Corvindale Claims Network, Ashgrove Municipal Services,
Foxglenn Relief Network, Harrowgate Logistics Exchange, Bellcrest
Freelance Guild, Oakmere Produce Collective, Ravenshollow Talent Agency,
Pemberwick Salvage Co., Cindermoor Parcel Network, Thistlebrook
Fulfillment Co-op, Wrenfield Dispatch Alliance, Hollowgate Courier
Network. Future chapters should extend this list, not restart it.

## Ollama check

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
(single warm-up request, run alone, NOT concurrent with any other request
-- the exact discipline Chapter 10's own disclosed 314s race motivated)

$ time curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"Say OK.","keep_alive":"120m"}'
real    0m11.123s
response: "What's on your mind? Need help with something or just want to chat?"
```

Every subsequent live call this session completed well within the
450-second budget. No call stalled or required a fallback to simulated
output -- unlike Chapter 3's and Chapter 10's own disclosed hangs, this
session's Ollama behaved reliably throughout, disclosed honestly either
way per this course's policy (no claim that this generalizes).

## Live calls, as captured

```
$ python3 scratchpad/ch11/live_retry.py
[attempt-1]                                  14.32s -> {"agent":"DockScout","shipment_id":"S-104","vehicle":"None"}
[attempt-2 (simulated retry of same key)]     3.02s -> {"agent":"DockScout","shipment_id":"S-104"}

$ python3 -c "... timeout=0.5 client test ..."
elapsed=3.07s  APITimeoutError: Request timed out.
```

## Code tested before writing

```
$ python3 scratchpad/ch11/ops.py          -> ALL OK (all deterministic mechanisms smoke-tested)
$ python3 exercises/solution.py           -> Score: 19/19
$ python3 exercises/starter.py            -> Score: 0/19, no crash
$ python3 practice/solution.py            -> TOTAL: 8/8
$ python3 practice/starter.py             -> TOTAL: 0/8, no crash
$ python3 project/solution.py             -> 9/9 checks passed
$ python3 project/starter.py              -> 3/9 checks passed, no crash
$ python3 assessments/module-assessments/module-5-.../solution.py -> 4/4
$ python3 assessments/module-assessments/module-5-.../starter.py  -> 0/4, no crash
$ python3 chapters/chapter-04-memory-and-state/project/solution.py -> 10/10 (L2 regression)
$ python3 chapters/chapter-07-evaluating-agent-reliability/project/solution.py -> 8/8 (Ch7 regression)
$ python3 chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py -> 9/9 (Ch8 regression)
$ python3 chapters/chapter-09-multi-agent-orchestration-patterns/project/solution.py -> 9/9 (Ch9 regression)
$ python3 chapters/chapter-10-multi-agent-coordination-and-communication/project/solution.py -> 9/9 (Ch10 regression)
$ python3 assessments/module-assessments/module-1-.../solution.py -> 4/4 (Module 1 regression)
$ python3 assessments/module-assessments/module-2-.../solution.py -> 5/5 (Module 2 regression)
$ python3 assessments/module-assessments/module-3-.../solution.py -> 3/3 (Module 3 regression)
$ python3 assessments/module-assessments/module-4-.../solution.py -> 3/3 (Module 4 regression)
```

## Local check

`scripts/local_check.sh < /dev/null` was run ALONE, with no other repo
command running concurrently, for the whole repo after all Chapter 11
files, the Module 5 assessment, and the site-wiring updates were in
place. All six checks passed clean: required folders, no placeholder
text, Python syntax, every `exercises/project/practice` `solution.py` run,
JS syntax + chapter-path validation, and no likely secrets found.
