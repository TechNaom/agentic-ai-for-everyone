# Discovery Notes — Agentic AI for Everyone

LAST_REVIEWED: 2026-09-24
Status: Discovery complete for this session. This document is a
documented, reasoned decision, not a confirmed-by-human one — flag any
disagreement and redirect before Chapters 2-13 are built.

## 1. Course vision — what "Agentic AI" means here, and why it's a
   distinct discipline from every existing TechNaom course

The single highest risk for this course is name-collision drift: there
are already four siblings whose names or descriptions could sound like
"this is basically the same course." The discovery task here was not
"pick a plausible scope" — it was to read what each of those four
siblings actually teaches (not just their titles) and draw a boundary
line this course cannot cross without becoming redundant scaffolding
wearing a new title.

**What this course actually owns:** the discipline of designing,
building, and operating an **autonomous AI agent as a system** — an LLM
wrapped in a loop that perceives its environment, reasons about what to
do next, acts (usually via tools), observes the result, and repeats,
with its own memory, its own planning behavior, its own failure modes,
and (once more than one agent is involved) its own coordination
problems. Concretely, this course teaches:

- **The agent loop itself** — perception → reasoning → action →
  observation as a first-class architectural pattern, not an
  implementation detail buried inside a bigger topic. Why a bare LLM
  call is not an agent, what turns it into one (state carried across
  iterations, a decision about what to do next made *by the model*,
  not by the calling code), and where the loop can go wrong (infinite
  loops, thrashing between two actions, silently giving up).
- **Planning and task decomposition** — breaking a high-level goal into
  a sequence or graph of steps, re-planning when a step fails, and the
  trade-offs between a fixed plan decided up front and a plan that
  emerges one step at a time (ReAct-style interleaved reasoning and
  acting).
- **Tool use and function calling** — how an agent decides *which* tool
  to call and *when*, how tool results get folded back into its
  reasoning, and the failure modes specific to tool-calling agents
  (wrong tool chosen, wrong arguments, ignoring a tool's error, calling
  a tool it didn't need).
- **Memory and state** — what an agent needs to remember across loop
  iterations (short-term / working memory) versus across sessions
  (long-term memory), and the concrete engineering trade-offs of each
  (context-window growth, staleness, retrieval cost).
- **Reflection and self-correction** — an agent noticing its own output
  or plan is wrong and revising it, as a designed architectural
  component (a critique step, a self-check prompt, a verifier), not an
  accident of a bigger model being "smart."
- **Guardrails and safety for autonomous systems** — the specific risks
  that appear once a system can *act* on its own (not just generate
  text): runaway loops, unintended side effects from a tool call,
  scope creep beyond the task it was given, and the human-approval /
  sandboxing / rate-limiting patterns that contain them.
- **Multi-agent orchestration and coordination** — when and why to use
  more than one agent (role specialization, parallelism, isolation of
  failure), the coordination patterns (supervisor/worker, pipeline,
  debate/critique pairs), and the new failure modes multi-agent systems
  introduce (miscommunication between agents, duplicated work,
  deadlock).
- **Evaluation and reliability of agents** — *from the systems-design
  side*: what makes an agent's behavior measurable at all (task
  completion rate, trajectory/step correctness, cost per successful
  run), and what to log and instrument so an agent's failures are
  diagnosable. This course teaches an agent-appropriate *evaluation
  mindset* as part of operating the system; it explicitly hands off the
  deep evaluation *methodology* — golden-set construction, statistical
  significance testing, judge-bias mitigation — to
  `llm-evaluation-for-everyone` (see 1.4 below).
- **Cost and latency control of agent loops** — every iteration of an
  agent loop is another model call; this course teaches the
  system-design levers (bounding iteration count, caching, cheaper
  models for cheaper sub-tasks, early-exit conditions) that keep an
  agent's cost and latency bounded in production.

### 1.1 Checked directly against `ai-coding-agents-for-everyone`

Read this session (curriculum map and representative chapters). That
course teaches how to *build a coding agent specifically* — an agent
whose tool surface is a codebase (read/write files, run a shell
command, run tests, use git) and whose domain-specific reasoning is
about code correctness, diffs, and test-driven iteration. Its agent
loop, planning, and tool-use material is real, but it is scoped
entirely to the coding domain: how an agent decides which file to
open, how it verifies a patch against a test suite, how it handles a
failing build.

**This course's boundary:** `agentic-ai-for-everyone` teaches the
*general* agent loop, planning, tool-use, memory, reflection, and
multi-agent patterns as domain-independent architecture — the same
loop that could drive a coding agent, a research agent, a customer-
support agent, or a data-pipeline agent. It uses non-coding scenarios
for its own hands-on chapters specifically so it doesn't read as "the
coding-agent course, generalized" — and it explicitly does not re-teach
codebase-specific tool design (file-diffing, test-running, git
workflows), which stays `ai-coding-agents-for-everyone`'s subject. A
learner who wants to build a coding agent should take that course for
the domain-specific tool design and this course for the underlying loop
architecture that makes any agent (coding or otherwise) work.

