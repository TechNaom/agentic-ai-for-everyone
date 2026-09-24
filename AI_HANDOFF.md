# AI_HANDOFF.md — Agentic AI for Everyone

Read this before touching anything in this repo. It's written so any
AI coding assistant can pick this up cold, with zero prior context, and
not redesign decisions that were already made.

## What this repository is

An open-source, free-to-read (and free-to-*run*) technical course
teaching the discipline of designing, building, and operating
**autonomous AI agents as systems**: the agent loop (perception,
reasoning, action, observation), planning and task decomposition, tool
use and function calling, memory and state, reflection and
self-correction, guardrails and safety for autonomous systems,
multi-agent orchestration and coordination, evaluating agent
reliability, and cost/latency control of agent loops — part of the
**TechNaom "for Everyone"** course ecosystem. Follows the same detailed
master course-building prompt as every sibling course.

## This course's own positioning and boundary (non-negotiable)

Full reasoning in `docs/discovery-notes.md`. In short, this course
occupies a deliberately narrow, verified gap against **five** named
siblings — more than most siblings have to check against, because
"agentic" is a word every adjacent course brushes up against:

- **`ai-coding-agents-for-everyone`** builds a *coding-domain-specific*
  agent (file/test/git tool surface, code-correctness reasoning). This
  course teaches the *general, domain-independent* agent loop,
  planning, memory, and multi-agent architecture — the same loop that
  could drive a coding agent, a research agent, or a customer-support
  agent — using deliberately non-coding scenarios so it never reads as
  "the coding-agent course, generalized."
- **`mcp-for-everyone`** teaches the Model Context Protocol itself —
  wire format, server implementation, transport, auth. This course
  teaches an agent's *decision-making* around tools (which to call,
  what arguments, how to handle failure), protocol-agnostic, using
  plain Python function-calling. The two are complementary and
  stackable, not overlapping: MCP is a pipe an agent's tool calls can
  travel through; this course is the brain deciding when to use it.
- **`ai-engineering-for-everyone`** teaches the broader LLM
  production-engineering stack (prompting, RAG basics, a six-layer
  pipeline, an introductory evaluation harness). This course assumes
  that foundation and goes deep on exactly the one pattern that course
  only gestures at: the autonomous, iterative loop.
