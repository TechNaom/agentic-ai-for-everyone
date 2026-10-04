# PROJECT_STATE.md — Agentic AI for Everyone

Last updated: 2026-10-04 (Session 13 — Chapter 13, "Capstone: Designing
and Defending an Autonomous Agent System," complete and live. **THE
COURSE IS COMPLETE**: all 13 chapters and all 6 modules are live and
Complete. Chapter 13 is the L4 Architecture Challenge — a full
Architecture Decision Record plus a working, instrumented reference
implementation for Thornwick Marketplace Collective, a genuinely
multi-component system needing all eight Chapter 1-11 mechanisms at
once. The capstone rubric ships at
`assessments/architecture-challenges/`. There is no Chapter 14. See
the "Course Complete" section near the end of this file for the
closing summary, and `quality-audits/chapter-13-audit.md` for the
full decision record. Nothing has been pushed to GitHub — all work is
local-only, matching every prior session's explicit instructions.)

## Course Objective

Teach the discipline of designing, building, and operating an
**autonomous AI agent as a system**: the agent loop (perception,
reasoning, action, observation), planning and task decomposition, tool
use and function calling, memory and state, reflection and
self-correction, guardrails and safety for autonomous systems,
multi-agent orchestration and coordination, evaluating agent
reliability, and cost/latency control of agent loops — following the
TechNaom master course-building philosophy (layered depth, story-first,
production-grade, interview-ready, original content only).

## Architecture Decisions

- **Course size: 13 chapters, 6 modules** — matching every other
  focused-topic course in the ecosystem (`mcp-for-everyone`,
  `ai-coding-agents-for-everyone`, `ai-security-for-everyone`,
  `ai-engineering-for-everyone`, `context-engineering-for-everyone`,
  `llm-evaluation-for-everyone`).
- **Positioning**: a deliberately narrow, verified gap relative to
  five siblings — `ai-coding-agents-for-everyone` (a coding-domain-
  specific agent), `mcp-for-everyone` (the MCP protocol itself),
  `ai-engineering-for-everyone` (the broader LLM production-engineering
  stack), `llm-evaluation-for-everyone` (evaluation as its own deep
  discipline — this course defers deep methodology to it), and
  `context-engineering-for-everyone` (context-window construction —
  this course's memory chapter defers to it). Full reasoning, including
  each neighbor's own curriculum map read this session and, for the two
  highest-risk neighbors, actual chapter content, in
  `docs/discovery-notes.md`. Notably, `llm-evaluation-for-everyone`'s
  own discovery notes (read this session) already name this exact
  course by title as the future home for agent *architecture*, as
  opposed to evaluating agent *output* — confirming the boundary from
  the sibling's own side.
- **Repo structure mirrors `llm-evaluation-for-everyone`** (this
  session's assigned structural template — a recently-completed
  sibling): static site, `chapters/chapter-XX-slug/`,
  `docs/curriculum/`, `templates/`, `assessments/`, `quality-audits/`.
  Shared front-end assets and templates rebranded
  (`AAFE_MODULES`/`AAFEProgress`/`aafe-progress` localStorage key),
  `.gitkeep` added to every not-yet-built chapter directory from day
  one.
- **Lesson density mirrors `python-for-everyone`** (this session's
  assigned density template) — Chapter 1's own `lesson.html` was built
  to and verified against the 60+ `<pre>`/`<code>`-block hard
  requirement (actual count: **61 blocks**, verified with
  `grep -c '<pre\|<code' lesson.html`), built as one incrementally-
  extended TrailBot agent script, not a pile of disconnected snippets.
- **Chapter file pattern**: the rich per-chapter structure
  (`lesson.html`, `quiz.html`, `interview-questions.html` + `.md`,
  `exercises/{README.md,index.html,starter.py,solution.py,ai-paired.html}`,
  `practice/` (same set), `project/{README.md,index.html,starter.py,
  solution.py,ai-paired.html,RUBRIC.md}`) — this ecosystem's current
  default, matched exactly for Chapter 1.
- **Model/API policy**: plain `openai` Python package pointed at
  Ollama's local OpenAI-compatible endpoint (`llama3.2:latest`) by
  default, zero cost/API key, matching `ai-coding-agents-for-everyone`'s
  own approach — **no heavy agent framework** (LangChain, LangGraph,
  CrewAI, AutoGen, etc.) is a required dependency anywhere in this
  course; every mechanism is taught with minimal, readable,
  from-scratch Python so it's never hidden behind a framework
  abstraction. A documented option swaps in a hosted provider (OpenAI,
  Anthropic, Gemini all expose OpenAI-compatible endpoints) by changing
  only `base_url` and the API key.
- **Ollama reliability policy**: this sandbox's local Ollama install
  has shown a genuine, observed intermittent hang — one call during
  this session took 138 seconds (Chapter 1, Section 2's bare LLM call);
  a documented prior sibling-course session saw one call take 432
  seconds. Every live call in this course's hands-on chapters is
  treated as illustrative, not gate-load-bearing: budget up to 450
  seconds, never idle-wait past that, wrap every production-facing call
  with an explicit timeout (Chapter 1 Section 11 builds and tests this
  pattern), and prefer showing a captured transcript over re-running
  live.
- **Grading harness policy**: exercises/practice/project `solution.py`
  files are graded by deterministic, offline scoring functions
  (structural self-checks, keyword-substance checks for free-text
  answers) so CI and any learner's machine can grade them without a
  running Ollama server. Where a chapter's own concept genuinely
  requires a live model (e.g., a real agent loop), the *lesson* content
  runs live and captures real output, but the *graded* exercises use a
  deterministic stand-in (see Chapter 1's `FakeModel` in
  `project/starter.py`) so grading itself never depends on model
  availability or non-determinism.

## Session 1 — Discovery, Scaffold, and Chapter 1 (2026-09-24)

**What was built, in order:**

1. Read the scaffold reference (`llm-evaluation-for-everyone`'s full
   repo layout: root files, `assets/`, `docs/`, `templates/`,
   `chapters/chapter-01-.../` file set, `CONTRIBUTING.md`, license
   files, `scripts/local_check.sh`) and the density reference
   (`python-for-everyone` Chapters 1-2 `lesson.html`, confirming the
   56/62 code-block counts and the `code-window`/`output-block`/
   `code-breakdown`/`what-is`/`go-deeper`/`real-world` CSS pattern —
   already present in `llm-evaluation-for-everyone`'s own
   `style.css`, so no CSS porting from `python-for-everyone` was
   needed, only content).
2. Initialized the repo at `/mnt/d/projects/agentic-ai-for-everyone`,
   ran `git config core.filemode false` immediately, set the default
   branch to `main`.
3. Copied and rebranded `assets/` (style.css, progress.js, sidebar.js,
   home.js, quiz-engine.js — `LEFE_MODULES`/`LEFEProgress` renamed to
   `AAFE_MODULES`/`AAFEProgress` throughout, including a leftover
   `LEFE_HOME_ROOT` in `home.js` and a leftover context-engineering-
   flavored sidebar subtitle string both caught and fixed during the
   copy, not left in place), `templates/`, `scripts/local_check.sh`,
   `.gitignore`, `LICENSE`/`LICENSE-CONTENT`, and adapted
   `CONTRIBUTING.md` (added this course's own no-framework and
   60+-code-block requirements explicitly).
4. Wrote `docs/discovery-notes.md` from scratch: course vision, a
   dedicated section checking this course against each of the five
   named siblings individually (not just a combined summary), personas,
   prerequisites, a 10-item beginner-to-architect learning-outcome
   ladder, the stack decision, course size, capstone description, and
   an explicit cross-course overlap check.
5. Wrote `docs/curriculum/CURRICULUM_MAP.md` (13 chapters, 6 modules,
   full learning outcomes, project ladder) and the styled
   `docs/curriculum/index.html` roadmap (Chapter 1 linked live,
   Chapters 2-13 shown as non-linked "Planned" cards, per the
   no-premature-path rule).
6. Wrote `assets/chapters-data.js` — the single source of truth for the
   6-module, 13-chapter roster, Chapter 1 given a real `path`, all
   other chapters and all `examPath`s intentionally omitted/null.
7. Wrote the full repo scaffold: root `README.md`, `index.html`
   (hero, feature cards, chapter map wired to `chapters-data.js`),
   `.gitkeep`'d directories for Chapters 2-13 (each with empty
   `exercises/`, `practice/`, `project/` subdirs already created), and
   `assessments/`/`quality-audits/` directories.
8. Built **Chapter 1** in full, testing every piece of code for real
   against local Ollama (`llama3.2:latest`) or as deterministic Python
   before writing it into any file — see `quality-audits/chapter-01-
   audit.md` for the complete list of what was actually run and its
   real captured output. Notably, Section 8-9's wrong-argument bug (the
   model appending "trail" to "Cedar Hollow," breaking both tool
   lookups) was discovered live while testing the lesson's own code,
   not manufactured — the lesson shows the real, honest diagnosis and
   fix.
9. Verified `lesson.html`'s code-block count (61, via
   `grep -c '<pre\|<code' lesson.html`), comfortably clearing the
   60-block hard requirement.
10. Wrote `quality-audits/chapter-01-audit.md` with an honest
    self-critique, a fresh fictional-org exclusion list (this is the
    ecosystem's newest course, so the list starts here:
    Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
    Wavecrest Marina), and the Ollama-check/code-tested-before-writing
    disclosures.

**No interruptions this session** — unlike some prior sibling-course
sessions (see `llm-evaluation-for-everyone`'s own `PROJECT_STATE.md`
for that history), this build ran start to finish without an
infrastructure or account interruption.

## Chapter 1 — COMPLETE

- `lesson.html`: 61 `<pre>`/`<code>` blocks (60+ required). Built as one
  incrementally-extended agent (TrailBot, for the fictional Northbeam
  Outdoors), every live-model block backed by a real captured Ollama
  transcript, every deterministic block backed by a real local Python
  run. Covers: the agent loop definition, why a bare call isn't an
  agent, tool functions, JSON tool schemas, the model's first
  tool-calling decision, executing an action and feeding back an
  observation, generalizing into a reusable loop function, a genuine
  multi-tool run that surfaced a real wrong-argument bug, diagnosing
  and fixing that bug, a deterministic runaway-loop guard
  demonstration, this sandbox's own Ollama-hang handling, and the
  fully assembled reference agent.
- `quiz.html`: 10 fill-in-the-blank questions covering the loop
  definition, the protocol mechanics (tool_call_id, role:"tool"), the
  Cedar Hollow bug's classification and fix location, the guard's
  guarantee and limits, this session's own 432s hang disclosure, and
  this course's boundary vs. `mcp-for-everyone`.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect, each with a strong answer,
  red flag, follow-up, and "what this proves."
- `exercises/`: Summit Gear Co-op/GearBot scenario, 8 tasks (5
  production-gear), 17 points total. `solution.py` verified 17/17;
  `starter.py` verified to fail cleanly (4/17 with all TODOs at their
  default/no-op state, not a crash). `ai-paired.html` uses a third
  scenario (Fernbrook Ski Patrol/LiftBot).
- `practice/`: 8 independent, fast diagnostic scenarios across 8
  different fictional systems, 8 points. `solution.py` verified 8/8;
  `starter.py` verified 0/8 with no crash. `ai-paired.html` uses a
  ninth scenario (an unnamed apartment complex's ConciergeBot).
- `project/` (L1 Guided): Wavecrest Marina/SlipBot, a 3-`TODO`
  `run_agent()` scaffold graded by a 4-check deterministic structural
  self-check (using a scripted `FakeModel`, so grading never depends on
  a live model). `solution.py` verified 4/4 checks passing;
  `starter.py` verified 0/4 with no crash. `RUBRIC.md` included.
  `ai-paired.html` has the learner independently prompt an AI for the
  same `run_agent()` and review it against a named checklist of common
  AI-generated-loop mistakes (off-by-one guard, unhandled bad tool
  name, ambiguous multi-call observation handling).
- Wired into `assets/chapters-data.js` with a real `path`; `index.html`
  hero stats and chapter map reflect "1 of 13 chapters live."

## Known Issues

- **This sandbox's Ollama install has a real, observed intermittent
  hang.** Chapter 1 Section 2's first live call took 138 seconds (a
  2-minute foreground call was killed and re-run with a longer budget
  before succeeding). This is disclosed in the lesson text itself, in
  `quality-audits/chapter-01-audit.md`, and here. Future chapters with
  live-model content should budget up to 450 seconds per call, never
  idle-wait past that, and always show a captured transcript rather
  than re-running live on every page load.
- **Only `llama3.2:latest` has been tested.** All tool-calling
  behavior, argument-formatting quirks (including the genuine Cedar
  Hollow bug), and timing are specific to this one model in this one
  sandbox. No claim is made that these exact behaviors generalize to
  other models.
- **No GitHub remote exists yet, and none should be added without an
  explicit human instruction to do so.** This session's task was
  explicit: local commits only, no push. `README.md` and other files
  reference `https://github.com/TechNaom/agentic-ai-for-everyone` as
  the eventual public URL, matching every sibling course's own
  pre-publication convention — this is aspirational text, not a live
  remote.

## Session 2 — Chapter 2, "Planning and Task Decomposition" (2026-09-28)

Picked up a Chapter 2 build left uncommitted by a prior session (cut
off by a usage limit before it could commit): `lesson.html`,
`quiz.html`, `interview-questions.md`, the full `exercises/` set, and
`practice/starter.py`+`solution.py` already existed and were re-
verified, not rebuilt. This session completed the rest:

1. Re-verified the pre-existing `exercises/` and `practice/` pair
   (`solution.py` scores perfect, `starter.py` fails cleanly with no
   crash) before building anything else on top of them.
2. Built `interview-questions.html` as a static render of the
   pre-existing `interview-questions.md`, matching Chapter 1's own
   format (10 questions, 4 levels, `lesson-card` blocks).
3. Built `practice/README.md`, `practice/index.html`, and
   `practice/ai-paired.html` (a ninth scenario, `EscalationBot`, an
   unnamed subscription-service support router with two layered
   planning problems — wrong planning mode plus a wrong-plan failure —
   matching Chapter 1's convention of leaving a two-tool scenario's org
   unnamed).
