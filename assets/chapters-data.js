/*
  Single source of truth for the Agentic AI for Everyone chapter
  roster. sidebar.js and home.js render navigation from this file. A
  chapter is "live" iff it has a `path` -- omit `path` for chapters
  that don't exist yet, do not set a placeholder path, or sidebar/home
  will link to a 404. The same rule applies to a module's `examPath`:
  set it to null until that module's written exam actually exists in
  assessments/written-exams/.

  Chapters 1-3 are live as of this build (Module 1 complete; Module 2
  in progress with Chapter 3 live, Chapter 4 still planned) -- see
  PROJECT_STATE.md for status. Chapters 4-13 are planned, `.gitkeep`'d,
  not yet built.
*/

window.AAFE_MODULES = [
  {
    title: "Module 1 — Foundations of the Agent Loop",
    summary: "What makes something an \"agent\" instead of a single model call, and how to break a goal into steps.",
    examPath: null,
    chapters: [
      {
        id: "chapter-01",
        num: 1,
        title: "The Agent Loop: Building Your First Autonomous Agent",
        description: "Perception, reasoning, action, observation -- the loop every agent in this course builds on.",
        path: "chapters/chapter-01-the-agent-loop-building-your-first-autonomous-agent/lesson.html"
      },
      {
        id: "chapter-02",
        num: 2,
        title: "Planning and Task Decomposition",
        description: "Breaking a goal into steps, re-planning on failure, fixed plans vs. emergent ReAct-style planning.",
        path: "chapters/chapter-02-planning-and-task-decomposition/lesson.html"
      }
    ]
  },
  {
    title: "Module 2 — Giving Agents Capabilities",
    summary: "Tool use and memory -- how an agent acts on the world and carries state across steps.",
    examPath: null,
    chapters: [
      {
        id: "chapter-03",
        num: 3,
        title: "Tool Use and Function Calling",
        description: "Choosing the right tool, forming correct arguments, and handling tool failure.",
        path: "chapters/chapter-03-tool-use-and-function-calling/lesson.html"
      },
      {
        id: "chapter-04",
        num: 4,
        title: "Memory and State",
        description: "Short-term working memory vs. long-term persisted memory, and their real engineering trade-offs."
      }
    ]
  },
  {
    title: "Module 3 — Making Agents Reliable",
    summary: "An agent that notices and corrects its own mistakes, and stays inside safe bounds while doing it.",
    examPath: null,
    chapters: [
      {
        id: "chapter-05",
        num: 5,
        title: "Reflection and Self-Correction",
        description: "An agent noticing and fixing its own mistakes, as a designed architectural component."
      },
      {
        id: "chapter-06",
        num: 6,
        title: "Guardrails and Safety for Autonomous Agents",
        description: "Iteration bounds, human approval, sandboxing, and rate limiting, mapped to the failures each one stops."
      }
    ]
  },
  {
    title: "Module 4 — Measuring and Controlling Agents",
    summary: "Knowing whether an agent is actually working, and keeping it affordable and fast.",
    examPath: null,
    chapters: [
      {
        id: "chapter-07",
        num: 7,
        title: "Evaluating Agent Reliability",
        description: "What makes agent behavior measurable, and what to log -- the systems-design side of agent evaluation."
      },
      {
        id: "chapter-08",
        num: 8,
        title: "Cost and Latency Control of Agent Loops",
        description: "Iteration bounding, model tiering, caching, and early exit for a bounded, affordable agent loop."
      }
    ]
  },
  {
    title: "Module 5 — Multi-Agent Systems",
    summary: "When and how to coordinate more than one agent, and running one in production.",
    examPath: null,
    chapters: [
      {
        id: "chapter-09",
        num: 9,
        title: "Multi-Agent Orchestration Patterns",
        description: "Supervisor/worker, pipeline, and debate/critique patterns, and when each earns its complexity."
      },
      {
        id: "chapter-10",
        num: 10,
        title: "Multi-Agent Coordination and Communication",
        description: "Message passing between agents, and the new failure modes (miscommunication, duplicated work, deadlock)."
      },
      {
        id: "chapter-11",
        num: 11,
        title: "Operating Agents in Production",
        description: "Retries, timeouts, structured logging, and operating a multi-agent system for real."
      }
    ]
  },
  {
    title: "Module 6 — Architecture and Capstone",
    summary: "Architect-level synthesis -- designing and defending a complete agent system.",
    examPath: null,
    chapters: [
      {
        id: "chapter-12",
        num: 12,
        title: "Designing Agent Architectures",
        description: "Architect-level synthesis: choosing a full agent architecture for a given problem."
      },
      {
        id: "chapter-13",
        num: 13,
        title: "Capstone: Designing and Defending an Autonomous Agent System",
        description: "A Level 4 architecture challenge composing loop design, planning, tools, memory, guardrails, evaluation, and cost control into one system."
      }
    ]
  }
];