### 1.2 Checked directly against `mcp-for-everyone`

Read this session. That course teaches the **Model Context Protocol**
itself — a specific, standardized wire protocol and its client/server
architecture for exposing tools, resources, and prompts to an LLM
application: how to write an MCP server, how a host application
discovers and calls it, transport details (stdio, HTTP+SSE),
authentication, and protocol versioning. It is plumbing: the pipe an
agent's tool calls can travel through, not the reasoning that decides
which tool to call or when.

**This course's boundary:** `agentic-ai-for-everyone`'s tool-use
chapter (Chapter 3) teaches an agent's *decision-making* around tools —
choosing which tool to call, forming correct arguments, handling a
tool's failure — using plain Python function-calling against a local
model, deliberately protocol-agnostic. It does not teach MCP's wire
format, server implementation, or transport layer; where a learner's
agent needs to talk to a real MCP server in production, this course
points to `mcp-for-everyone` rather than re-explaining the protocol.
The two courses are complementary and stackable: `mcp-for-everyone`
teaches the standardized pipe, this course teaches the agent brain
deciding when to use it.

### 1.3 Checked directly against `ai-engineering-for-everyone`

Read this session (curriculum map). That course teaches the full LLM
production-engineering stack broadly — prompting, RAG basics, a
six-layer production pipeline including its own introductory evaluation
harness (Module 3), cost/latency awareness at the level of a single LLM
call, and shipping one feature end to end. Agents appear in that course
only as one *pattern* mentioned in passing on the way to a broader
"production LLM systems" goal, not as the course's own subject.

**This course's boundary:** `agentic-ai-for-everyone` assumes the LLM
production-engineering foundation `ai-engineering-for-everyone` already
teaches (prompting discipline, a basic production mindset, why
evaluation matters) and goes deep on exactly one architectural pattern
that course only gestures at: the autonomous loop, with its own
planning, memory, multi-step tool use, and multi-agent coordination.
Where `ai-engineering-for-everyone` teaches "call the model once (or a
fixed pipeline of a few calls), get a good result, ship it,"
`agentic-ai-for-everyone` teaches "let the model decide, iteratively,
what to call next, and design the system so that loop stays correct,
safe, and bounded."

### 1.4 Checked directly against `llm-evaluation-for-everyone`

Read this session in full (own `docs/discovery-notes.md`, curriculum
map, and Chapter 1). That course teaches evaluation as its own deep
discipline: metric validity theory, golden-set/eval-dataset
construction methodology, human evaluation and inter-annotator
agreement, LLM-as-judge design and a developed bias-mitigation
taxonomy, statistical rigor (sample size, confidence intervals,
significance testing), and task-type-specific evaluation methodology —
explicitly including a chapter on "Evaluating Agents and Tool-Use"
(its own Chapter 11) that evaluates agent *output and trajectory
quality*, and whose own discovery notes name this exact course
(`agentic-ai-for-everyone`, listed there as a "feeds forward" future
course) as the place agent *architecture* itself, as opposed to
evaluating an agent's output, would be taught.

**This course's boundary:** `agentic-ai-for-everyone`'s evaluation
chapter (Chapter 7, "Evaluating Agent Reliability") teaches evaluation
from the *systems-design* side only — what to log, what makes an
agent's behavior observable, and how to reason about reliability while
designing the loop. It explicitly does not re-teach golden-set
sampling methodology, statistical significance testing, or a developed
judge-bias-mitigation playbook; every mention of those techniques in
this course points to `llm-evaluation-for-everyone` by name rather than
re-deriving them. Conversely, this course is where `llm-evaluation-for-
everyone`'s own Chapter 11 should point a learner who wants to
understand agent *architecture* (the loop, planning, memory,
multi-agent coordination) rather than only how to *score* an agent's
existing output.

### 1.5 Checked directly against `context-engineering-for-everyone`

Read this session (curriculum map). That course teaches what goes
*into* the model's context window — retrieval, ordering, compression,
system-instruction design, and evaluating context quality
(input-side, before the model runs) — as its own deep discipline
independent of any particular application architecture (agentic or
otherwise).

**This course's boundary:** an agent's reasoning step is itself a
context-engineering problem (what goes into the prompt at each loop
iteration — the running history, tool results, the current plan), and
this course's chapters reference that fact explicitly, but do not
re-teach context-window construction, retrieval design, or context-
quality evaluation as their own subject — that discipline is assumed
as a given, exactly the way `llm-evaluation-for-everyone` assumes
`ai-engineering-for-everyone` Module 3's harness-building basics. Where
an agent's memory chapter (Chapter 4) needs to decide what to keep in
the agent's working context each turn, it names the trade-off and
points to `context-engineering-for-everyone` for the deep methodology,
rather than re-deriving it.