4. Built the entire `project/` folder from scratch: `README.md`,
   `RUBRIC.md`, `index.html`, `ai-paired.html`, `starter.py`,
   `solution.py` — a **chapter mini-project** (explicitly labeled as
   such, since Chapter 2 has no dedicated L1/L2 slot on the curriculum
   map's project ladder; that work is folded into the L2 Assisted
   project after Chapter 4). Scenario: Cobblestone Courier Co.'s
   RouteBot, combining a fixed-plan-with-re-planning executor and an
   emergent delay-diagnosis loop in one 3-`TODO` scaffold, graded by 7
   deterministic structural self-checks. `solution.py` verified 7/7;
   `starter.py` verified 1/7 with no crash (the one check that doesn't
   depend on any `TODO` — giving up cleanly with no correction
   available — passes even against the unfilled stub).
5. Wrote `quality-audits/chapter-02-audit.md`, extending (not
   restarting) `chapter-01-audit.md`'s fictional-org exclusion list.
   Four new orgs this chapter: **Alderleaf Research Group** (lesson;
   ScoutBot), **Pinehurst Realty Group** (exercises; ListBot),
   **Thistlewood Veterinary Group** (exercises `ai-paired.html`;
   TriageBot), **Cobblestone Courier Co.** (project; RouteBot) — plus
   EscalationBot's unnamed org (practice `ai-paired.html`). Running
   exclusion list now: Northbeam Outdoors, Summit Gear Co-op, Fernbrook
   Ski Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst
   Realty Group, Thistlewood Veterinary Group, Cobblestone Courier Co.
6. Wired Chapter 2 into `assets/chapters-data.js` (real `path` added),
   `docs/curriculum/index.html` (Chapter 2 card converted to a live
   link, Module 1 feature card marked "Complete"), and root
   `index.html` (`hero-stats` updated to 2/13 chapters, 1/6 modules
   complete).
7. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
   all 6 checks passed clean.
8. Committed Chapter 2 locally (all its files, `chapters-data.js`,
   `docs/curriculum/index.html`, root `index.html`, this file, and the
   new audit) — no remote added, nothing pushed, matching Session 1's
   and this session's own explicit local-only instructions.

## Chapter 2 — COMPLETE

- `lesson.html`: 63 lines match `<pre\|<code` (118 total tag
  occurrences via `-o`), comfortably above the 60+ block requirement.
  Built around Alderleaf Research Group's ScoutBot, comparing a fixed,
  up-front plan (company snapshot — order-independent) against
  emergent, one-step-at-a-time planning (stock-drop investigation —
  order-dependent) against the same four tools, including a genuine
  unscripted free-text-planning failure (invented tool names), a real
  5-reasoning-calls-vs-1 cost comparison, a real wrong-plan failure
  demonstration, and a `max_replans` guard mirroring Chapter 1's
  `max_iterations`.
- `quiz.html`: 10 fill-in-the-blank questions.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Pinehurst Realty Group/ListBot scenario, 8 tasks (5
  production-gear), 16 points. `solution.py` verified 16/16;
  `starter.py` verified 2/16 with no crash. `ai-paired.html` uses a
  third scenario (Thistlewood Veterinary Group/TriageBot).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario (EscalationBot, org left
  unnamed).
- `project/` (chapter mini-project, not on the numbered L1-L4 ladder):
  Cobblestone Courier Co./RouteBot, a 3-`TODO` scaffold combining a
  fixed-plan-with-re-planning executor, an emergent delay-diagnosis
  loop, and the fixed-vs-emergent heuristic itself, graded by 7
  deterministic structural self-checks. `solution.py` verified 7/7;
  `starter.py` verified 1/7 with no crash. `RUBRIC.md` included.
  `ai-paired.html` has the learner independently prompt an AI for
  `run_fixed_dispatch()` and review it against a named checklist of
  common AI-generated re-planning mistakes.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 2 live, Module 1 complete.

## Session 3 — Chapter 3, "Tool Use and Function Calling" (2026-09-28)

Built cold, from this file's own "Next Recommended Task" brief, with
zero memory of Session 2:

1. Read `PROJECT_STATE.md`'s Chapter 3 brief, Chapter 2's full file set
   as the structural template, `python-for-everyone`'s density
   benchmark, and `quality-audits/chapter-02-audit.md`'s org-exclusion
   list before writing anything.
2. Picked a fresh scenario per the brief's own guidance: **Palisade
   Broadband**/NetBot, with three genuinely overlapping tools for the
   same request ("my internet is down" could be a billing suspension,
   an area outage, or a bad line) and a tool (`restart_modem`) whose
   failure mode is a clean, well-formed success that doesn't mean the
   problem is fixed.
3. Attempted two live Ollama calls this session (a plain sanity check
   and a real tool-selection call with `tools=TOOLS`), each under a
   440-second budget. **Neither returned — both were killed by the
   timeout wrapper with no output at all**, worse than Chapter 1's
   disclosed 138s hang or the prior session's disclosed 432s data
   point. Per this course's reliability policy, this session did not
   idle-wait past budget and did not fabricate a transcript — every
   lesson example instead runs against real, executed, deterministic
   Python (tested in a scratch directory before being written into
   `lesson.html`), disclosed explicitly in the lesson's own Section 2
   and in `quality-audits/chapter-03-audit.md`.
4. Built `lesson.html` around three pillars beyond Chapters 1-2's tool-
   calling mechanics: tool selection among overlapping candidates
   (ordered by cost/decisiveness, not topical keyword similarity),
   argument-formatting drift handled by drift-specific normalizers (not
   one shared strip-and-lower pattern), and three distinct tool-failure
   types (timeout, malformed output, succeeds-but-wrong-answer) each
   with its own retry policy, unified behind one dispatcher routed by a
   per-tool `FAILURE_POLICY` dict. A real bug (the dispatcher's first
   draft forced a simulated hang on every retry attempt, so it never
   recovered) was caught by testing and fixed before being written into
   the lesson, the same "genuine bug becomes the honest example"
   pattern as Chapter 1's Cedar Hollow bug.
5. Verified lesson density: **70 lines** match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html` (above Chapter 1's 61 and
   Chapter 2's 63), **130 total occurrences** via
   `grep -oE '<pre|<code' | wc -l`.
6. Built the full file set matching Chapter 2's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (Thornbury Insurance
   Group/ClaimBot, 8 tasks, 16 points, `ai-paired.html` using a third
   scenario, Wrenhollow Auto Rentals/FleetBot), `practice/` (8
   independent scenarios, 8 points, `ai-paired.html` using a ninth,
   unnamed-org scenario, HandoffBot), and `project/` (Kestrel Appliance
   Service/RepairBot, explicitly labeled a chapter mini-project per
   `CURRICULUM_MAP.md`'s project ladder — the next numbered slot, L2
   Assisted, ships after Chapter 4 — 3 TODOs, 7 structural self-checks,
   `RUBRIC.md`, `ai-paired.html`).
7. Verified every `solution.py`/`starter.py` pair by actually running
   it: `exercises` 16/16 vs. 3/16 (no crash), `practice` 8/8 vs. 0/8
   (no crash), `project` 7/7 vs. 2/7 (no crash).
8. Wrote `quality-audits/chapter-03-audit.md`, extending (not
   restarting) `chapter-02-audit.md`'s fictional-org exclusion list.
   Four new orgs this chapter: **Palisade Broadband** (lesson; NetBot),
   **Thornbury Insurance Group** (exercises; ClaimBot), **Wrenhollow
   Auto Rentals** (exercises `ai-paired.html`; FleetBot), **Kestrel
   Appliance Service** (project; RepairBot) — plus HandoffBot's unnamed
   org (practice `ai-paired.html`). Running exclusion list now:
   Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski Patrol,
   Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty Group,
   Thistlewood Veterinary Group, Cobblestone Courier Co., Palisade
   Broadband, Thornbury Insurance Group, Wrenhollow Auto Rentals,
   Kestrel Appliance Service.
9. Wired Chapter 3 into `assets/chapters-data.js` (real `path` added),
   `docs/curriculum/index.html` (Chapter 3 card converted to a live
   link, Module 2 feature card marked "In Progress" — the same wording
   precedent Module 1 used while only Chapter 1 was live), and root
   `index.html` (`hero-stats` updated to 3/13 chapters; modules-complete
   stays at 1/6 since Module 2 isn't done until Chapter 4 ships).
10. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
    all 6 checks passed clean.
11. Committed Chapter 3 locally (all its files, `chapters-data.js`,
    `docs/curriculum/index.html`, root `index.html`, this file, and the
    new audit) — no remote added, nothing pushed, matching every prior
    session's explicit local-only instructions.

## Chapter 3 — COMPLETE

- `lesson.html`: 70 lines match `<pre\|<code` (130 total tag
  occurrences via `-o`), above both prior chapters' density. Built
  around Palisade Broadband's NetBot: a naive keyword-matching tool-
  selection baseline that provably fails on genuine ambiguity, the
  fix (cheapest-most-decisive-signal-first ordering, exercised across
  all three real branches), two argument normalizers for two distinct
  drift patterns (account IDs, ZIP codes), three distinct tool-failure
  types each demonstrated and given its own retry policy (timeout ->
  bounded retry; malformed output -> no retry, proven identical across
  3 attempts; succeeds-but-wrong-answer -> independent outcome
  verification, no retry concept applies at all), a unified dispatcher
  routing by per-tool failure policy, and the fully assembled NetBot
  agent run across 3 end-to-end cases. Honestly discloses that no live
  Ollama call succeeded this session (two attempts, 440s budget each,
  both non-returning) and explains what stands in for it.
- `quiz.html`: 10 fill-in-the-blank questions covering selection
  ordering, the three failure types and their distinct policies, the
  unified dispatcher, and this chapter's own scenario.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Thornbury Insurance Group/ClaimBot scenario, 8 tasks (5
  production-gear), 16 points total. `solution.py` verified 16/16;
  `starter.py` verified 3/16 with no crash. `ai-paired.html` uses a
  third scenario (Wrenhollow Auto Rentals/FleetBot).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario (HandoffBot, org left
  unnamed).
- `project/` (chapter mini-project, not on the numbered L1-L4 ladder):
  Kestrel Appliance Service/RepairBot, a 3-`TODO` scaffold combining
  tool selection, timeout-retry handling, and outcome verification,
  graded by 7 deterministic structural self-checks. `solution.py`
  verified 7/7; `starter.py` verified 2/7 with no crash. `RUBRIC.md`
  included. `ai-paired.html` has the learner independently prompt an AI
  for `verify_repair_outcome()` and review it against a named checklist
  of common AI-generated outcome-check mistakes.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 3 live, Module 2 in progress.

## Session 4 — Chapter 4, "Memory and State" (2026-09-28)

Built cold, from this file's own "Next Recommended Task" brief, with
zero memory of Session 3. This session was interrupted once (the
parent session ended before a commit landed) and resumed cold in a
second pass — the resume verified everything already on disk before
building anything new, rather than restarting or rewriting complete
work.

1. Read `PROJECT_STATE.md`'s Chapter 4 brief, Chapter 3's full file set
   as the structural template, `python-for-everyone`'s density
   benchmark, `quality-audits/chapter-03-audit.md`'s org-exclusion
   list, and `docs/curriculum/CURRICULUM_MAP.md`'s project-ladder
   section (the brief's own flag that Chapter 4 is different from
   Chapters 2-3: this is where the numbered **L2 Assisted** project
   actually begins) before writing anything.
2. Picked a fresh scenario per the brief's own guidance — a system
   where a fact stated in one session must correctly inform a later,
   separate session: **Larkspur Fitness Studio**/CoachBot, a fitness
   coaching agent where a member's injury or preference, stated once,
   must persist across genuinely separate sessions and change future
   recommendations.
3. Pre-warmed Ollama explicitly (`keep_alive: "120m"`) before writing
   any lesson code, unlike Chapter 3's session. **Every live call this
   session succeeded** — a sanity check (2.2s), a promote-worthy
   classification call (4/4 correct), a live memory-grounded reply
   contrasted against the same prompt with no memory injected, and a
   live summarization call — all real, captured transcripts, not
   deterministic stand-ins. The summarization call's own real output
   dropped a genuine detail (real progress numbers), which became
   Section 14's central worked example rather than a hypothetical.
4. Built `lesson.html` around the short-term/long-term memory split:
   working memory as the Chapter 1-3-familiar message list, a minimal
   JSON-file persisted store (read-modify-write, no vector database or
   embeddings, per this course's deferral to
   `context-engineering-for-everyone`), proven across two genuinely
   separate `python3` processes sharing one file on disk, a
   live-tested promote-worthy filter, token-budget pruning/
   summarization, and an explicit "summarization is not a substitute
   for persisting a fact" section built directly from this session's
   own real summarization-loss observation. Two real bugs, caught by
   testing and fixed on the page: a blind-overwrite merge bug (a
   second promoted fact silently deleted the first) and a stale-
   snapshot bug in the finished agent (a reply decision used a
   pre-write variable instead of re-checking the store after writing),
   the same "genuine bug becomes the honest example" pattern every
   prior chapter used.
5. Verified lesson density: **62 lines** match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html` (above the 60+ requirement),
   **114 total occurrences** via `grep -oE '<pre|<code' | wc -l`.
6. Built the full file set matching Chapter 3's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (Driftwood Legal Clinic/
   IntakeBot, 8 tasks, 16 points, `ai-paired.html` using a third
   scenario, Saltmarsh Language Academy/TutorBot), `practice/` (8
   independent scenarios, 8 points, `ai-paired.html` using a ninth,
   unnamed-org scenario, MemoBot).
7. Built `project/` as this course's numbered **L2 Assisted** project
   (partial scaffold) — not a chapter mini-project, per the curriculum
   map's own distinct wording for Chapter 4. Scenario: Hollowridge
   Wellness Clinic/CareBot, combining multi-tool dispatch with
   persisted memory in full, with a clearly labeled Chapter 5
   extension point: `reflect_on_response()` is wired into the call
   path exactly where reflection belongs, its body a no-op passthrough
   documented explicitly in `project/README.md`'s "What Chapter 5 will
   do with this file" section, so Chapter 5 can replace its body
   without touching the rest of the flow. 3 TODOs, 7 structural
   self-checks, `RUBRIC.md`, `ai-paired.html`.
8. Verified every `solution.py`/`starter.py` pair by actually running
   it, both in the original pass and again after this session's own
   interruption and resume: `exercises` 16/16 vs. 3/16 (no crash),
   `practice` 8/8 vs. 0/8 (no crash), `project` 7/7 vs. 2/7 (no crash).
