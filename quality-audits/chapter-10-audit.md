# Chapter 10 Quality Audit: Multi-Agent Coordination and Communication

Session date: 2026-10-04. This session built Chapter 10 in full, cold,
from `PROJECT_STATE.md`'s "Next Recommended Task" brief: `lesson.html`,
`quiz.html`, `interview-questions.html` + `.md`, the full `exercises/`
and `practice/` sets, a chapter mini-project `project/` (README + RUBRIC
+ index.html + ai-paired.html + starter.py + solution.py, matching
Chapters 7-9's own pattern, NOT the L3 Independent project), this audit,
wiring `assets/chapters-data.js` and `docs/curriculum/index.html`,
updating root `index.html`'s hero stats and intro paragraph, and
rewriting `PROJECT_STATE.md`'s "Next Recommended Task" for Chapter 11.

## Honest self-critique

**What's strong:**
- **A genuine, unscripted duplicated-work result became the chapter's
  central worked example.** Two peer agents (DockScout and YardScout),
  each asked only to claim a shipment for itself with no knowledge of
  the other's decision, BOTH independently claimed `S-104` in the same
  test run (Sections 5, 6, 8). Neither agent did anything wrong on its
  own; the failure is architectural. This was not manufactured.
- **A genuine malformed message, same run.** YardScout's call emitted
  JSON keys padded with whitespace (`" recipient "`, `"shipment_id "`)
  and a mismatched message type (`"query"` for a claim) -- Section 6.
  Section 7's `parse_message_safely` was built and tested against this
  EXACT real output.
- **A genuine live consensus/self-resolution.** DockScout, told that
  YardScout had also claimed `S-104`, voluntarily sent a `reject` for its
  own claim (Section 10) -- and in that same real output, a
  `"note":"null"` string-literal defect, disclosed rather than cleaned up.
- **An honest non-reproduction of deadlock.** The live deadlock attempt
  (Section 12) did NOT reproduce: both agents broke their own "never go
  first" policy and sent a query anyway. This is disclosed directly in
  the lesson, not hidden, and Section 13 constructs deadlock
  deterministically per this course's own reliability policy.
- Every deterministic Python snippet in the lesson was actually run,
  including the new ones added after the first draft (verified by
  `scratchpad/ch10/verify_lesson.py`, whose printed outputs match the
  lesson's own captured output blocks line for line).
- Lesson density: **61** matches via `grep -c '<pre\|<code' lesson.html`
  (above the 60+ requirement, matching the same range as Chapters 1-9).
- This chapter explicitly hands off from, rather than re-teaches,
  Chapter 9's dispatch machinery, and extends TWO prior mechanisms by
  name: Chapter 9's `which_agent_responsible` becomes
  `which_agent_caused_miscommunication` (Section 15, dispatch-level to
  message-level), and Chapter 9's blackboard lock becomes a locked
  check-and-claim (Section 9).

**What's a known limitation, disclosed rather than hidden:**
- **The live results are non-deterministic and were NOT re-run to
  "get a clean result."** The duplicated claim (Sections 5-6, 8), the
  malformed YardScout message (Section 6), the reject resolution
  (Section 10), and the non-reproducing deadlock attempt (Section 12)
  are each a single-shot capture from this session. Re-running any of
  them could plausibly produce a different outcome.
- **The sanity check's 314.35s cold-load time** (Section 2) is far
  outside the fast warm calls the earlier chapters saw. Two concurrent
  background warm-up requests appear to have raced and left the model
  unloaded. Disclosed in the lesson's Section 2 text.
- **Deadlock, miscommunication-by-validation, consensus, and the
  shared claim-check are deterministic Python.** The "both agents
  waiting" deadlock, the lock-based claim-check, and the tie-breaking
  rule are constructed inputs to deterministic logic, not emergent
  live-model behavior. This mirrors Chapter 9's own disclosure.
- **Only two peer agents were exercised.** The architect-level question
  (Interview Q10) names a five-agent system but does not build one.
- The practice-bank and exercises' concept-naming answers still rely on
  keyword matching rather than fully semantic grading -- the same
  necessarily-incomplete, disclosed limitation as every prior chapter.

## L3 Independent project and Module 5 assessment -- both still deferred, restated explicitly

Per `PROJECT_STATE.md`'s own Chapter 10 hand-off (written at Chapter 9's
session) and this course's standing discipline of never letting a
deferred decision silently disappear:

- **The L3 Independent project** ("design and implement a
  reliability-instrumented, cost-bounded agent for a given problem, no
  scaffold," per the curriculum map's project ladder) was deferred past
  Chapter 8, past Chapter 9, and has **still not been built** as of this
  chapter. This chapter's own `project/` directory is a chapter
  mini-project (Ravenshollow Talent Agency), matching Chapters 7-9's own
  pattern, explicitly NOT the L3 project. This flag is restated, a
  FOURTH consecutive time, in `PROJECT_STATE.md`'s Chapter 11 hand-off.
- **Module 5's own assessment** ("multi-agent coordination-pattern
  exercise," spanning Chapters 9-11) was NOT built this session. It needs
  Chapter 9's coordination-pattern code, Chapter 10's communication code,
  AND Chapter 11's production-operating code all to exist first,
  following the exact precedent Module 4's own assessment set (built at
  Chapter 8, its closing chapter). **It is scheduled for Chapter 11's own
  session** (Chapter 11 is Module 5's closing chapter, per
  `docs/curriculum/CURRICULUM_MAP.md`'s module architecture: "Chapters:
  9, 10, 11"). Module 5 stays **"In Progress"**, not "Complete," after
  this chapter.

## Fictional-org exclusion check

Extending, not restarting, the list from `chapter-09-audit.md` (35 orgs).

**Five new fictional orgs used this chapter, all checked clean against
the full running list and against each other:**

- **Harrowgate Logistics Exchange** (lesson; peer agents DockScout and
  YardScout)
- **Bellcrest Freelance Guild** (exercises; peer agents DesignScout and
  DevScout)
- **Oakmere Produce Collective** (exercises `ai-paired.html`; peer
  agents FarmScout and MarketScout)
- **Ravenshollow Talent Agency** (project; peer agents CastingScout and
  BookingScout)
- **Pemberwick Salvage Co.** (project `ai-paired.html`; peer agents
  WreckScout and PartsScout)

**"NegotiatorBot"'s employer** (practice `ai-paired.html`) is left
unnamed/generic on purpose, the same convention every prior chapter's
own unnamed-org scenario used.

Every distinctive root word above (Harrowgate, Bellcrest, Oakmere,
Ravenshollow, Pemberwick) was checked for zero overlap against the
chapter's own scenarios and the full 35-org Chapter 1-9 list. The running
exclusion list for future chapters is now:
Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol, Wavecrest
Marina, Alderleaf Research Group, Pinehurst Realty Group, Thistlewood
Veterinary Group, Cobblestone Courier Co., Palisade Broadband, Thornbury
Insurance Group, Wrenhollow Auto Rentals, Kestrel Appliance Service,
Larkspur Fitness Studio, Driftwood Legal Clinic, Saltmarsh Language
Academy, Hollowridge Wellness Clinic, Briarcliff Bike Rentals, Fenwick
Home Repair Co-op, Mossgate Dental Group, Millbrook Credit Union,
Amberlock Self-Storage, Cascadia Home Security, Greywick Dispatch,
Larkmoor Archive Service, Thornmere Public Transit, Emberlyn
Underwriting, Brambleford Analytics, Caldwell Ridge Observatory, Portage
Grain Cooperative, Marrowvale Textile Mill, Quillmark Journeys, Hadleigh
Civic Records Bureau, Corvindale Claims Network, Ashgrove Municipal
Services, Foxglenn Relief Network, Harrowgate Logistics Exchange,
Bellcrest Freelance Guild, Oakmere Produce Collective, Ravenshollow
Talent Agency, Pemberwick Salvage Co. Future chapters should extend this
list, not restart it.

## Ollama check

```
$ curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'
(warm-up; completed in the background, concurrent with other requests)

$ python3 sanity.py
elapsed: 314.35
How can I assist you today?
```

Every subsequent live call this session completed well within the
450-second budget, and none required idle-waiting past it.

## Live calls, as captured

```
$ python3 live_p2p.py
[dockscout]  95.24s -> send_message {"recipient":"YardScout","note":" claim morning produce shipment","shipment_id":"S-104","type":"claim"}
[yardscout]  19.36s -> send_message {" recipient ":"DockScout","note":"Claiming highest priority shift for me","shipment_id ":"S-104","type":"query"}
[dockscout]  29.02s -> send_message {"shipment_id":"S-104","type":"reject","recipient":"YardScout","note":"null"}

$ python3 live_deadlock.py
[dockscout]  28.65s -> send_message {"recipient":"YardScout","type":"query","shipment_id":"S-104"}
[yardscout]  33.2s  -> send_message {"note":"Awaiting proposal for shipment assignment","recipient":"DockScout","shipment_id":"S-104","type":"query"}
RESULT: did not reproduce a clean live deadlock this run
```

## Code tested before writing

```
$ python3 scratchpad/ch10/test_lesson.py    -> all deterministic snippets ran
$ python3 scratchpad/ch10/verify_lesson.py  -> ALL VERIFIED (outputs match lesson blocks)
$ python3 exercises/solution.py   -> Score: 19/19
$ python3 exercises/starter.py    -> Score: 0/19, no crash
$ python3 practice/solution.py    -> TOTAL: 8/8
$ python3 practice/starter.py     -> TOTAL: 0/8, no crash
$ python3 project/solution.py     -> 9/9 checks passed
$ python3 project/starter.py      -> 2/9 checks passed, no crash
$ python3 chapters/chapter-04-memory-and-state/project/solution.py -> 10/10 (L2 regression)
$ python3 chapters/chapter-07-evaluating-agent-reliability/project/solution.py -> 8/8 (Ch7 regression)
$ python3 chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py -> 9/9 (Ch8 regression)
$ python3 chapters/chapter-09-multi-agent-orchestration-patterns/project/solution.py -> 9/9 (Ch9 regression)
```

## Local check

`scripts/local_check.sh < /dev/null` was run for the whole repo after all
Chapter 10 files and the site-wiring updates were in place; see the
commit for the full output.
