# Chapter 12 Project: Driftlight Energy Cooperative — the L3 Independent Project

**This is this course's numbered L3 Independent project**, not a chapter
mini-project. Per `docs/curriculum/CURRICULUM_MAP.md`'s project ladder,
L3 reads: *"Design and implement a reliability-instrumented,
cost-bounded agent for a given problem, no scaffold."* It was due
after Chapter 8 and was deferred, explicitly and loudly, across
Chapters 9, 10, and 11 — five consecutive sessions. This chapter's
session made the call documented in `quality-audits/chapter-12-audit.md`:
**ship it now, as this chapter's own project**, because Chapter 12's
decision framework (characterize → select mechanisms → state a
budget → implement → instrument) is, almost word for word, what L3
asks a learner to do independently against a brand-new problem.

**There is deliberately no `starter.py` in this directory.** L3's own
definition is "no scaffold" — the point of "independent" is that you
are handed a problem statement, not a fill-in-the-blank file with
`# TODO`s. `solution.py` is the reference deliverable: read the
problem statement below, then (before looking at `solution.py`) try
building your own characterization, mechanism selection, budget,
implementation, and instrumentation. Compare your own work against
`solution.py` and self-grade with `RUBRIC.md` afterward.

## The problem statement

**Driftlight Energy Cooperative** is a fictional residential and
small-business energy cooperative running a demand-response program.
Members enroll once and **pledge** a kilowatt-hour amount they're
willing to curtail during a grid-load spike (a heat wave, a cold
snap). That pledge is recorded **at enrollment — a separate, earlier
session** — and must correctly inform **every later demand-response
event**, which can happen weeks or months afterward.

When the grid operator signals a load spike, Driftlight's agent must:

1. **Dispatch a curtailment request** to every enrolled member whose
   pledge applies, referencing their on-file pledge amount.
2. **Compute and apply a credit** afterward, based on the kilowatt-
   hours the member actually curtailed, at a fixed rate per kWh.
3. Handle the case where a member has **no pledge on file** (e.g., a
   data error, or a member who enrolled but never completed the
   pledge step) without crashing or guessing a default.

Demand-response events are **not scheduled during business hours** —
a heat wave can spike grid load at 2am, with no Driftlight staff
watching the system directly. A member's credit, once paid, is real
money leaving the cooperative; a dispatch retried after a network
blip must not double-credit the same member for the same event.

## Why this is a genuinely new problem, not a copy of the lesson's Copperfield

Copperfield Municipal Utilities (the lesson's own worked example)
needed only guardrails, reliability measurement, and cost control.
Driftlight needs those three **plus memory** (the pledge persists
across a separate, later session — Chapter 4's own CoachBot shape)
**plus the operating layer** (demand-response events run unattended
— Chapter 11's own DockScout/YardScout shape). It does **not** need
multi-agent dispatch, peer communication, or reflection. Working
through Driftlight cold, with the same four-question framework, is
the actual exercise — recalling Copperfield's verdicts by heart won't
get you through it, the same convention this chapter's own
`exercises/` and `practice/` banks already use.

## What `solution.py` actually does, in order

1. **Characterizes** the problem (`characterize_problem`) — reaches
   single-agent, because dispatch and crediting read/write the SAME
   member+event record and there's no concurrent independent actor.
2. **Selects mechanisms** (`select_mechanisms`) — confirms memory,
   guardrails, reliability measurement, cost control, and the
   operating layer are all load-bearing; reflection, multi-agent
   dispatch, and peer communication are not.
3. **States a reliability/cost budget** (`reliability_cost_budget`) —
   the tight, irreversible-action tier (95% minimum task-success rate,
   8-cent maximum cost per run).
4. **Implements** the selected mechanisms as real code:
   - `MemoryStore` — a JSON-file-backed, read-modify-write store for
     member pledges, proven to persist across two genuinely separate
     instantiations (not just claimed).
   - `apply_credit` — a fail-closed guardrail: credits above $50
     require explicit `human_approved=True`, matching Chapter 6's own
     fail-safe-default lesson.
   - `idempotency_key` + `commit_once` — an exactly-once commit layer
     for the credit side effect, matching Chapter 11's own fix (key on
     the fields that define the effect, not raw call arguments).
5. **Instruments** the implementation with a deterministic reliability/
   cost harness (`run_driftlight_harness`, `cost_per_success`,
   `is_within_budget` — reused in logic from Chapters 7-8) across
   three task types, and **proves** the stated budget is actually met
   with real measured numbers, not an assertion.
6. **Assembles the Architecture Decision Record** (`build_adr`) for
   the shipped design.

## Why deterministic, constructed cases, not a live Ollama call

Same grading policy as every prior chapter's `exercises/`/`practice/`/
`project/`: grading and the harness never depend on a live model, so
they run identically everywhere, including CI with no Ollama server
running. This also matches this chapter's own lesson, which
deliberately ran no live call — the skill being exercised is judgment
against written facts, not a model's live behavior.

## How to run it

```bash
python3 solution.py
```

This prints the assembled ADR, then a 12-point self-check report, then
the harness's real measured numbers.

## How to check your own independent attempt

1. Write your own characterization, mechanism selection, budget,
   implementation, and harness for Driftlight **before** reading
   `solution.py`.
2. Run your own code and confirm your harness actually meets the
   budget you stated — not just that it runs without crashing.
3. Compare your design against `solution.py`, not to match it
   line-for-line, but to check whether you reached the same load-
   bearing-mechanism verdicts for the same reasons.
4. Self-grade against `RUBRIC.md`.

## Files

- `solution.py` — the reference deliverable; no scaffold, no starter,
  per L3's own "independent" definition. Scores 12/12.
- `RUBRIC.md` — self-grading criteria.
- `index.html` — the browsable version of this page.
- `ai-paired.html` — a solo-build-then-critique exercise using a
  fourth scenario, Mirelake Water Authority.
