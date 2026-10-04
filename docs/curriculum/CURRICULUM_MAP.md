# Agentic AI for Everyone — Curriculum Map

LAST_REVIEWED: 2026-09-24

## Course Size

Focused emerging topic: 13 chapters, 4 projects (L1-L4), 1 capstone —
same sizing model as `mcp-for-everyone`, `ai-coding-agents-for-everyone`,
`ai-security-for-everyone`, `ai-engineering-for-everyone`,
`context-engineering-for-everyone`, and `llm-evaluation-for-everyone`.

## Course Vision

Full reasoning and cross-course overlap check in `../discovery-notes.md`.
In short: this course teaches the discipline of designing, building, and
operating an autonomous AI agent as a system — the agent loop
(perception → reasoning → action → observation), planning and task
decomposition, tool use and function calling, memory and state,
reflection and self-correction, guardrails and safety for autonomous
systems, multi-agent orchestration and coordination, and the
reliability/cost discipline of operating an agent loop in production.
It is not `ai-coding-agents-for-everyone` (a coding-domain-specific
agent), not `mcp-for-everyone` (the MCP protocol itself), not
`ai-engineering-for-everyone` (the broader LLM production-engineering
stack), not `llm-evaluation-for-everyone` (evaluation as its own
discipline — this course applies an agent-appropriate evaluation
mindset and defers deep methodology), and not `context-engineering-
for-everyone` (what goes into the context window).

## Personas

- **`ai-engineering-for-everyone` graduate ready to go autonomous** —
  can ship one well-prompted feature or a fixed pipeline, has never
  built a loop where the model decides what to do next.
- **Backend/platform engineer asked to "add an agent"** — comfortable
  with services, unfamiliar with an autonomous system's new failure
  modes (runaway loops, tool misuse, runaway cost).
- **`ai-coding-agents-for-everyone` / `mcp-for-everyone` graduate**
  wanting the general, domain-independent loop/planning/memory/multi-
  agent architecture underneath the one domain or protocol they've
  already touched.
- **Team lead evaluating whether an agentic approach is the right
  call** — needs to weigh what an agent buys over a fixed pipeline
  against its complexity, reliability, and cost.

## Prerequisites

- Comfortable with Python (`python-for-everyone` level).
- Soft prerequisite, strongly recommended: `ai-engineering-for-everyone`
  (basic LLM API calls, prompting, production mindset).
- Helpful, not required: `mcp-for-everyone` (real-world tool-transport
  option), `context-engineering-for-everyone` (memory chapter's context-
  window trade-offs), `llm-evaluation-for-everyone` (deep evaluation
  methodology this course's own evaluation chapter defers to).

## Learning Outcomes

1. Explain the perception → reasoning → action → observation agent
   loop; build a minimal working agent; explain why a single LLM call
   is not an agent.
2. Decompose a goal into executable steps; re-plan on failure; compare
   fixed up-front planning to emergent, interleaved (ReAct-style)
   planning.
3. Design a tool-calling interface (schema, validation, error
   handling); diagnose wrong-tool, wrong-argument, and ignored-error
   failures.
4. Design an agent's memory architecture (short-term working state vs.
   long-term persisted memory) and reason about its context-growth and
   staleness costs.
5. Add a reflection/self-correction step and demonstrate, with real
   before/after traces, the error class it catches.
6. Design guardrails (iteration bounds, human approval, sandboxing,
   rate limiting) and map each to the specific failure mode it
   contains.
7. Design a reliability/observability plan for an agent in production
   and apply agent-appropriate evaluation, citing
   `llm-evaluation-for-everyone` for deep methodology.
8. Apply cost/latency-control techniques (iteration bounding, model
   tiering, caching, early exit) to bound an agent loop's production
   cost.
9. Design a multi-agent system: choose a coordination pattern
   (supervisor/worker, pipeline, debate/critique) and reason about its
   new failure modes.
10. Design and defend a complete autonomous agent system architecture
    for a realistic multi-component product (the capstone).

## Module Architecture

### Module 1 — Foundations of the Agent Loop
**Purpose:** what makes something an "agent" instead of a single model
call, and how to break a goal into steps.
**Outcomes:** build and run a minimal agent loop; decompose and
re-plan a multi-step goal.
**Chapters:** 1, 2
**Labs:** build a working perception-reasoning-action-observation loop
against a local model; decompose a goal into a step plan and re-plan
after an injected failure
**Assessment:** agent-loop-tracing + planning exercise

### Module 2 — Giving Agents Capabilities
**Purpose:** tool use and memory — how an agent acts on the world and
carries state across steps.
**Prerequisites:** Module 1
**Outcomes:** design a tool-calling interface with real error handling;
design a memory architecture with a defensible short-term/long-term
split.
**Chapters:** 3, 4
**Labs:** build a multi-tool agent and diagnose a live tool-misuse
failure; add persisted long-term memory to an agent and show a session
where it changes the outcome
**Assessment:** tool-interface design + memory-architecture exercise

