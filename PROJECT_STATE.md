# PROJECT_STATE.md — Agentic AI for Everyone

Last updated: 2026-09-28 (Session 6 — Chapter 6, "Guardrails and Safety
for Autonomous Agents," complete and live, **closing Module 3 — Making
Agents Reliable**. Modules 1, 2, and 3 (Chapters 1-6) are now all fully
complete. This session also extended Chapter 4's L2 Assisted project in
place a third and final time: `run_visit_session()` in
`chapters/chapter-04-memory-and-state/project/` now calls a real
`guardrail_check_booking()` check immediately before
`schedule_followup()` is dispatched — the L2 project is now complete
across Chapters 4-6 (memory, reflection, guardrails). Chapters 7-13 are
scaffolded (`.gitkeep`'d directories), not yet built. Nothing has been
pushed to GitHub — all work is local-only, matching every prior
session's explicit instructions and this session's own.)

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

## Next Recommended Task: Chapter 7 — "Evaluating Agent Reliability"

This is written so a fresh session, with zero memory of this one, can
pick it up cold.

**Where it sits:** Module 4 — Measuring and Controlling Agents,
*opening* the module (per `docs/curriculum/CURRICULUM_MAP.md`, Module 4
covers Chapters 7-8). Chapters 1-6 (Modules 1-3) are all complete.
Chapter 7 owns the evaluation half of Module 4's outcome: "design an
agent reliability/observability plan." Chapter 8 (cost/latency control)
is the module's other half and is NOT this session's job. Difficulty:
Advanced, same tier as Chapters 5-6. Module 4 does **not** become
complete until Chapter 8 also ships — do not mark it "Complete" this
session; "In Progress" is correct once Chapter 7 is live (following
Chapter 3's own precedent for a module's first-of-two chapter).

**What it must teach, and — just as important — what it must NOT
teach:** per `docs/discovery-notes.md` Section 1.4 (read this before
starting), this course's own boundary against `llm-evaluation-for-
everyone` was decided explicitly and confirmed from both sides: that
sibling course's own discovery notes name THIS course
(`agentic-ai-for-everyone`) as the future home for agent
*architecture*, as opposed to evaluating agent *output*. Chapter 7
teaches evaluation from the **systems-design side only**: what makes
agent behavior measurable and observable, and how to reason about
reliability while designing the loop. It must explicitly reference (by
name, not re-derive) `llm-evaluation-for-everyone` for: golden-set/eval-
dataset construction methodology, human evaluation and inter-annotator
agreement, LLM-as-judge design and bias mitigation, and statistical
rigor (sample size, confidence intervals, significance testing) — the
same "defer, don't re-teach" pattern this course's own Chapter 4 used
for `context-engineering-for-everyone`. What IS this chapter's own,
non-duplicative territory, per the curriculum map's own outcome and lab
language: **task success measurement, trajectory/tool-call correctness
(did the agent call the right tools in a sane order, not just "did it
eventually get the right answer"), and multi-turn drift** (does a
long-running agent's behavior degrade across many turns/sessions) —
instrumenting an agent with task-completion and trajectory logging is
the module's own stated lab. A good test while drafting: if a
paragraph would apply equally to evaluating a single, non-agentic LLM
call, it belongs in `llm-evaluation-for-everyone`, not here; if it's
specifically about evaluating a *loop's* behavior over multiple
steps/tools/turns, it belongs here.

**Hand-off point:** Chapter 6's own `lesson.html` doesn't name Chapter
7 directly the way Chapter 5 named Chapter 6 (guardrails and evaluation
are less directly coupled than guardrails and reflection were) — there
is no required "extend this exact mechanism" hand-off comment to find.
Instead, the natural continuity is architectural: Chapter 6's own
`dispatch_tool_call()` / `guardrail_check_booking()` pattern already
produces a structured `tool_trace` (a list of `(tool_name, result)`
pairs) on every run — Chapter 7's own trajectory-logging material has a
ready-made, already-demonstrated data source to build on and reference,
rather than inventing tracing from scratch. Consider opening Chapter
7's lesson by pointing at this continuity explicitly (an agent that
already produces a `tool_trace` is most of the way to being
*measurable*; Chapter 7 is what makes that trace worth something).

**No L2/L3/L4 project work this chapter.** Per
`docs/curriculum/CURRICULUM_MAP.md`'s project ladder, the L2 Assisted
project (Hollowridge Wellness Clinic's CareBot) closed at Chapter 6 —
do NOT extend `chapters/chapter-04-memory-and-state/project/` again.
The next numbered project, **L3 Independent** ("Design and implement a
reliability-instrumented, cost-bounded agent for a given problem, no
scaffold"), ships after Chapter 8, not Chapter 7 — so Chapter 7's own
`project/` directory should be a **chapter mini-project** (the same
"not yet on the numbered ladder" pattern Chapters 2-3 used before the
L2 slot opened at Chapter 4), not a signpost and not a new numbered
scaffold. Build it as a real, standalone `starter.py`/`solution.py`
scaffold with its own structural self-checks, clearly labeled in
`README.md`/`RUBRIC.md` as a chapter mini-project, not the L3 project.

**Module 4 assessment status — check and flag, do not silently skip:**
`docs/curriculum/CURRICULUM_MAP.md` states Module 4's own assessment is
"reliability-plan + cost-control exercise." As of this session,
`assessments/module-assessments/` is **empty across the entire repo** —
no module (including Modules 1-3, already complete) has shipped a
module-level assessment file yet. This is a pre-existing gap, not
something Chapter 6 introduced, but it should not keep being silently
deferred forever. This session should explicitly decide one of: (a)
build Module 4's assessment now, once both halves (Chapter 7's
reliability-plan component) exist — likely premature until Chapter 8
also ships the cost-control half; (b) explicitly flag in this file's
own next hand-off that a future, dedicated session should audit
`assessments/` across ALL modules once Chapter 8 ships and Module 4
closes, rather than each chapter session continuing to defer it
individually with no plan to ever actually build it. Do not simply
repeat this note verbatim without making an actual decision — pick (a)
or (b) explicitly and say why.

**Concrete build steps:**

1. Pick a fresh fictional scenario, distinct from every org in
   `quality-audits/chapter-06-audit.md`'s running exclusion list
   (currently: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski
   Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst Realty
   Group, Thistlewood Veterinary Group, Cobblestone Courier Co.,
   Palisade Broadband, Thornbury Insurance Group, Wrenhollow Auto
   Rentals, Kestrel Appliance Service, Larkspur Fitness Studio,
   Driftwood Legal Clinic, Saltmarsh Language Academy, Hollowridge
   Wellness Clinic, Briarcliff Bike Rentals, Fenwick Home Repair
   Co-op, Mossgate Dental Group, Millbrook Credit Union, Amberlock
   Self-Storage, Cascadia Home Security) — extend that list, don't
   restart it. A natural fit: a multi-tool, multi-turn agent where
   "did it work" isn't a single yes/no (a research/investigation agent,
   a multi-step booking or diagnosis agent) so task-success and
   trajectory-correctness are genuinely distinct, non-trivial questions.
2. Re-warm and test every code example for real (local Ollama,
   `llama3.2:latest`, `base_url="http://localhost:11434/v1"`) before
   writing it into `lesson.html`, exactly like Chapters 1-6's
   scratchpad-first discipline — see `CONTRIBUTING.md`'s non-negotiable
   rule. Budget up to 450s per live call, never idle-wait past that.
   This session's own calls were all fast (under 16s) despite Chapter
   5's disclosed 413.8s stall the session before it — do not assume
   fast timing is now the norm; pre-warm anyway
   (`curl -s localhost:11434/api/generate -d
   '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'`, allow up to
   ~450s if cold), and disclose honestly (per Chapters 3, 5, and 6's own
   precedent) whatever actually happens.
3. Build `lesson.html` to the same 60+ `<pre>`/`<code>`-block density
   bar, verified with `grep -c '<pre\|<code' lesson.html` before
   calling it done — do not skip this check.
4. Build the full file set matching Chapter 6's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (8+ tasks, 5+ production-
   gear, `starter.py`/`solution.py` both run and verified), `practice/`
   (8+ scenarios, same file set), and a **chapter mini-project**
   `project/` (real scaffold, not a signpost — see above).
5. `assets/chapters-data.js`: add Chapter 7's real `path` only once
   `lesson.html` exists. Chapters 8-13 stay without a `path`. Module
   4's `examPath` stays `null` until a written exam actually exists.
6. Update `docs/curriculum/index.html`'s Chapter 7 card from a
   non-linked "Planned" `<div>` to a linked `<a class="chapter-card">`.
   Module 4 ("Measuring and Controlling Agents") goes to **"In
   Progress"**, NOT "Complete" — Chapter 8 still has to ship first.
7. Update root `index.html`'s `hero-stats`: chapter count to 7 of 13
   live. Module-complete count **stays at 3 of 6** (Module 4 isn't done
   until Chapter 8 ships) — do not increment it this session.
8. Write `quality-audits/chapter-07-audit.md` following
   `chapter-06-audit.md`'s exact format: honest self-critique, the
   extended fictional-org exclusion list, source verification (this
   chapter likely names `llm-evaluation-for-everyone` — confirm that
   reference is accurate against that course's own current curriculum
   map/chapter list before citing specifics, the same verification
   discipline this course's own discovery-notes work already used), a
   fresh Ollama check with honest disclosure either way, and the full
   code-tested-before-writing disclosure.
9. Run `bash scripts/local_check.sh < /dev/null` before considering the
   chapter done — fix anything it flags.
10. Update this file's "Last updated" line, add a new "Session 7"
    section documenting what was built, move Chapter 7 from "Next
    Recommended Task" into a "Chapter 7 — COMPLETE" section, and
    rewrite "Next Recommended Task" for Chapter 8 ("Cost and Latency
    Control of Agent Loops," closing Module 4) with the same concrete,
    cold-pickup detail as this section, including a final, explicit
    decision on the Module 4 assessment question raised above, before
    ending the session.

**Do not** re-teach Chapters 1-6's own mechanics (the agent loop, tool
selection, memory, reflection/self-correction, or guardrails) from
scratch — assume the reader can already build a working, memory-
equipped, reflection-capable, guardrail-bounded agent; Chapter 7's job
is making that agent's behavior *measurable*, not re-explaining how it
decides what to do.