**The one-sentence differentiator:** every sibling above teaches either
a narrower slice of the agent stack (a specific domain, like
`ai-coding-agents-for-everyone`; a specific protocol, like
`mcp-for-everyone`) or a different axis of the same broader system (LLM
production engineering broadly, like `ai-engineering-for-everyone`;
output evaluation, like `llm-evaluation-for-everyone`; input context,
like `context-engineering-for-everyone`) — this course is the one place
that teaches the autonomous loop itself, end to end, as a system:
perception, reasoning, action, observation, planning, memory,
reflection, guardrails, multi-agent coordination, and the reliability
and cost discipline of operating that loop in production.

## 2. Personas

- **`ai-engineering-for-everyone` graduate ready to go autonomous** —
  can ship a single well-prompted LLM feature or a fixed multi-step
  pipeline, but has never built a system where the model itself decides
  what to do next, iteratively, and doesn't know how to keep that loop
  from running away or silently failing.
- **Backend/platform engineer asked to "add an agent" to a product** —
  comfortable with services and APIs, unfamiliar with the specific new
  failure modes (unbounded loops, tool misuse, runaway cost) an
  autonomous system introduces that a normal request/response service
  doesn't have.
- **`ai-coding-agents-for-everyone` or `mcp-for-everyone` graduate
  wanting the general pattern** — has built (or wired up) one
  domain-specific agent or one MCP server, and wants the underlying
  loop/planning/memory/multi-agent architecture that generalizes beyond
  that one domain or protocol.
- **Team lead evaluating whether an agentic approach is even the right
  call** — needs to understand what an agent architecture actually buys
  over a fixed pipeline, and what it costs in complexity, reliability
  risk, and operating cost, before committing a team to building one.

## 3. Prerequisites

- `python-for-everyone` level Python (or equivalent) — every hands-on
  chapter uses Python.
- `ai-engineering-for-everyone` (soft prerequisite, strongly
  recommended) — this course assumes comfort with basic LLM API calls,
  prompting, and a production mindset, and does not re-teach those from
  zero.
- Helpful, not required: `mcp-for-everyone` (this course's tool-use
  chapter is protocol-agnostic but references MCP as one real-world
  transport option), `context-engineering-for-everyone` (this course's
  memory chapter references but does not re-teach context-window
  construction methodology), `llm-evaluation-for-everyone` (this
  course's evaluation chapter references but does not re-teach eval
  methodology).

## 4. Learning outcomes (beginner → architect ladder)

By the end, a learner can:

1. **(Beginner)** Explain the perception → reasoning → action →
   observation agent loop, build a minimal working agent that runs this
   loop against a local model, and explain precisely why a single LLM
   call is not an agent.
2. **(Beginner/Intermediate)** Decompose a high-level goal into a
   sequence of steps an agent can execute, and re-plan when a step
   fails, distinguishing a fixed up-front plan from an emergent,
   interleaved (ReAct-style) planning loop.
3. **(Intermediate)** Design a tool-calling interface for an agent
   (schema, argument validation, error handling) and diagnose the
   specific ways an agent misuses a tool (wrong tool, wrong arguments,
   ignoring an error).
4. **(Intermediate)** Design an agent's memory architecture — what
   belongs in short-term working state versus long-term persisted
   memory — and reason about the context-growth and staleness costs of
   each choice.
5. **(Intermediate/Advanced)** Add a reflection/self-correction step to
   an agent loop and show, with real before/after traces, the class of
   error it catches that a non-reflective loop misses.
6. **(Advanced)** Design guardrails for an autonomous agent — iteration
   bounds, human-approval checkpoints, sandboxing, rate limiting — and
   explain which specific failure mode each guardrail contains.
7. **(Advanced)** Design a reliability/observability plan for an agent
   in production (what to log, what "success" means operationally) and
   apply agent-appropriate evaluation methodology, correctly citing
   `llm-evaluation-for-everyone` for the deeper statistical/judge-design
   methodology rather than re-deriving it.
8. **(Advanced)** Apply concrete cost- and latency-control techniques
   (iteration bounding, model tiering, caching, early exit) to keep an
   agent loop's production cost and latency bounded.
9. **(Advanced/Architect)** Design a multi-agent system: choose a
   coordination pattern (supervisor/worker, pipeline, debate/critique)
   for a given problem, and reason about the new failure modes
   (miscommunication, duplicated work, deadlock) multi-agent systems
   introduce.