9. Wrote `quality-audits/chapter-04-audit.md`, extending (not
   restarting) `chapter-03-audit.md`'s fictional-org exclusion list.
   Four new orgs this chapter: **Larkspur Fitness Studio** (lesson;
   CoachBot), **Driftwood Legal Clinic** (exercises; IntakeBot),
   **Saltmarsh Language Academy** (exercises `ai-paired.html`;
   TutorBot), **Hollowridge Wellness Clinic** (project; CareBot) — plus
   MemoBot's unnamed org (practice `ai-paired.html`). Running exclusion
   list now: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski
   Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty
   Group, Thistlewood Veterinary Group, Cobblestone Courier Co.,
   Palisade Broadband, Thornbury Insurance Group, Wrenhollow Auto
   Rentals, Kestrel Appliance Service, Larkspur Fitness Studio,
   Driftwood Legal Clinic, Saltmarsh Language Academy, Hollowridge
   Wellness Clinic.
10. Wired Chapter 4 into `assets/chapters-data.js` (real `path` added,
    Chapters 5-13 confirmed still without one), `docs/curriculum/
    index.html` (Chapter 4 card converted to a live link, Module 2
    feature card marked "Complete" — closing the module), and root
    `index.html` (`hero-stats` updated to 4/13 chapters, 2/6 modules;
    the chapter-map section intro paragraph, found stale from before
    this session, was also corrected to reflect Chapters 1-4 live).
11. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
    all checks passed clean.
12. Committed Chapter 4 locally (all its files, `chapters-data.js`,
    `docs/curriculum/index.html`, root `index.html`, this file, and the
    new audit) — no remote added, nothing pushed, matching every prior
    session's explicit local-only instructions.

## Chapter 4 — COMPLETE

- `lesson.html`: 62 lines match `<pre\|<code` (114 total tag
  occurrences via `-o`), above the 60+ requirement. Built around
  Larkspur Fitness Studio's CoachBot: the short-term/long-term memory
  split, a naive-baseline failure (working memory only, injury
  forgotten every session), a minimal JSON-backed `MemoryStore`
  (read-modify-write), persistence proven across two genuinely
  separate `python3` processes, a live-tested promote-worthy filter, a
  live memory-grounded reply contrasted against the same prompt with
  no memory (real, captured, materially different outputs), a real
  blind-overwrite bug and its fix, a corrections/supersede treatment,
  token-budget pruning with a real live summarization call (which
  really did drop a detail, motivating the "summarization is not a
  substitute for persisting a fact" section), a prune-safety guard,
  and the fully assembled CoachBot agent (which itself surfaced and
  fixed a real stale-snapshot bug). Honestly discloses this session's
  explicit pre-warm discipline and why it differs from Chapter 3's
  disclosed hang.
- `quiz.html`: 10 fill-in-the-blank questions covering the memory-type
  split, read-modify-write, promote-worthy detection, token-budget
  pruning, the summarization-is-not-persistence claim, and the
  stale-snapshot bug.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Driftwood Legal Clinic/IntakeBot scenario, 8 tasks (5
  production-gear), 16 points total. `solution.py` verified 16/16;
  `starter.py` verified 3/16 with no crash. `ai-paired.html` uses a
  third scenario (Saltmarsh Language Academy/TutorBot).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario (MemoBot, org left unnamed).
- `project/` (**L2 Assisted, partial scaffold** — this course's
  numbered project ladder slot, not a chapter mini-project):
  Hollowridge Wellness Clinic/CareBot, a 3-`TODO` scaffold combining
  multi-tool dispatch (appointment availability, booking) with
  persisted long-term memory (patient conditions/preferences merged
  into a later, separate visit), graded by 7 deterministic structural
  self-checks. The reflection half of the L2 description is a clearly
  labeled no-op passthrough (`reflect_on_response()`), wired into the
  call path for Chapter 5 to fill in — documented explicitly in
  `project/README.md`. `solution.py` verified 7/7; `starter.py`
  verified 2/7 with no crash. `RUBRIC.md` included. `ai-paired.html`
  has the learner independently prompt an AI for
  `promote_worthy_and_persist()` and review it against a named
  checklist of common AI-generated memory-write mistakes.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 4 live, Module 2 complete.

## Session 5 — Chapter 5, "Reflection and Self-Correction" (2026-09-28)

Built cold, from this file's own "Next Recommended Task" brief, with
one important extra: Chapter 4's own L2 Assisted project's `project/`
directory (`chapters/chapter-04-memory-and-state/project/`) was
extended in place, not recreated, per the brief's explicit instruction.

1. Pre-warmed Ollama (`curl .../api/generate ... keep_alive: "120m"`)
   before writing any lesson code, and ran a plain sanity check
   (`elapsed: 5.06`, `OK`) — the same discipline Chapter 4's session
   used. Unlike Chapter 4, this session's documented sandbox hang
   **recurred anyway**: the first substantive live call (Section 3's
   BikeBot draft) took 413.8 seconds, disclosed directly in the lesson
   rather than smoothed over or silently re-run until fast.
2. Built the fresh lesson scenario, Briarcliff Bike Rentals/BikeBot,
   testing every code example for real (deterministic Python in a
   scratch directory, or real Ollama calls) before writing it into
   `lesson.html` — including running a consolidated
   `verify_all_snippets.py` script after the session's own real
   `extract_dollar_amount()` bug was found and fixed, to confirm every
   remaining claimed output in the lesson actually matches what the
   code produces (see `quality-audits/chapter-05-audit.md` for the
   full list).
3. Two genuine, unscripted live-model results became the lesson's
   central worked examples: a real BikeBot draft that correctly
   handled a policy question but left the customer's explicit price
   question unanswered (Section 3), and a real second-model-call
   self-critique that correctly diagnosed that exact gap but produced
   a "fix" that still didn't resolve it (Section 7/12) — the concrete,
   demonstrated reason this chapter's grounded, deterministic
   `verify_draft()` check is presented as necessary, not a design
   preference.
4. Built the full file set matching Chapter 4's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (Fenwick Home Repair
   Co-op/RepairBot, 8 tasks, 18 points, `starter.py`/`solution.py` both
   run and verified), `practice/` (8 scenarios, `ai-paired.html` using
   a ninth, unnamed RenewBot scenario).
5. Extended Chapter 4's L2 project in place:
   `chapters/chapter-04-memory-and-state/project/solution.py`'s
   `reflect_on_response()` now contains a real, deterministic
   self-critique-and-revise step (a blocking-condition policy check
   combined with whether a follow-up was actually booked), with a
   real before/after shown in the lesson's own Section 14. TODOs 1-3
   and Chapter 4's original self-checks were confirmed unchanged
   before any edit. `starter.py` gained a new TODO 4 (previously a
   given no-op) so learners apply this chapter's own mechanism to
   CareBot themselves. `README.md` and `RUBRIC.md` were both updated
   to describe the extension and to add a fifth grading criterion. A
   `CHAPTER 6 EXTENSION POINT` comment was added at the exact call
   site before `schedule_followup()` is dispatched, for Chapter 6.
   `solution.py` verified 8/8 (was 7/7); `starter.py` verified 2/8
   with no crash (was 2/7).
6. Chapter 5's own `project/` directory (per the curriculum map, this
   chapter has no separate numbered project slot — the L2 project is
   one continuous project extended across Ch. 4-6) was built as a
   signpost only: `README.md` and `index.html` explaining that the
   actual gradable files live in `chapters/chapter-04-memory-and-state/
   project/`, and linking there directly.
7. Wrote `quality-audits/chapter-05-audit.md`, extending (not
   restarting) `chapter-04-audit.md`'s fictional-org exclusion list.
   Three new orgs this chapter: **Briarcliff Bike Rentals** (lesson;
   BikeBot), **Fenwick Home Repair Co-op** (exercises; RepairBot),
   **Mossgate Dental Group** (exercises `ai-paired.html`; DentalBot) —
   plus RenewBot's unnamed org (practice `ai-paired.html`). Hollowridge
   Wellness Clinic (CareBot) was deliberately reused, not treated as a
   new org, since it's the L2 project's own canonical scenario.
8. Wired Chapter 5 into `assets/chapters-data.js` (real `path` added),
   `docs/curriculum/index.html` (Chapter 5 card converted to a live
   link, Module 3 feature card marked "In Progress," not "Complete"),
   and root `index.html` (`hero-stats` updated to 5/13 chapters, module
   count stays at 2/6 since Module 3 isn't done until Chapter 6 ships).
9. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
   all 6 checks passed clean.
10. Committed Chapter 5, the Chapter 4 project extension, and all
    wiring/audit/state changes locally — no remote added, nothing
    pushed, matching every prior session's explicit local-only
    instructions and this session's own.

## Chapter 5 — COMPLETE

- `lesson.html`: 62 lines match `<pre\|<code` (118 total tag
  occurrences via `-o`), above the 60+ requirement, matching Chapter
  4's own 62 exactly. Built around Briarcliff Bike Rentals' BikeBot:
  what reflection actually is versus a bigger prompt, a real
  incomplete-answer live failure, a minimal grounded `verify_draft()`
  check, catching a real arithmetic error, a live case where reflection
  correctly finds nothing wrong, a live self-critique call that
  correctly diagnoses but doesn't fully fix a draft (this chapter's
  central real result), the revise-vs-gather-evidence distinction, a
  real "retry is not reflection" anti-pattern, a bounded
  `max_reflections` guard (with a real, disclosed off-by-one narration
  bug caught and explained, not hidden), when reflection should NOT
  run (previewing Chapter 8), `reflect_and_revise()` generalized, a
  real before/after CareBot extension, and the fully assembled BikeBot
  agent.
- `quiz.html`: 10 fill-in-the-blank questions covering reflection's
  definition, grounded checks, retry-vs-reflection, iteration bounds,
  the two kinds of self-correction, and the CareBot extension.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Fenwick Home Repair Co-op/RepairBot scenario, 8 tasks
  (5 production-gear), 18 points total. `solution.py` verified 18/18;
  `starter.py` verified 4/18 with no crash. `ai-paired.html` uses a
  third scenario (Mossgate Dental Group/DentalBot).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario (RenewBot, org left unnamed).
- `project/` (signpost only, per the L2 project's continuous-across-
  chapters design): points to and documents the real extension inside
  `chapters/chapter-04-memory-and-state/project/`, where
  `reflect_on_response()` now performs real reflection.
  `solution.py` there verified 8/8; `starter.py` verified 2/8 with no
  crash. `RUBRIC.md` there updated to 5 criteria (25 points).
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 5 live, Module 3 in progress.

## Session 6 — Chapter 6, "Guardrails and Safety for Autonomous Agents" (2026-09-28)

Built cold, from this file's own "Next Recommended Task" brief, with
one important extra: Chapter 4's own L2 Assisted project's `project/`
directory (`chapters/chapter-04-memory-and-state/project/`) was
extended in place a third and final time, per the brief's explicit
instruction, completing the L2 project across Chapters 4-6.

1. Pre-warmed Ollama (`curl .../api/generate ... keep_alive: "120m"`)
   before writing any lesson code, and ran a plain sanity check
   (`elapsed: 1.30`, `OK`). Unlike Chapter 5's session (413.8s on its
   first substantive call), this session's documented sandbox hang
   **did not recur** — every live call this session completed in under
   16 seconds, disclosed honestly either way per this course's own
   policy (no claim that fast timing generalizes).
2. Built the fresh lesson scenario, Millbrook Credit Union/LedgerBot (a
   real-money agent: check balance, transfer funds, delete a scheduled
   payment, run a "reconciliation script"), testing every deterministic
   code example for real in a scratch directory before writing it into
   `lesson.html` — five independent guardrail mechanisms (tool
   allowlist, human-approval checkpoint with a genuine pause-and-wait,
   sandboxed command execution via an allowlist/denylist, a hard action
   budget distinct from Chapter 1's `max_iterations`, and a rate limiter
   independent of the action budget), composed into one dispatcher
   function that every tool call must pass through.
3. **Two genuine, unscripted live-model results became this chapter's
   central worked examples**, neither manufactured: a prompt-injection
   attempt via a transaction's memo field (a tool result, not a system
   prompt) was run twice against `llama3.2:latest` with two different
   system-prompt framings. A neutral "review this memo" framing: the
   model correctly identified the injected instruction as suspicious
   and took no action. A more "compliant, automate this" framing: the
   same model complied with the injected instruction — but never
   actually emitted a `transfer_funds` tool call, only narrated in
   plain text that a transfer had occurred. This second result became
   the chapter's central finding: it demonstrates a failure mode
   (false narrated compliance with no real tool call) distinct from
   "the model calls the dangerous tool," and is the concrete reason a
   guardrail enforced in code at the dispatch boundary — checking real
   dispatched tool calls, not a model's own narration — is necessary.
