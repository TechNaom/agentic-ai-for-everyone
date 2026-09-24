# Chapter 1 Project (L1 Guided): Build and Trace a Minimal Agent Loop

This is the course's first project — the **L1 Guided** project (per the
curriculum map's project ladder), shipping in full with Chapter 1
itself. Scenario: **Wavecrest Marina** wants **SlipBot**, an agent that
answers boat-slip availability questions using one tool,
`check_slip_availability(slip_id)`.

## The task

`starter.py` gives you a working `FakeModel` (a deterministic
stand-in for a real model, scripted to request a tool call on its
first turn and answer using the observation on its second) and an
incomplete `run_agent()` function with three `# TODO`s. Complete
`run_agent()` so it correctly runs the perception → reasoning → action
→ observation loop from the lesson:

1. **TODO 1** — recognize a final answer (no `tool_calls`) and return it.
2. **TODO 2** — execute every requested tool call, trace it, and feed
   the observation back in.
3. **TODO 3** — the guard: halt cleanly at `max_iterations` if the
   model never stops.

## Why a fake model, not the real Ollama client

This project is gradable the same way every time, everywhere —
including in CI, which has no Ollama server running. The `FakeModel`
plays two scripted behaviors (`"normal"` and `"runaway"`) so your
`run_agent()` gets tested against both the happy path and the exact
failure mode Section 10 of the lesson covers, without depending on a
live model's non-determinism.

**Once your self-check passes**, if you want the full live experience,
swap `FakeModel` for the real thing using Chapter 1's own
`trailbot_agent.py` pattern:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# replace model.step(...) with a real
# client.chat.completions.create(model="llama3.2:latest", messages=messages, tools=TOOLS)
# call, feeding SlipBot's TOOLS and TOOL_IMPLS from starter.py instead
# of TrailBot's.
```

## How to run it

```bash
python3 starter.py
```

This prints a structural self-check: 4 checks, each testing a
different piece of the loop (resolving an available slip, tracing the
real tool call, surfacing a real unavailability reason, and the guard
halting a runaway model). It does not grade code style — only whether
your loop behaves correctly against all 4 scenarios.

## How to check your work for real

1. Run the self-check above until all 4 checks pass.
2. Compare your `run_agent()` against `solution.py` — not to match its
   exact line-for-line shape, but to check whether your loop handles
   the same cases (final answer, tool execution, the guard) the same
   way.
3. Self-grade against `RUBRIC.md`.
4. Optional: try the live-Ollama swap described above and watch a real
   model drive the same loop.

## Files

- `starter.py` — the scaffold with 3 `# TODO`s and the self-check.
- `solution.py` — the fully filled-in reference; passes all 4 checks.
- `RUBRIC.md` — self-grading criteria.
- `ai-paired.html` — a solo-diagnosis-then-critique exercise using this
  project's own scenario.
