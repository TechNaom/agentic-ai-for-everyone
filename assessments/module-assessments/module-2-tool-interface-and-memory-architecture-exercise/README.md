# Module 2 Combined Assessment: Tool-Interface Design + Memory-Architecture Exercise

Per `docs/curriculum/CURRICULUM_MAP.md`, Module 2's stated assessment is
a "tool-interface design + memory-architecture exercise," spanning
Chapter 3 (tool use and function calling) and Chapter 4 (memory and
state). Built during Chapter 7's own session, closing a pre-existing
gap across all of Modules 1-3 (see
`quality-audits/chapter-07-audit.md`'s assessment-decision section).

## The scenario

This assessment reuses the EXACT functions Chapter 3's and Chapter 4's
own projects already built and tested:

- **Chapter 3** (`diagnose_appliance_issue`) — RepairBot, applied to
  appliance `"appl-301"`, whose warranty is already on file as
  expired in Chapter 3's own fixture data.
- **Chapter 4** (`MemoryStore`, `build_working_context`,
  `run_visit_session`) — CareBot, applied to patient `"pt-88"`
  reporting a peanut allergy across two separate calls, proving the
  fact persists between them.

## The task

Using `starter.py`, produce:

1. **Tool-interface behavior** (Chapter 3) — call
   `diagnose_appliance_issue("appl-301")` and record the selected tool
   and result.
2. **Memory-architecture behavior** (Chapter 4) — confirm the working
   context starts empty, run a visit session that reports a new
   condition, and confirm a fresh context call afterward still sees
   the persisted fact.
3. **Cross-chapter synthesis** — the one genuinely new task this
   assessment adds: explain why RepairBot's stateless tools don't need
   persisted memory the way CareBot's do, referencing what would
   specifically break for each if the roles were reversed.

## Why this exercise, and why this scope

This reuses the exact functions Chapters 3 and 4 each built and tested
in their own lessons and projects, applied together, rather than
inventing new content — intentionally smaller than a full chapter
project.

## How to run it

```bash
python3 starter.py
```

Part 3's justification is open-ended, so the script runs a
**structural self-check** on Parts 1-2 plus a basic substance check on
Part 3. It does not grade whether your justification prose matches the
reference solution's exact wording.

## How to check your work for real

1. Run the structural self-check above until it passes.
2. Compare your full response against `solution.py`.
3. Self-grade against `RUBRIC.md`.

## Files

- `starter.py` — the scenario, your response template, and the
  structural self-check. It loads Chapter 3's and Chapter 4's own
  `project/solution.py` files directly via `importlib`.
- `solution.py` — one complete, valid reference response.
- `RUBRIC.md` — the grading criteria.

`starter.py`/`solution.py` create and clean up a scratch memory file
(`_module2_memory_scratch.json`) in this same directory during the
self-check; it should not persist after a run completes.
