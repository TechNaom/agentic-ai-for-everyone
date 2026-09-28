# PROJECT_STATE.md — Agentic AI for Everyone

Last updated: 2026-09-28 (Session 3 — Chapter 3, "Tool Use and
Function Calling," complete and live, opening **Module 2 — Giving
Agents Capabilities** (Module 1 — Foundations of the Agent Loop —
remains fully complete: Chapters 1-2. Module 2 is now in progress:
Chapter 3 live, Chapter 4 still planned). Chapters 4-13 are scaffolded
(`.gitkeep`'d directories), not yet built. Nothing has been pushed to
GitHub — all work is local-only, matching every prior session's
explicit instructions and this session's own.)

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

## Next Recommended Task: Chapter 4 — "Memory and State"

This is written so a fresh Sonnet session, with zero memory of this
one, can pick it up cold.

**Where it sits:** Module 2 — Giving Agents Capabilities, *closing*
the module (Chapter 3, "Tool Use and Function Calling," opened it and
is now live). Per `docs/curriculum/CURRICULUM_MAP.md`, difficulty:
Intermediate. Completing Chapter 4 completes Module 2 — update the
module-complete count in `docs/curriculum/index.html` and root
`index.html` accordingly when this chapter ships.

**What it must teach**, per the curriculum map and discovery notes:
short-term *working* memory (what stays in an agent's context within a
single run — conversation history, tool results so far, the working
plan) versus long-term *persisted* memory (what survives across
separate runs/sessions — facts about a user, past outcomes, learned
corrections), and the real engineering trade-offs between them: what
to keep in-context vs. what to write out to storage, when a working-
memory buffer needs to be summarized or pruned as it grows (token-
budget pressure, a preview of Chapter 8's cost/latency subject, not
its full treatment), what a minimal persisted-memory store actually
looks like in code (a plain dict/JSON-file/SQLite-style key-value
store is enough — no vector database or embedding framework required
to teach the *engineering* decision, matching this course's no-heavy-
framework policy), and how a persisted fact gets retrieved and
correctly merged back into a later run's working context. This course
explicitly **defers deep RAG/embedding-retrieval methodology** to
`context-engineering-for-everyone` (see `docs/discovery-notes.md`'s
cross-course boundary check) — Chapter 4's job is the *architectural*
short-term/long-term split and its trade-offs, not a retrieval-quality
or embedding-similarity deep dive.

**Hand-off point:** Chapter 3's own `lesson.html` closing section
(Section 13's final paragraph) should be read before starting — it
names what Chapter 4 adds ("memory so a plan's outcome can be recalled
in a later session instead of vanishing when a function returns"),
matching the same explicit hand-off convention Chapter 2's closing
section used for Chapter 3. Read it for the exact framing this
session should pick up.

**Project-ladder note, read before deciding whether to build a mini-
project or a real one:** `docs/curriculum/CURRICULUM_MAP.md`'s
"Projects" section states the **L2 Assisted project ships after
Chapter 4** ("Build a multi-tool agent with memory and a reflection
step for a provided scenario, partial scaffold... ships after Ch. 4,
extended through Ch. 5-6's reflection/guardrail material"). This is
different from Chapters 2-3, which both explicitly had no ladder slot
and built a chapter mini-project instead. Chapter 4 is the chapter
where the ladder says the L2 project actually begins — decide, and
state explicitly in `project/README.md` and this file's own "Chapter 4
— COMPLETE" section, whether this chapter's `project/` folder is (a)
the actual start of the L2 Assisted project scaffold (a multi-tool
agent using memory, with reflection deferred to Chapters 5-6 since
that material doesn't exist yet), or (b) still a chapter mini-project
with the real L2 scaffold deferred to Chapter 6 once reflection/
guardrail material exists to extend it through. Don't default to the
mini-project pattern silently just because Chapters 2-3 used it — the
curriculum map's own wording for Chapter 4 is different from theirs.

**Directory already scaffolded:**
`chapters/chapter-04-memory-and-state/` with empty `exercises/`,
`practice/`, `project/` subdirs and a `.gitkeep`. No `lesson.html` etc.
exist yet — Chapter 3's own directory
(`chapters/chapter-03-tool-use-and-function-calling/`) is the most
recent and closest-in-shape reference for the exact file set to
produce.

**Concrete build steps:**

1. Pick a fresh fictional scenario, distinct from every org in
   `quality-audits/chapter-03-audit.md`'s running exclusion list
   (currently: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski
   Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst
   Realty Group, Thistlewood Veterinary Group, Cobblestone Courier
   Co., Palisade Broadband, Thornbury Insurance Group, Wrenhollow Auto
   Rentals, Kestrel Appliance Service) — extend that list, don't
   restart it. A natural fit: a system where a user interacts across
   multiple separate sessions, where something learned or stated in an
   earlier session needs to correctly inform a later one (so the
   short-term/long-term split is real and demonstrable, not a
   strawman) — e.g., a preference stated once that should persist, or
   an outcome from a prior run that should change later behavior.
2. Test every code example for real (local Ollama, `llama3.2:latest`,
   `base_url="http://localhost:11434/v1"`) before writing it into
   `lesson.html`, exactly like Chapters 1-3's scratchpad-first
   discipline — see `CONTRIBUTING.md`'s non-negotiable rule. Budget up
   to 450s per live call, never idle-wait past that. **Chapter 3's own
   session saw both of its live-call attempts fail to return at all
   within that budget** (see `quality-audits/chapter-03-audit.md`) —
   if this recurs, disclose it exactly as Chapter 3 did (state the
   attempt, the timeout, and use deterministic Python for every
   teaching example instead of fabricating a transcript) rather than
   assuming this session's own attempt will succeed just because prior
   sessions' did.
3. Build `lesson.html` to the same 60+ `<pre>`/`<code>`-block density
   bar, verified with `grep -c '<pre\|<code' lesson.html` (Chapter 3
   used this exact method, scoring 70) before calling it done — do not
   skip this check.
4. Build the full file set matching Chapter 3's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (8+ tasks, 5+ production-
   gear, `starter.py`/`solution.py` both run and verified — starter
   fails cleanly, solution scores perfect — `README.md`, `index.html`,
   `ai-paired.html`), `practice/` (8+ scenarios, same file set,
   `ai-paired.html`), and `project/` per the project-ladder note above
   — resolve that question explicitly before building, don't default
   silently.
5. Wire Chapter 4 into `assets/chapters-data.js` — add its real `path`
   only once `lesson.html` exists; the module's `examPath` stays
   `null` until a written exam actually exists. Chapters 5-13 stay
   without a `path`.
6. Update `docs/curriculum/index.html`'s Chapter 4 card from a
   non-linked "Planned" `<div>` to a linked `<a class="chapter-card">`.
   Module 2 ("Giving Agents Capabilities") **should** go to "Complete"
   this time (unlike Chapter 3's session, where Module 2 stayed "In
   Progress" because Chapter 4 wasn't done yet) — this is the chapter
   that closes it.
7. Update root `index.html`'s `hero-stats`: chapter count to 4 of 13
   live, and the module-complete count to 2 of 6 (Module 1 + Module 2
   both complete once this chapter ships).
8. Write `quality-audits/chapter-04-audit.md` following
   `chapter-03-audit.md`'s exact format: honest self-critique, the
   extended fictional-org exclusion list, source verification (if any
   external sources are cited — this chapter may be the first to
   legitimately need one, if it cites any general memory-architecture
   convention; if so, verify it for real, don't assert it uncited),
   the Ollama check done fresh (with an honest disclosure either way,
   following Chapter 3's precedent for what to do if it hangs again),
   and the full code-tested-before-writing disclosure.
9. Run `bash scripts/local_check.sh < /dev/null` before considering the
   chapter done — fix anything it flags.
10. Update this file's "Last updated" line, add a new "Session 4"
    section documenting what was built, move Chapter 4 from "Next
    Recommended Task" into a "Chapter 4 — COMPLETE" section (matching
    how this session moved Chapter 3 from planned to complete), and
    rewrite "Next Recommended Task" for Chapter 5 ("Reflection and
    Self-Correction," opening Module 3) with the same concrete,
    cold-pickup detail as this section, before ending the session.

**Do not** re-teach Chapters 1-3's own tool-calling mechanics (the JSON
schema shape, tool selection, argument normalization, or the three
differentiated failure types) from scratch — assume the reader can
already build a working, robust tool-calling loop; Chapter 4's job is
adding memory as a genuinely new architectural layer on top of that,
not re-explaining tool use.
