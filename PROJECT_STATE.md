# PROJECT_STATE.md — Agentic AI for Everyone

Last updated: 2026-09-28 (Session 4 — Chapter 4, "Memory and State,"
complete and live, **closing Module 2 — Giving Agents Capabilities**.
Module 1 — Foundations of the Agent Loop — and Module 2 are now both
fully complete: Chapters 1-4. Chapter 4's `project/` also ships this
course's numbered **L2 Assisted** project (partial scaffold, per the
curriculum map's project ladder), not a chapter mini-project. Chapters
5-13 are scaffolded (`.gitkeep`'d directories), not yet built. Nothing
has been pushed to GitHub — all work is local-only, matching every
prior session's explicit instructions and this session's own.)

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

## Next Recommended Task: Chapter 5 — "Reflection and Self-Correction"

This is written so a fresh session, with zero memory of this one, can
pick it up cold.

**Where it sits:** Module 3 — Making Agents Reliable, *opening* the
module (per `docs/curriculum/CURRICULUM_MAP.md`, Module 3 covers
Chapters 5-6: "an agent that notices and corrects its own mistakes,
and stays inside safe bounds while doing it"). Per the map, difficulty:
Advanced — the first Advanced-tier chapter in this course (Chapters
1-4 were Beginner/Intermediate). Module 3's own outcome:
"add a reflection/self-correction loop; design guardrails mapped to
specific failure modes" — Chapter 5 owns the reflection half, Chapter
6 the guardrails half. Module 3 is NOT complete until Chapter 6 also
ships — do not mark Module 3 "Complete" in `docs/curriculum/index.html`
or root `index.html` when Chapter 5 alone ships; use "In Progress" the
same way Module 2 was marked while only Chapter 3 was live.

**What it must teach**, per the curriculum map and this course's own
architecture: a self-critique-and-revise step — an agent that produces
a draft response or action, evaluates it against some standard
(correctness, completeness, policy compliance), and revises it before
it's returned or executed, as a genuinely separate, designed
architectural component — not the model "trying harder" via a bigger
prompt. The map's own lab framing: "add a self-critique step and show
a real before/after correction." This should cover: what reflection
actually is (a second, distinct model call or check evaluating the
first call's output, not a retry of the same call), what makes a
reflection step worth its extra cost (catching a real, demonstrable
class of error the first pass alone misses — not reflection for its
own sake), the difference between self-correction that revises an
answer and self-correction that decides to call a different tool or
gather more evidence, and when reflection should NOT run (a
cost/latency trade-off this chapter should name honestly, previewing
Chapter 8 without fully treating it, the same "preview, not full
treatment" pattern Chapter 4 used for its own token-budget-pressure
section referencing Chapter 8).

**Hand-off point:** Chapter 4's own `lesson.html` doesn't have a
dedicated closing hand-off paragraph naming Chapter 5 the way Chapter
2's and Chapter 3's closing sections did — Chapter 4's actual hand-off
to Chapter 5 lives in `project/README.md`'s "What Chapter 5 will do
with this file" section instead (see below). Read that section before
starting; it's the authoritative statement of what Chapter 5 is
expected to build on top of, more precise than a lesson-prose
hand-off would be.

**This chapter MUST extend the existing L2 Assisted project, not start
a new one.** `chapters/chapter-04-memory-and-state/project/` already
exists in full (`README.md`, `RUBRIC.md`, `starter.py`, `solution.py`,
`index.html`, `ai-paired.html`) and ships Hollowridge Wellness Clinic's
CareBot with a `reflect_on_response(draft_response, context)` function
that is currently a **labeled no-op passthrough**, called at the
correct point inside `run_visit_session()` (right before the final
response is returned). Chapter 5's job:

1. Replace `reflect_on_response()`'s **body** — not its call site, not
   `run_visit_session()`'s own structure — with a real self-critique-
   and-revise implementation. A concrete, demonstrable target: CareBot
   drafting a response that recommends/allows scheduling a follow-up
   visit despite an unresolved condition that should have blocked it
   (or should have at least flagged it for review) — reflection should
   catch this class of mistake and revise the draft before it's
   returned, with a real before/after example, the same way Chapter
   1's Cedar Hollow bug and Chapter 4's blind-overwrite bug were real,
   not manufactured.
2. Decide, and build for real, whether this chapter's reflection step
   is a second live-model call (self-critique via a second prompt) or
   a deterministic check-and-revise function (mirroring how Chapters
   1-4's finished agents used deterministic stand-ins for their own
   live-model steps so the assembled file runs without Ollama) — most
   likely both: a live version demonstrated and captured in the
   lesson, a deterministic version in the finished project code for
   gradability, exactly Chapter 4's own Section 6/Section 15 split
   between `promote_check.py`'s live call and `coachbot_agent.py`'s
   deterministic `is_promote_worthy`.
3. Update `chapters/chapter-04-memory-and-state/project/solution.py`
   and `starter.py` only as needed to reflect the new
   `reflect_on_response()` body (the self-check count may need a new
   check or two for reflection-specific behavior) — but the existing
   TODOs 1-3 (working-context merge, fact promotion, composed visit
   flow) must NOT be broken or restructured; Chapter 4's own grading
   contract for those three should still pass unchanged.
4. Chapter 5's OWN `lesson.html`, `quiz.html`, etc. should use a fresh
   scenario for teaching the general reflection mechanism (per this
   course's per-chapter fresh-scenario convention), but must explicitly
   show, in at least one section, the CareBot/Hollowridge extension
   described above — this is the concrete proof the L2 project is
   genuinely being extended, not abandoned in favor of an unrelated
   chapter mini-project.

**Directory already scaffolded:**
`chapters/chapter-05-reflection-and-self-correction/` with empty
`exercises/`, `practice/`, `project/` subdirs and a `.gitkeep`. No
`lesson.html` etc. exist yet — Chapter 4's own directory
(`chapters/chapter-04-memory-and-state/`) is the most recent and
closest-in-shape reference for the exact file set to produce, EXCEPT
for `project/`, which must be extended in place (see above), not
recreated from scratch in the Chapter 5 directory. Confirm which
directory holds the canonical L2 project files before writing anything
— it is `chapters/chapter-04-memory-and-state/project/`, not a new
`chapters/chapter-05-reflection-and-self-correction/project/`.

**Concrete build steps:**

1. Pick a fresh fictional scenario, distinct from every org in
   `quality-audits/chapter-04-audit.md`'s running exclusion list
   (currently: Northbeam Outdoors, Summit Gear Co-op, Fernbrook Ski
   Patrol, Wavecrest Marina, Alderleaf Research Group, Pinehurst
   Realty Group, Thistlewood Veterinary Group, Cobblestone Courier
   Co., Palisade Broadband, Thornbury Insurance Group, Wrenhollow Auto
   Rentals, Kestrel Appliance Service, Larkspur Fitness Studio,
   Driftwood Legal Clinic, Saltmarsh Language Academy, Hollowridge
   Wellness Clinic) — extend that list, don't restart it. A natural
   fit: a system where a draft response/action has a real, checkable
   failure mode a second evaluation pass can catch (a math/logic error,
   a policy violation, an incomplete answer, a recommendation that
   contradicts known constraints) — something genuinely demonstrable,
   not a strawman "the model reflects and magically does better."
2. Re-warm and test every code example for real (local Ollama,
   `llama3.2:latest`, `base_url="http://localhost:11434/v1"`) before
   writing it into `lesson.html`, exactly like Chapters 1-4's
   scratchpad-first discipline — see `CONTRIBUTING.md`'s non-negotiable
   rule. Budget up to 450s per live call, never idle-wait past that.
   **Chapter 4's session pre-warmed Ollama explicitly before writing
   any lesson code and every live call succeeded** — do the same
   (`curl -s localhost:11434/api/generate -d
   '{"model":"llama3.2","prompt":"","keep_alive":"120m"}'`, allow up to
   ~450s if cold) rather than assuming a prior session's warm state
   persists, and disclose honestly (per Chapter 3's precedent) if a
   hang recurs anyway.
3. Build `lesson.html` to the same 60+ `<pre>`/`<code>`-block density
   bar, verified with `grep -c '<pre\|<code' lesson.html` before
   calling it done — do not skip this check.
4. Build the full file set matching Chapter 4's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (8+ tasks, 5+ production-
   gear, `starter.py`/`solution.py` both run and verified), `practice/`
   (8+ scenarios, same file set), and the L2 project EXTENSION
   described above (not a new project folder).
5. `assets/chapters-data.js`: add Chapter 5's real `path` only once
   `lesson.html` exists. Chapters 6-13 stay without a `path`. The
   module's `examPath` stays `null` until a written exam actually
   exists.
6. Update `docs/curriculum/index.html`'s Chapter 5 card from a
   non-linked "Planned" `<div>` to a linked `<a class="chapter-card">`.
   Module 3 ("Making Agents Reliable") should go to **"In Progress"**,
   not "Complete" — Chapter 6 is still needed to close it.
7. Update root `index.html`'s `hero-stats`: chapter count to 5 of 13
   live. Module-complete count stays at 2 of 6 (Module 3 isn't done
   until Chapter 6 ships).
8. Write `quality-audits/chapter-05-audit.md` following
   `chapter-04-audit.md`'s exact format: honest self-critique, the
   extended fictional-org exclusion list, source verification (if any
   external sources are cited), a fresh Ollama check with honest
   disclosure either way, and the full code-tested-before-writing
   disclosure.
9. Run `bash scripts/local_check.sh < /dev/null` before considering the
   chapter done — fix anything it flags.
10. Update this file's "Last updated" line, add a new "Session 5"
    section documenting what was built, move Chapter 5 from "Next
    Recommended Task" into a "Chapter 5 — COMPLETE" section, and
    rewrite "Next Recommended Task" for Chapter 6 ("Guardrails and
    Safety for Autonomous Agents," closing Module 3) with the same
    concrete, cold-pickup detail as this section — including how
    Chapter 6 should extend the L2 project a second time (guardrails
    around the tool-dispatch step, per this chapter's own
    `project/README.md` forward-reference) — before ending the
    session.

**Do not** re-teach Chapters 1-4's own mechanics (the agent loop, tool
selection, argument normalization, differentiated tool failure, or the
short-term/long-term memory split) from scratch — assume the reader
can already build a working, memory-equipped, tool-calling agent;
Chapter 5's job is adding reflection as a genuinely new architectural
layer that evaluates and revises that agent's own output, not
re-explaining what came before it.