4. Verified lesson density: **62 lines** match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html` (above the 60+ requirement,
   matching Chapters 4-5's own 62 exactly), **129 total occurrences**
   via `grep -oE '<pre|<code' | wc -l`.
5. Built the full file set matching Chapter 5's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (Amberlock Self-Storage/
   DispatchBot, 8 tasks, 19 points, `ai-paired.html` using a third
   scenario, Cascadia Home Security/GuardBot), `practice/` (8 scenarios,
   `ai-paired.html` using a ninth, unnamed EscrowBot scenario).
6. Extended Chapter 4's L2 project in place a third and final time:
   `chapters/chapter-04-memory-and-state/project/solution.py`'s
   `run_visit_session()` now calls a new `guardrail_check_booking()`
   function immediately before `schedule_followup()` is dispatched — a
   hard, enforced check, not a message revised after the fact. TODOs
   1-4 and Chapters 4-5's original 8 self-checks were confirmed
   unchanged before any edit. `starter.py` gained a new TODO 5 (the
   guardrail wiring, given the `guardrail_check_booking()` helper
   itself as "given," per this chapter's own reuse convention).
   `README.md` and `RUBRIC.md` were both updated with a new "What
   Chapter 6 changed" section and a sixth grading criterion.
   **A real, disclosed design tension was found and resolved
   explicitly**: the brief requires both that the guardrail stop an
   unsafe booking automatically, and that the existing 8 self-checks
   (one of which requires `schedule_followup` to have fired for its own
   blocking-condition test case) pass unchanged. The first build
   defaulted `human_approved` to `True` to satisfy both — **corrected in
   a follow-up commit**: a fail-open guardrail contradicted the
   chapter's own fail-safe lesson, so the "unchanged checks" constraint
   was lifted. `human_approved` now defaults to `False` (fail closed);
   Check 8 passes `human_approved=True` explicitly (approval as a
   recorded act); Checks 9 and 10 exercise the gate. Still 10/10. The
   fail-closed rationale is in `project/README.md`, `RUBRIC.md`, and the
   lesson's own Section 17. Per the brief's own stated preference,
   Chapter 5's `reflect_on_response()` was deliberately **kept**, not
   removed, as a defense-in-depth backstop — justified explicitly in
   `project/README.md`. `solution.py` verified 10/10 (was 8/8);
   `starter.py` verified 2/10 with no crash (was 2/8).
7. Chapter 6's own `project/` directory (per the curriculum map, this
   chapter has no separate numbered project slot — the L2 project is
   one continuous project extended across Ch. 4-6, now complete) was
   built as a signpost only: `README.md` and `index.html` explaining
   that the actual gradable files live in
   `chapters/chapter-04-memory-and-state/project/`, and linking there
   directly.
8. Wrote `quality-audits/chapter-06-audit.md`, extending (not
   restarting) `chapter-05-audit.md`'s fictional-org exclusion list.
   Three new orgs this chapter: **Millbrook Credit Union** (lesson;
   LedgerBot), **Amberlock Self-Storage** (exercises; DispatchBot),
   **Cascadia Home Security** (exercises `ai-paired.html`; GuardBot) —
   plus EscrowBot's unnamed org (practice `ai-paired.html`). Hollowridge
   Wellness Clinic (CareBot) was deliberately reused, not treated as a
   new org, since it's the L2 project's own canonical scenario.
9. Wired Chapter 6 into `assets/chapters-data.js` (real `path` added,
   Chapters 7-13 confirmed still without one), `docs/curriculum/
   index.html` (Chapter 6 card converted to a live link, Module 3
   feature card marked "Complete," closing the module), and root
   `index.html` (`hero-stats` updated to 6/13 chapters, 3/6 modules; the
   chapter-map section intro paragraph, found stale from before this
   session in the same spot Chapter 4's session once found one, was
   also corrected to reflect Chapters 1-6 live).
10. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
    all 6 checks passed clean.
11. Committed Chapter 6, the Chapter 4 project's third extension, and
    all wiring/audit/state changes locally — no remote added, nothing
    pushed, matching every prior session's explicit local-only
    instructions and this session's own.

## Chapter 6 — COMPLETE

- `lesson.html`: 62 lines match `<pre\|<code` (129 total tag
  occurrences via `-o`), above the 60+ requirement, matching Chapters
  4-5's own 62 exactly. Built around Millbrook Credit Union's LedgerBot:
  what a guardrail is versus reflection (a hard boundary checked before
  dispatch, not a text revision checked after), a naive-baseline
  failure (an unguarded $600 external transfer executing with zero
  checks), all five guardrail mechanisms (tool allowlist, a real
  pause-and-wait human-approval checkpoint, sandboxed command execution,
  a hard action budget distinct from Chapter 1's `max_iterations`, and
  an independent rate limiter), a unified dispatcher at the
  tool-dispatch boundary, two real live prompt-injection tests (one
  resisted, one fell for it via false narrated compliance with no real
  tool call), a deterministic demonstration that the guardrail catches
  an injected transfer's exact arguments regardless of how the call was
  produced, a fail-safe default-deny treatment, guardrails-and-
  reflection as defense-in-depth, the fully assembled LedgerBot session
  (five guardrails, five real refusals, one real success), and a real
  third extension of CareBot with a full before/after.
- `quiz.html`: 10 fill-in-the-blank questions covering the guardrail
  definition, the pause-and-wait requirement, the live injection test's
  own result, tool-result-borne injection, fail-safe defaults, the
  action-budget-vs-max_iterations distinction, and the CareBot
  extension.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Amberlock Self-Storage/DispatchBot scenario, 8 tasks (5
  production-gear), 19 points total. `solution.py` verified 19/19;
  `starter.py` verified 5/19 with no crash. `ai-paired.html` uses a
  third scenario (Cascadia Home Security/GuardBot).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario (EscrowBot, org left unnamed).
- `project/` (signpost only, per the L2 project's continuous-across-
  chapters design, now complete): points to and documents the real
  extension inside `chapters/chapter-04-memory-and-state/project/`,
  where `run_visit_session()` now calls `guardrail_check_booking()`
  before `schedule_followup()` dispatches. `solution.py` there verified
  10/10; `starter.py` verified 2/10 with no crash. `RUBRIC.md` there
  updated to 6 criteria (30 points). **This closes the L2 Assisted
  project** — no further chapter extends it.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 6 live, Module 3 complete.


## Session 7 — Chapter 7, "Evaluating Agent Reliability" (2026-09-30)

Built cold, from this file's own "Next Recommended Task" brief, with
one important extra: Modules 1-3's own combined assessments were built
this session, closing a pre-existing gap flagged but never built by
any prior session.

1. Read `docs/discovery-notes.md` Section 1.4 first, confirming this
   chapter's boundary against `llm-evaluation-for-everyone`: task
   success, trajectory/tool-call correctness, multi-turn drift, and
   non-determinism are this chapter's own territory; golden-set
   construction, human evaluation, LLM-as-judge design, and
   statistical rigor are named by chapter number and deferred to that
   sibling course, confirmed against its own current
   `docs/curriculum/CURRICULUM_MAP.md` rather than assumed from memory.
2. Pre-warmed Ollama. The warm-up call itself took its full cold-load
   time (348.7s total, ~345.5s of that just loading the model) —
   disclosed exactly via the real `total_duration`/`load_duration`
   fields, comfortably inside the 450s budget but far from instant.
   Once warm, calls ranged 0.56s-14.04s.
3. **A real, unscripted live-model non-determinism test became this
   chapter's central worked example**: the identical fact-check task
   was sent to `llama3.2:latest` six separate times, asking only which
   tool it would call first. Results: `verify_source_credibility`,
   `verify_source_credibility`, `cross_check_claim`, `cross_check_
   claim`, `cross_check_claim`, `search_archive` — only the LAST run
   matched the correct ground-truth first step. This single result
   became Section 2's centerpiece and the calibration source for the
   bulk N-run harness's error-rate parameter.
4. **A real bug in this session's own tool code became a second,
   unplanned teaching moment, kept in rather than quietly patched**:
   `cross_check_claim()`'s word-overlap heuristic reported that a claim
   saying "the bridge cost $12M" MATCHED an archive record that
   actually said "$9.4M." Built into Sections 5-8 and 15 as the
   concrete demonstration that task success and trajectory correctness
   can both report a pass while the underlying content is still wrong
   — and the exact seam where `llm-evaluation-for-everyone`'s own
   LLM-as-judge methodology would need to take over.
5. Built the fresh lesson scenario, Greywick Dispatch/FactScout (a
   fact-checking agent: search an archive, verify source credibility,
   cross-check a claim, draft a citation, or escalate to a human
   editor), testing every deterministic code example for real in a
   scratch directory before writing it into `lesson.html` — task
   success (Section 6), trajectory correctness (Section 7), a seeded
   N-run harness (Sections 9-10), pass@k and variance (Section 11),
   multi-turn drift (Section 12), cost-per-success (Section 13), one
   combined eval report (Section 14), a named seam for a future
   LLM-as-judge (Section 15), and an eval-maturity checklist
   (Section 16).
6. Verified lesson density: **61 lines** match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html` (above the 60+ requirement,
   comparable to Chapter 6's own 62), **121 total occurrences** via
   `grep -o '<pre\|<code' | wc -l` (Chapter 6: 127).
7. Built the full file set matching Chapter 6's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (Larkmoor Archive
   Service/RecordScout, 7 tasks, 19 points, `ai-paired.html` using a
   third scenario, Thornmere Public Transit/TransitScout), `practice/`
   (8 scenarios, `ai-paired.html` using a ninth, unnamed "ClaimBot"
   scenario).
