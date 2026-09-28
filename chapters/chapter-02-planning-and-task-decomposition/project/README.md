# Chapter 2 Project: Dual-Mode Planning for RouteBot

This is a **chapter mini-project**, not one of this course's numbered
L1-L4 projects (per `docs/curriculum/CURRICULUM_MAP.md`'s project
ladder, this chapter's material is folded into the L2 Assisted project
that ships after Chapter 4). It exists so Chapter 2's two planning
strategies get one combined, hands-on build of their own before that
larger project arrives. Scenario: **Cobblestone Courier Co.**, a
fictional local delivery service, wants **RouteBot** to handle two
kinds of task with two different planning strategies — the same
dual-mode shape as the lesson's own PlanBot (Section 14), applied to a
fresh scenario you build yourself.

## The two tasks

**Task A — Processing a new delivery order (fixed, up-front plan).**
Verify the delivery address, calculate the route, dispatch a driver.
Every order needs all three steps, in that exact order, and nothing
about the address changes whether the route is worth calculating —
per Section 12's heuristic, this is a fixed-shape task.

**Task B — Diagnosing a delayed delivery (emergent, one-step-at-a-time
plan).** Check the delay status first, and only *then* decide whether
the right follow-up is a traffic check, a weather check, or a driver
check-in — because that choice depends entirely on what the delay
status notes actually say. This cannot be a fixed plan, the same
reason the lesson's stock-drop investigation needed emergent planning.

## The three TODOs

`starter.py` gives you all the tool functions and fixtures already
implemented — this project is about the *planning* layer, not
re-building Chapter 1's tool mechanics.

1. **TODO 1** — `run_fixed_dispatch()`: the fixed-plan executor,
   **with a re-planning guard built in** (mirrors the lesson's Section
   13 `run_fixed_plan_with_replan_guard`, but as one combined function
   this time instead of two separate ones).
2. **TODO 2** — `decide_next_delay_check()`: the emergent decision
   function, branching on what the delay status notes actually say
   (traffic vs. weather vs. driver check-in).
3. **TODO 3** — `classify_task_planning_mode()`: the fixed-vs-emergent
   decision heuristic itself (Section 12), so you implement the rule,
   not just apply functions that already encode it.

## Why deterministic fixtures, not a live Ollama call

Same grading policy as this chapter's `exercises/` and `practice/`,
and Chapter 1's own project: `solution.py`'s pass/fail checks never
depend on a live model, so grading works the same way everywhere,
including CI with no Ollama server running. If you want the full live
experience once your self-check passes, swap the planning decisions
for real `openai`-against-Ollama calls using the exact pattern from
`lesson.html` Section 4 (`client.chat.completions.create(...,
tools=TOOLS)` for the fixed plan) and Section 7 (a live call per step
for the emergent loop) — `base_url="http://localhost:11434/v1"`,
`model="llama3.2:latest"`.

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 7 checks across the fixed-plan
executor (happy path, one successful re-plan, and giving up cleanly
with no correction available), the emergent decision function (all
three branches — traffic, weather, driver check-in), and the planning
heuristic (all three input combinations).

## How to check your work for real

1. Run the self-check above until all 7 checks pass.
2. Compare your implementation against `solution.py` — not to match
   its exact line-for-line shape, but to check whether your logic
   handles the same cases (a successful re-plan, giving up cleanly,
   all three emergent branches) the same way.
3. Self-grade against `RUBRIC.md`.
4. Optional: try the live-Ollama swap described above.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 7 checks.
- `RUBRIC.md` — self-grading criteria.
- `ai-paired.html` — a solo-build-then-critique exercise using this
  same RouteBot scenario.
