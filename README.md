# Agentic AI for Everyone

Free, interactive course on designing, building, and operating
**autonomous AI agents as systems**: the agent loop (perception,
reasoning, action, observation), planning and task decomposition, tool
use and function calling, memory and state, reflection and
self-correction, guardrails and safety for autonomous systems,
multi-agent orchestration and coordination, evaluating agent
reliability, and cost/latency control of agent loops — closing with a
capstone that designs and defends a complete autonomous agent system.

🔗 **Repo:** <https://github.com/TechNaom/agentic-ai-for-everyone>
🔗 **Live UI:** <https://technaom.github.io/agentic-ai-for-everyone/>
*(GitHub Pages not yet enabled)*

This course follows the same philosophy as the rest of the TechNaom
"for Everyone" ecosystem:

- Plain-language first, without hiding the real engineering.
- One chapter at a time, validated before scaling.
- No signup required to *read or run* the course. Hands-on chapters
  that need a real model run against a local, open-source model via
  [Ollama](https://ollama.com) by default — no API key, no account, no
  per-run cost — with a documented option to point the same code at a
  hosted provider instead.
- Browser-first learning pages.
- Every guardrail and design pattern is tied to a real agent failure
  mode it prevents, never taught as abstract "best practice."
- Hands-on code tested for real before being written into a lesson.
- Interview-ready explanations.
- Strong architecture and trade-off thinking.
- No heavy agent framework required — every concept is taught with
  minimal, readable, from-scratch Python so the underlying mechanism is
  never hidden behind a framework abstraction.

All examples, scenarios, exercises, projects, and thought-process
journals in this course are original.

## What this is

`Agentic AI for Everyone` teaches the autonomous agent loop itself as a
system — the one architectural pattern the rest of the TechNaom
ecosystem only touches in passing. It is not `ai-coding-agents-for-
everyone` (a coding-domain-specific agent), not `mcp-for-everyone` (the
Model Context Protocol itself), not `ai-engineering-for-everyone` (the
broader LLM production-engineering stack), not `llm-evaluation-for-
everyone` (evaluation as its own deep discipline — this course applies
an agent-appropriate evaluation mindset and defers deep methodology to
that course), and not `context-engineering-for-everyone` (what goes
into the context window — this course's memory chapter defers to that
course's methodology). Full reasoning and a verified cross-course
overlap check live in
[`docs/discovery-notes.md`](docs/discovery-notes.md).

## Model/API versions

Hands-on chapters that need a real model use the plain **`openai`**
Python package (`pip install openai`) pointed, by default, at
**Ollama**'s local OpenAI-compatible endpoint — zero cost, zero API
key. A documented option points the exact same code at a hosted
provider (OpenAI, Anthropic, Gemini — all expose OpenAI-compatible
endpoints). See `PROJECT_STATE.md` for the full policy, including this
session's live Ollama reachability check and the documented
intermittent-hang behavior of this sandbox's Ollama install.

## Who this is for

- **`ai-engineering-for-everyone` graduates** ready to move from a
  single well-prompted feature or fixed pipeline to a system where the
  model itself decides what to do next.
- **Backend/platform engineers asked to "add an agent"** to a product,
  who need to understand the new failure modes an autonomous system
  introduces that a normal request/response service doesn't have.
- **`ai-coding-agents-for-everyone` / `mcp-for-everyone` graduates**
  who want the general, domain-independent loop/planning/memory/multi-
  agent architecture underneath the one domain or protocol they've
  already touched.
- **Team leads evaluating whether an agentic approach is the right
  call**, who need to weigh what an agent buys over a fixed pipeline
  against its complexity, reliability, and operating cost.

## Learning path

See [`docs/curriculum/CURRICULUM_MAP.md`](docs/curriculum/CURRICULUM_MAP.md)
for the full module/chapter roadmap, learning outcomes, and project
ladder.

## Repository structure

```text
agentic-ai-for-everyone/
  chapters/            per-chapter lessons, quizzes, labs, interview prep
  docs/curriculum/      curriculum map (source of truth) + styled roadmap
  docs/discovery-notes.md   positioning/scope decisions and reasoning
  templates/            reusable chapter/quiz/lab/project templates
  assessments/          quizzes, written exams, interview questions
  quality-audits/       per-chapter quality gate checklists
  assets/                shared site styling, sidebar, progress, quiz engine
  PROJECT_STATE.md       current build status (read this first)
  AI_HANDOFF.md          for any AI coding assistant picking this up cold
```

## Current status

**Chapter 1 of 13 is live** — "The Agent Loop: Building Your First
Autonomous Agent," the reference chapter the rest of the course's
structure and depth will be built to match. Module 1 (Foundations of
the Agent Loop) is started; Modules 2-6 and Chapters 2-13 are
scaffolded (`.gitkeep`'d directories) and planned per the curriculum
map, not yet built. See `PROJECT_STATE.md` for the full, current
status and the next recommended session's task.

## Projects

Four project levels, from guided to architecture-challenge — see the
curriculum map's Projects section. Chapter 1 ships the course's first,
real L1 Guided project.

## Capstone

Design and defend a complete autonomous agent system for a realistic
multi-component product — loop architecture, planning strategy, tool
surface and failure handling, memory architecture, guardrails, a
reliability/evaluation plan, cost/latency controls, and a defended
single-agent-versus-multi-agent decision — matching the same rigor as
`ai-engineering-for-everyone`'s and `llm-evaluation-for-everyone`'s own
capstones.

## Contributing

Solo-maintained; not open to external PRs. See `CONTRIBUTING.md` if
you're forking this for your own use.

## License

Code is licensed under [MIT](LICENSE). Educational content (lessons,
diagrams, exercises, interview questions) is licensed under
[CC BY 4.0](LICENSE-CONTENT).
