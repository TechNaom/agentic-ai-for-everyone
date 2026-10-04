# Chapter 13 Quality Audit: Capstone — Designing and Defending an Autonomous Agent System

Session date: 2026-10-04. This is the FINAL chapter of the 13-chapter,
6-module course. Built cold from `PROJECT_STATE.md`'s "Next Recommended
Task: Chapter 13" brief. Nothing from prior chapters was rebuilt;
Chapter 12's own framework functions were imported, not redefined.

## Honest self-critique

**What's strong:**
- **Genuinely multi-component, not a bigger single-agent problem.**
  Thornwick Marketplace Collective's characterization fires BOTH of
  Chapter 9's and Chapter 10's own multi-agent tests (distinct
  independently-runnable subtasks AND concurrent actors racing on the
  same shared inventory ledger), and all eight Chapter 1-11
  mechanisms come out load-bearing simultaneously. No prior chapter's
  own worked example did either of these at once.
- **Framework imported, never redefined.** `project/solution.py` loads
  Chapter 12's own `project/solution.py` via `importlib`, the same
  pattern `module-6-architecture-design-exercise/solution.py` already
  proved, rather than copying its five functions a third time.
- **Every mechanism proven with executed code, not just named.** The
  claim-check is actually raced (two concurrent claims on one unit,
  exactly one wins), the memory store is actually re-instantiated in
  a separate session, the refund guardrail is actually tested
  fail-closed, the commit is actually retried and replayed, and the
  reflection check is actually fed a fact-complete and a fact-free
  explanation.
- **Real harness numbers, checked against the stated budget.** The
  three task types measure 1.00 success rate and average costs of
  $0.0304, $0.0500, and $0.0609, all under the stated $0.08 ceiling.

**What's weak, stated plainly:**
- **`grounded_reflect` is a substring check.** It verifies that the
  required fact NAMES appear in the text, not that they're used
  correctly. A model could satisfy it without grounding anything. The
  lesson states this as a deliberate limitation (see the interview
  question on it), not a hidden one, but it is genuinely a weaker
  check than a production verifier would be.