- **`llm-evaluation-for-everyone`** teaches evaluation as its own deep
  discipline (metric validity, golden sets, judge design and bias,
  statistics, task-type methodology — including its own "Evaluating
  Agents and Tool-Use" chapter, scoped to output/trajectory
  *evaluation*). This course's own evaluation chapter (Chapter 7)
  teaches evaluation from the *systems-design* side only (what to log,
  what makes behavior observable) and explicitly defers deep
  methodology to that course by name, every time. **This is not
  optional or occasional — every mention of evaluation methodology
  beyond "what to instrument" should cite `llm-evaluation-for-everyone`
  rather than re-deriving it.** That sibling's own discovery notes
  (read during this course's own discovery session) already name this
  course as the future home of agent *architecture* — the boundary is
  confirmed from both sides.
- **`context-engineering-for-everyone`** teaches context-window
  construction and input-side context-quality evaluation. This course's
  memory chapter (Chapter 4) references the trade-off but defers deep
  methodology to that course, the same way this course's evaluation
  chapter defers to `llm-evaluation-for-everyone`.

**Every new chapter should continue Chapter 1's practice of stating
this positioning explicitly, by name, in its own lesson text** wherever
its subject sits close to one of these five neighbors — not just in
`docs/discovery-notes.md`. This is the discipline that keeps the course
from drifting into duplicating a sibling course over many sessions, and
it matters more here than in most siblings because this course has more
adjacent neighbors than most.

## Current state (as of 2026-09-24)

**Read `PROJECT_STATE.md` for the authoritative, up-to-date status.**
Short version: **Chapter 1 of 13 is complete and live**, opening Module
1 of 6. Chapters 2-13 are scaffolded (`.gitkeep`'d empty directories
under `chapters/`) and fully specified in
`docs/curriculum/CURRICULUM_MAP.md`, but not yet built.
`PROJECT_STATE.md`'s "Next Recommended Task" section has a complete,
concrete brief for building Chapter 2 — read it before starting any new
chapter work.

## The non-negotiable build disciplines (inherited from every sibling course)

1. **Test every code example for real before writing it into a
   lesson.** Every agent loop, tool-calling harness, memory store,
   reflection loop, guardrail check, or multi-agent orchestrator must
   actually run — against the real `openai` client pointed at a real
   local Ollama server with a real model pulled, where applicable —
   before it goes into `lesson.html`. Never write from memory or adapt
   from an older tutorial. See `CONTRIBUTING.md` for the exact venv
   workflow.
2. **This sandbox's Ollama has a real, observed intermittent hang.**
   Chapter 1's own first live call took 138 seconds; a documented prior
   sibling-course session saw 432 seconds. Treat every live call as
   illustrative, not gate-load-bearing: budget up to 450 seconds, never
   idle-wait past that, and show a captured transcript rather than
   re-running live. Wrap production-facing code with an explicit
   timeout (Chapter 1 Section 11 has the reference pattern).
3. **No heavy agent framework as a required dependency, anywhere.**
   LangChain, LangGraph, CrewAI, AutoGen, etc. may be *named* and
   briefly mapped to ("this is what LangGraph's state machine is doing
   under the hood") but every concept must be teachable and gradable
   with plain Python and the plain `openai` client. This is a standing
   user preference, not a style choice — do not relax it because a
   framework would make a chapter faster to write.
4. **Lesson density is a hard requirement, not a stretch goal.** Every
   `lesson.html` needs 60+ real `<pre>`/`<code>` blocks — actually run,
   actually captured, built as one incrementally-extended agent script
   per chapter (the way Chapter 1 built TrailBot one section at a
   time), not a conceptual essay with occasional snippets. Verify with
   `grep -c '<pre\|<code' lesson.html` before calling a chapter done.
   This ecosystem has shipped under-dense chapters before
   (`ai-coding-agents-for-everyone`, `context-engineering-for-everyone`
   both needed a later retrofit) — don't repeat it.
5. **Grading must work without a live model.** Exercises, practice, and
   project `solution.py` files are graded by deterministic, offline
   scoring — structural self-checks or keyword-substance checks for
   free-text answers — so CI and any learner's machine can grade them
   without a running Ollama server. Where a concept genuinely needs a
   live model, teach it live in the lesson but grade it with a
   deterministic stand-in (see Chapter 1's `FakeModel` pattern in
   `project/starter.py`).
6. **A chapter's own fictional orgs must not collide with any prior
   chapter's.** Each chapter's `quality-audits/chapter-0N-audit.md`
   maintains and extends a running exclusion list — read the most
   recent one before inventing new company names.
7. **No placeholder text, ever, anywhere merged.** No `[insert X]`, no
   Lorem ipsum. `scripts/local_check.sh` scans for this — run it before
   considering any chapter done.
8. **Never add a GitHub remote or push, unless a human explicitly
   instructs it.** This repo was built local-only by explicit
   instruction; `README.md` and other files reference
   `https://github.com/TechNaom/agentic-ai-for-everyone` as
   aspirational text for the eventual public repo, not a live remote.

## File pattern reference

Chapter 1's own directory,
`chapters/chapter-01-the-agent-loop-building-your-first-autonomous-agent/`,
is the complete, canonical reference for every file a chapter needs:
`lesson.html`, `quiz.html`, `interview-questions.html` + `.md`,
`exercises/{README.md,index.html,starter.py,solution.py,ai-paired.html}`,
`practice/` (same set), `project/{README.md,index.html,starter.py,
solution.py,ai-paired.html,RUBRIC.md}`. Copy its shape, not its content,
for every future chapter.

## Where to look for what

- **Course positioning and boundaries**: `docs/discovery-notes.md`
- **Curriculum, module/chapter breakdown, learning outcomes**:
  `docs/curriculum/CURRICULUM_MAP.md` (source of truth) and
  `docs/curriculum/index.html` (styled, must stay in sync)
- **Build status, architecture decisions, next task**:
  `PROJECT_STATE.md`
- **Chapter roster wired to the site**: `assets/chapters-data.js`
  (a chapter is live iff it has a `path` — never set one before the
  chapter's `lesson.html` actually exists)
- **Per-chapter honest self-critique and verification trail**:
  `quality-audits/chapter-0N-audit.md`
- **Reusable HTML skeletons for a new chapter's files**: `templates/`
- **Local pre-push checks**: `scripts/local_check.sh`

## What to do next

Read `PROJECT_STATE.md`'s "Next Recommended Task" section in full — it
specifies Chapter 2, "Planning and Task Decomposition," in enough
concrete detail (scenario constraints, file list, wiring steps, and the
exact commands to verify each requirement) to build it cold.