10. **(Architect)** Design and defend a complete autonomous agent
    system architecture for a realistic, multi-component product (the
    capstone) — loop design, planning strategy, tool surface, memory
    architecture, guardrails, evaluation plan, and cost controls,
    trading off single-agent versus multi-agent design.

## 5. Stack decision (hands-on chapters)

No hard dependency on a paid API. Mirrors `ai-coding-agents-for-
everyone`'s own approach: hands-on code runs against **local Ollama by
default**, via the plain **`openai`** Python client pointed at Ollama's
OpenAI-compatible endpoint (`base_url="http://localhost:11434/v1"`),
with a documented option to swap in a hosted provider (OpenAI,
Anthropic, Gemini all expose an OpenAI-compatible endpoint, so the same
code runs unchanged against any of them by swapping `base_url` and the
API key). No heavy agent framework (LangChain, LangGraph, CrewAI,
AutoGen, etc.) is a required dependency anywhere in the course — every
concept (the loop, planning, tool-calling, memory, reflection,
multi-agent coordination) is taught with minimal, readable, from-
scratch Python so the mechanism is never hidden behind a framework
abstraction. Frameworks may be named and briefly mapped to ("this is
what LangGraph's state machine is doing under the hood") but are never
required to complete a chapter. Full reasoning in `PROJECT_STATE.md`'s
Architecture Decisions.

This sandbox has a documented intermittent Ollama hang (one call took
432s during a sibling course's build). Every hands-on chapter treats
live model calls as illustrative, not gate-load-bearing: real output is
captured and shown once, up to a 450s budget per call, and the lesson
never idle-blocks waiting on a hung call — it shows the captured
transcript instead of re-running live on every read.

## 6. Course size

13 chapters, 6 modules — the ecosystem's established sizing for a
focused, emerging-topic course (matching `mcp-for-everyone`,
`ai-coding-agents-for-everyone`, `ai-security-for-everyone`,
`ai-engineering-for-everyone`, `context-engineering-for-everyone`, and
`llm-evaluation-for-everyone`). See `docs/curriculum/CURRICULUM_MAP.md`
for the full module/chapter breakdown.

## 7. Capstone

Chapter 13 requires the learner to take a realistic, given multi-
component product brief (e.g., a research-and-report agent that must
plan a multi-step investigation, call several tools, remember findings
across steps, and know when to stop) and produce a complete agent
system design: loop architecture, planning strategy, tool surface and
failure handling, memory architecture, guardrails, a reliability/
evaluation plan (correctly deferring to `llm-evaluation-for-everyone`
for deep methodology), cost/latency controls, and — if the brief
warrants it — a defended single-agent-versus-multi-agent decision. This
matches the ecosystem's established L4 capstone rigor (business/system
brief only, no planted single right answer, trade-offs documented and
defended).

## 8. Cross-course overlap check (explicit, verified this session)

Checked this session by reading each neighbor's own curriculum map and,
for the highest-risk neighbors, representative chapter content:

- `ai-coding-agents-for-everyone` (curriculum map + representative
  chapters read): deep on a *coding*-domain agent specifically
  (file/test/git tool surface, code-correctness reasoning). No content
  found teaching the general, domain-independent agent loop, planning,
  memory, or multi-agent coordination patterns as their own subject.
- `mcp-for-everyone` (curriculum map read): deep on the MCP protocol
  itself (wire format, server implementation, transport,
  authentication). No content found on an agent's own reasoning about
  which tool to call or when — that decision-making layer is this
  course's subject, MCP is one possible transport underneath it.
- `ai-engineering-for-everyone` (curriculum map read): deep on the
  broader LLM production-engineering stack (prompting, a six-layer
  pipeline, an introductory evaluation harness). Agents mentioned only
  in passing as one pattern; no dedicated agent-loop, planning-,
  memory-, or multi-agent architecture content found.
- `llm-evaluation-for-everyone` (own discovery notes, curriculum map,
  and Chapter 1 read in full): deep on evaluation *methodology*
  (metric validity, golden sets, judge design and bias, statistics,
  task-type evaluation, including an "Evaluating Agents and Tool-Use"
  chapter scoped explicitly to output/trajectory *evaluation*, not
  agent *architecture*). Its own discovery notes name this course by
  title as the future home for agent architecture itself — confirming,
  from the sibling's side, the boundary drawn here.
- `context-engineering-for-everyone` (curriculum map read): deep on
  context-window construction and input-side context-quality
  evaluation, architecture-independent. No content found on agent
  loops, planning, tool-use decision-making, or multi-agent
  coordination.

No existing course teaches the general-purpose autonomous agent loop,
planning and task decomposition, tool-use decision-making, memory
architecture, reflection/self-correction, guardrails and safety for
autonomous systems, multi-agent orchestration and coordination, or
cost/latency control of agent loops as a dedicated, domain-independent
subject. This course's scope is confirmed non-duplicative.