### Module 3 — Making Agents Reliable
**Purpose:** an agent that notices and corrects its own mistakes, and
stays inside safe bounds while doing it.
**Prerequisites:** Module 2
**Outcomes:** add a reflection/self-correction loop; design guardrails
mapped to specific failure modes.
**Chapters:** 5, 6
**Labs:** add a self-critique step and show a real before/after
correction; add iteration bounds, a human-approval checkpoint, and a
sandboxed tool, then break each on purpose to show the guardrail catch
it
**Assessment:** reliability-and-safety design review

### Module 4 — Measuring and Controlling Agents
**Purpose:** knowing whether an agent is actually working, and keeping
it affordable and fast.
**Prerequisites:** Module 3
**Outcomes:** design an agent reliability/observability plan; apply
cost- and latency-control techniques to a running agent loop.
**Chapters:** 7, 8
**Labs:** instrument an agent with task-completion and trajectory
logging; add iteration bounding, model tiering, and caching to a
loop and measure the before/after cost and latency
**Assessment:** reliability-plan + cost-control exercise

### Module 5 — Multi-Agent Systems
**Purpose:** when and how to coordinate more than one agent, and
running one in production.
**Prerequisites:** Module 4
**Outcomes:** choose and implement a multi-agent coordination pattern;
operate an agent system in a production-shaped setting.
**Chapters:** 9, 10, 11
**Labs:** build a supervisor/worker multi-agent system; build a
pipeline and a debate/critique pair and compare failure modes; add
production operating concerns (retries, timeouts, structured logging)
to a multi-agent system
**Assessment:** multi-agent coordination-pattern exercise

### Module 6 — Architecture and Capstone
**Purpose:** architect-level synthesis — designing and defending a
complete agent system.
**Prerequisites:** Module 5
**Chapters:** 12, 13
**Assessment:** architecture-design exercise (Ch. 12) + capstone rubric
(Ch. 13, architecture challenge, Level 4)

## Chapter Roadmap

| # | Chapter | Module | Difficulty |
|---|---------|--------|------------|
| 1 | The Agent Loop: Building Your First Autonomous Agent | 1 | Beginner |
| 2 | Planning and Task Decomposition | 1 | Intermediate |
| 3 | Tool Use and Function Calling | 2 | Intermediate |
| 4 | Memory and State | 2 | Intermediate |
| 5 | Reflection and Self-Correction | 3 | Advanced |
| 6 | Guardrails and Safety for Autonomous Agents | 3 | Advanced |
| 7 | Evaluating Agent Reliability | 4 | Advanced |
| 8 | Cost and Latency Control of Agent Loops | 4 | Advanced |
| 9 | Multi-Agent Orchestration Patterns | 5 | Advanced |
| 10 | Multi-Agent Coordination and Communication | 5 | Advanced |
| 11 | Operating Agents in Production | 5 | Advanced |
| 12 | Designing Agent Architectures | 6 | Architect |
| 13 | Capstone: Designing and Defending an Autonomous Agent System | 6 | Architect |

## Projects

- **L1 Guided** — Build and trace a minimal single-tool agent loop
  against a provided scenario, with a starter scaffold (ships with
  Ch. 1).
- **L2 Assisted** — Build a multi-tool agent with memory and a
  reflection step for a provided scenario, partial scaffold (ships
  after Ch. 4, extended through Ch. 5-6's reflection/guardrail
  material).
- **L3 Independent** — Design and implement a reliability-instrumented,
  cost-bounded agent for a given problem, no scaffold. **SHIPPED at
  Ch. 12**, after five deferrals across Ch. 8-11 — see
  `chapters/chapter-12-designing-agent-architectures/project/` (Driftlight
  Energy Cooperative) and `quality-audits/chapter-12-audit.md` for the
  decision record.
- **L4 Architecture Challenge** — Design and defend a complete
  multi-component autonomous agent system; business/system problem
  only (this is the capstone, Ch. 13).

## Cross-Course Links

- Builds on: `python-for-everyone` (baseline), `ai-engineering-for-
  everyone` (LLM production-engineering foundation).
- Complements, does not duplicate: `ai-coding-agents-for-everyone`
  (a coding-domain-specific agent), `mcp-for-everyone` (the MCP
  protocol itself), `llm-evaluation-for-everyone` (deep evaluation
  methodology this course's own Ch. 7 defers to), `context-engineering-
  for-everyone` (context-window construction this course's own Ch. 4
  defers to).
- Feeds: a future `AI Governance for Everyone` (this course's
  guardrails material is one building block of a fuller governance
  discipline) and any future domain-specific agent course (this course
  is the general architecture layer underneath each of them).
