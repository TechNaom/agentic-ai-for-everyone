# Module 1 Combined Assessment: Agent-Loop Tracing + Planning Exercise

Per `docs/curriculum/CURRICULUM_MAP.md`, Module 1's stated assessment is
an "agent-loop-tracing + planning exercise," spanning Chapter 1 (the
agent loop) and Chapter 2 (planning and task decomposition). Modules
1-3 were all built and marked complete in earlier sessions without a
module-assessment file ever being created; this file closes that gap
for Module 1, built during Chapter 7's own session once the gap was
flagged and a decision was made not to keep deferring it (see
`quality-audits/chapter-07-audit.md`'s "Module 1-3 assessment
decision" section for the full reasoning, and the sibling course
`ai-engineering-for-everyone`'s own `module-4-cost-latency-reliability-
engineering-exercise` for the combined-assessment format this follows).

## The scenario

This assessment reuses the EXACT functions Chapter 1's and Chapter 2's
own projects already built and tested, applied to a fresh combination
of fixture data, rather than inventing new mechanics:

- **Chapter 1** (`run_agent`, `FakeModel`) — Wavecrest Marina's SlipBot,
  applied to a slip (`"c19"`) the chapter's own self-check exercised
  under a different scenario shape.
- **Chapter 2** (`decide_next_delay_check`, `classify_task_planning_mode`)
  — a fresh delay-diagnosis history for a new order, where the most
  recent tool result mentions both "weather" and "icy roads."

## The task

Using `starter.py`, produce:

1. **Agent-loop tracing** (Chapter 1) — run `ch1.run_agent("c19",
   ch1.FakeModel("normal"))` and record the `(answer, trace)` result.
2. **Planning decisions** (Chapter 2) — apply
   `ch2.decide_next_delay_check()` to the given history, and apply
   `ch2.classify_task_planning_mode()` to classify the diagnosis task.
3. **Cross-chapter synthesis** — the one genuinely new task this
   assessment adds beyond either chapter's own project: explain, using
   Chapter 2's own `classify_task_planning_mode` logic (not just
   "fixed is simpler"), why Chapter 1's SlipBot loop counts as fixed
   rather than emergent even though it's implemented as a loop.

## Why this exercise, and why this scope

This reuses the exact decision functions Chapters 1 and 2 each built
and tested in their own lessons and projects, applied together, rather
than inventing new content. It is intentionally smaller than a full
chapter project: two chapters combined instead of three, and one
cross-chapter synthesis question instead of a full new build.

## How to run it

```bash
python3 starter.py
```

Part 3's justification is open-ended (there's more than one defensible
way to phrase it), so the script runs a **structural self-check**: are
Parts 1-2 correctly computed, and is Part 3 a real, descriptive note
referencing the actual concept ("fixed") rather than a placeholder. It
does not grade whether your justification prose matches the reference
solution's exact wording.

## How to check your work for real

1. Run the structural self-check above until it passes.
2. Compare your full response against `solution.py` — check whether
   your Part 3 justification actually applies
   `classify_task_planning_mode`'s own logic, not a generic assumption.
3. Self-grade against `RUBRIC.md`.

## Files

- `starter.py` — the scenario, your response template, and the
  structural self-check. It loads Chapter 1's and Chapter 2's own
  `project/solution.py` files directly via `importlib`, so it always
  stays in sync with those chapters' real, tested functions.
- `solution.py` — one complete, valid reference response.
- `RUBRIC.md` — the grading criteria.