- **The harness is deterministic and synthetic.** Its success
  rates are 1.00 because the simulated tasks are constructed to pass
  when the mechanisms work. A harness that could fail in
  interesting ways (e.g., a race that sometimes lets both claims
  through, a fact that sometimes doesn't persist) would be a stronger
  proof. This matches Chapter 12's own L3 harness convention and is
  disclosed, not hidden.
- **`characterize_problem` reports only the first branch that fires.**
  For Thornwick it reports the subtask-independence reason, not the
  concurrent-actors reason, even though both hold. The lesson
  (Section 6) and the rubric (Criterion 1) both handle this explicitly
  rather than trusting the function's output alone.
- **The smell check has no rule for an UNNECESSARY operating layer or
  peer-communication layer.** It only flags missing mechanisms (under-
  engineering) and a few over-engineering cases (multi-agent without
  distinct subtasks, reflection without a hard-to-verify output).
  Chapter 12's own smell rules were not extended here, to keep this
  chapter's reuse clean. The exercises' subset variant works around
  this by demonstrating a dropped memory mechanism instead.

## Ollama decision

**No live model call. Decided explicitly, not defaulted.** Reasoning:
this capstone's own skill is architecture judgment and proof-of-design
against a written problem statement, the same property Chapter 12's
own L3 project (Driftlight) had -- and Driftlight also implemented
real memory, guardrail, and idempotency code with zero live calls.
A live call would illustrate nothing the deterministic harness doesn't
already prove, and would make grading depend on a running Ollama server
for no benefit. The lesson's Section 2 states this and the contrast
case (a capstone that DOES need a live model's own behavior).

No warm-up, no sanity check, no live request was made this session.

## Scenario and exclusion list

**One new fictional organization** this chapter, per
`PROJECT_STATE.md`'s instruction to pick a fresh org and reference prior
chapters' scenarios by name without excluding them:

- **Thornwick Marketplace Collective** (lesson, project, rubric,
  exercises' subset variant). A fictional artisan marketplace with a
  conversational Buyer Concierge, an overnight Maker Fulfillment batch,
  and a Fraud & Dispute Review process sharing one inventory ledger.

Prior chapters' scenarios (Copperfield, Harrowgate, Driftlight,
Mirelake, Alderwood, Lantern Hill, Vantage Peak, Wrenfield, CareBot,
LedgerBot, DockScout/YardScout) are referenced BY NAME as worked
comparisons or cross-check cases, and do not count as new exclusions.

Practice bank uses abstract system names (RouteDesk, ClaimGate,
StockMesh, ReviewSpan, NightLedger, FactField, GateCheck, SpanCapstone)
per Chapter 12's own practice-bank convention. `ai-paired.html` pages
use unnamed/generic second marketplace and employer references, not
new full orgs, so no further exclusions were needed.

The running exclusion list for future work (extended from
`chapter-12-audit.md`'s 50-org list, now 51 orgs):

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
Network, Copperfield Municipal Utilities, Lantern Hill Senior Living,
Vantage Peak Ski Resorts, Driftlight Energy Cooperative, Mirelake Water
Authority, Alderwood Transit Cooperative, **Thornwick Marketplace
Collective**. Future chapters should extend this list, not restart it.

Note: this course is now complete. The exclusion list is kept for any
future course or addendum built in this ecosystem.

## Lesson density

`chapters/chapter-13-.../lesson.html`: `grep -c '<pre\|<code'` = **60**
(exactly the course minimum), `grep -oE '<pre|<code' ... | wc -l` = 121.

**Why the density pattern is adapted, not copied, from Chapter 12's
`lesson.html`:** Chapter 12's own shape (a decision framework applied to
a sequence of single-agent worked examples) produced many small
characterization/budget snippets. Chapter 13's shape is one large,
multi-component system walked through in build order (import ->
characterize -> select -> budget -> trade-off -> smell -> ADR ->
implement each mechanism -> instrument -> self-check -> cross-check).
Density is still held at 60+ `<pre>`/`<code>` blocks, but each block
is a real build step rather than a standalone calculation.

## Capstone shape, and what changed vs. the standard chapter file set

**This chapter has no separate lesson-vs-project split** (per L4's own
definition in `CURRICULUM_MAP.md`). The file set is:

- `lesson.html` -- the walkthrough, same filename as every prior
  chapter so `assets/chapters-data.js`'s `path` stays consistent.
- `project/solution.py` + `project/README.md` -- the actual L4
  deliverable (reference implementation + problem statement).
- `project/index.html` + `project/ai-paired.html` -- the browsable and
  AI-paired pages, matching prior chapters' shape.
- **No `project/starter.py` and no `project/RUBRIC.md`.** Following
  L3's own "no scaffold" precedent, L4 is "business/system problem
  only." The grading rubric instead lives in
  `assessments/architecture-challenges/RUBRIC.md`, the directory the
  curriculum map explicitly reserves for this capstone, NOT inside the
  chapter's own `project/` directory.
- `quiz.html`, `interview-questions.html` + `.md`,
  `exercises/{README.md,index.html,starter.py,solution.py,ai-paired.html}`,
  `practice/{README.md,index.html,starter.py,solution.py,ai-paired.html}`
  -- the standard per-chapter file set, adapted to Thornwick's own
  scenario (exercises use a two-component SUBSET of Thornwick; practice
  uses abstract system names).

## Module 6 completion

`docs/curriculum/CURRICULUM_MAP.md`'s Module 6 assessment reads
"architecture-design exercise (Ch. 12) + capstone rubric (Ch. 13,
architecture challenge, Level 4)" -- both now shipped:

- Architecture-design exercise: `assessments/module-assessments/module-6-architecture-design-exercise/` (shipped Chapter 12, 6/6).
- Capstone rubric: `assessments/architecture-challenges/RUBRIC.md` (shipped Chapter 13, grades `chapters/chapter-13-.../project/solution.py`).

Module 6 is therefore **Complete**, which closes the course.

## Code tested before writing

```
$ python3 chapters/chapter-13-.../project/solution.py      -> Score: 14/14 (L4 capstone)
$ python3 chapters/chapter-13-.../exercises/solution.py    -> Score: 17/17
$ python3 chapters/chapter-13-.../exercises/starter.py     -> Score: 0/17, no crash
$ python3 chapters/chapter-13-.../practice/solution.py     -> TOTAL: 8/8
$ python3 chapters/chapter-13-.../practice/starter.py      -> TOTAL: 0/8, no crash
$ python3 /tmp/.../lesson_demo.py                          -> every lesson output block captured from real execution
$ python3 /tmp/.../cross_check.py                          -> Copperfield 3/8, Harrowgate 3/8, Thornwick 8/8, all flags=0
```

Capstone rubric grading (`assessments/architecture-challenges/RUBRIC.md`,
5 criteria x 5 points = 25 points, passing bar 20/25 with zero criteria at 0):
applied by self-grading `project/solution.py` against the rubric's own
criteria. Reference implementation: Criterion 1 = 5, Criterion 2 = 5,
Criterion 3 = 5, Criterion 4 = 5, Criterion 5 = 5 = **25/25**.

## Regression check (all unchanged, re-run this session)

```
$ python3 chapters/chapter-04-memory-and-state/project/solution.py -> 10/10 (L2 regression)
$ python3 chapters/chapter-07-evaluating-agent-reliability/project/solution.py -> 8/8
$ python3 chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py -> 9/9
$ python3 chapters/chapter-09-multi-agent-orchestration-patterns/project/solution.py -> 9/9
$ python3 chapters/chapter-10-multi-agent-coordination-and-communication/project/solution.py -> 9/9
$ python3 chapters/chapter-11-operating-agents-in-production/project/solution.py -> 9/9
$ python3 chapters/chapter-12-designing-agent-architectures/project/solution.py -> 12/12 (L3 regression)
$ python3 assessments/module-assessments/module-1-.../solution.py -> 4/4
$ python3 assessments/module-assessments/module-2-.../solution.py -> 5/5
$ python3 assessments/module-assessments/module-3-.../solution.py -> 3/3
$ python3 assessments/module-assessments/module-4-.../solution.py -> 3/3
$ python3 assessments/module-assessments/module-5-.../solution.py -> 4/4
$ python3 assessments/module-assessments/module-6-.../solution.py -> 6/6
```

## Local check

`bash scripts/local_check.sh < /dev/null` was run ALONE, with no other
repo command running concurrently, after every Chapter 13 file, the
capstone rubric, and all site wiring were in place. All six checks
passed clean: required folders, no placeholder text, Python syntax,
every `exercises/project/practice` `solution.py` run, JS syntax and
chapter-path validation (now including Chapter 13's own `path`), and no
likely secrets found.
