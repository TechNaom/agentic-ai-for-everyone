# PROJECT_STATE.md — Agentic AI for Everyone

Last updated: 2026-09-24 (Session 1 — Discovery, the curriculum map,
the full repository scaffold, and Chapter 1, "The Agent Loop: Building
Your First Autonomous Agent," complete and live, opening **Module 1 —
Foundations of the Agent Loop**. Chapters 2-13 are scaffolded
(`.gitkeep`'d directories), not yet built. Nothing has been pushed to
GitHub — all work is local-only per this session's explicit
instructions.)

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

## Next Recommended Task: Chapter 2 — "Planning and Task Decomposition"

This is written so a fresh Sonnet session, with zero memory of this
one, can pick it up cold.

**Where it sits:** Module 1 — Foundations of the Agent Loop, closing
the module (Chapter 1 opened it). Per
`docs/curriculum/CURRICULUM_MAP.md`, difficulty: Intermediate.

**What it must teach**, per the curriculum map and discovery notes:
breaking a high-level goal into a sequence (or graph) of executable
steps; re-planning when a step fails; the trade-off between a **fixed,
up-front plan** decided before any action happens and an **emergent,
interleaved plan** (ReAct-style: reason about the next single step,
act, observe, reason about the *next* step, never committing to a full
plan in advance). Chapter 1's `run_agent()` already does emergent,
one-step-at-a-time planning implicitly (it never plans more than one
tool call ahead) — Chapter 2's job is to make planning a *visible,
separate, inspectable step* rather than something implicit in the
model's per-turn tool choice, and to show a genuine case where a fixed
up-front plan is the better choice (e.g., a task with known, ordered
sub-steps where re-planning after every single action wastes calls) vs.
a genuine case where emergent planning is better (e.g., a task where an
early step's result changes what later steps should even be).

**Directory already scaffolded:**
`chapters/chapter-02-planning-and-task-decomposition/` with empty
`exercises/`, `practice/`, `project/` subdirs and a `.gitkeep`. No
`lesson.html` etc. exist yet — Chapter 1's own directory is the
complete reference for the exact file set to produce.

**Concrete build steps:**

1. Pick a fresh fictional scenario, distinct from TrailBot/Northbeam
   Outdoors and from Chapter 1's exercises/practice/project orgs
   (Summit Gear Co-op, Fernbrook Ski Patrol, Wavecrest Marina — see
   `quality-audits/chapter-01-audit.md`'s exclusion list, and extend
   it, don't restart it). A natural fit: a multi-step task that
   genuinely benefits from decomposition — e.g., an agent that has to
   research something across multiple sources and assemble a report,
   or plan and execute a multi-stop errand/logistics task with
   real ordering constraints (some steps depend on earlier steps'
   results, some don't).
2. Test every code example for real (local Ollama, `llama3.2:latest`,
   `base_url="http://localhost:11434/v1"`) before writing it into
   `lesson.html`, exactly like Chapter 1's scratchpad-first discipline
   — see `CONTRIBUTING.md`'s non-negotiable rule. Budget up to 450s per
   live call; if a call genuinely can't be captured this session, say
   so explicitly in the lesson text (don't claim a transcript that
   wasn't observed).
3. Build `lesson.html` to the same 60+ `<pre>`/`<code>`-block density
   bar, verified with
   `grep -c '<pre\|<code' chapters/chapter-02-.../lesson.html` before
   calling it done — do not skip this check.
4. Build the full file set matching Chapter 1's exactly: `quiz.html`
   (10 fill-in-the-blank), `interview-questions.html` + `.md` (10
   questions across 4 levels), `exercises/` (8+ tasks, 5+ production-
   gear, `starter.py`/`solution.py` both run and verified — starter
   fails cleanly, solution scores perfect — `README.md`, `index.html`,
   `ai-paired.html`), `practice/` (8+ scenarios, same file set,
   `ai-paired.html`), `project/` (this chapter has no dedicated L1/L2
   project per the curriculum map's project ladder — Chapter 2's own
   project work is folded into the L2 Assisted project that ships
   after Chapter 4 — so `project/` may be a thinner deliverable here;
   check the curriculum map before assuming a full graded project is
   required).
5. Wire Chapter 2 into `assets/chapters-data.js` — add its real `path`
   only once `lesson.html` exists; the module's `examPath` stays
   `null` until a written exam actually exists.
6. Update `docs/curriculum/index.html`'s Chapter 2 card from a
   non-linked "Planned" `<div>` to a linked `<a class="chapter-card">`,
   and update the "Module 1" feature card's status from "In Progress"
   to "Complete" (Chapter 2 closes Module 1).
7. Update root `index.html`'s `hero-stats` chapter/module counts (2 of
   13 chapters, still 1 of 6 modules *complete* — Module 1 completes
   with Chapter 2, so this becomes "1 of 6 modules complete" once
   Chapter 2 ships).
8. Write `quality-audits/chapter-02-audit.md` following
   `chapter-01-audit.md`'s exact format: honest self-critique, the
   extended fictional-org exclusion list, source verification (if any
   external sources are cited), the Ollama check done fresh, and the
   full code-tested-before-writing disclosure.
9. Run `bash scripts/local_check.sh < /dev/null` before considering the
   chapter done — fix anything it flags.
10. Update this file's "Last updated" line, "Session" section, and
    "Next Recommended Task" (rewritten for Chapter 3) before ending the
    session, exactly as this section was written for Chapter 2.

**Do not** re-teach Chapter 1's own agent-loop mechanics from scratch —
assume the reader just finished Chapter 1 and can already build a
working tool-calling loop; Chapter 2's job is adding a genuinely new
capability (visible, inspectable planning) on top of that loop, not
re-explaining perception/reasoning/action/observation.