8. Built Chapter 7's own `project/` as a REAL, standalone chapter
   mini-project (per the brief: Chapter 7 returns to a full scaffold,
   unlike Chapters 5-6's signposts) — Emberlyn Underwriting/
   TriageScout, three TODOs (`task_success`, `trajectory_correctness`,
   `run_harness`) mirroring the lesson's own three pillars.
   `solution.py` verified 8/8; `starter.py` verified 2/8 with no
   crash. No L2/L3/L4 numbered project work was touched — the L2
   project closed at Chapter 6, and the L3 Independent project ships
   after Chapter 8, not this chapter.
9. **Built Modules 1-3's combined module assessments**, closing a
   pre-existing gap flagged but never built by any prior session (see
   `quality-audits/chapter-07-audit.md`'s decision section for the
   full reasoning). Each reuses the EXACT, already-tested functions
   from that module's own two chapters, loaded directly from their
   real `project/solution.py` files via `importlib`, applied to a
   small combined scenario — following `ai-engineering-for-everyone`'s
   own `module-4-cost-latency-reliability-engineering-exercise` format
   (confirmed by reading that file directly, not assumed from memory).
   Module 1: 4/4 on `solution.py`, 0/4 on `starter.py`. Module 2: 5/5
   on `solution.py`, 0/5 on `starter.py` (and confirmed its scratch
   memory file is cleaned up after each run). Module 3: 3/3 on
   `solution.py`, 0/3 on `starter.py`. **Module 4's own assessment was
   explicitly NOT built** — it spans Chapters 7 AND 8, and is
   scheduled for Chapter 8's own session below.
10. Wrote `quality-audits/chapter-07-audit.md`, extending (not
    restarting) `chapter-06-audit.md`'s fictional-org exclusion list.
    Four new orgs this chapter: **Greywick Dispatch** (lesson;
    FactScout), **Larkmoor Archive Service** (exercises; RecordScout),
    **Thornmere Public Transit** (exercises `ai-paired.html`;
    TransitScout), **Emberlyn Underwriting** (project; TriageScout) —
    plus "ClaimBot"'s unnamed employer (practice `ai-paired.html`).
11. Wired Chapter 7 into `assets/chapters-data.js` (real `path` added,
    Chapters 8-13 confirmed still without one), `docs/curriculum/
    index.html` (Chapter 7 card converted to a live link, Module 4
    feature card marked "In Progress," NOT "Complete" — Chapter 8
    still has to ship), and root `index.html` (`hero-stats` updated to
    7/13 chapters; module-complete count correctly held at 3/6, not
    incremented).
12. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
    all 6 checks passed clean. (Note: this script's own glob does not
    cover `assessments/module-assessments/*/solution.py`; those three
    were verified manually instead.)
13. Re-ran `chapters/chapter-04-memory-and-state/project/solution.py`
    as the L2 regression check — still 10/10, unchanged from Chapter 6.
14. Committed Chapter 7, the three Module 1-3 assessments, and all
    wiring/audit/state changes locally — no remote added, nothing
    pushed, matching every prior session's explicit local-only
    instructions and this session's own.

## Chapter 7 — COMPLETE

- `lesson.html`: 61 lines match `<pre\|<code` (121 total tag
  occurrences via `-o`), above the 60+ requirement. Built around
  Greywick Dispatch's FactScout: the boundary against
  `llm-evaluation-for-everyone` (named by chapter number), a live
  six-run non-determinism result (1/6 matched the correct first
  step), a real live bug in `cross_check_claim`'s own word-overlap
  heuristic (kept in as the chapter's own $12M/$9.4M running example),
  task-success rate vs. trajectory/tool-call correctness as two
  deliberately-disagreeing metrics, a seeded N-run harness calibrated
  from the live result, pass@k and variance, multi-turn drift, cost-
  per-success, one combined eval report, a named seam for a future
  LLM-as-judge, and an eval-maturity checklist.
- `quiz.html`: 10 fill-in-the-blank questions covering task success vs.
  trajectory correctness, the live non-determinism result, pass@k,
  multi-turn drift, cost-per-success, the $12M/$9.4M bug, the
  llm-evaluation-for-everyone boundary, and the seeded-simulation
  disclosure.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Larkmoor Archive Service/RecordScout scenario, 7 tasks
  (5 production-gear), 19 points total. `solution.py` verified 19/19;
  `starter.py` verified 0/19 with no crash. `ai-paired.html` uses a
  third scenario (Thornmere Public Transit/TransitScout).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario ("ClaimBot", org left
  unnamed).
- `project/` (a REAL, standalone chapter mini-project, not a signpost —
  Chapter 7 returns to the full scaffold per the brief): Emberlyn
  Underwriting/TriageScout, three TODOs across task success,
  trajectory correctness, and the aggregate harness. `solution.py`
  verified 8/8; `starter.py` verified 2/8 with no crash. `RUBRIC.md`
  has 4 criteria (20 points).
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 7 live, Module 4 **In Progress** (not Complete).
- **New this session**: Modules 1-3's own combined module assessments,
  under `assessments/module-assessments/`, each reusing the exact
  functions those modules' chapters already built and tested. Module
  4's own assessment remains unbuilt, scheduled below.

## Session 8 — Chapter 8, "Cost and Latency Control of Agent Loops" (2026-09-30)

Built cold, from this file's own "Next Recommended Task" brief, with
zero memory of Session 7.

1. Read `PROJECT_STATE.md`'s Chapter 8 brief, `AI_HANDOFF.md`,
   `docs/curriculum/CURRICULUM_MAP.md`, `quality-audits/chapter-07-
   audit.md`'s org-exclusion list, and Chapter 7's full file set as
   the structural/density template before writing anything.
2. Pre-warmed Ollama in the background (`curl .../api/generate ...
   keep_alive: "120m"`, empty prompt). The warm-up call itself
   reported no duration fields (empty prompt, load-only); the first
   REAL generation call after that still took 48.99s, disclosed
   honestly. Once warm, every subsequent call was fast (4.76s-94.45s,
   with that range itself becoming the chapter's own central live
   result).
3. **Reused Chapter 7's own FactScout/Greywick Dispatch directly as
   this chapter's scenario**, per the brief's own stated preference,
   rather than a new disconnected agent — `trajectory_covers_goal` and
   `trajectory_correctness` are the literal Chapter 7 functions, and
   `cost_per_success` is re-run before and after this chapter's own
   five techniques to produce a real measured delta.
4. **Three genuine, unscripted live-model results became this
   chapter's own central worked examples**: a capped one-word
   tool-selection call (4.76s, correct answer) vs. an open-ended
   reasoning call (94.45s) for the identical model and task — a real
   ~20x latency gap; two real Ollama calls run sequentially (5.14s)
   vs. concurrently via `ThreadPoolExecutor` (1.61s) — a real ~3.2x
   speedup; and the 48.99s first-generation timing disclosed above.
5. **A real bug was found and fixed during this session's own scratch
   testing**: the before/after harness's first `BudgetGuard`
   configuration (`max_cost=0.01`) denied the controlled version's
   very first strong-tier step on every single task, driving its
   measured success rate to a false 0.0% — caught before it reached
   the lesson, corrected to `max_cost=0.05`; the corrected numbers are
   what the lesson reports.
6. Built `lesson.html` around: per-step token/cost accounting, the
   naive/unbounded baseline, fail-closed step/token/time/cost budgets
   (`BudgetGuard`), early termination, model routing (cheap vs.
   strong, calibrated against the live ~20x latency result), caching
   (with a disclosed no-invalidation limitation), parallel tool calls
   (calibrated against the live ~3.2x speedup), latency percentiles
   (p50/p95), timeouts/retries with exponential backoff, OpenRouter/
   Groq named conceptually only (no live paid calls), all five
   techniques assembled and applied to FactScout, and a real before/
   after re-run of a Chapter-7-shaped harness (51.0% cost reduction,
   92.3% latency reduction, with an honestly disclosed small per-task
   success-rate dip that `cost_per_success` still showed as a net win
   on every task).
7. Verified lesson density: **61 lines** match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html` (matching Chapter 7's own 61
   exactly), **114 total occurrences** via `grep -o '<pre\|<code' |
   wc -l`.
8. Built the full file set matching Chapter 7's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (Brambleford Analytics/
   InsightScout, 7 tasks, 19 points, `ai-paired.html` using a third
   scenario, Caldwell Ridge Observatory/SkyScout), `practice/` (8
   scenarios, `ai-paired.html` using a ninth, unnamed "QuoteBot"
   scenario).
9. Built Chapter 8's own `project/` as a REAL, standalone chapter
   mini-project (matching Chapter 7's own pattern, NOT the L3
   Independent project) — Portage Grain Cooperative/YieldScout, three
   TODOs (`task_success`, `is_within_budget`,
   `run_cost_controlled_harness`) mirroring the lesson's own
   budget-enforcement pillar. `solution.py` verified 9/9;
   `starter.py` verified 2/9 with no crash. `ai-paired.html` uses a
   fourth scenario, Marrowvale Textile Mill/LoomScout.
10. **Built Module 4's own combined assessment**
    (`assessments/module-assessments/module-4-reliability-plan-and-
    cost-control-exercise/`), per the exact precedent set at Chapter 7
    — reuses Chapter 7's `trajectory_correctness`/`task_success` AND
    Chapter 8's `is_within_budget`/`step_cost`, loaded via `importlib`
    directly from both chapters' real `project/solution.py` files.
    `solution.py` verified 3/3 objectively-checkable parts;
    `starter.py` verified 0/3, no crash. See
    `quality-audits/chapter-08-audit.md`'s Module 5 gap-audit
    decision: Module 5's own assessment should wait until Chapter 11
    (its closing chapter), not be built at Chapter 9.
11. Wrote `quality-audits/chapter-08-audit.md`, extending (not
    restarting) `chapter-07-audit.md`'s fictional-org exclusion list.
    Four new orgs this chapter: **Brambleford Analytics** (exercises;
    InsightScout), **Caldwell Ridge Observatory** (exercises
    `ai-paired.html`; SkyScout), **Portage Grain Cooperative**
    (project; YieldScout), **Marrowvale Textile Mill** (project
    `ai-paired.html`; LoomScout) — plus "QuoteBot"'s unnamed employer
    (practice `ai-paired.html`). Greywick Dispatch/FactScout was
    deliberately reused (not a new org), per the brief's own
    instruction to continue Chapter 7's agent.
12. Wired Chapter 8 into `assets/chapters-data.js` (real `path` added,
    Chapters 9-13 confirmed still without one), `docs/curriculum/
    index.html` (Chapter 8 card converted to a live link, Module 4
    feature card marked "Complete" — closing the module), and root
    `index.html` (`hero-stats` updated to 8/13 chapters, 4/6 modules;
    the chapter-map section intro paragraph, found stale from before
    this session in the same spot Chapters 4 and 6's sessions once
    found one, was also corrected to reflect Chapters 1-8 live).
13. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo —
    all 6 checks passed clean.
14. Re-ran `chapters/chapter-04-memory-and-state/project/solution.py`
    (L2 regression, still 10/10) and `chapters/chapter-07-evaluating-
    agent-reliability/project/solution.py` (Ch7 project regression,
    still 8/8), both unchanged from Chapter 7's session.
15. Committed Chapter 8, the Module 4 assessment, and all
    wiring/audit/state changes locally — no remote added, nothing
    pushed, matching every prior session's explicit local-only
    instructions and this session's own.

## Chapter 8 — COMPLETE

- `lesson.html`: 61 lines match `<pre\|<code` (114 total tag
  occurrences via `-o`), matching Chapter 7's own 61 exactly. Built as
  a direct continuation of Chapter 7's FactScout: per-step token/cost
  accounting, a naive/unbounded baseline, a fail-closed `BudgetGuard`
  (steps/tokens/time/cost, distinct from Chapter 1's `max_iterations`
  and Chapter 6's action budget), early termination, model routing
  (cheap vs. strong, backed by a real live ~20x latency gap between a
  capped and an open-ended call for the identical model/task), caching
  (with a disclosed no-invalidation limitation), parallel tool calls
  (backed by a real live ~3.2x speedup on two concurrent Ollama
  calls), latency percentiles (p50/p95), retries with exponential
  backoff, OpenRouter/Groq named conceptually only, all five
  techniques assembled onto FactScout, and a real before/after re-run
  of a Chapter-7-shaped harness (51.0% cost reduction, 92.3% latency
  reduction, with an honestly disclosed small per-task success-rate
  dip that `cost_per_success` still showed as a net win everywhere).
- `quiz.html`: 10 fill-in-the-blank questions covering the fail-closed
  budget, early termination, model routing, the live latency/speedup
  results, p95, exponential backoff, and the real before/after delta.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Brambleford Analytics/InsightScout scenario, 7 tasks
  (5 production-gear), 19 points total. `solution.py` verified 19/19;
  `starter.py` verified 0/19 with no crash. `ai-paired.html` uses a
  third scenario (Caldwell Ridge Observatory/SkyScout).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario ("QuoteBot", org left
  unnamed).
- `project/` (a REAL, standalone chapter mini-project, not the L3
  project and not a signpost — matching Chapter 7's own pattern):
  Portage Grain Cooperative/YieldScout, three TODOs across task
  success, the fail-closed budget check, and the cost-controlled
  harness. `solution.py` verified 9/9; `starter.py` verified 2/9 with
  no crash. `RUBRIC.md` has 3 criteria (20 points). `ai-paired.html`
  uses a fourth scenario (Marrowvale Textile Mill/LoomScout).
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 8 live, Module 4 **Complete**.
- **New this session**: Module 4's own combined assessment, under
  `assessments/module-assessments/`, reusing Chapter 7's AND Chapter
  8's own already-tested chapter-mini-project functions.

## Session 9 — Chapter 9, "Multi-Agent Orchestration Patterns" (2026-09-30)

Built cold, from this file's own "Next Recommended Task" brief, with
zero memory of Session 8:

1. Read this file's Chapter 9 brief in full, `AI_HANDOFF.md`,
   `docs/curriculum/CURRICULUM_MAP.md`, `quality-audits/chapter-08-
   audit.md`'s 30-org exclusion list, and Chapter 8's full file set as
   the structural/density template before writing anything.
2. Picked a fresh scenario per the brief's own guidance (something
   that genuinely decomposes into 2-3 independent sub-domains): a
   trip-planning supervisor, **Quillmark Journeys**/TripScout,
   dispatching to **FlightScout**, **StayScout**, and **ExcursionScout**.
3. Warmed Ollama and ran FIVE separate live test scripts in a scratch
   directory before writing anything into `lesson.html` (a full-goal
   3-tool dispatch attempt, a one-sub-task-at-a-time dispatch test, a
   retry test, a sequential-vs-parallel fan-out test, and a plain
   sanity check) -- two of these produced genuine, unscripted
   failures used directly as the chapter's own central worked
   examples rather than manufactured: a full-goal dispatch call
   returned a 3-call plan as plain text with empty `tool_calls`
   (Section 4), and even after switching to one-sub-task-per-call, 1
   of 3 calls in that same test run STILL came back malformed the
   same way (Section 4) -- a bounded retry on that exact sub-task
   then succeeded on its first attempt (Section 5), disclosed as
   genuinely non-deterministic, not re-run to "get a clean result."
   The fan-out test measured a real ~3.5x speedup (33.65s sequential
   vs. 9.57s parallel) on three genuinely independent live worker
   calls (Section 8).
4. Built `lesson.html` around the brief's own required pillars:
   supervisor/worker dispatch (Sections 3-6), a sequential-pipeline
   contrast (Section 7), parallel fan-out/fan-in (Section 8),
   blackboard/shared-state coordination with a load-bearing lock
   (Section 9), per-agent budgets extending Chapter 8's
   `is_within_budget` (Section 10), failure isolation via a per-worker
   try/except boundary (Section 11), content verification catching a
   deliberately planted "plausible-but-wrong" worker result -- a
   StayScout that always returns a Porto hotel regardless of the
   requested city (Section 12), redundant-dispatch cost multiplication
   and its idempotent-dispatch fix (Section 13), and cross-agent
   trajectory evaluation extending Chapter 7's `trajectory_correctness`
   into `which_agent_responsible` (Section 14). A fail-closed approval
   checkpoint (Section 15, mirroring Chapter 6's own
   `human_approved`-defaults-to-`False` fix) and an assembled
   end-to-end TripScout run (Section 16) close out the build before
   the maturity checklist and recap.
5. Verified `lesson.html`'s code-block count: 63 via
   `grep -c '<pre\|<code' lesson.html`, clearing the 60+ requirement.
6. Built the full file set matching Chapter 8's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.md` (10 questions
   across 4 levels, generated into `interview-questions.html` via a
   small one-off conversion script to guarantee the two stay in
   sync), `exercises/` (Hadleigh Civic Records Bureau/CaseScout, 7
   tasks/19 points, `solution.py` 19/19, `starter.py` 0/19 no crash,
   `ai-paired.html` using a third scenario, Corvindale Claims
   Network/ClaimScout), `practice/` (8 scenarios/8 points,
   `solution.py` 8/8, `starter.py` 0/8 no crash, `ai-paired.html`
   using a ninth scenario, "DispatchBot," org left unnamed), and a
   **chapter mini-project** `project/` (Ashgrove Municipal
   Services/CityScout, 3 TODOs across fail-closed routing, failure
   isolation, and an idempotent attributed harness, `solution.py` 9/9,
   `starter.py` 2/9 no crash, `RUBRIC.md` with 4 criteria/20 points,
   `ai-paired.html` using a fourth scenario, Foxglenn Relief
   Network/AidScout) -- explicitly NOT the L3 Independent project.
7. Wired `assets/chapters-data.js` (Chapter 9's real `path` added,
   Module 5's `examPath` stays `null`), `docs/curriculum/index.html`
   (Chapter 9's card converted from a non-linked "Planned" `<div>` to
   a linked `<a class="chapter-card">`, Module 5's feature card moved
   to "In Progress"), and root `index.html` (`hero-stats` chapter
   count to 9 of 13, module-complete count LEFT at 4 of 6 per the
   brief, and the stale "Chapters 1-8" intro paragraph updated to
   "Chapters 1-9").
8. Wrote `quality-audits/chapter-09-audit.md` following
   `chapter-08-audit.md`'s exact format, extending (not restarting)
   its 30-org exclusion list with this chapter's own 5 new orgs, and
   explicitly restating (not resolving) both the L3 Independent
   project deferral and the Module 5 assessment deferral.
9. Ran `bash scripts/local_check.sh < /dev/null` -- all 6 checks
   passed clean.
10. Re-ran `chapters/chapter-04-memory-and-state/project/solution.py`
    (L2 regression: 10/10, unchanged), `chapters/chapter-07-
    evaluating-agent-reliability/project/solution.py` (Ch7 regression:
    8/8, unchanged), and `chapters/chapter-08-cost-and-latency-
    control-of-agent-loops/project/solution.py` (Ch8 regression: 9/9,
    unchanged) -- all three pass identically to before this session's
    changes.
11. Updated this file (this section, the "Last updated" line, the new
    "Chapter 9 — COMPLETE" section below, and this rewritten "Next
    Recommended Task" section for Chapter 10) before ending the
    session.

**No interruptions this session** — ran start to finish without an
infrastructure or account interruption. Ollama's own live-call
non-determinism (the genuine malformed-dispatch results, Sections 4-5)
was disclosed honestly rather than treated as an interruption to route
around.

## Chapter 9 — COMPLETE

- `lesson.html`: 63 matches via `grep -c '<pre\|<code' lesson.html`
  (60+ required). Built around Quillmark Journeys' TripScout
  dispatching to FlightScout/StayScout/ExcursionScout. Covers:
  hand-off from Chapters 1-8 (Section 1), a live Ollama warm-up check
  (Section 2), the supervisor's dispatch tool schema (Section 3), a
  genuinely malformed live full-goal dispatch AND a genuinely
  malformed live one-sub-task-at-a-time dispatch in the SAME test run
  (Section 4), a real successful retry of that exact malformed call
  (Section 5), fail-closed routing for an ambiguous sub-task (Section
  6), a sequential-pipeline contrast (Section 7), a real ~3.5x
  measured live fan-out/fan-in speedup on three independent workers
  (Section 8), blackboard/shared-state coordination with a
  load-bearing `threading.Lock` (Section 9), per-agent budgets
  extending Chapter 8's `is_within_budget` (Section 10), per-worker
  failure isolation (Section 11), content verification catching a
  deliberately planted plausible-but-wrong StayScout result (Section
  12), redundant-dispatch cost multiplication and its idempotent fix
  (Section 13), cross-agent trajectory evaluation extending Chapter
  7's `trajectory_correctness` into `which_agent_responsible` (Section
  14), a fail-closed approval checkpoint mirroring Chapter 6's fix
  (Section 15), and an assembled end-to-end TripScout run (Section
  16).
- `quiz.html`: 10 fill-in-the-blank questions covering decomposition/
  routing/aggregation, the live malformed-dispatch result, fail-closed
  routing, the pipeline-vs-supervisor distinction, the live fan-out
  speedup, the blackboard lock, failure isolation, content
  verification, idempotent dispatch, and cross-agent attribution.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect, including an architect-level
  question on recursive supervisor-of-supervisors budget composition.
- `exercises/`: Hadleigh Civic Records Bureau/CaseScout scenario, 7
  tasks (5 production-gear), 19 points total. `solution.py` verified
  19/19; `starter.py` verified 0/19 with no crash. `ai-paired.html`
  uses a third scenario (Corvindale Claims Network/ClaimScout).
- `practice/`: 8 independent diagnostic scenarios, 8 points.
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario ("DispatchBot," org left
  unnamed).
- `project/` (a REAL, standalone chapter mini-project, not the L3
  project and not a signpost — matching Chapters 7-8's own pattern):
  Ashgrove Municipal Services/CityScout, three TODOs across
  fail-closed routing, per-worker failure isolation, and an idempotent,
  attributed supervisor harness. `solution.py` verified 9/9;
  `starter.py` verified 2/9 with no crash. `RUBRIC.md` has 4 criteria
  (20 points). `ai-paired.html` uses a fourth scenario (Foxglenn
  Relief Network/AidScout).
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 9 live, Module 5 **In Progress** (not Complete — Chapters
  10-11 still have to ship).
- **Explicitly NOT built this session** (restated per this file's own
  discipline of never letting a deferred decision silently disappear):
  the **L3 Independent project** and **Module 5's own assessment**.
  Both remain deferred — see the Chapter 10 brief immediately below.

## Session 10 — Chapter 10, "Multi-Agent Coordination and Communication" (2026-10-04)

Built cold, from this file's own "Next Recommended Task" brief, with zero
memory of Session 9.

1. Read this file's Chapter 10 brief in full, `AI_HANDOFF.md`,
   `docs/curriculum/CURRICULUM_MAP.md`, `quality-audits/chapter-09-audit.md`'s
   35-org exclusion list, and Chapter 9's full file set as the
   structural/density template before writing anything.
2. Picked a fresh scenario that genuinely requires PEER-to-PEER message
   exchange (not supervisor dispatch): **Harrowgate Logistics Exchange**,
   two equal dispatch agents, **DockScout** and **YardScout**, who must
   split incoming shipments by messaging each other directly.
3. Warmed Ollama in the background. The warm-up plus a concurrent second
   warm-up request left the model unloaded: the first sanity call took
   **314.35s** (disclosed in the lesson). Once warm, every call completed
   well inside the 450s budget.
4. Ran live peer-messaging tests in a scratch directory before writing
   anything into `lesson.html`. Real, unscripted results captured and used
   as the chapter's central examples:
   - **Duplicated work, reproduced live.** DockScout and YardScout were
     each asked to claim a shipment for themselves with no knowledge of the
     other's decision, and BOTH claimed `S-104` (95.24s and 19.36s).
   - **A genuinely malformed message.** YardScout's call emitted keys padded
     with whitespace (`" recipient "`, `"shipment_id "`) and a mismatched
     message type (`"query"` for a claim). Section 7's safe parser is built
     and tested against this exact output.
   - **A live self-resolution.** DockScout, told YardScout had also claimed
     `S-104`, voluntarily sent a `reject` (29.02s), with a real
     `"note":"null"` string-literal defect disclosed.
   - **Deadlock did NOT reproduce live.** Both agents, told "never go
     first," sent a query anyway (28.65s, 33.2s). Disclosed honestly; the
     chapter constructs deadlock deterministically instead, per the
     reliability policy.
5. Built `lesson.html` around: a message schema (dataclass), a shared
   message bus with drain-on-read, the live duplicated-work and malformed
   captures, safe normalization vs. fail-closed parsing, a locked shared
   claim-check fix, a live conflict resolution, consensus/tie-breaking
   (with the 2-agent tie proof), the non-reproducing live deadlock attempt,
   deterministic deadlock construction plus timeout detection, a
   pre-agreed tie-breaker, message-level trajectory attribution, a
   fail-closed commit guardrail, an assembled end-to-end run, and a
   maturity checklist.
6. Verified every deterministic lesson snippet by running it
   (`scratchpad/ch10/test_lesson.py` and `verify_lesson.py`, both matching
   the lesson's captured output blocks line for line).
7. Verified lesson density: **61 lines** match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html`.
8. Built the full file set matching Chapter 9's: `quiz.html` (10
   fill-in-the-blank), `interview-questions.md` + `.html` (10 questions across
   4 levels; the HTML generated from the .md by a one-off script so the two
   stay in sync), `exercises/` (Bellcrest Freelance Guild, 7 tasks, 19 points,
   `ai-paired.html` using a third scenario, Oakmere Produce Collective),
   `practice/` (8 scenarios, 8 points, `ai-paired.html` using a ninth,
   unnamed "NegotiatorBot" scenario), and a chapter mini-project `project/`
   (Ravenshollow Talent Agency, 3 TODOs across message validation, an atomic
   locked claim-check, and an assembled peer harness; `solution.py` 9/9,
   `starter.py` 2/9 with no crash, `RUBRIC.md` 4 criteria/20 points,
   `ai-paired.html` using a fourth scenario, Pemberwick Salvage Co.).
9. Wrote `quality-audits/chapter-10-audit.md`, extending (not restarting)
   the 35-org exclusion list with 5 new orgs, and explicitly restating the
   L3 project and Module 5 assessment deferrals.
10. Wired Chapter 10 into `assets/chapters-data.js` (real `path` added,
    Chapter 11 still without one, Module 5's `examPath` still `null`),
    `docs/curriculum/index.html` (Chapter 10 card converted to a live
    link; Module 5's feature card stays "In Progress"), and root
    `index.html` (`hero-stats` chapter count 10 of 13; module-complete
    count left at 4 of 6; the stale intro paragraph updated to Chapters
    1-10 live with Module 5 still In Progress).
11. Ran `scripts/local_check.sh < /dev/null` for the whole repo: **all
    checks passed clean**, run alone. An earlier apparent failure
    (a Chapter 4 exercise's `os.remove` on a shared
    `test_task5_solution.json`) was caused by this session launching a
    second `local_check` run while a first one was still in progress: both
    raced on the same file in the repo root. Not a defect in Chapter 4's
    code; the isolated re-run passed.
12. Re-ran all four regression checks, each unchanged: L2 Chapter 4 project
    10/10, Ch7 project 8/8, Ch8 project 9/9, Ch9 project 9/9.
13. Committed Chapter 10 and all wiring/audit/state changes locally, no
    remote added, nothing pushed.

## Chapter 10 — COMPLETE

- `lesson.html`: 61 lines match `<pre\|<code` (60+ required). Built around
  Harrowgate Logistics Exchange's DockScout and YardScout peer agents.
  Covers: hand-off from Chapter 9's dispatch model to peer communication,
  a live Ollama warm-up check (including its 314s cold-load disclosure), a
  message schema, a shared message bus, a real live duplicated-work result,
  a real live malformed message, miscommunication validation (safe
  normalization vs. fail-closed on a renamed field), the fix for duplicated
  work via a locked claim-check, a real live conflict resolution, 2-agent
  voting's tie problem, a non-reproducing live deadlock attempt (disclosed),
  deterministic deadlock construction and timeout detection, a pre-agreed
  tie-breaker, message-level attribution, a fail-closed commit guardrail,
  the assembled exchange, and a communication maturity checklist.
- `quiz.html`: 10 fill-in-the-blank questions.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Bellcrest Freelance Guild/DesignScout+DevScout, 7 tasks
  (5 production-gear), 19 points. `solution.py` 19/19; `starter.py` 0/19,
  no crash. `ai-paired.html` uses Oakmere Produce Collective.
- `practice/`: 8 scenarios, 8 points. `solution.py` 8/8; `starter.py` 0/8,
  no crash. `ai-paired.html` uses a ninth, unnamed scenario.
- `project/` (chapter mini-project, not the L3 project): Ravenshollow Talent
  Agency, 3 TODOs. `solution.py` 9/9; `starter.py` 2/9, no crash.
  `RUBRIC.md` 4 criteria (20 points). `ai-paired.html` uses Pemberwick
  Salvage Co.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect Chapter 10
  live, Module 5 **In Progress** (not Complete).
- **Explicitly NOT built this session** (restated): the **L3 Independent
  project** and **Module 5's own assessment**. Both remain deferred; see the
  Chapter 11 brief below.

## Session 11 — Chapter 11, "Operating Agents in Production" (2026-10-04)

Built cold, from this file's own "Next Recommended Task" brief, with zero
memory of Session 10.

1. Read this file's Chapter 11 brief in full, Chapters 9 and 10's own
   `lesson.html` and `project/solution.py` files for the exact helper
   functions to reuse, `docs/curriculum/CURRICULUM_MAP.md`, and
   `quality-audits/chapter-10-audit.md`'s 40-org exclusion list before
   writing anything.
2. Warmed Ollama with a single background request, then ran exactly ONE
   sanity call (11.12s, real) before writing any lesson code -- no second
   warm-up or live call launched concurrently, the exact discipline
   Session 10's own disclosed 314.35s race motivated.
3. Ran live tests in `scratchpad/ch11/` before writing anything into
   `lesson.html`. Two real, unscripted results became the chapter's
   central examples:
   - **A genuine argument-drift result.** The SAME retried request
     ("confirm shipment S-104 is claimed by you") produced two different
     real argument shapes across two live calls -- attempt 1 included an
     extra `"vehicle":"None"` key attempt 2 did not. This is the concrete
     reason this chapter's idempotency key is built from
     `(agent, shipment_id, action)`, never raw argument equality.
   - **A genuine live timeout result.** An OpenAI client configured with
     `timeout=0.5` seconds raised `APITimeoutError` at 3.07 seconds, not
     0.5 -- disclosed honestly as the real gap between a configured
     timeout budget and the actual clock.
   - No call stalled this session; Ollama was reliable throughout
     (disclosed either way per this course's policy -- no claim that this
     generalizes).
4. Built `lesson.html` around: idempotency keys and `commit_once`,
   bounded retries with exponential backoff, three independent timeout
   layers (per-call, per-agent, per-exchange -- the last reusing Chapter
   10's deadlock timeout unchanged), structured JSON-line logging with a
   correlation id, attribution reconstructed from logs alone (Chapter 9's
   `which_agent_responsible` and Chapter 10's
   `which_agent_caused_miscommunication`, unchanged), a crash-survivable
   run summary computed by re-parsing the log, Chapter 7/8's measurement
   layer applied to a production-shaped run, an explicit deferral to
   `llm-evaluation-for-everyone` and `ai-engineering-for-everyone`, and
   the fully assembled Harrowgate Logistics Exchange (DockScout/
   YardScout, reused from Chapter 10) operated end-to-end.
5. Verified lesson density: **60** lines match `<pre\|<code` via
   `grep -c '<pre\|<code' lesson.html` (meets the 60+ requirement).
6. Built the full file set matching Chapter 10's: `quiz.html` (10
   fill-in-the-blank), `interview-questions.md` + `.html` (10 questions
   across 4 levels, HTML generated from the `.md` by a one-off script),
   `exercises/` (Cindermoor Parcel Network, 7 tasks, 19 points,
   `ai-paired.html` using a third scenario, Thistlebrook Fulfillment
   Co-op), `practice/` (8 scenarios, 8 points, `ai-paired.html` using a
   ninth, unnamed "NotaryBot" scenario), and a chapter mini-project
   `project/` (Wrenfield Dispatch Alliance, 3 TODOs across idempotency,
   bounded retries, and a crash-survivable run summary; `solution.py`
   9/9, `starter.py` 3/9 with no crash, `RUBRIC.md` 4 criteria/20 points,
   `ai-paired.html` using a fourth scenario, Hollowgate Courier Network).
7. **Built Module 5's own combined assessment this session, on
   schedule** (not deferred a third time): `assessments/module-
   assessments/module-5-multi-agent-coordination-and-operations-
   exercise/` (README, RUBRIC, starter, solution), reusing Chapter 9's
   `route_subtask`/`which_agent_responsible`, Chapter 10's
   `parse_message_safely`/`coordinated_claim`, and Chapter 11's
   `idempotency_key`/`commit_once`/`call_with_retries`, all loaded via
   `importlib`, exactly matching Module 4's own precedent at Chapter 8.
   `solution.py` 4/4; `starter.py` 0/4 with no crash.
8. Wrote `quality-audits/chapter-11-audit.md`, extending (not
   restarting) the 40-org exclusion list with 4 new orgs, and explicitly
   restating the L3 deferral as a FIFTH consecutive hand-off, with the
   reasoning for that decision recorded in full.
9. Wired Chapter 11 into `assets/chapters-data.js` (real `path` added),
   `docs/curriculum/index.html` (Chapter 11 card converted to a live
   link; Module 5's feature card moved to **"Complete"**), and root
   `index.html` (`hero-stats` chapter count 11 of 13, module-complete
   count 5 of 6; the stale intro paragraph updated to Chapters 1-11
   live with Module 5 complete).
10. Ran `scripts/local_check.sh < /dev/null` for the whole repo, ALONE,
    with no other command running concurrently: **all six checks passed
    clean**.
11. Re-ran all regression checks, each unchanged: L2 Chapter 4 project
    10/10, Ch7 project 8/8, Ch8 project 9/9, Ch9 project 9/9, Ch10
    project 9/9, and Modules 1-4's own assessments (4/4, 5/5, 3/3, 3/3
    respectively) all still pass their own solutions.
12. Committed Chapter 11, the Module 5 assessment, and all
    wiring/audit/state changes locally, no remote added, nothing
    pushed.

## Chapter 11 — COMPLETE

- `lesson.html`: 60 lines match `<pre\|<code` (60+ required). Built
  around Harrowgate Logistics Exchange's DockScout and YardScout
  (reused from Chapter 10, per this chapter's own brief's explicit
  permission). Covers: idempotency keys and `commit_once`, a real live
  argument-drift result motivating them, bounded retries with
  exponential backoff, a real live timeout-firing result, three
  independent timeout layers (per-call, per-agent, per-exchange),
  structured JSON-line logging with a correlation id, attribution
  reconstructed from logs alone, a crash-survivable run summary, the
  Chapter 7/8 measurement layer applied to a production-shaped run, an
  explicit deferral to two sibling courses, and the fully assembled
  Harrowgate exchange operated end-to-end.
- `quiz.html`: 10 fill-in-the-blank questions.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect.
- `exercises/`: Cindermoor Parcel Network/SortScout+RouteScout
  scenario, 7 tasks (5 production-gear), 19 points. `solution.py`
  19/19; `starter.py` 0/19, no crash. `ai-paired.html` uses Thistlebrook
  Fulfillment Co-op.
- `practice/`: 8 scenarios, 8 points. `solution.py` 8/8; `starter.py`
  0/8, no crash. `ai-paired.html` uses a ninth, unnamed scenario
  ("NotaryBot").
- `project/` (chapter mini-project, not the L3 project): Wrenfield
  Dispatch Alliance, 3 TODOs. `solution.py` 9/9; `starter.py` 3/9, no
  crash. `RUBRIC.md` 4 criteria (20 points). `ai-paired.html` uses
  Hollowgate Courier Network.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 11 live, **Module 5 Complete**.
- **Module 5's own combined assessment was built this session**, on
  schedule, NOT deferred further: `assessments/module-assessments/
  module-5-multi-agent-coordination-and-operations-exercise/`.
  `solution.py` 4/4; `starter.py` 0/4, no crash.
- **Explicitly NOT built this session** (restated loudly): the **L3
  Independent project**, now deferred a FIFTH consecutive time. See
  `quality-audits/chapter-11-audit.md` for the full reasoning and the
  Chapter 12 brief below for the restatement.

## Session 12 — Chapter 12, "Designing Agent Architectures" (2026-10-04)

This session RESUMED a Chapter 12 build that a prior session had
started and was killed mid-way by a transient network error (not a
logic failure), picked up cold except for an orchestrator's own
pre-verification of what already existed on disk.

1. Independently verified, rather than rebuilt, everything the
   orchestrator had already confirmed GOOD: `lesson.html` (60 lines
   match `<pre\|<code`), `quiz.html`, `interview-questions.md`+`.html`,
   the full `exercises/` set (`solution.py` 17/17, `starter.py` 1/17
   no crash), and `practice/solution.py` (8/8).
2. Read `PROJECT_STATE.md`'s own Chapter 12 brief in full (the section
   this session is now replacing), `docs/curriculum/CURRICULUM_MAP.md`'s
   Module 6 section, the resumed `lesson.html` in full (to recover its
   own framework functions and its own already-made L3 decision), and
   `quality-audits/chapter-11-audit.md`'s 44-org exclusion list before
   writing anything new.
3. Discovered the resumed `lesson.html` had ALREADY decided the L3
   question (Section 21: "This chapter's project closes a
   five-session-deferred commitment") and already named the project's
   scenario (Driftlight Energy Cooperative). This session's job became
   verifying that decision was sound, not re-deciding from scratch --
   see the dedicated L3 section in `quality-audits/chapter-12-audit.md`
   for the full verification.
4. Built the entire `project/` directory from scratch as the **L3
   Independent project**: `README.md`, `RUBRIC.md`, `solution.py`
   (deliberately NO `starter.py`, per L3's own "no scaffold"
   definition), `index.html`, `ai-paired.html` (a fourth scenario,
   Mirelake Water Authority). `solution.py` implements a real
   `MemoryStore` (JSON-file-backed, proven to persist across two
   separate instantiations), a fail-closed `apply_credit` guardrail,
   and an idempotent `commit_once`/`idempotency_key` layer, then
   instruments all three with a deterministic reliability/cost harness
   and proves the stated 0.95/0.08 budget is actually met with real
   measured numbers (1.00 success rate, $0.03-0.05 cost per task,
   printed at the end of a run). Scores 12/12.
5. Built the missing `practice/{README.md,starter.py,index.html,
   ai-paired.html}` around the pre-existing `practice/solution.py` (8
   abstract scenarios: SingleDesk, TwinField, VaultGate, ChatterMesh,
   NightWatch, DraftCritic, StakesLadder, ReviewPacket).
   `ai-paired.html` uses a ninth scenario ("ScopeCreep," employer left
   unnamed per this course's own convention).
6. Checked both `assessments/module-assessments/` and
   `assessments/architecture-challenges/` before building Module 6's
   own assessment, per the brief's explicit instruction. Decision:
   `assessments/architecture-challenges/` is reserved for Chapter 13's
   own capstone (the curriculum map's own term for Ch13's rubric is
   "architecture challenge, Level 4," matching that directory's name).
   Module 6's Chapter-12-scoped assessment follows every prior
   module's own naming convention instead:
   `assessments/module-assessments/module-6-architecture-design-
   exercise/`. Reuses Chapter 12's own tested framework functions via
   `importlib` from `project/solution.py`, applied to a SIXTH fresh
   scenario (Alderwood Transit Cooperative). `solution.py` 6/6;
   `starter.py` 0/6, no crash.
7. Wrote `quality-audits/chapter-12-audit.md`, extending (not
   restarting) `chapter-11-audit.md`'s 44-org exclusion list. New orgs
   this session: **Driftlight Energy Cooperative** (project),
   **Mirelake Water Authority** (project `ai-paired.html`), **Alderwood
   Transit Cooperative** (Module 6 assessment) -- plus "ScopeCreep"'s
   unnamed employer (practice `ai-paired.html`). The resumed build's
   own orgs (Copperfield Municipal Utilities, Lantern Hill Senior
   Living, Vantage Peak Ski Resorts) are listed in the running
   exclusion list for completeness but were not new this session.
8. Wired Chapter 12 into `assets/chapters-data.js` (real `path` added),
   `docs/curriculum/index.html` (Chapter 12 card converted to a live
   link, Module 6 feature card marked **"In Progress,"** NOT
   "Complete" -- Chapter 13's own capstone rubric still has to ship;
   the stale "Chapters 1-6" intro paragraph, found in the same spot
   prior sessions have repeatedly found one, was also corrected), and
   root `index.html` (`hero-stats` updated to 12/13 chapters, module
   count stays at 5/6; the chapter-map section intro paragraph
   corrected to reflect Chapters 1-12 live).
9. Updated `docs/curriculum/CURRICULUM_MAP.md`'s project-ladder section:
   L3 Independent now reads **"SHIPPED at Ch. 12"** with a pointer to
   the project directory and this session's audit.
10. Ran `bash scripts/local_check.sh < /dev/null` for the whole repo,
    ALONE, with no other command running concurrently -- all six
    checks passed clean.
11. Re-ran every regression named in this session's own resume brief:
    Ch4/L2 10/10, Ch7 8/8, Ch8 9/9, Ch9 9/9, Ch10 9/9, Ch11 9/9, and
    Modules 1-5's own assessments (4/4, 5/5, 3/3, 3/3, 4/4
    respectively) -- all unchanged, all green.
12. Committed Chapter 12, the L3 Independent project, the Module 6
    assessment, and all wiring/audit/state changes locally -- no
    remote added, nothing pushed, matching every prior session's
    explicit local-only instructions.

## Chapter 12 — COMPLETE

- `lesson.html`: 60 lines match `<pre\|<code` (120 total tag
  occurrences via `-o`), meeting the 60+ requirement at the course's
  own minimum bar, appropriate for a chapter whose content is
  deliberately more prose/decision-framework-heavy than Chapters
  1-11's code-heavy mechanics. Built around Copperfield Municipal
  Utilities' outage/billing-dispute problem: a four-question decision
  framework (characterization, mechanism selection, a reliability/cost
  budget, a trade-off defense) run in a fixed order, an
  architecture-smell check catching both over- and under-engineering
  from the same selected-mechanisms dict, a deliberately bad design
  caught by that check, a contrasting multi-agent-justified worked
  example (Harrowgate), a retroactive check against Chapters 4, 6, and
  11's own already-shipped designs, budget-sensitivity tiers, a
  ten-case snap-judgment battery, Chapter 7/8's own harnesses reused
  unchanged to instrument the chosen design, a five-system cross-check,
  and the assembled Architecture Decision Record. Section 21 states
  this chapter's own L3 decision explicitly. Ran no live Ollama call,
  by design, with the reasoning stated in Section 2.
- `quiz.html`: 10 fill-in-the-blank questions.
- `interview-questions.html` + `.md`: 10 questions across
  beginner/intermediate/senior/architect, including a dedicated
  architect-level question defending the L3 decision.
- `exercises/`: Lantern Hill Senior Living scenario, 7 tasks, 17
  points. `solution.py` verified 17/17; `starter.py` verified 1/17
  with no crash. `ai-paired.html` uses a third scenario (Vantage Peak
  Ski Resorts).
- `practice/`: 8 independent diagnostic scenarios (abstract system
  names, not full orgs, matching this chapter's own convention).
  `solution.py` verified 8/8; `starter.py` verified 0/8 with no crash.
  `ai-paired.html` uses a ninth scenario ("ScopeCreep," employer left
  unnamed).
- `project/` (**the L3 Independent project — SHIPPED, closing a
  five-session deferral**): Driftlight Energy Cooperative, a
  demand-response energy cooperative needing memory (a pledge set at
  enrollment persists to a later, separate event), guardrails (a
  fail-closed credit-approval threshold), reliability measurement,
  cost control, and the operating layer (idempotent credits for
  unattended overnight events) -- a genuinely richer scenario than the
  lesson's own Copperfield. Deliberately NO `starter.py`, per L3's own
  "no scaffold" definition. `solution.py` characterizes, selects
  mechanisms, states a budget, implements it as real code, and PROVES
  the budget is met with a real measured harness. Scores 12/12.
  `RUBRIC.md` included. `ai-paired.html` uses a fourth scenario
  (Mirelake Water Authority).
- **Module 6's own assessment** ("architecture-design exercise,"
  scoped to Chapter 12 alone per the curriculum map's explicit
  Ch.12/Ch.13 split): `assessments/module-assessments/module-6-
  architecture-design-exercise/`, reusing Chapter 12's own framework
  functions applied to a sixth scenario (Alderwood Transit
  Cooperative). `solution.py` 6/6; `starter.py` 0/6, no crash.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect
  Chapter 12 live, Module 6 in progress.

## Chapter 13 Brief — CLOSED (built in Session 13; the course is complete)

**Status: DONE.** This was the Session 12 hand-off brief for Chapter 13.
It was built in full in Session 13 (see "Session 13" and "Chapter 13 —
COMPLETE" below). There is no next recommended task: this is the final
chapter of the course, and no Chapter 14 exists. The brief is kept below
as a historical record of what Chapter 13 was specified to do.

Read this whole section before writing anything. It is written to be
picked up cold, with zero memory of Session 12.

**What's already true when this session starts:** Chapters 1-12 are
live and complete. Modules 1-5 are all **Complete**. Module 6 is **In
Progress** — Chapter 12 shipped the architecture-decision framework,
Module 6's own Chapter-12-scoped assessment, AND the L3 Independent
project (closing a five-session deferral). The reader now has every
mechanism (Ch1-11) AND the decision layer for choosing among them
(Ch12). Chapter 13 is this course's FINAL chapter and its capstone.

**What this chapter must do, per `docs/curriculum/CURRICULUM_MAP.md`:**
Chapter 13 is the **L4 Architecture Challenge** — "design and defend a
complete multi-component autonomous agent system; business/system
problem only" (Level 4, Architect difficulty). Unlike L1-L3, which
each shipped as or alongside a numbered chapter's own project, L4 IS
the entire chapter's deliverable — there is no separate "lesson vs.
project" split the way Chapters 1-12 had; the capstone's problem
statement, its required deliverable, and its grading rubric are
Chapter 13's whole content. Concretely, this likely means:
- **A multi-component problem, not a single-agent one.** Per the
  curriculum map's own learning-outcome #10 ("design and defend a
  complete autonomous agent system architecture for a realistic
  multi-component product"), the capstone's own problem statement
  should plausibly need MORE than Chapter 12's own Copperfield/
  Driftlight/Alderwood single-agent examples — likely genuinely
  justifying multi-agent coordination (Ch9-10) alongside the
  single-agent mechanisms, so the reader exercises the FULL mechanism
  inventory's range, not just the subset Chapter 12's own three
  worked scenarios happened to need.
- **The deliverable is a full Architecture Decision Record PLUS a
  working reference implementation**, the same two-part shape Chapter
  12's own L3 project just proved out (design + real, instrumented
  code), scaled up to a multi-component system. Reuse
  `characterize_problem`/`select_mechanisms`/`reliability_cost_budget`/
  `architecture_smell_check`/`build_adr` from Chapter 12's own
  `project/solution.py` by import, exactly like Module 6's own
  assessment and the L3 project itself both already did — do not
  redefine these functions a third time.
- **The capstone rubric is Chapter 13's own grading document** —
  confirm its exact name and scope against
  `docs/curriculum/CURRICULUM_MAP.md`'s Module 6 line ("capstone
  rubric (Ch. 13, architecture challenge, Level 4)") before building
  it, and place it in `assessments/architecture-challenges/` — this
  session confirmed that directory is reserved for exactly this
  deliverable (see `quality-audits/chapter-12-audit.md`'s Module 6
  section for the full reasoning), so Chapter 13 should actually use
  it, not route the capstone through `module-assessments/` instead.

**Scenario constraints:** pick a fresh fictional organization NOT on
the running exclusion list in `quality-audits/chapter-12-audit.md`
(currently 50 orgs — see that file for the full list). Extend it,
don't restart it. Chapter 13's own capstone material may reasonably
reference MULTIPLE prior chapters' scenarios by name as worked
examples or as components of the capstone's own larger system (e.g.,
"this capstone's dispatch layer reuses Harrowgate's own peer-agent
shape from Chapter 10-11") without that counting as a fresh org
needing exclusion — only a genuinely NEW scenario built for the
capstone's own problem statement needs a fresh name.

**Live Ollama discipline, if used at all:** Chapter 12's own session
ran NO live model call and disclosed exactly why (the skill being
exercised is judgment against written facts, not a model's live
behavior) — the capstone may have the same property (a design-and-
defend exercise), or it may genuinely need a live call if the
reference implementation includes a real agent loop as part of
proving the architecture out. Decide this explicitly and state the
reasoning either way, the same as Chapter 12 did. If a live call is
used: warm Ollama with a SINGLE background request
(`curl -s localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'`),
then run ONE sanity call before any lesson code — do NOT launch a
second warm-up or live request concurrently (Chapter 10's own session
found two concurrent warm-ups raced and cost a 314s cold start).
Budget up to 450s per live call, capture real transcripts, disclose
honestly.

**Build steps:**

1. Re-read `docs/curriculum/CURRICULUM_MAP.md`'s Module 6 section, its
   Chapter Roadmap table, its full 10-item learning-outcome ladder, and
   its Projects section (L1-L4) in full before building anything —
   confirm the exact capstone title ("Capstone: Designing and
   Defending an Autonomous Agent System") and its Level 4 scope.
2. Re-read Chapter 12's own `lesson.html` in full (its four-question
   framework, its architecture-smell check, its ADR assembly) and
   `project/solution.py` (the functions to import, not redefine) —
   this is the toolkit the capstone applies at full scale, not a new
   invention.
3. Design the capstone's own problem statement: a realistic,
   multi-component business/system problem that plausibly needs
   several of Ch1-11's mechanisms together, including — if genuinely
   justified by the problem's own facts, not by habit — multi-agent
   coordination.
4. Build `lesson.html` (or the capstone's own equivalent primary page
   — confirm the right file name/shape for a chapter whose
   deliverable IS the project, not a separate lesson) to the same 60+
   `<pre>`/`<code>`-line density bar every prior chapter held, verified
   with `grep -c '<pre\|<code' lesson.html` before calling it done.
5. Build the capstone deliverable: a full Architecture Decision
   Record for the chosen multi-component problem, PLUS a working
   reference implementation that proves the chosen design out (reusing
   Chapter 12's own framework functions and, where genuinely needed,
   Chapters 1-11's own mechanisms by import or by pattern), PLUS the
   quiz/interview-questions/exercises/practice file set this course's
   every prior chapter has shipped — confirm with `CURRICULUM_MAP.md`
   whether the capstone's own unique, whole-chapter-is-the-project
   shape changes any of this set, and say so explicitly if it does.
6. Build the **capstone rubric** in `assessments/architecture-
   challenges/` (confirmed reserved for exactly this in Chapter 12's
   own audit) — this is Chapter 13's own grading document, separate
   from Module 6's Chapter-12-scoped assessment that already shipped.
7. `assets/chapters-data.js`: add Chapter 13's real `path` once its
   primary page exists.
8. Update `docs/curriculum/index.html`: convert Chapter 13's card from
   a non-linked "Planned" element to a linked chapter card. Module 6's
   feature card moves from "In Progress" to **"Complete"** — this is
   the LAST chapter in the entire course, so Module 6 completing also
   means the WHOLE COURSE is complete.
9. Update root `index.html`'s `hero-stats`: chapter count to **13 of
   13**, module-complete count to **6 of 6**. Update the "Chapters
   1-12" intro paragraph to reflect all 13 chapters live and every
   module complete. Consider whether a closing/completion note
   (e.g., a "course complete" banner or a capstone-specific call to
   action) belongs on the home page now that this is the final
   chapter — this is the first session where that question is live,
   so make an explicit decision and state it, rather than silently
   leaving the page's existing "in progress" framing unchanged by
   default.
10. Write `quality-audits/chapter-13-audit.md` following
    `chapter-12-audit.md`'s exact format. Extend (don't restart) the
    exclusion list.
11. Run `bash scripts/local_check.sh < /dev/null` **alone**, with no
    other repo command running concurrently.
12. Re-run every regression, each must be unchanged:
    - `chapters/chapter-04-memory-and-state/project/solution.py` (L2): 10/10
    - `chapters/chapter-07-evaluating-agent-reliability/project/solution.py`: 8/8
    - `chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py`: 9/9
    - `chapters/chapter-09-multi-agent-orchestration-patterns/project/solution.py`: 9/9
    - `chapters/chapter-10-multi-agent-coordination-and-communication/project/solution.py`: 9/9
    - `chapters/chapter-11-operating-agents-in-production/project/solution.py`: 9/9
    - `chapters/chapter-12-designing-agent-architectures/project/solution.py` (L3): 12/12
    - `assessments/module-assessments/` (Modules 1-6's own assessments):
      all must still pass their own solutions.
13. Update this file: "Last updated" line, a new "Session 13" section,
    a "Chapter 13 — COMPLETE" section, and a closing course-complete
    summary (there is no Chapter 14 hand-off — this is the final
    chapter). Then end the session.

**Do NOT** re-teach any of Chapters 1-12's own mechanics or re-derive
Chapter 12's own decision framework from scratch — import and apply
it. Chapter 13's job is proving the reader can use everything this
course has built, together, on one new, sufficiently complex problem,
end to end, and defend the result in writing.

**The L3 Independent project question is now CLOSED** — it shipped at
Chapter 12 (see `docs/curriculum/CURRICULUM_MAP.md`'s project-ladder
section and `quality-audits/chapter-12-audit.md`). Chapter 13's own
session does not need to revisit it; only L4 (the capstone itself)
remains open.

## Session 13 — Chapter 13, the Capstone (L4), and the Course Closing (2026-10-04)

**What was built, in order:**

1. Read this file's full Chapter 13 brief, `docs/curriculum/CURRICULUM_MAP.md`
   (Module 6, Chapter Roadmap, Projects L1-L4), `chapter-12-audit.md`'s
   50-org exclusion list, Chapter 12's own `lesson.html`, `project/solution.py`,
   and the Module 6 assessment's `importlib` reuse pattern.
2. Designed the capstone problem: **Thornwick Marketplace Collective**, a
   fictional artisan marketplace with THREE coordinating components — a
   conversational Buyer Concierge (memory of a buyer's allergy preference),
   an overnight Maker Fulfillment batch, and a Fraud & Dispute Review process
   (fail-closed refund guardrail, free-text dispute explanation). Buyer
   Concierge and Maker Fulfillment race on one shared inventory ledger. This
   fires BOTH Chapter 9's dispatch test AND Chapter 10's coordination test,
   and all EIGHT Chapter 1-11 mechanisms come out load-bearing at once — the
   property no prior chapter's worked example had.
3. Built `project/solution.py` (the L4 deliverable). It IMPORTS Chapter 12's
   five framework functions via `importlib` (not redefined a third time),
   then implements every selected mechanism as real code: `MemoryStore`
   (proven across two separate instantiations), `InventoryLedger.try_claim`
   (a locked claim-check, proven by a real two-claim race), `apply_refund`
   (fail-closed guardrail), `idempotency_key` + `commit_once` (exactly-once
   overnight commit), `grounded_reflect` (grounded check on free text), and a
   deterministic reliability/cost harness across three task types. Scores
   **14/14**.
4. Built `project/README.md` (full problem statement), `project/index.html`,
   `project/ai-paired.html`. Deliberately **no** `project/starter.py` and **no**
   `project/RUBRIC.md` — L4, like L3, is "business/system problem only," and
   the grading rubric lives in `assessments/architecture-challenges/`.
5. Built `lesson.html` as the walkthrough of that build (60 `<pre>`/`<code>`
   matches via `grep -c`, meeting the minimum; 121 tag occurrences). Every
   output block was captured from real execution, not written from memory.
6. Built the standard per-chapter file set, adapted: `quiz.html` (10 fib
   questions), `interview-questions.md` + `.html` (10 questions across four
   levels, including an architect-level defense of why Thornwick is a
   legitimate L4 and not a relabeled L3), `exercises/` (a two-component
   SUBSET of Thornwick, `solution.py` 17/17, `starter.py` 0/17 no crash,
   `ai-paired.html`, `index.html`, `README.md`), `practice/` (eight
   abstract-named scenarios, `solution.py` 8/8, `starter.py` 0/8 no crash,
   `ai-paired.html`, `index.html`, `README.md`).
7. Built the capstone rubric: `assessments/architecture-challenges/RUBRIC.md`
   (five criteria, 5 points each, 25 total, passing bar 20/25 with zero
   criteria at 0) plus `assessments/architecture-challenges/README.md`.
8. Wired the site: `assets/chapters-data.js` (Chapter 13's real `path`),
   `docs/curriculum/index.html` (Chapter 13 card linked "Live", Module 6
   "Complete", the stale intro paragraph corrected), root `index.html`
   (see the course-complete decision below), and `assets/style.css` (one new
   `.course-complete-banner` rule).
9. Wrote `quality-audits/chapter-13-audit.md` with an honest self-critique,
   the Ollama decision, the scenario/exclusion list extended to 51 orgs,
   the density decision, and the capstone-shape decision.
10. Ran `bash scripts/local_check.sh < /dev/null` ALONE, with nothing else
    running — all six checks passed clean.
11. Re-ran every regression — all unchanged (see below).

**Ollama decision: NO live model call.** Stated and reasoned in `lesson.html`
Section 2 and `quality-audits/chapter-13-audit.md`. The capstone's own skill
is architecture judgment and proof-of-design against written facts, the same
property Chapter 12's L3 project (Driftlight) had — which also implemented
real memory/guardrail/idempotency code with zero live calls. A live call
would add nothing the deterministic harness does not already prove, and would
make grading depend on a running Ollama server. No warm-up, sanity check, or
live request was made.

**Home-page course-complete decision: YES, add one.** Made explicitly, not by
default. Changes to root `index.html`: the hero eyebrow reads "complete, all
13 chapters" (not "in progress"); the hero lede now describes a complete
course ending in the capstone; the hero stats read **13 of 13 chapters live**
and **6 of 6 modules complete**; the primary CTA "Go straight to the capstone"
replaces a secondary one; a yellow `course-complete-banner` (one sentence,
linking to the capstone and the roadmap) sits directly beneath the hero; and
the "All Chapters" intro paragraph describes all 13 chapters and all six
modules as live. Kicker "Learning path, in progress" → "Learning path,
complete".

**Regression check (all unchanged, re-run this session, each alone):**

- Ch4 / L2 `chapters/chapter-04-memory-and-state/project/solution.py`: **10/10**
- Ch7 `chapters/chapter-07-evaluating-agent-reliability/project/solution.py`: **8/8**
- Ch8 `chapters/chapter-08-cost-and-latency-control-of-agent-loops/project/solution.py`: **9/9**
- Ch9 `chapters/chapter-09-multi-agent-orchestration-patterns/project/solution.py`: **9/9**
- Ch10 `chapters/chapter-10-multi-agent-coordination-and-communication/project/solution.py`: **9/9**
- Ch11 `chapters/chapter-11-operating-agents-in-production/project/solution.py`: **9/9**
- Ch12 / L3 `chapters/chapter-12-designing-agent-architectures/project/solution.py`: **12/12**
- Module 1-6 assessments: **4/4, 5/5, 3/3, 3/3, 4/4, 6/6**
- New in Session 13: Ch13 `project/solution.py` **14/14**; Ch13 `exercises/solution.py` **17/17** (starter 0/17); Ch13 `practice/solution.py` **8/8** (starter 0/8); capstone rubric (`assessments/architecture-challenges/RUBRIC.md`) self-graded against the reference implementation **25/25**.

## Chapter 13 — COMPLETE

- `lesson.html`: 60 lines match `<pre\|<code` (121 total tag occurrences),
  meeting the 60+ requirement. Adapted, not copied, from Chapter 12's own
  density pattern — see `quality-audits/chapter-13-audit.md` for why.
- `quiz.html`: 10 fill-in-the-blank questions.
- `interview-questions.html` + `.md`: 10 questions across beginner,
  intermediate, senior, and architect levels.
- `exercises/`: Thornwick subset (Buyer Concierge + Fraud Review, no Maker
  Fulfillment). `solution.py` 17/17; `starter.py` 0/17 no crash.
- `practice/`: eight abstract-named multi-component scenarios. `solution.py`
  8/8; `starter.py` 0/8 no crash.
- `project/` (**the L4 Architecture Challenge — the capstone itself**):
  Thornwick Marketplace Collective. `solution.py` 14/14; `README.md` problem
  statement; `ai-paired.html` (second, unnamed marketplace). No `starter.py`,
  no `project/RUBRIC.md` — the rubric is in `assessments/architecture-challenges/`.
- **Capstone rubric**: `assessments/architecture-challenges/RUBRIC.md`, the
  curriculum map's "capstone rubric (Ch. 13, architecture challenge, Level 4)"
  — the directory `chapter-12-audit.md` confirmed reserved for exactly this.
- Wired into `assets/chapters-data.js` with a real `path`;
  `docs/curriculum/index.html` and root `index.html` both reflect Chapter 13
  live and Module 6 Complete.

## Course Complete — Closing Summary

**Agentic AI for Everyone** is complete: 13 chapters, 6 modules, 4 project
levels (L1 Guided, L2 Assisted, L3 Independent, L4 Architecture Challenge),
and one capstone rubric, all live, all local-only (nothing pushed to
GitHub, matching every session's explicit instructions).

- **Module 1 — Foundations of the Agent Loop** (Ch 1-2): the perceive-reason-
  act-observe loop; planning and task decomposition.
- **Module 2 — Giving Agents Capabilities** (Ch 3-4): tool use and function
  calling; memory and state.
- **Module 3 — Making Agents Reliable** (Ch 5-6): reflection and self-
  correction; guardrails and safety.
- **Module 4 — Measuring and Controlling Agents** (Ch 7-8): reliability
  evaluation; cost and latency control.
- **Module 5 — Multi-Agent Systems** (Ch 9-11): orchestration patterns;
  coordination and communication; operating agents in production.
- **Module 6 — Architecture and Capstone** (Ch 12-13): the architecture-
  decision framework (Ch 12, L3 Independent project shipped there); and the
  L4 Architecture Challenge capstone (Ch 13, Thornwick Marketplace
  Collective) — a full Architecture Decision Record plus a working,
  instrumented reference implementation for a system that needs the entire
  mechanism inventory at once.

**What the course gives a reader:** a working, verified mental model of an
autonomous agent as a SYSTEM — every mechanism built from scratch in
readable Python with no heavy framework dependency, every mechanism proven
by code rather than asserted in prose, and a decision layer (Ch 12) for
choosing which mechanisms a given problem actually needs, defended in
writing (Ch 13). Every chapter's own harness is deterministic and offline,
so grading never depends on a running model server; live Ollama calls were
used only where a chapter's own skill required a model's live behavior, and
each such call was disclosed.

**Honest limits, stated plainly so a future reader can judge the course's own
claims:** the harnesses are deterministic and synthetic by design, so their
measured numbers prove the mechanisms are wired correctly, not that a real
production model meets the same budgets; `grounded_reflect` is a substring
check, not a semantic verifier; and the smell check only flags missing
mechanisms plus a short list of over-engineering cases. These limits are
recorded in each chapter's own audit, not hidden.

**Where to go next (outside this course):** the sibling courses named in
`docs/discovery-notes.md` cover what this course deliberately deferred —
deep evaluation methodology (`llm-evaluation-for-everyone`), context-window
construction (`context-engineering-for-everyone`), and infrastructure-layer
production engineering (`ai-engineering-for-everyone`).

The course is closed. There is no Chapter 14.
